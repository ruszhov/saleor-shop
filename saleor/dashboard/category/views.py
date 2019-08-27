from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import pgettext_lazy

from ...core.utils import get_paginator_items
from ...product.models import Category, CategoryTranslation
from ..menu.utils import get_menus_that_needs_update, update_menus
from ..views import staff_member_required
from .filters import CategoryFilter
from .forms import CategoryForm, CategoryTranslationForm

from django.db.models import Max

@staff_member_required
@permission_required('product.manage_products')
def category_list(request):
    categories = Category.tree.root_nodes().order_by('name')
    category_filter = CategoryFilter(request.GET, queryset=categories)
    categories = get_paginator_items(
        category_filter.qs, settings.DASHBOARD_PAGINATE_BY,
        request.GET.get('page'))
    ctx = {
        'categories': categories, 'filter_set': category_filter,
        'is_empty': not category_filter.queryset.exists()}
    return TemplateResponse(request, 'dashboard/category/list.html', ctx)


@staff_member_required
@permission_required('product.manage_products')
def category_create(request, root_pk=None):
    path = None
    category = Category()
    if root_pk:
        root = get_object_or_404(Category, pk=root_pk)
        path = root.get_ancestors(include_self=True) if root else []
    form = CategoryForm(
        request.POST or None, request.FILES or None, parent_pk=root_pk)
    if form.is_valid():
        category = form.save()
        messages.success(
            request,
            pgettext_lazy(
                'Dashboard message', 'Added category %s') % category)
        if root_pk:
            return redirect('dashboard:category-details', pk=root_pk)
        return redirect('dashboard:category-list')
    ctx = {'category': category, 'form': form, 'path': path}
    return TemplateResponse(request, 'dashboard/category/form.html', ctx)


@staff_member_required
@permission_required('category.manage_products')
def category_translation_create(request, root_pk):
    category = get_object_or_404(Category.objects.all(), pk=root_pk)
    form = CategoryTranslationForm(request.POST or None)
    if form.is_valid():
        cat_trans = form.save(commit=False)
        cat_trans.id = CategoryTranslation.objects.all().aggregate(Max('id'))['id__max'] + 1
        cat_trans.category_id = root_pk
        cat_trans.save()
        msg = pgettext_lazy(
            'Dashboard message', 'Saved categorie %s') % (category.name,)
        messages.success(request, msg)
        return redirect(
            'dashboard:category-details', pk=category.pk)
    ctx = {'form': form, 'category': category}
    return TemplateResponse(
        request,
        'dashboard/category/category_translation/form.html',
        ctx)


@staff_member_required
@permission_required('product.manage_products')
def category_edit(request, root_pk=None):
    path = None
    category = get_object_or_404(Category, pk=root_pk)
    if root_pk:
        root = get_object_or_404(Category, pk=root_pk)
        path = root.get_ancestors(include_self=True) if root else []
    form = CategoryForm(
        request.POST or None, request.FILES or None, instance=category,
        parent_pk=category.parent_id)
    status = 200
    if form.is_valid():
        category = form.save()
        messages.success(
            request,
            pgettext_lazy(
                'Dashboard message', 'Updated category %s') % category)
        if root_pk:
            return redirect('dashboard:category-details', pk=root_pk)
        return redirect('dashboard:category-list')
    elif form.errors:
        status = 400
    ctx = {'category': category, 'form': form, 'status': status, 'path': path}
    template = 'dashboard/category/form.html'
    return TemplateResponse(request, template, ctx, status=status)


@staff_member_required
@permission_required('category.manage_products')
def category_translation_edit(request, root_pk, translation_pk):
    category = get_object_or_404(Category.objects.all(), pk=root_pk)
    translation = get_object_or_404(category.translations.all(), pk=translation_pk)
    form = CategoryTranslationForm(request.POST or None, instance=translation)
    if form.is_valid():
        form.save()
        msg = pgettext_lazy(
            'Dashboard message', 'Saved variant %s') % (translation.name,)
        messages.success(request, msg)
        return redirect(
            'dashboard:category-translation-details', pk=category.pk,
            translation_pk=translation.pk)
    ctx = {'form': form, 'category': category, 'translation': translation}
    return TemplateResponse(
        request,
        'dashboard/category/category_translation/form.html',
        ctx)


@staff_member_required
@permission_required('product.manage_products')
def category_details(request, pk):
    categories_all = Category.objects.prefetch_related('translations').all()
    root = get_object_or_404(categories_all, pk=pk)
    path = root.get_ancestors(include_self=True) if root else []
    categories = root.get_children().order_by('name')
    category_filter = CategoryFilter(request.GET, queryset=categories)
    translations = root.translations.all()
    categories = get_paginator_items(
        category_filter.qs, settings.DASHBOARD_PAGINATE_BY,
        request.GET.get('page'))
    ctx = {'categories': categories, 'path': path, 'root': root,
           'filter_set': category_filter, 'translations':translations,
           'is_empty': not category_filter.queryset.exists()}
    return TemplateResponse(request, 'dashboard/category/detail.html', ctx)


@staff_member_required
@permission_required('product.manage_products')
def category_translation_details(request, pk, translation_pk):
    category = get_object_or_404(Category, pk=pk)
    translation = get_object_or_404(category.translations.all(), pk=translation_pk)

    ctx = {
        'category': category, 'translation': translation}
    return TemplateResponse(
        request,
        'dashboard/category/category_translation/detail.html',
        ctx)


@staff_member_required
@permission_required('product.manage_products')
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        descendants = category.get_descendants()
        menus = get_menus_that_needs_update(categories=descendants)
        category.delete()
        if menus:
            update_menus(menus)
        messages.success(
            request,
            pgettext_lazy(
                'Dashboard message', 'Removed category %s') % category)
        root_pk = None
        if category.parent:
            root_pk = category.parent.pk
        if root_pk:
            if request.is_ajax():
                response = {'redirectUrl': reverse(
                    'dashboard:category-details', kwargs={'pk': root_pk})}
                return JsonResponse(response)
            return redirect('dashboard:category-details', pk=root_pk)
        else:
            if request.is_ajax():
                response = {'redirectUrl': reverse('dashboard:category-list')}
                return JsonResponse(response)
            return redirect('dashboard:category-list')
    ctx = {'category': category,
           'descendants': list(category.get_descendants()),
           'products_count': len(category.products.all())}
    return TemplateResponse(
        request, 'dashboard/category/modal/confirm_delete.html', ctx)

@staff_member_required
@permission_required('product.manage_products')
def category_translation_delete(request, pk, translation_pk):
    category = get_object_or_404(Category, pk=pk)
    translation = get_object_or_404(category.translations, pk=translation_pk)
    if request.method == 'POST':
        translation.delete()
        msg = pgettext_lazy(
            'Dashboard message', 'Removed translation %s') % (translation.name,)
        messages.success(request, msg)
        return redirect('dashboard:category-details', pk=category.pk)
    ctx = {
        'category': category,
        'translation': translation}
    return TemplateResponse(
        request,
        'dashboard/category/category_translation/modal/confirm_delete.html',
        ctx)
