"""
Import json data from JSON file to Datababse
"""
import os
import json
from ....product.models import ProductType, Attribute, AttributeValue, Product
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

    def make_filters(self):
        data_folder = os.path.join(PROJECT_ROOT, 'saleor', 'api_par_com', 'resources', 'json_file')

        #################################################################
        ####            Product Material Attribute creating          ####
        #################################################################

        product_type = ProductType.objects.get(name='Сувенірна продукція').id
        attr_update = {
            "name": 'Material',
            "slug": 'material',
            # "product_type_id": product_type,
            "product_type_id": product_type
        }
        try:
            attribute = Attribute.objects.get(product_type_id=product_type)
            for key, value in attr_update.items():
                setattr(attribute, key, value)
            attribute.save()
            display_format = "\nAttribute, {}, has been edited."
            print(display_format.format(attribute))
        except Attribute.DoesNotExist:
            attr_create = {
                "name": 'Material',
                "slug": 'material',
                # "product_type_id": product_type,
                "product_type_id": product_type
            }
            attr_update.update(attr_update)
            attribute = Attribute(**attr_create)
            attribute.save()
            display_format = "\nAttribbute, {}, has been created."
            print(display_format.format(attribute))

        #################################################################
        ####            Product Color Attribute creating          ####
        #################################################################

        attr_update = {
            "name": 'Color',
            "slug": 'color',
            # "product_type_id": product_type,
            "product_variant_type_id": product_type
        }
        try:
            attribute = Attribute.objects.get(product_variant_type_id=product_type)
            for key, value in attr_update.items():
                setattr(attribute, key, value)
            attribute.save()
            display_format = "\nAttribute, {}, has been edited."
            print(display_format.format(attribute))
        except Attribute.DoesNotExist:
            attr_create = {
                "name": 'Color',
                "slug": 'color',
                # "product_type_id": product_type,
                "product_variant_type_id": product_type
            }
            attr_update.update(attr_update)
            attribute = Attribute(**attr_create)
            attribute.save()
            display_format = "\nAttribbute, {}, has been created."
            print(display_format.format(attribute))


        ######################################################################
        material_diactionary = {
            'poliester': ["poliester 190T", "plusz", "oxford", "mikrofibra", "poliester 600D", "poliester", "poliester 190 T", "mikrofibra poliestrowa 190T", "190T poliester", "pongee 190T", "pongee 190t", "poliester 210 D", "polyester 600D", "poliester 420D", "poliester 210", "poliester 210D", "poliester 600 D", "poliester 600D Oxford", "poliester 250 D", "poliestrowy twill", "mikrofibra poliestrowa", "poliester 290T", "poliester 230 D", "poliester 300D", "1680D", "polar"],
            'plastik': ["plastik", "polietylen", "poliuretan", "tworzywo sztuczne", "tworzywo elastyczne", "tritan", "ABS", "plastik PCV", "mikki plastik", "tworzywo sztuczne (PVC)", "plastik ABS", "PVC", "plastik PET", "poliwglan", "polimer PCTG", "plastik PETG", "PETG", "tworzywo sztuczne z dodatkiem silikonu"],
            'drewno': ["drewno", "drewno kauczukowe", "MDF", "drewno lipowe", "korek", "metal, drewno, bawena", "drewno bambusowe"],
            'nylon': ["nylon 420 D", "nylon 1680 D", "nylon 840D", "tiul" ],
            'polipropylen': ["polipropylen", "polistyren", "filc"],
            'stal': ["stal nierdzewna", "metal", "metal, drewno, bawena", "stal nierdzewna 18/8", "stal", "stal 3CR13", "metal 2CR14", "metal 2CR13", "stal nierdzewna 18/8 i 18/0"],
            'aluminium': ["aluminium", "aluminum", "folia alumiowa", "Aluminium"],
            'bawena': ["bawena", "bawena 180 g/m2"],
            'skra': ["skra", "ekoskra", "PU", "skra naturalna"],
            'non woven': ["non woven", "non woven 80g/m2", "welur"],
            'papier': ["papier", "karton"],
            'szko': ["szko", "szko borokrzemianowe", "szko borokrzemowe", "kryszta"],
            'len': ["len", "sztuczny len"],
            'EVA': ["EVA", "tworzywo EVA", "TPR"],
            'wosk': ["wosk", "parafina"],
            'ripstop': ["ripstop", "akard"],
            'materia odblaskowy': "materia odblaskowy",
            'akryl': "akryl",
            'tektura': "tektura",
            'other': ''
        }
        ################################################################
        #          Attribute Material Values Making
        ################################################################
        attr_id = Attribute.objects.get(name='Material').id
        for k, v in material_diactionary.items():
            attr_slug = slugify(k)
            attr_update = {
                # "id": id,
                "name": k,
                "attribute_id": attr_id,
                "slug": attr_slug
            }
            try:
                obj = AttributeValue.objects.get(slug=attr_slug)
                for key, value in attr_update.items():
                    setattr(obj, key, value)
                obj.save()
                display_format = "\nProduct, {}, has been edited."
                print(display_format.format(obj))
            except AttributeValue.DoesNotExist:
                attr_create = {
                    # "id": id,
                    "name": k,
                    "attribute_id": attr_id,
                    "slug": attr_slug
                }
                attr_create.update(attr_update)
                obj = AttributeValue(**attr_create)
                obj.save()
                display_format = "\nProduct, {}, has been created."
                print(display_format.format(obj))

        ####################################################################################
        #                            Product attributes
        ####################################################################################
        with open(os.path.join(data_folder, "products.json"), encoding='utf-8') as data_file:
            data = json.loads(data_file.read())

            for data_object in data['products']['product']:
                id = data_object.get('id', None)
                material = data_object.get('material_wykonania', None)
                attr_id = Attribute.objects.get(name='Material').id
                # attr_slug = slugify(material)
                for k,v  in material_diactionary.items():
                    if material in v:
                        main_atr_id = attr_id
                        atr_id = AttributeValue.objects.get(name=k).id
                        mai = str(main_atr_id)
                        ai = str(atr_id)
                        out = '"'+mai+'"=>"'+ai+'"'
                        print(out)
                        prod_attr_upd ={
                            "attributes": out
                        }
                        try:
                            obj = Product.objects.get(id=id)
                            for key, value in prod_attr_upd.items():
                                setattr(obj, key, value)
                            obj.save()
                            display_format = "\nKey, {}, has been edited."
                            print(display_format.format(obj))
                        except Product.DoesNotExist:
                            prod_attr_crt = {
                                "attributes": out
                            }
                            prod_attr_crt.update(prod_attr_upd)
                            obj = Product(**prod_attr_crt)
                            obj.save()
                            display_format = "\nKey, {}, has been created."
                            print(display_format.format(obj))

                    elif material == v:
                        pass
                        # main_atr_id = attr_id
                        # atr_id = AttributeValue.objects.get(name=k).id
                        # mai = str(main_atr_id)
                        # ai = str(atr_id)
                        # out = '"' + mai + '"=>"' + ai + '"'
                        # prod_attr_upd = {
                        #     "attributes": out
                        # }
                        # try:
                        #     obj = Product.objects.get(id=id)
                        #     for key, value in prod_attr_upd.items():
                        #         setattr(obj, key, value)
                        #     obj.save()
                        #     display_format = "\nKey, {}, has been edited."
                        #     print(display_format.format(obj))
                        # except Product.DoesNotExist:
                        #     prod_attr_crt = {
                        #         "attributes": out
                        #     }
                        #     prod_attr_crt.update(prod_attr_upd)
                        #     obj = Product(**prod_attr_crt)
                        #     obj.save()
                        #     display_format = "\nKey, {}, has been created."
                        #     print(display_format.format(obj))

                    else:
                        pass
                        # main_atr_id = attr_id
                        # atr_id = AttributeValue.objects.get(name='other').id
                        # mai = str(main_atr_id)
                        # ai = str(atr_id)
                        # out = '"' + mai + '"=>"' + ai + '"'
                        # prod_attr_upd = {
                        #     "attributes": out
                        # }
                        # try:
                        #     obj = Product.objects.get(id=id)
                        #     for key, value in prod_attr_upd.items():
                        #         setattr(obj, key, value)
                        #     obj.save()
                        #     display_format = "\nKey, {}, has been edited."
                        #     print(display_format.format(obj))
                        # except Product.DoesNotExist:
                        #     prod_attr_crt = {
                        #         "attributes": out
                        #     }
                        #     prod_attr_crt.update(prod_attr_upd)
                        #     obj = Product(**prod_attr_crt)
                        #     obj.save()
                        #     display_format = "\nKey, {}, has been created."
                        #     print(display_format.format(obj))




                # sku = data_object.get('kod', None)
                # color_name = data_object.get('kolor_podstawowy', None)
                #
                # attr_id = Attribute.objects.get(name='Color').id
                # # attr_slug = slugify(material)
                # for k, v in material_diactionary.items():
                #     if material in v:
                #         main_atr_id = attr_id
                #         atr_id = AttributeValue.objects.get(name=k).id
                #         mai = str(main_atr_id)
                #         ai = str(atr_id)
                #         out = '"' + mai + '"=>"' + ai + '"'
                #         prod_attr_upd = {
                #             "attributes": out
                #         }
                #         try:
                #             obj = Product.objects.get(id=id)
                #             for key, value in prod_attr_upd.items():
                #                 setattr(obj, key, value)
                #             obj.save()
                #             display_format = "\nKey, {}, has been edited."
                #             print(display_format.format(obj))
                #         except Product.DoesNotExist:
                #             prod_attr_crt = {
                #                 "attributes": out
                #             }
                #             prod_attr_crt.update(prod_attr_upd)
                #             obj = Product(**prod_attr_crt)
                #             obj.save()
                #             display_format = "\nKey, {}, has been created."
                #             print(display_format.format(obj))
                #
                #     elif material == v:
                #         main_atr_id = attr_id
                #         atr_id = AttributeValue.objects.get(name=k).id
                #         mai = str(main_atr_id)
                #         ai = str(atr_id)
                #         out = '"' + mai + '"=>"' + ai + '"'
                #         prod_attr_upd = {
                #             "attributes": out
                #         }
                #         try:
                #             obj = Product.objects.get(id=id)
                #             for key, value in prod_attr_upd.items():
                #                 setattr(obj, key, value)
                #             obj.save()
                #             display_format = "\nKey, {}, has been edited."
                #             print(display_format.format(obj))
                #         except Product.DoesNotExist:
                #             prod_attr_crt = {
                #                 "attributes": out
                #             }
                #             prod_attr_crt.update(prod_attr_upd)
                #             obj = Product(**prod_attr_crt)
                #             obj.save()
                #             display_format = "\nKey, {}, has been created."
                #             print(display_format.format(obj))
                #
                #     else:
                #         main_atr_id = attr_id
                #         atr_id = AttributeValue.objects.get(name='other').id
                #         mai = str(main_atr_id)
                #         ai = str(atr_id)
                #         out = '"' + mai + '"=>"' + ai + '"'
                #         prod_attr_upd = {
                #             "attributes": out
                #         }
                #         try:
                #             obj = Product.objects.get(id=id)
                #             for key, value in prod_attr_upd.items():
                #                 setattr(obj, key, value)
                #             obj.save()
                #             display_format = "\nKey, {}, has been edited."
                #             print(display_format.format(obj))
                #         except Product.DoesNotExist:
                #             prod_attr_crt = {
                #                 "attributes": out
                #             }
                #             prod_attr_crt.update(prod_attr_upd)
                #             obj = Product(**prod_attr_crt)
                #             obj.save()
                #             display_format = "\nKey, {}, has been created."
                #             print(display_format.format(obj))


    def handle(self, *args, **options):
        """
        Call the function to import data
        """
        self.make_filters()

