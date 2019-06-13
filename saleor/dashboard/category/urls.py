from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',
        views.category_list, name='category-list'),
    url(r'^(?P<pk>[0-9]+)/$',
        views.category_details, name='category-details'),
    url(r'^add/$',
        views.category_create, name='category-add'),
    url(r'^(?P<root_pk>[0-9]+)/add/$',
        views.category_create, name='category-add'),
    url(r'^(?P<root_pk>[0-9]+)/edit/$',
        views.category_edit, name='category-edit'),
    url(r'^(?P<pk>[0-9]+)/delete/$',
        views.category_delete, name='category-delete'),

    url(r'^(?P<pk>[0-9]+)/translations/(?P<translation_pk>[0-9]+)$',
        views.category_translation_details, name='category-translation-details'),
    url(r'^add/category/translation/$',
        views.category_translation_create, name='category-translation-add'),
    url(r'^(?P<root_pk>[0-9]+)/translation/add/$',
        views.category_translation_create, name='category-translation-add'),
    url(r'^(?P<root_pk>[0-9]+)/translations/(?P<translation_pk>[0-9]+)/edit/$',
        views.category_translation_edit, name='category-translation-update'),
    url(r'^(?P<pk>[0-9]+)/translations/(?P<translation_pk>[0-9]+)/delete/$',
        views.category_translation_delete, name='category-translation-delete')]
