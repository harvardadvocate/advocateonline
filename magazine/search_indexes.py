from haystack import indexes
from .models import Content
from .models import Section
from blog.models import Post

class ContentIndex(indexes.SearchIndex, indexes.Indexable):
    title = indexes.CharField(model_attr='title')
    section = indexes.CharField()
    text = indexes.CharField(document=True, use_template=True)
    suggestions = indexes.CharField()

    def prepare(self, obj):
        prepared_data = super(ContentIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text'][0:300]
        return prepared_data

    def prepare_section(self, obj):
        return obj.section.name

    def get_model(self):
        return Content

    def index_queryset(self, using=None):
        return self.get_model().objects.all().select_related('section')

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    title = indexes.CharField(model_attr='title')
    section = indexes.CharField()
    text = indexes.CharField(document=True, use_template=True)
    suggestions = indexes.CharField()

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
