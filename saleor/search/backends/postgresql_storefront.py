from django.contrib.postgres.search import (
    SearchQuery, SearchRank, SearchVector)

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q

from ...product.models import Product
from django.utils import translation
import re

def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

def search(phrase):
    """Return matching products for storefront views.

    Fuzzy storefront search that is resistant to small typing errors made
    by user. Name is matched using trigram similarity, description uses
    standard postgres full text search.

    Args:
        phrase (str): searched phrase

    """
    name_sim = TrigramSimilarity('name', phrase)
    tr_name = TrigramSimilarity('translations__name', phrase)
    sku = TrigramSimilarity('variants__sku', phrase)
    published = Q(is_published=True)
    ft_in_description = Q(description__search=phrase)
    name_similar = Q(name_sim__gt=0.2)
    tr_name_similar = Q(tr_name__gt=0.2)
    sku_similar = Q(sku__gt=0.7)
    if phrase.isalpha():
        if has_cyrillic(phrase) is True:
            return Product.objects.annotate(tr_name=tr_name).filter((ft_in_description | tr_name_similar) & published)
        else:
            return Product.objects.annotate(name_sim=name_sim).filter((ft_in_description | name_similar) & published)
    else:
        return Product.objects.annotate(sku=sku).filter(sku_similar & published)
