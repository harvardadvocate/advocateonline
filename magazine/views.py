from django.shortcuts import get_object_or_404, render
from django.template.context import RequestContext
from django.http import HttpResponse, JsonResponse
# from .models import Article, Content, Issue , Subscriber# '.' signifies the current directory
from .models import Article, Content, Image, Issue, Contributor, ShopItem # '.' signifies the current directory
import django.db.models as models
from .forms import UploadShopItemForm
from blog.models import Post, Author
from collections import OrderedDict
from itertools import chain
import json
import stripe
from django.conf import settings
import random
import re
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from advertisement.helper import getAds

from haystack.query import SearchQuerySet
from haystack.views import SearchView
from haystack.forms import SearchForm
from django.shortcuts import redirect
from itertools import chain
import logging


logger = logging.getLogger("magazine")


# Create your views here.
def index(request):
  issue = Issue.objects.last()

  # for each article with this issue id
  articles_in_issue = Article.objects.published().filter(issue=issue)
  data = {
    'blog': { },
    'sections': { },
    'issue': issue,
  }
  # Put articles into their respective sections
  for article in articles_in_issue:
    SectionName = str(article.section).lower()
    if SectionName not in data['sections']:
      data['sections'][SectionName] = [article]
    else:
        data['sections'][SectionName].append(article)
  data['sections']['art'] =  Image.objects.published().filter(issue=issue)

  # Randomly choice an article for every section
  for key in data['sections']:
    if data['sections'][key]:
      data['sections'][key]= random.choice(data['sections'][key])
  posts = Post.objects.all()
  recent_blog = list(reversed(sorted(posts, key=lambda i: i.created)))[:2 ]
  data['blog']['post1'] = recent_blog[0]
  data['blog']['post2'] = recent_blog[1]

  data['toplist'] = [{'title' : "article one", 'url' : "google.com", 'author' : "samantha"}, {'title' : "article two", 'url' : "google.com", 'author' : "cameron"}, {'title' : "article three", 'url' : "google.com", 'author' : "joe"}]

  data['ads'] = getAds('home')
  data['MEDIA_URL'] = settings.MEDIA_URL
  template_name = 'index.html'
  return render(request, template_name, data)

def homepage_redesign_jack(request):
  data = {}

  # current_issue
  CURRENT_ISSUE = "Summer 2018"

  for issue in Issue.objects.all():
    if str(issue) == CURRENT_ISSUE:
      break
      
  data['issue_name'] = issue
  data['issue_cover_image'] = issue.cover_image
  data['issue_url'] = issue.get_absolute_url()
  # ads
  data['ads'] = getAds('home')
  all_articles = Article.objects.published()
  articles_in_issue = all_articles.filter(issue=issue)
  art_in_issue = Image.objects.published().filter(issue=issue)
  # from the blog
  posts = Post.objects.all()
  recent_blog = list(reversed(sorted(posts, key=lambda i: i.created)))[:2 ]
  # most_read (from Google Analytics)
  most_read_list = []
  most_read = []
  for item in most_read_list:
    article, _ = item
    most_read.append(article)
  data['most_read'] = most_read
  # editors_picks (randomly generated)
  editors_picks = []
  editors_picks_article_indicies = random.sample(range(0, len(all_articles) - 1), 5)
  for index in editors_picks_article_indicies:
    editors_picks.append(all_articles[index])
  data['editors_picks'] = editors_picks
  # feature_1 - Any
  data['feature_1'] = articles_in_issue[1]
  # feature_2 - Blog
  data['feature_2'] = articles_in_issue[2]
  # feature_3 - Art
  data['feature_3'] = articles_in_issue[2]
  # feature_4 - Any
  data['feature_4'] = articles_in_issue[3]

  # feature_5 - Any
  data['feature_5'] = recent_blog[0]

  # feature_6 - Any
  data['feature_6'] = all_articles[7]
  # feature_7 - Any
  data['feature_7'] = all_articles[15]
  # feature_8 - Any

  template_name = 'homepage_redesign_jack.html'
  return render(request, template_name, data)


def article(request, id, slug):
  article = get_object_or_404(Article, id=id)
  data = {
    'article': article
  }
  template_name = 'article.html'
  return render(request, template_name, data)

def content_piece(request, slug, id=''):
  if slug.isdigit():
    image = get_object_or_404(Content, id=slug)
  else: # handle legacy links in the form of /content/short-slug
    try:
      image = Content.objects.get(slug__iexact=slug)
    except ObjectDoesNotExist:
      # check if linked slug is simply shortened and missing words
      slug_regex = r"[a-zA-Z\d_\-]*" + slug.replace("-", r"-([a-zA-Z\d_\-]+-)?") + r"[a-zA-Z\d_\-]*"
      try:
        image = Content.objects.get(slug__iregex=slug_regex)
      except (MultipleObjectsReturned, ObjectDoesNotExist):
        # search the words instead if there isn't exactly one match
        slug = slug.replace("-","+")
        return redirect('/search/?q=' + slug)
  # print image.contributors
  data = {
    'art_content': image
  }
  template_name = 'content.html'
  # if not data['art_content']:
  #   print "here"
  return render(request, template_name, data)

def contributor_page(request, author_id, name):
  author =  get_object_or_404( Contributor, id=author_id, name = name.replace("_", " "))
  # author.name = name.replace("_", " ")
  # author.id = author_id
  data = {}
  data["author"] = author.name
  data["articles"] =  chain( Article.objects.filter(contributors=author) , Image.objects.filter(contributors=author))
  template_name = 'contributor.html'
  return render(request, template_name, data)


def issues(request):
  all_issues = Issue.objects.all()
  season = {'Winter': 0, 'Spring': 1, 'Commencement': 2, 'Fall': 3}

  #all_issues_sorted = reversed(sorted(all_issues, key=lambda i: i.year))
  all_issues_sorted = reversed(sorted(all_issues, key=lambda i: i.year * 10 + season[i.issue]))
  data = {
    'issues': all_issues_sorted
  }
  template_name = 'issues.html'
  return render(request, template_name, data)

def masthead(request):
  template_name = 'about_us.html'
  return render(request, template_name, {})

def singleissue(request, season, year):
  template_name = 'singleissue.html'
  issue = get_object_or_404(Issue, issue__iexact=season, year=year)

  # TODO: Once we figure out contenttypes, bring back this line!
  # issue_content = Content.objects.filter(issue=issue)

  content = OrderedDict()

  articles_in_issue = Article.objects.published().filter(issue=issue)

  for article in articles_in_issue:
    SectionName = str(article.section).lower()
    if SectionName not in content:
     content[SectionName] = [article]
    else:
       content[SectionName].append(article)
  content['art'] =  Image.objects.published().filter(issue=issue)

  # issue_content = Article.objects.filter(issue=issue)
  # section = ('Features','Fiction','Poetry')

  # content = OrderedDict()
  # for s in section:
  #   content[s] = issue_content.published().filter(section__name=s)
  # content['Art'] =  Image.objects.published().filter(issue=issue)
  data = {
    'issue' : issue,
    'content_list' : content
    }

  return render(request, template_name, data)

class FilterSearchView(SearchView):
        template_name = 'search/search.html'
        queryset = SearchQuerySet().all()
        form_class = SearchForm
        type_filter = 'all'

        def __call__(self, request, type_filter = None):

                self.request = request

                self.form = self.build_form()
                self.query = self.get_query()
                self.results = self.get_results()

                if type_filter is not None:
                        self.results = self.results.filter(section=type_filter)
                        self.type_filter = type_filter
                else:
                        self.type_filter = 'all'

                return self.create_response()

        def extra_context(self):
                return {'type_filter' : self.type_filter}

        def create_response(self):
                (pageinator, page) = self.build_page()

                context = {
                        'query' : self.query,
                        'form' : self.form,
                        'page' : page,
                        'pageinator' : pageinator,
                        'suggestion' : None,
                }

                context['suggestion'] = self.form.get_suggestion()

                #for dict in Contributor.objects.all():
                #        if (dict['name'] == self.query):
                #                print dict

                try:
                        return redirect(Article.objects.get(title = self.query))
                except Article.DoesNotExist:
                        pass

                try:
                        return redirect(Contributor.objects.get(name = self.query))
                except Contributor.DoesNotExist:
                        pass
                try:
                        return redirect(Post.objects.get(title = self.query))
                except Post.DoesNotExist:
                        pass
                try:
                        return redirect(Author.objects.get(name = self.query))
                except Author.DoesNotExist:
                        pass

                context.update(self.extra_context())
                return render(self.query, self.template, context)


def subscribe(request):
  template_name = 'subscribe.html'
  return render(request, template_name)

def gala(request):
  template_name = 'gala.html'
  return render(request, template_name)

def financialaid(request):
  template_name = 'financialaid.html'
  return render(request, template_name)


def stripeSubmit(request):
  # Get the credit card details submitted by the form
  token = request.POST['stripeToken']
  stripe.api_key = settings.STRIPE_SECRET_KEY
  # Create the charge on Stripe's servers - this will charge the user's card
  try:
    charge = stripe.Charge.create(
      amount=123, # amount in cents, again
      currency="usd",
      card=token,
      description="payinguser@example.com",
    )

    subscriber = Subscriber.objects.create(
      name=request.POST['name'],
      email=request.POST['email'],
      streetAddress1=request.POST['streetAddress1'],
      streetAddress2=request.POST['streetAddress2'],
      city=request.POST['city'],
      state=request.POST['state'],
      country=request.POST['country'],
      zipCode=request.POST['zipCode'],
      renew=request.POST['renew'],
      subscriptionType=request.POST['subscriptionType'],
    )
    return subscribe(request)
  except stripe.CardError, e:
    # The card has been declined
    pass

def sections(request):
  section = request.path
  section = section.split('/')[-2]

  # For all issues
  all_issues = query_all_issues_sorted()
  season = {'Winter': 0, 'Spring': 1, 'Commencement': 2, 'Fall': 3}
  featured_articles = list(Article.objects.published().filter(section__name =section).order_by('-publishDate')[:5])
  if section == "art":
      images = list(Image.objects.published().filter(section__name =section).order_by('-publishDate')[:5])
      if featured_articles:
        featured_articles = sorted(featured_articles + images, key = lambda x: x.publishDate)[5:]
      else:
        featured_articles = images
  data = {
    "section": section,
    "featured_articles": list(featured_articles)[:5],
    "ads": getAds(section),
    "issues": list(all_issues),
    "MEDIA_URL": settings.MEDIA_URL
  }
  template_name = 'section.html'
  return render(request, template_name, data)

def query_all_issues_sorted():
  return Issue.objects.annotate(custom_order=
    models.Case(
      models.When(issue='Winter', then=models.Value(0)),
      models.When(issue='Spring', then=models.Value(1)),
      models.When(issue='Commencement', then=models.Value(2)),
      models.When(issue='Summer', then=models.Value(3)),
      models.When(issue='Fall', then=models.Value(4)),
      default = models.Value(5),
      output_field = models.IntegerField(), )
    ).order_by('-year', '-custom_order')

def explore_archives(request):
  section, num, issue = request.GET.get("section"), int(request.GET.get("num")), request.GET.get("issue")
  last_issue = Issue.objects.get
  articles = None
  if issue:
    articles = list(Article.objects.published().filter(section__name=section, issue=issue))
    articles += list(Image.objects.published().filter(section__name=section, issue=issue))
  else:
    if section == "art":
      image_query = Image.objects.published().filter(section__name=section)
      articles = select_random(num, image_query)
    else:
      article_query = Article.objects.published().filter(section__name=section)
      articles = select_random(num, article_query)
  result = {
    "result": [serialize_article(a) for a in articles]
  }
  return JsonResponse(result, safe=False)

def serialize_article(a):
  return {
    "id": a.id,
    "title": a.title,
    "contributors": [str(c) for c in a.contributors.all()],
    "body": a.body,
    "photo": settings.MEDIA_URL+str(a.photo) if a.photo else str(a.photo)
  }

def select_random(num, query):
  total = query.count()
  indx = [random.randint(0, total-1) for _ in xrange(num)]
  return [query[i] for i in indx]

def submit(request):
  template_name = 'submit.html'
  return render(request, template_name)

def contact(request):
  template_name = 'contact_us.html'
  return render(request, template_name)

def alumni(request):
  template_name = 'alumni.html'
  return render(request, template_name)

def advertise(request):
  template_name = 'advertise.html'
  return render(request, template_name)

def adSubmit(request):
  template_name = 'adSubmit.html'
  return render(request, template_name)

def shop(request):
  all_items = ShopItem.objects.all()
  data = {
    'items': all_items,
    'page': 'shop',
  }
  template_name = 'shop.html'
  return render(request, template_name, data)

def shopItemView(request, id):
  item = ShopItem.objects.filter(id=id)
  if item:
    data = {
      'item': item[0],
      'page': 'shopItemView',
    }
    template_name = 'shop_item_view.html'
    return render(request, template_name, data)
  else: # item does not exist
    return HttpResponse('404: Page not found.')


def shop_admin(request):
  if request.method == 'GET':
    form = UploadShopItemForm()
    return render(request, 'shop-admin.html', {'shop_items': ShopItem.objects.all(), 'form': form})
  #return HttpResponse("")
  return HttpResponse("<script>window.location = window.location.origin + '/shop-admin';</script>")

def shop_upload(request):
  if request.method == 'POST':
    item_name = request.POST['name']
    item_description = request.POST['description']
    item_price = request.POST['price']
    item_imagefile = request.POST['imagefile']
    new_item = ShopItem(name=item_name, description=item_description, price=item_price)#, profile_image=item_imagefile)
    new_item.save()
    return render(request, 'shop-admin.html', {})
  return HttpResponse("There's nothing here.")

def shop_delete(request):
  if request.method == 'POST':
    print "request.POST:"
    print dir(request.POST)
    print "keys"
    print request.POST.keys()
    print "token"
    print request.POST['csrfmiddlewaretoken']
    ShopItem.objects.filter(id=request.POST['id']).delete()
    return HttpResponse("success!")

def cart(request):
  if request.method == 'GET':
    cartSession = request.session.get('cartItems', False)
    if cartSession:
      all_items = ShopItem.objects.filter(id__in=cartSession)
      purchase_description = [itm.title for itm in all_items]
      purchase_description = ', '.join(purchase_description)
      purchase_description = purchase_description.replace('"', "'")
      total = int(sum([item.price for item in all_items])*100)
      totalStr = str(total)
      totalStr = totalStr[:-2] + "." + totalStr[-2:]
      data = {'items': all_items, 'page': 'cart', 'total': total, 'totalStr': totalStr, 'purchaseDescription': purchase_description}
      return render(request, "cart.html", data)
    else:
      data = {'items': [], 'page': 'cart'}
      return render(request, "cart.html", data)
  if request.method == 'POST':
    if request.POST['itemId']:
      cartSession = request.session.get('cartItems', False)
      # insert request
      if request.POST['action'] == "insert":
        if cartSession:
          if request.POST['itemId'] in cartSession:
            return HttpResponse('{"code": 1, "responseText": "Item already added."}')
          else:
            request.session['cartItems'].append(request.POST['itemId'])
            request.session.modified = True
        else:
          request.session['cartItems'] = [request.POST['itemId']]
          request.session.modified = True
        return HttpResponse('{"code": 0, "responseText": "success!"}')
      # delete request
      elif request.POST['action'] == "delete":
        if request.POST['itemId'] in cartSession:
          cartSession = [i for i in cartSession if i != request.POST['itemId']]
          request.session['cartItems'] = cartSession
          request.session.modified = True
          return HttpResponse('{"code": 0, "responseText": "success!"}')
        else:
          return HttpResponse('{"code": 0, "responseText": "nothing to delete."}')
      else:
        return HttpResponse('{"code": 4, "responseText": "Invalid action"}')
    else:
      return HttpResponse('{"code": 2, "responseText": "Invalid post data."}')
  return HttpResponse('{"code": 3, "responseText": "Invalid request"}')

def onefifty(request):
  template_name = '150th.html'
  return render(request, template_name)

def comp(request):
  template_name = 'comp.html'
  return render(request, template_name)

def tech(request):
  template_name = 'tech.html'
  return render(request, template_name)


