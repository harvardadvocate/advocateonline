from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from ajax_select import urls as ajax_select_urls

from magazine.views import FilterSearchView
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/magazine/images/favicon.ico', permanent=True)

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'magazine.views.index'),
    url(r'^issues$', 'magazine.views.issues'),
    url(r'^about$', 'magazine.views.masthead'),
    url(r'^issue/(?P<season>[a-zA-Z]+)-(?P<year>[\d]{4})/$', 'magazine.views.singleissue'),
    url(r'^subscribe$', 'payments.views.subscribe'),
    url(r'^submit$', 'magazine.views.submit'),
    url(r'^contact$', 'magazine.views.contact'),
    url(r'^alumni$', 'magazine.views.alumni'),
    url(r"^fiction/$|^poetry/$|^art/$|^features/$|^columns/$|^notes/$", 'magazine.views.sections'),
    url(r'^advertise$', 'magazine.views.advertise'),
    url(r'^adSubmit$', 'magazine.views.adSubmit'),
    url(r'^150th$', 'magazine.views.onefifty'),
    url(r'^shop$', 'magazine.views.shop'),
    url(r'^shop/(?P<id>\d+)$', 'magazine.views.shopItemView'),
    url(r'^cart$', 'magazine.views.cart'),
    url(r'^shop-admin$', 'magazine.views.shop_admin'),
    url(r'^shop-upload$', 'magazine.views.shop_upload'),
    url(r'^shop-delete$', 'magazine.views.shop_delete'),
    url(r'^benefit$', 'magazine.views.gala'),
    url(r'^financialaid$', 'magazine.views.financialaid'),
    url(r'^comp$', 'magazine.views.comp'),
    url(r'^article/(?P<id>[\d]+)/(?P<slug>[a-zA-Z\d_\-]+)/$', 'magazine.views.article'),
    url(r'^content/(?P<slug>[a-zA-Z\d_\-]+)/$', 'magazine.views.content_piece'),
    url(r'^contributor/(?P<author_id>[\d]+)/(?P<name>.*)/$', 'magazine.views.contributor_page'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^mce_filebrowser/', include('mce_filebrowser.urls')),
    url(r'^search(?:/(?P<type_filter>[art|features|poetry|fiction|blog]+))?/?$', FilterSearchView(), name='filter_search'),
    url(r'^blog/', include('blog.urls')),
    url(r'^shopSubmit$','payments.views.shopSubmit'),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^tinymce/', include('tinymce.urls')),

    url(r'^donate$', 'payments.views.donate'),
    url(r'^sendDonation$','payments.views.sendDonation'),
    url(r'^galadonation$','payments.views.galaDonation'),
    url(r'^financialdonation$', 'payments.views.financialdonation'),
    url(r'^stripeSubmit$','payments.views.stripeSubmit'),
    url(r'^stripeSubmitShop$','payments.views.stripeSubmitShop'),
    #http://stackoverflow.com/questions/901551/how-do-i-include-image-files-in-django-templates
    #http://stackoverflow.com/questions/19132123/name-settings-is-not-defined
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^anthology/', include('anthology.urls')),
    url(r'^advertisement$',include('advertisement.urls')),
    url(r'^favicon\.ico$', favicon_view),

    url(r'^explore_archives', 'magazine.views.explore_archives')
)

