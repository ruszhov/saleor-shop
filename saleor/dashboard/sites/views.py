from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import pgettext_lazy

from ...site.models import AuthorizationKey, SiteSettings, SiteSettingsTranslation
from ..views import staff_member_required
from .forms import AuthorizationKeyForm, SiteForm, SiteSettingsForm, SiteSettingsTranslationForm


@staff_member_required
@permission_required('site.manage_settings')
def index(request):
    site = get_current_site(request)
    settings = site.settings
    return redirect('dashboard:site-details', pk=settings.pk)


@staff_member_required
@permission_required('site.manage_settings')
def site_settings_edit(request, pk):
    site_settings = get_object_or_404(SiteSettings, pk=pk)
    site = site_settings.site
    site_settings_form = SiteSettingsForm(
        request.POST or None, instance=site_settings)
    site_form = SiteForm(request.POST or None, instance=site)

    if site_settings_form.is_valid() and site_form.is_valid():
        site = site_form.save()
        site_settings_form.instance.site = site
        site_settings = site_settings_form.save()
        messages.success(request, pgettext_lazy(
            'Dashboard message', 'Updated site settings'))
        return redirect('dashboard:site-details', pk=site_settings.id)
    ctx = {'site_settings': site_settings,
           'site_settings_form': site_settings_form,
           'site_form': site_form}
    return TemplateResponse(request, 'dashboard/sites/form.html', ctx)


@staff_member_required
@permission_required('site.manage_settings')
def site_settings_details(request, pk):
    site_settings = get_object_or_404(SiteSettings, pk=pk)
    authorization_keys = AuthorizationKey.objects.filter(
        site_settings=site_settings)
    translations = site_settings.translations.all()
    ctx = {
        'site_settings': site_settings,
        'translations': translations,
        'authorization_keys': authorization_keys,
        'is_empty': not authorization_keys.exists()}
    return TemplateResponse(request, 'dashboard/sites/detail.html', ctx)


@staff_member_required
@permission_required('site.manage_settings')
def authorization_key_add(request, site_settings_pk):
    key = AuthorizationKey(site_settings_id=site_settings_pk)
    form = AuthorizationKeyForm(request.POST or None, instance=key)
    if form.is_valid():
        key = form.save()
        msg = pgettext_lazy(
            'Dashboard message', 'Added authorization key %s') % (key,)
        messages.success(request, msg)
        return redirect('dashboard:site-details', pk=site_settings_pk)
    ctx = {'form': form, 'site_settings_pk': site_settings_pk, 'key': key}
    return TemplateResponse(
        request, 'dashboard/sites/authorization_keys/form.html', ctx)


@staff_member_required
@permission_required('site.manage_settings')
def authorization_key_edit(request, site_settings_pk, key_pk):
    key = get_object_or_404(AuthorizationKey, pk=key_pk)
    form = AuthorizationKeyForm(request.POST or None, instance=key)
    if form.is_valid():
        key = form.save()
        msg = pgettext_lazy(
            'dashboard message', 'Updated authorization key %s') % (key,)
        messages.success(request, msg)
        return redirect('dashboard:site-details', pk=site_settings_pk)
    ctx = {'form': form, 'site_settings_pk': site_settings_pk, 'key': key}
    return TemplateResponse(
        request, 'dashboard/sites/authorization_keys/form.html', ctx)


@staff_member_required
@permission_required('site.manage_settings')
def authorization_key_delete(request, site_settings_pk, key_pk):
    key = get_object_or_404(AuthorizationKey, pk=key_pk)
    if request.method == 'POST':
        key.delete()
        messages.success(
            request,
            pgettext_lazy(
                'Dashboard message',
                'Removed site authorization key %s') %
            (key,))
        return redirect(
            'dashboard:site-details', pk=site_settings_pk)
    return TemplateResponse(
        request, 'dashboard/sites/modal/confirm_delete.html',
        {'key': key, 'site_settings_pk': site_settings_pk})


@staff_member_required
@permission_required('product.manage_products')
def site_settings_translation_details(request, pk, translation_pk):
    site_settings = get_object_or_404(SiteSettings, pk=pk)
    translation = get_object_or_404(site_settings.translations.all(), pk=translation_pk)

    ctx = {
        'site_settings': site_settings, 'translation': translation}
    return TemplateResponse(
        request,
        'dashboard/sites/site_settings_translation/detail.html',
        ctx)

@staff_member_required
@permission_required('site_settings.manage_products')
def site_settings_translation_create(request, pk):
    site_settings = get_object_or_404(SiteSettings.objects.all(), pk=pk)
    form = SiteSettingsTranslationForm(request.POST or None)
    if form.is_valid():
        cat_trans = form.save(commit=False)
        # cat_trans.id = site_settingsTranslation.objects.all().aggregate(Max('id'))['id__max'] + 1
        cat_trans.site_settings_id = pk
        cat_trans.save()
        msg = pgettext_lazy(
            'Dashboard message', 'Saved site_settingss %s') % (site_settings.header_text,)
        messages.success(request, msg)
        return redirect(
            'dashboard:site-details', pk=site_settings.pk)
    ctx = {'form': form, 'site_settings': site_settings}
    return TemplateResponse(
        request,
        'dashboard/sites/site_settings_translation/form.html',
        ctx)

@staff_member_required
@permission_required('site_settings.manage_products')
def site_settings_translation_edit(request, pk, translation_pk):
    site_settings = get_object_or_404(SiteSettings.objects.all(), pk=pk)
    translation = get_object_or_404(site_settings.translations.all(), pk=translation_pk)
    form = SiteSettingsTranslationForm(request.POST or None, instance=translation)
    if form.is_valid():
        form.save()
        msg = pgettext_lazy(
            'Dashboard message', 'Saved site_settingss %s') % (translation.header_text,)
        messages.success(request, msg)
        return redirect(
            'dashboard:site-settings-translation-details', pk=site_settings.pk,
            translation_pk=translation.pk)
    ctx = {'form': form, 'site_settings': site_settings, 'translation': translation}
    return TemplateResponse(
        request,
        'dashboard/sites/site_settings_translation/form.html',
        ctx)

@staff_member_required
@permission_required('product.manage_products')
def site_settings_translation_delete(request, pk, translation_pk):
    site_settings = get_object_or_404(SiteSettings, pk=pk)
    translation = get_object_or_404(site_settings.translations, pk=translation_pk)
    if request.method == 'POST':
        translation.delete()
        msg = pgettext_lazy(
            'Dashboard message', 'Removed translation %s') % (translation.header_text,)
        messages.success(request, msg)
        return redirect('dashboard:site-details', pk=site_settings.pk)
    ctx = {
        'site_settings': site_settings,
        'translation': translation}
    return TemplateResponse(
        request,
        'dashboard/sites/site_settings_translation/modal/confirm_delete.html',
        ctx)
