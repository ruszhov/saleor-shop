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
from itertools import groupby
import itertools

class Command(BaseCommand):

    def create_variants(self):

        data_folder = os.path.join(PROJECT_ROOT, 'saleor','api_par_com', 'resources', 'json_file')

        kod_with_point = []
        dict={}

        with open(os.path.join(data_folder, "products_en.json"), encoding='utf-8') as data_file:
            data = json.loads(data_file.read())

            for data_object in data['products']['product']:

                sale = data_object.get('wyprzedaz', None)
                if sale == 'false':
                    kod = data_object.get('kod', None)
                    # product_id = data_object.get('id', None)
                    if '.' in kod:
                        color_name = data_object.get('kolor_podstawowy', None)
                        product_id = data_object.get('id', None)
                        out_list = []
                        out_list.append(kod)
                        out_list.append(color_name)
                        out_list.append(product_id)
                        kod_with_point.append(out_list)
                        # print(color_name)
                else:
                    pass

        for el in kod_with_point:
            l_sku = el[0]
            cuted_el = l_sku[:6]
            l_color = el[1]
            l_product = el[2]
            dict[l_sku, l_color, l_product] = cuted_el

        new_dict = {}
        for key, value in dict.items():
            if value in new_dict:
                new_dict[value].append(key)
            else:
                new_dict[value] = [key]
        # print(kod_with_point)
        for k,v in new_dict.items():
            if len(v) == 1:
                pass
            else:
                print('len:', len(v))
                # count=0
                # for item in v:
                for idx, item in enumerate(v):
                    # count+=1
                    # product = ProductVariant.objects.get(sku=item[0])
                    # attr_id = Attribute.objects.get(name='Color').id
                    # print(idx)
                    print('item:', item)
                    print('v:', idx,v)
                    # for sku_set in v:
                    #     if sku_set != item:
                    #         print(sku_set)
                    i = 0
                    while i < len(v):
                        sku_set = v[i]
                        if sku_set != item:
                            # print('sku_set:',sku_set)
                            akv_sku = sku_set[0]+'('+str(idx+1)+')'+'-'+sku_set[2]
                            # print('akv_sku:', akv_sku)
                            # print('product_id:', product_id)
                            product_id = item[2]
                            name = sku_set[1]
                            print(akv_sku, name, product_id)

                            variants_update = {
                                # "id": id,
                                "sku": akv_sku,
                                "name": name,
                                "price_override": None,
                                "product_id": product_id,
                                "attributes": "",
                                "cost_price": None,
                                "quantity": 22222222,
                                "quantity_allocated": 0,
                                "track_inventory": False,
                                "weight": None
                            }
                            try:
                                variant = ProductVariant.objects.get(sku=akv_sku)
                                # for key, value in variants_update.items():
                                #     setattr(variant, key, value)
                                # variant.save()
                                display_format = "\nVariant, {}, has been edited."
                                # print(display_format.format(variant.id))
                            except ProductVariant.DoesNotExist:
                                variants_create = {
                                    # "id": id,
                                    "sku": akv_sku,
                                    "name": name,
                                    "price_override": None,
                                    "product_id": product_id,
                                    "attributes": "",
                                    "cost_price": None,
                                    "quantity": 22222222,
                                    "quantity_allocated": 0,
                                    "track_inventory": False,
                                    "weight": None
                                }
                                # variants_update.update(variants_update)
                                variant = ProductVariant(**variants_create)
                                # variant.save()
                                display_format = "Variant, {}, has been created. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                                print(display_format.format(akv_sku))
                        else:
                            pass
                        i += 1

    def handle(self, *args, **options):
        """
        Call the function to import data
        """
        self.create_variants()



