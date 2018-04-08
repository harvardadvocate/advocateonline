from .models import Article, Content, Image, Issue, Contributor
from blog.models import Post, Author
from django.core import serializers
import json

def search_typeahead(request):
    author_list = []
    for dict in Contributor.objects.values():
        author_list.append(dict['name'])
    for dict in Author.objects.values():
        author_list.append(dict['name'])

    title_list = []
    for dict in Article.objects.values():
        title_list.append(dict['title'])
    for dict in Post.objects.values():
        title_list.append(dict['title'])

    return {'typeahead_authors' : json.dumps(list(author_list)), 'typeahead_titles' : json.dumps(list(title_list))}
