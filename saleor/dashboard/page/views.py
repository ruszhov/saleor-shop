from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import pgettext_lazy

from ...core.utils import get_paginator_items
from ...page.models import Page, PageTranslation
from ..menu.utils import get_menus_that_needs_update, update_menus
from ..views import staff_member_required
from .filters import PageFilter
from .forms import PageForm, PageTranslationForm

from django.db.models import Max


@staff_member_required
@permission_required('page.manage_pages')
def page_list(request):
    pages = Page.objects.all()
    pages_filter = PageFilter(request.GET, queryset=pages)
    pages = get_paginator_items(
        pages_filter.qs, settings.DASHBOARD_PAGINATE_BY,
        request.GET.get('page'))
    ctx = {
        'pages': pages, 'filter_set': pages_filter,
        'is_empty': not pages_filter.queryset.exists()}
    return TemplateResponse(request, 'dashboard/page/list.html', ctx)


@staff_member_required
@permission_required('page.manage_pages')
def page_update(request, pk):
    page = get_object_or_404(Page, pk=pk)
    return _page_edit(request, page)


@staff_member_required
@permission_required('page.manage_pages')
def page_add(request):
    page = Page()
    return _page_edit(request, page)


def _page_edit(request, page):
    form = PageForm(request.POST or None, instance=page)
    if form.is_valid():
        form.save()
        msg = pgettext_lazy('Dashboard message', 'Saved page')
        messages.success(request, msg)
        return redirect('dashboard:page-details', pk=page.pk)
    ctx = {
        'page': page, 'form': form}
    return TemplateResponse(request, 'dashboard/page/form.html', ctx)


@staff_member_required
@permission_required('page.manage_pages')
def page_delete(request, pk):
    page = get_object_or_404(Page, pk=pk)
    if request.POST:
        menus = get_menus_that_needs_update(page=page)
        page.delete()
        if menus:
            update_menus(menus)
        msg = pgettext_lazy(
            'Dashboard message', 'Removed page %s') % (page.title,)
        messages.success(request, msg)
        return redirect('dashboard:page-list')
    ctx = {'page': page}
    return TemplateResponse(request, 'dashboard/page/modal_delete.html', ctx)


@staff_member_required
@permission_required('page.manage_pages')
def page_details(request, pk):
    page = get_object_or_404(Page, pk=pk)
    translations = page.translations.all()
    ctx = {'page': page, 'translations': translations}
    return TemplateResponse(request, 'dashboard/page/detail.html', ctx)


@staff_member_required
@permission_required('product.manage_products')
def page_translation_details(request, pk, translation_pk):
    page = get_object_or_404(Page, pk=pk)
    translation = get_object_or_404(page.translations.all(), pk=translation_pk)

    ctx = {
        'page': page, 'translation': translation}
    return TemplateResponse(
        request,
        'dashboard/page/page_translation/detail.html',
        ctx)

@staff_member_required
@permission_required('page.manage_products')
def page_translation_create(request, pk):
    page = get_object_or_404(Page.objects.all(), pk=pk)
    form = PageTranslationForm(request.POST or None)
    if form.is_valid():
        cat_trans = form.save(commit=False)
        # cat_trans.id = PageTranslation.objects.all().aggregate(Max('id'))['id__max'] + 1
        cat_trans.page_id = pk
        cat_trans.save()
        msg = pgettext_lazy(
            'Dashboard message', 'Saved pages %s') % (page.title,)
        messages.success(request, msg)
        return redirect(
            'dashboard:page-details', pk=page.pk)
    ctx = {'form': form, 'page': page}
    return TemplateResponse(
        request,
        'dashboard/page/page_translation/form.html',
        ctx)

@staff_member_required
@permission_required('page.manage_products')
def page_translation_edit(request, pk, translation_pk):
    page = get_object_or_404(Page.objects.all(), pk=pk)
    translation = get_object_or_404(page.translations.all(), pk=translation_pk)
    form = PageTranslationForm(request.POST or None, instance=translation)
    if form.is_valid():
        form.save()
        msg = pgettext_lazy(
            'Dashboard message', 'Saved pages %s') % (translation.title,)
        messages.success(request, msg)
        return redirect(
            'dashboard:page-translation-details', pk=page.pk,
            translation_pk=translation.pk)
    ctx = {'form': form, 'page': page, 'translation': translation}
    return TemplateResponse(
        request,
        'dashboard/page/page_translation/form.html',
        ctx)

@staff_member_required
@permission_required('product.manage_products')
def page_translation_delete(request, pk, translation_pk):
    page = get_object_or_404(Page, pk=pk)
    translation = get_object_or_404(page.translations, pk=translation_pk)
    if request.method == 'POST':
        translation.delete()
        msg = pgettext_lazy(
            'Dashboard message', 'Removed translation %s') % (translation.title,)
        messages.success(request, msg)
        return redirect('dashboard:page-details', pk=page.pk)
    ctx = {
        'page': page,
        'translation': translation}
    return TemplateResponse(
        request,
        'dashboard/page/page_translation/modal/confirm_delete.html',
        ctx)
