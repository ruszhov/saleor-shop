"""
Import json data from JSON file to Datababse
"""
import os
import json
from ....product.models import ProductType, Product, ProductVariant, Attribute, AttributeValue, Category
from django.core.management.base import BaseCommand
from datetime import datetime
from ....settings import PROJECT_ROOT, DEFAULT_CURRENCY
import requests
import xmltodict
from django.utils.text import slugify
import graphene
import shutil
import decimal
from decimal import Decimal
from prices import Money
from django.contrib.postgres.fields import HStoreField

class Command(BaseCommand):

    def compare(self):
    #     #!!!
    #     url = (requests.get('https://www.par.com.pl/en/api/products/', auth=('v.perekhaylo@akvarium.pro', 'AQWA22222'), stream = True)).text
    # #     # print(url)
        data_folder = os.path.join(PROJECT_ROOT, 'saleor','api_par_com', 'resources', 'json_file')

        def Diff(li1, li2):
            li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
            return li_dif

        file_ids = []
        brak_sku = []
        db_ids = []

        with open(os.path.join(data_folder, "products_en.json"), encoding='utf-8') as data_file:
            data = json.loads(data_file.read())

            for data_object in data['products']['product']:

                sale = data_object.get('wyprzedaz', None)
                if sale == 'false':
                    id = data_object.get('id', None)
                    file_ids.append(int(id))
                else:
                    pass

        # Compare products in database and in file
        ids_form_bd = Product.objects.all()
        for bid in ids_form_bd:
            id = bid.id
            db_ids.append(id)

        file_ids.sort()
        db_ids.sort()

        if file_ids == db_ids:
            print("All products are synchronized!")
        else:
            diffrent = Diff(file_ids, db_ids)
            # print('diffrent:', diffrent)

            print("These products are not on the site PAR Bakula:")
            for i in diffrent:
                stock = ProductVariant.objects.filter(product_id=i)
                for sku in stock:
                    print(sku.sku)
                    # print('product_id:',i)

        #m2m comparing

        for data_object in data['products']['product']:
            sale = data_object.get('wyprzedaz', None)
            if sale == 'false':
                category_dict = data_object.get('kategorie', None)
                product_id = data_object.get('id', None)
                # print(category_dict)
                for cat, v in category_dict.items():
                    if type(v) is dict:
                        category_list = []
                        cat_id = v['@id']
                        categ = Category.objects.get(id=cat_id)
                        category_list.append(int(cat_id))
                        prod = Product.objects.get(id=product_id)
                        m2m = prod.category.all()
                        m2m_list = []
                        for m in m2m:
                            m2m_list.append(m.id)
                        if category_list == m2m_list:
                            pass
                        else:
                            diffrent = Diff(category_list, m2m_list)
                            if not diffrent:
                                pass
                            else:
                                print('product_id:',product_id)
                                for i in diffrent:
                                    product = Product.objects.get(pk=product_id)
                                    diffrent_category = Category.objects.get(pk=i)
                                    m2m = product.category.remove(diffrent_category)
                    else:
                        category_list = []
                        for d in v:
                            cat_id = d['@id']
                            category_list.append(int(cat_id))
                            categ = Category.objects.get(id=cat_id)
                            prod = Product.objects.get(id=product_id)
                            m2m = prod.category.all()
                            m2m_list = []
                            for m in m2m:
                                m2m_list.append(m.id)
                            if category_list == m2m_list:
                                pass
                            else:
                                diffrent = Diff(category_list, m2m_list)
                                if not diffrent:
                                    pass
                                else:
                                    for i in diffrent:
                                        product = Product.objects.get(pk=product_id)
                                        diffrent_category = Category.objects.get(pk=i)
                                        m2m = product.category.remove(diffrent_category)

    def handle(self, *args, **options):
        """
        Call the function to import data
        """
        self.compare()



