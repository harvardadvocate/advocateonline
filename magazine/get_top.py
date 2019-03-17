import os
import datetime
from collections import defaultdict

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http

from .models import Content
from blog.models import Post
from django.conf import settings

# Column indices. UNIQUE_PAGEVIEWS = 2, TIME_ON_PAGE = 3, etc.
PAGE_URL = 0
PAGEVIEWS = 1

# These are the columns numbers for the rows returned by the Google
# Analytics query. A row will look like
# [url, pageviews, uniquePageviews, timeOnPage, bounces, ...]
METRICS = ['ga:pageviews', 'ga:uniquePageviews', 'ga:timeOnPage',
           'ga:bounces', 'ga:entrances', 'ga:exits']

KEY_FILTERS = {
    # starts with /article or /blog/post
    'magazine': 'ga:pagePath=~/article/',
    'blog': 'ga:pagePath=~/blog/post/'
}


def slug_from_page_path(page_path):
    end = page_path.rfind('/')
    start = page_path.rfind('/', 0, end) + 1
    return page_path[start:end]

LAST_REFRESHED_TIME = None
GET_ANALYTICS_CACHE = None

# def get_analytics(top=10):
#     """
#     Generate list of the most read articles.

#     Grab the most visited urls from Google Analytics, find the
#     corresponding content, and return a sorted list consisting of tuples
#     of the corresponding Content/(Blog)Post Object and its number
#     of page views.
#     """

#     # Use cache data if it is within last day
#     global LAST_REFRESHED_TIME
#     global GET_ANALYTICS_CACHE
    
#     if LAST_REFRESHED_TIME != None and LAST_REFRESHED_TIME - datetime.datetime.now() < datetime.timedelta(days=1):
#         return GET_ANALYTICS_CACHE

#     end_date = datetime.datetime.now()
#     start_date = end_date - datetime.timedelta(days=10)

#     # Authorize an http object with our stored credentials
#     credentials = ServiceAccountCredentials.from_json_keyfile_dict(
#         settings.ANALYTICS_CONFIG,
#         scopes='https://www.googleapis.com/auth/analytics.readonly')
#     http_auth = credentials.authorize(Http())
#     analytics = build('analytics', 'v3', http=http_auth)

#     # Copy defaults
#     DEFAULT_QUERY_OPTIONS = {
#         'ids': 'ga:97067115',
#         'start_date': start_date.strftime('%Y-%m-%d'),
#         'end_date': end_date.strftime('%Y-%m-%d'),
#         'dimensions': 'ga:pagePath',
#         'metrics': ','.join(METRICS),
#         'sort': '-ga:pageviews',
#         'max_results': '15'
#     }
#     query_options = dict(DEFAULT_QUERY_OPTIONS)
#     article_views = defaultdict(int)

#     for (key, filters) in KEY_FILTERS.items():
#         print 'Fetching most read for key "{}"'.format(key)

#         query_options['filters'] = filters
#         query = analytics.data().ga().get(**query_options)
#         results = query.execute()
#         for entry in results['rows']:
#                 # see `METRICS` for entry format
#             page_path = entry[PAGE_URL]
#             slug = slug_from_page_path(page_path)
#             pageviews = int(entry[PAGEVIEWS])

#             content = None
#             # Try to find the content from the url
#             if '/article/' in page_path:
#                 matches = Content.objects.filter(slug=slug)
#                  # If there are duplicate slugs, assume the most recent
#                 if matches:
#                     content = matches.order_by('-publishDate').first()
#             elif '/blog/' in page_path:
#                 matches = Post.objects.filter(slug=slug)
#                 # If there are duplicate slugs, assume the most recent
#                 if matches:
#                     content = matches.order_by('-created').first()
#             else:
#                 content = None

#             # If we found something, add it to our list
#             if content:
#                 article_views[content] += pageviews
#             else:
#                 print 'ERROR: could not find %s' % page_path

#         # sort all content and return
#         articles = sorted(article_views.items(),
#                           key=lambda x: x[1], reverse=True)[:top]
#     for idx, article in enumerate(articles):
#         print '\t{}. {}, {}'.format(idx + 1,
#                                     article[0].title.encode('utf-8'), article[1])

#     print(articles)

#     if len(articles) == top:
#         GET_ANALYTICS_CACHE = articles
#         LAST_REFRESHED_TIME = datetime.datetime.now()        
#         return articles
#     else:
#         print "\tCouldn't find five most read articles; skipping"
#         return None
