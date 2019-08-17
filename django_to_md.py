import os
import re
from pprint import pprint

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "advo.settings")

# your imports, e.g. Django models
from magazine.models import Article, Image

def convert_to_md(article):
    from markdownify import markdownify as md
    def slugify(value):
        import re
        """
        Normalizes string, converts to lowercase, removes non-alpha characters,
        and converts spaces to hyphens.
        """
        import unicodedata
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
        value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
        value = unicode(re.sub('[-\s]+', '-', value))
        return value
    import unicodedata
    images = []
    if article.photo:
        images.append(str(article.photo))

    authors = []
    for author in article.contributors.all():
        authors.append(author.name.encode('utf-8'))

    title = unicodedata.normalize('NFKD', article.title).encode('ascii', 'ignore')
    title = title.replace('"', '\\"')
    
    date_map = {
        "Winter": "{}-01-01",
        "Spring": "{}-03-01",
        "Summer": "{}-06-01",
        "Commencement": "{}-06-01",
        "Fall": "{}-09-01"
    }

    with open('generated/' + slugify(article.title)+".md","w+") as f:
        f.write('---\n')
        f.write('title: "' + title + '"\n')
        f.write('slug: "' + slugify(article.title) + '"\n')
        f.write('issue: "' + str(article.issue).split()[0] + '"\n')
        f.write('issue_full_name: "' + str(article.issue) + '"\n')
        f.write('year: "' + str(article.issue).split()[1] + '"\n')
        f.write('date: "' + date_map[str(article.issue).split()[0]].format(str(article.issue).split()[1]) + '"\n')
        f.write('authors: ' + str(authors) + '\n')
        f.write('section: "' + str(article.section).lower() + '"\n')
        f.write('audio: []\n')
        f.write('main_image: ""\n')
        f.write('banner_image: ""\n')
        f.write("images: {}\n".format(images))
        f.write("videos: []\n")
        f.write('---\n')
        f.write(md(article.body).encode('utf-8'))

for article in Article.objects.all():
    convert_to_md(article)

for article in Image.objects.all():
    convert_to_md(article)