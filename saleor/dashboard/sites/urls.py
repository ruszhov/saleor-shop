from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='site-index'),
    url(r'^(?P<pk>\d+)/update/$', views.site_settings_edit,
        name='site-update'),
    url(r'^(?P<pk>\d+)/$', views.site_settings_details,
        name='site-details'),
    url(r'^(?P<pk>\d+)/delete/$', views.site_settings_edit,
        name='site-delete'),

    url(r'^(?P<site_settings_pk>\d+)/authorization_key/add/$',
        views.authorization_key_add, name='authorization-key-add'),
    url(r'^(?P<site_settings_pk>\d+)/authorization_key/'
        r'(?P<key_pk>\d+)/update/$',
        views.authorization_key_edit, name='authorization-key-edit'),
    url(r'^(?P<site_settings_pk>\d+)/authorization_key/'
        r'(?P<key_pk>\d+)/delete/$',
        views.authorization_key_delete, name='authorization-key-delete'),
    

    url(r'^(?P<pk>[0-9]+)/translations/(?P<translation_pk>[0-9]+)$',
        views.site_settings_translation_details, name='site-settings-translation-details'),
    url(r'^add/site_settings/translation/$',
        views.site_settings_translation_create, name='site-settings-translation-add'),
    url(r'^(?P<pk>[0-9]+)/translation/add/$',
        views.site_settings_translation_create, name='site-settings-translation-add'),
    url(r'^(?P<pk>[0-9]+)/translations/(?P<translation_pk>[0-9]+)/edit/$',
        views.site_settings_translation_edit, name='site-settings-translation-update'),
    url(r'^(?P<pk>[0-9]+)/translations/(?P<translation_pk>[0-9]+)/delete/$',
        views.site_settings_translation_delete, name='site-settings-translation-delete')
]
