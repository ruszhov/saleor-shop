import datetime
import json

from django.http import HttpResponsePermanentRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from ..checkout.utils import set_cart_cookie
from ..core.utils import serialize_decimal
from ..seo.schema.product import product_json_ld
from .filters import ProductCategoryFilter, ProductCollectionFilter
from .models import Category, CategoryTranslation, ProductVariant, Product, AttributeValue
from .utils import (
    collections_visible_to_user, get_product_images, get_product_list_context,
    handle_cart_form, products_for_cart, products_for_products_list,
    products_with_details)
from .utils.attributes import get_product_attributes_data
from .utils.availability import get_availability
from .utils.variants_picker import get_variant_picker_data
from django.template.defaultfilters import slugify

def product_details(request, slug, product_id, form=None):
    """Product details page.

    The following variables are available to the template:

    product:
        The Product instance itself.

    is_visible:
        Whether the product is visible to regular users (for cases when an
        admin is previewing a product before publishing).

    form:
        The add-to-cart form.

    price_range:
        The PriceRange for the product including all discounts.

    undiscounted_price_range:
        The PriceRange excluding all discounts.

    discount:
        Either a Price instance equal to the discount value or None if no
        discount was available.

    local_price_range:
        The same PriceRange from price_range represented in user's local
        currency. The value will be None if exchange rate is not available or
        the local currency is the same as site's default currency.
    """
    products = products_with_details(user=request.user)
    product = get_object_or_404(products, id=product_id)
    if product.get_slug() != slug:
        return HttpResponsePermanentRedirect(product.get_absolute_url())
    today = datetime.date.today()
    is_visible = (
        product.publication_date is None or product.publication_date <= today)
    if form is None:
        form = handle_cart_form(request, product, create_cart=False)[0]
    availability = get_availability(
        product, discounts=request.discounts, taxes=request.taxes,
        local_currency=request.currency)
    product_images = get_product_images(product)
    variant_picker_data = get_variant_picker_data(
        product, request.discounts, request.taxes, request.currency)
    product_attributes = get_product_attributes_data(product)
    show_variant_picker = all([v.attributes for v in product.variants.all()])
    json_ld_data = product_json_ld(product, product_attributes)
    categories = Category.objects.prefetch_related('translations')

    # sku = get_object_or_404(ProductVariant, product_id=product_id)
    sku = ProductVariant.objects.filter(product_id=product_id).exclude(sku__contains="-")
    try:
        cat = get_object_or_404(categories, pk=request.session.get('category_id'))
    except:
        cat = Product.objects.prefetch_related('products').all()
    try:
        parent = get_object_or_404(categories, pk=cat.parent_id)
    except:
        parent = None

    if parent:
        ctx = {
            'is_visible': is_visible,
            'form': form,
            'availability': availability,
            'product': product,
            'prod_cat': cat,
            'sku': sku,
            'parent_cat': parent,
            'product_attributes': product_attributes,
            'product_images': product_images,
            'show_variant_picker': show_variant_picker,
            'variant_picker_data': json.dumps(
                variant_picker_data, default=serialize_decimal),
            'json_ld_product_data': json.dumps(
                json_ld_data, default=serialize_decimal)}
    else:
        ctx = {
            'is_visible': is_visible,
            'form': form,
            'availability': availability,
            'product': product,
            'prod_cat': cat,
            'sku': sku,
            'product_attributes': product_attributes,
            'product_images': product_images,
            'show_variant_picker': show_variant_picker,
            'variant_picker_data': json.dumps(
                variant_picker_data, default=serialize_decimal),
            'json_ld_product_data': json.dumps(
                json_ld_data, default=serialize_decimal)}

    return TemplateResponse(request, 'product/details.html', ctx)


def product_add_to_cart(request, slug, product_id):
    # types: (int, str, dict) -> None

    if not request.method == 'POST':
        return redirect(reverse(
            'product:details',
            kwargs={'product_id': product_id, 'slug': slug}))

    products = products_for_cart(user=request.user)
    product = get_object_or_404(products, pk=product_id)
    form, cart = handle_cart_form(request, product, create_cart=True)
    if form.is_valid():
        form.save()
        if request.is_ajax():
            response = JsonResponse(
                {'next': reverse('cart:index')}, status=200)
        else:
            response = redirect('cart:index')
    else:
        if request.is_ajax():
            response = JsonResponse({'error': form.errors}, status=400)
        else:
            response = product_details(request, slug, product_id, form)
    if not request.user.is_authenticated:
        set_cart_cookie(cart, response)
    return response


def category_index(request, slug, category_id):
    categories = Category.objects.prefetch_related('translations')
    category = get_object_or_404(categories, id=category_id)
    # colors = Product.objects.filter(category=category_id)
    # list = []
    # for item in colors:
    #     color = ProductVariant.objects.filter(id=item.id)
    #     for c in color:
    #         slug_c = slugify(c)
    #         for a in slug_c:
    #             aid = AttributeValue.objects.filter(slug=slug_c)
    #             for item_id in aid:
    #                 list.append(item_id.id)
    # color_set = set(list)
    # products = Product.objects.filter(category=category_id)
    # for product in products:
    #     attributes = product.product_type.product_attributes.all()
    #     print(attributes)
    request.session['category_id'] = category_id
    if slug != category.slug:
        return redirect(
            'product:category', permanent=True, slug=category.slug,
            category_id=category_id)
    # Check for subcategories
    categories = category.get_descendants(include_self=True)
    products = products_for_products_list(user=request.user).filter(
        category__in=categories).order_by('name').distinct()
    for product in products:
        attributes = product.product_type.product_attributes.all()
    product_filter = ProductCategoryFilter(
        request.GET, queryset=products, category=category)
    ctx = get_product_list_context(request, product_filter)
    ctx.update({'object': category, 'attributes': attributes})
    return TemplateResponse(request, 'category/index.html', ctx)


def collection_index(request, slug, pk):
    collections = collections_visible_to_user(request.user).prefetch_related(
        'translations')
    collection = get_object_or_404(collections, id=pk)
    if collection.slug != slug:
        return HttpResponsePermanentRedirect(collection.get_absolute_url())
    products = products_for_products_list(user=request.user).filter(
        collections__id=collection.id).order_by('name')
    product_filter = ProductCollectionFilter(
        request.GET, queryset=products, collection=collection)
    ctx = get_product_list_context(request, product_filter)
    ctx.update({'object': collection})
    return TemplateResponse(request, 'collection/index.html', ctx)

def ajax_selected_variant(request):
    if request.method == "POST" and request.is_ajax():
        sku = ProductVariant.objects.get(pk=request.POST["value"]).sku
        if "(" in sku:
            index = sku.index("(")
            finsku = sku[:index]
            sku_db = ProductVariant.objects.get(sku=finsku)
            product_id = sku_db.product_id
            slug = slugify(Product.objects.get(id=product_id).name)
            response_url = slug + '-' + str(product_id)
            return JsonResponse(response_url, safe=False)
        else:
            return JsonResponse(False, safe=False)
    else:
        return JsonResponse(False, safe=False)
