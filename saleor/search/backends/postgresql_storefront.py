from django.contrib.postgres.search import (
    SearchQuery, SearchRank, SearchVector)

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q, Count

from ...product.models import Product
from django.utils import translation
import re
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.utils import translation

def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

def num_there(s):
    return any(i.isdigit() for i in s)

def search(phrase):
    """Return matching products for storefront views.

    Fuzzy storefront search that is resistant to small typing errors made
    by user. Name is matched using trigram similarity, description uses
    standard postgres full text search.

    Args:
        phrase (str): searched phrase

    """
    name_sim = TrigramSimilarity('name', phrase)
    sku = TrigramSimilarity('variants__sku', phrase)
    published = Q(is_published=True)
    ft_in_description = Q(description__search=phrase)
    name_similar = Q(name_sim__gt=0.2)
    sku_similar = Q(sku__gt=0.7)
    lang = translation.get_language()

    vector = SearchVector('translations__name', weight='A') + \
             SearchVector('translations__description', wheight='B') +\
             SearchVector('translations__language_code', weight='C')

    if not num_there(phrase):
        if has_cyrillic(phrase) is True:
            return Product.objects.annotate(search=vector).filter(search=SearchQuery(lang) & SearchQuery(phrase))
        else:
            en_res = Product.objects.annotate(name_sim=name_sim).filter((ft_in_description | name_similar) & published)
            if en_res.count() != 0:
                return en_res
            else:
                return Product.objects.annotate(search=vector).filter(search=SearchQuery(phrase) & SearchQuery('pl'))
    else:
        return Product.objects.annotate(sku=sku).filter(sku_similar & published)
