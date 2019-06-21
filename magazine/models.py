import os
import datetime

from django.db import models
from django.db.models import Q, ImageField
from django.utils.text import slugify
from django.utils.encoding import smart_unicode, smart_str
from django.urls import reverse
from tinymce import models as tinymce_models
from bs4 import BeautifulSoup
import re
from versatileimagefield.fields import VersatileImageField
from redactor.fields import RedactorField


def now():
    now = int((datetime.datetime.utcnow() -
                datetime.datetime(2014, 1, 1)).total_seconds() * 10 ** 6)
    return unicode(now)

# upload issue cover images
# issue_covers/issue.year/filename.jpg
def issue_upload_to(instance, filename):
    fname = ''.join([c for c in filename if c.isalnum() or c == '.'])
    return os.path.join('issue_covers', str(instance.year), now() + '_' + fname)

# upload artwork and illustrations accompanying articles
def upload_image_to(instance, filename):
    fname = ''.join([c for c in filename if c.isalnum() or c == '.'])
    print instance.issue.name
    return os.path.join('sites', 'default', 'files', fname)
    #return os.path.join('images', str(instance.issue.year), str(instance.issue.issue), now() + '_' + fname)

def get_image_path(instance, filename):
    return os.path.join('static/images/shop/', filename)

class Issue(models.Model):
    name = models.CharField(max_length=255, unique=True)
    theme = models.CharField(max_length=255, blank=True, null=True)
    cover_image = ImageField(upload_to=issue_upload_to, blank=True, null=True)

    ISSUE_CHOICES = (
        ('Fall', 'Fall'),
        ('Winter', 'Winter'),
        ('Spring', 'Spring'),
        ('Commencement', 'Commencement'),
    )
    issue = models.CharField(max_length=255, choices=ISSUE_CHOICES, default='Fall')
    year = models.IntegerField(blank=True, null=True)
    pub_date = models.DateField()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('issue', args=[self.issue.lower(), self.year])

class Section(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

class Contributor(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)

    def __unicode__(self):
      return self.name
    def slug(self):
      return self.name.replace(" ", "_")
    def get_absolute_url(self):
     return reverse('contributor', args=[self.id, self.name])



class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)

    def __unicode__(self):
        return self.name

class ContentQuerySet(models.query.QuerySet):
    def published(self):
        return self.filter(Q(publishDate__lte=datetime.datetime.now()) | Q(publishDate__isnull=True))

class ContentManager(models.Manager):
    def get_queryset(self):
        return ContentQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

class Content(models.Model):
    objects = ContentManager()
    title = models.CharField(max_length=255)
    publishDate = models.DateTimeField(default=datetime.datetime.now)
    subtitle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    teaser = tinymce_models.HTMLField(blank=True)
    body = RedactorField(
        verbose_name=u'Text',
        redactor_options={'lang': 'en', 'focus': 'true'},
        upload_to='tmp/',
        allow_file_upload=True,
        allow_image_upload=True
    )

    # Legacy fields; we should probably get rid of this eventually
    medium = tinymce_models.HTMLField(blank=True)
    size = tinymce_models.HTMLField(blank=True)
    statement = tinymce_models.HTMLField(blank=True)

    issue = models.ForeignKey('Issue')
    section = models.ForeignKey('Section', related_name="section")
    contributors = models.ManyToManyField(Contributor)
    tags = models.ManyToManyField(Tag, blank=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('content', args[self.id])

    def description(self):
        txt = ' '.join(BeautifulSoup(self.teaser).findAll(text=True))
        return txt
  
class Article(Content):
    objects = ContentManager()
    photo = VersatileImageField(upload_to=upload_image_to, blank=True, null=True)
    def get_absolute_url(self):
        return reverse('article', args=[self.id, self.slug.lower()])

class Image(Content):
    objects = ContentManager()
    photo = VersatileImageField(upload_to=upload_image_to)

class Donation(models.Model):

    amount = models.IntegerField()
    comment = models.TextField(blank=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    streetAddress1 = models.CharField(max_length=255)
    streetAddress2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=255)
    customerID = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name + "  " + self.comment


class Subscriber(models.Model):

    SUBSCRIPTION_CHOICES = (
        ('Three year; US', 'Three year; US'),
        ('Two year; US', 'Two year; US'),
        ('One year; US', 'One year; US'),
        ('Three year; non-US', 'Three year; non-US'),
        ('Two year; non-US', 'Two year; non-US'),
        ('One year; non-US', 'One year; non-US')
    )

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    streetAddress1 = models.CharField(max_length=255)
    streetAddress2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=255)
    customerID = models.CharField(max_length=255)
    renew = models.BooleanField(default=False)
    subscriptionType = models.CharField(max_length=255, choices=SUBSCRIPTION_CHOICES)
    time = models.CharField(max_length=255)

class Purchase(models.Model):

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    streetAddress1 = models.CharField(max_length=255)
    streetAddress2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)    
    state = models.CharField(max_length=255)    
    country = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=255)
    customerID = models.CharField(max_length=255) 
    amount = models.IntegerField()
    purchases_json = models.CharField(max_length=255)
    time = models.CharField(max_length=255)

class ShopItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)




