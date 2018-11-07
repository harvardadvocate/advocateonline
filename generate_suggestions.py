import urllib2, json, re, unicodedata, sys, os
from bs4 import BeautifulSoup
from collections import Counter
import nltk;
from nltk.corpus import stopwords
from textblob import TextBlob
from django.core.wsgi import get_wsgi_application
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('brown')
nltk.download('averaged_perceptron_tagger')
os.environ['DJANGO_SETTINGS_MODULE'] = 'advo.settings'

application = get_wsgi_application()
from django.db import models
from magazine.models import Content

#dict of punctuation
tbl = dict.fromkeys(i for i in xrange(sys.maxunicode)
                      if unicodedata.category(unichr(i)).startswith('P'))

#removes html tags
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


#gets suggested articles for given article id
def getSuggested(n):
    to_return = []
    pairs = articleset[str(n)]
    for i in range(0, len(pairs)):
        try:
            key = str(pairs[i][0])
        except:
            continue
        if key not in newmasterset:
            continue
        related = newmasterset[key]
        for r in related:
            if int(r) != int(n) and not int(r) in to_return:
                to_return += [int(r)]
                if len(to_return) >= 5:
                    break
        if len(to_return) >= 5:
            break
    return to_return

#insert into database
def insertIntoDatabase(django_id, suggested):
    article = Content.objects.get(pk=django_id)
    print(str(suggested))
    article.suggested_ids = str(suggested)
    article.save()

#retrieve data from solr server
url = "http://127.0.0.1:8983/solr/collection1/select?q=section%3Apoetry&wt=json&indent=true&rows=2147483647"
json = json.loads(urllib2.urlopen(url).read().decode('utf-8'))

#extract metadata
num_found = json['response']['numFound']
documents = json['response']['docs']

#masterset maps words to articles that contain them
masterset = {}

#articleset maps articles to (word, frequency)
articleset = {}

#a list storing the django ids of all articles processed
django_ids = []

for doc in documents:
    #extract article metadata
    django_id = doc['django_id']
    django_ids += [django_id]

    #clean data
    text = cleanhtml(BeautifulSoup(doc['text']).text)
    text = text.translate(tbl)
    text = text.replace("nbsp", "")
    text = text.lower()

    #filter words to remove all non natural nouns
    is_nn = lambda pos: pos[:2] == 'NN'
    tokenized = nltk.word_tokenize(text)
    tokenized = [word for (word, pos) in nltk.pos_tag(tokenized) if is_nn(pos)]
    tokenized = [word for word in tokenized if word not in stopwords.words('english')]

    #count frequency of each word
    freqlist = Counter(tokenized);
    filteredfreqlist = [];

    for key, value in freqlist.iteritems():
        if value >= 2:
            filteredfreqlist += [(key, value)];
            if key in masterset:
                masterset[key] += [django_id]
            else:
                masterset[key] = [django_id]
        articleset[django_id] = sorted(filteredfreqlist, key=lambda (x, y): y, reverse=True);
newmasterset = dict(masterset)

#filter masterset threshold
for k, v in masterset.iteritems():
    if len(v) <= 1:
        del newmasterset[k]

#insert results into database
for ident in django_ids:
    insertIntoDatabase(ident, getSuggested(ident))


#insertIntoDatabase(29, [3])
#debug
#for key, value in masterset.iteritems():
    #if len(value) >= 4:
        #print("%s ::: %s" % (key, value))


