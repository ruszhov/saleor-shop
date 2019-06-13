from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.page_list, name='page-list'),
    url(r'^add/$', views.page_add, name='page-add'),
    url(r'^(?P<pk>[0-9]+)/$', views.page_details, name='page-details'),
    url(r'^(?P<pk>[0-9]+)/update/$', views.page_update, name='page-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.page_delete, name='page-delete'),

    url(r'^(?P<pk>[0-9]+)/translations/(?P<translation_pk>[0-9]+)$',
        views.page_translation_details, name='page-translation-details'),
    url(r'^add/page/translation/$',
        views.page_translation_create, name='page-translation-add'),
    url(r'^(?P<pk>[0-9]+)/translation/add/$',
        views.page_translation_create, name='page-translation-add'),
    url(r'^(?P<pk>[0-9]+)/translations/(?P<translation_pk>[0-9]+)/edit/$',
        views.page_translation_edit, name='page-translation-update'),
    url(r'^(?P<pk>[0-9]+)/translations/(?P<translation_pk>[0-9]+)/delete/$',
        views.page_translation_delete, name='page-translation-delete')
]
