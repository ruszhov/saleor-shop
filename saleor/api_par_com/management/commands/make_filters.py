"""
Import json data from JSON file to Datababse
"""
import os
import json
from ....product.models import ProductType, Product, ProductVariant, Attribute, AttributeTranslation, AttributeValue, AttributeValueTranslation
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
from googletrans import Translator

class Command(BaseCommand):

    def make_colors(self):

        #################################################################
        ####            Product Material Attribute creating          ####
        #################################################################
        data_folder = os.path.join(PROJECT_ROOT, 'saleor', 'api_par_com', 'resources', 'json_file')
        product_type = ProductType.objects.get(name='Сувенірна продукція').id
        attr_update = {
            # "name": 'Material',
            # "slug": 'material',
            # "product_type_id": product_type,
            # "product_variant_type_id": product_type
        }
        try:
            attribute = Attribute.objects.get(product_type_id=product_type)
            for key, value in attr_update.items():
                setattr(attribute, key, value)
            attribute.save()
            display_format = "\nAttribute, {}, has been edited."
            # print(display_format.format(attribute))
        except Attribute.DoesNotExist:
            attr_create = {
                "name": 'Material',
                "slug": 'material',
                "product_type_id": product_type,
                # "product_variant_type_id": product_type
            }
            attr_create.update(attr_update)
            attribute = Attribute(**attr_create)
            attribute.save()
            display_format = "\nAttribbute, {}, has been created."
            print(display_format.format(attribute))

        attr_update = {
            # "name": 'Color',
            # "slug": 'color',
            # "product_type_id": product_type,
            # "product_variant_type_id": product_type
        }
        try:
            attribute = Attribute.objects.get(product_variant_type_id=product_type)
            for key, value in attr_update.items():
                setattr(attribute, key, value)
            attribute.save()
            display_format = "\nAttribute, {}, has been edited."
            # print(display_format.format(attribute))
        except Attribute.DoesNotExist:
            attr_create = {
                "name": 'Color',
                "slug": 'color',
                # "product_type_id": product_type,
                "product_variant_type_id": product_type
            }
            attr_create.update(attr_update)
            attribute = Attribute(**attr_create)
            attribute.save()
            display_format = "\nAttribbute, {}, has been created."
            print(display_format.format(attribute))

        ####################################################################################
        #                            Product material attributes                           #
        ####################################################################################
        with open(os.path.join(data_folder, "products_en.json"), encoding='utf-8') as data_file:
            data = json.loads(data_file.read())

            for data_object in data['products']['product']:
                id = data_object.get('id', None)
                material = data_object.get('material_wykonania', None)
                attr_id = Attribute.objects.get(name='Material').id
                attr_slug = slugify(material)

                if material:

                    attr_update = {
                        "name": material,
                        "attribute_id": attr_id,
                        "slug": attr_slug,
                        "value": material
                    }
                    try:
                        attribute = AttributeValue.objects.get(slug=attr_slug)
                        for key, value in attr_update.items():
                            setattr(attribute, key, value)
                        attribute.save()
                        display_format = "\nMaterial-attribute, {}, has been edited."
                        print(display_format.format(attribute))
                    except AttributeValue.DoesNotExist:
                        attr_create = {
                            "name": material,
                            "attribute_id": attr_id,
                            "slug": attr_slug,
                            "value": material
                        }
                        attr_create.update(attr_update)
                        attribute = AttributeValue(**attr_create)
                        attribute.save()
                        display_format = "\nMaterial-attribute, {}, has been created."
                        print(display_format.format(attribute))


                    products = Product.objects.get(id=id)
                    # print(type(products))
                    # for product in products:
                    attr_val_id = AttributeValue.objects.get(name=material).id
                    ai = str(attr_id)
                    avi = str(attr_val_id)
                    out = '"' + ai + '"=>"' + avi + '"'

                    prod_attr_upd = {
                        "attributes": out
                    }
                    try:
                        obj = Product.objects.get(id=products.id)
                        for key, value in prod_attr_upd.items():
                            setattr(obj, key, value)
                        obj.save()
                        display_format = "\nMaterial-attribute, {}, has been edited."
                        print(display_format.format(obj))
                    except Product.DoesNotExist:
                        prod_attr_crt = {
                            "attributes": out
                        }
                        prod_attr_crt.update(prod_attr_upd)
                        obj = Product(**prod_attr_crt)
                        obj.save()
                        display_format = "\nMaterial-attribute, {}, has been created."
                        print(display_format.format(obj))
                else:
                    pass

        #################################################################
        ####            Product Color Attribute creating          ####
        #################################################################
        data_folder = os.path.join(PROJECT_ROOT, 'saleor', 'api_par_com', 'resources', 'json_file')
        product_type = ProductType.objects.get(name='Сувенірна продукція').id
        attr_update = {
            # "name": 'Color',
            # "slug": 'color',
            # "product_type_id": product_type,
            # "product_variant_type_id": product_type
        }
        try:
            attribute = Attribute.objects.get(product_variant_type_id=product_type)
            for key, value in attr_update.items():
                setattr(attribute, key, value)
            attribute.save()
            display_format = "\nAttribute, {}, has been edited."
            # print(display_format.format(attribute))
        except Attribute.DoesNotExist:
            attr_create = {
                "name": 'Color',
                "slug": 'color',
                # "product_type_id": product_type,
                "product_variant_type_id": product_type
            }
            attr_create.update(attr_update)
            attribute = Attribute(**attr_create)
            attribute.save()
            display_format = "\nColor-attribute, {}, has been created."
            print(display_format.format(attribute))

        ####################################################################################
        #                            Product color attributes                              #
        ####################################################################################
        with open(os.path.join(data_folder, "products_en.json"), encoding='utf-8') as data_file:
            data = json.loads(data_file.read())

            for data_object in data['products']['product']:
                id = data_object.get('id', None)
                color = data_object.get('kolor_podstawowy', None)
                attr_id = Attribute.objects.get(name='Color').id
                attr_slug = slugify(color)

                color_attr_update = {
                    "name": color,
                    "attribute_id": attr_id,
                    "slug": attr_slug,
                    "value": color
                }
                try:
                    attribute = AttributeValue.objects.get(slug=attr_slug)
                    for key, value in color_attr_update.items():
                        setattr(attribute, key, value)
                    attribute.save()
                    display_format = "\nColor-attribute, {}, has been edited."
                    print(display_format.format(attribute))
                except AttributeValue.DoesNotExist:
                    color_attr_create = {
                        "name": color,
                        "attribute_id": attr_id,
                        "slug": attr_slug,
                        "value": color
                    }
                    color_attr_create.update(color_attr_update)
                    attribute = AttributeValue(**color_attr_create)
                    attribute.save()
                    display_format = "\nColor-attribute, {}, has been created."
                    print(display_format.format(attribute))

        attribute = Attribute.objects.get(name="Color")
        variants = ProductVariant.objects.all()
        for variant in variants:
            attr_val_id = AttributeValue.objects.get(name=variant.name).id
            ai = str(attr_id)
            avi = str(attr_val_id)
            out = '"' + ai + '"=>"' + avi + '"'

            prod_attr_upd = {
                "attributes": out
            }
            try:
                obj = ProductVariant.objects.get(id=variant.id)
                for key, value in prod_attr_upd.items():
                    setattr(obj, key, value)
                obj.save()
                display_format = "\nKey, {}, has been edited."
                print(display_format.format(obj))
            except ProductVariant.DoesNotExist:
                prod_attr_crt = {
                    "attributes": out
                }
                prod_attr_crt.update(prod_attr_upd)
                obj = ProductVariant(**prod_attr_crt)
                obj.save()
                display_format = "\nKey, {}, has been created."
                print(display_format.format(obj))

        #######################################################################
        #                           Translation                               #
        #######################################################################

        translator = Translator(service_urls=[
            'translate.google.com',
            'translate.google.co.kr',
        ])

        #######################################################################
        #                           Attribute  Translation                    #
        #######################################################################

        attr_id = Attribute.objects.all()
        for attr_id in attr_id:

            ###########      Polska   ##############################
            pl_name = attr_id.name
            language_code = 'pl'
            # print(pl_color)
            pl_attr_update = {
                # "name": pl_color,
                # "language_code": 'pl',
                # "product_type_id": product_type,
                # "attribute_id": attr_id.id
            }
            try:
                attribute = AttributeTranslation.objects.get(attribute_id=attr_id.id, language_code=language_code)
                for key, value in pl_attr_update.items():
                    setattr(attribute, key, value)
                attribute.save()
                # display_format = "\nAttribute, {}, has been edited."
                # print(display_format.format(attribute))
            except AttributeTranslation.DoesNotExist:
                try:
                    pl_color = translator.translate(pl_name, dest=language_code).text
                    pl_attr_create = {
                        "name": pl_color,
                        "language_code": language_code,
                        # "product_type_id": product_type,
                        "attribute_id": attr_id.id
                    }
                    pl_attr_create.update(pl_attr_update)
                    attribute = AttributeTranslation(**pl_attr_create)
                    attribute.save()
                    display_format = "\nAttribbute, {}, has been created."
                    print(display_format.format(attribute))
                except ValueError:  # includes simplejson.decoder.JSONDecodeError
                    print('Decoding JSON has failed PL', attribute.id)


            ############  Ukrainian ##########################
            uk_name = attr_id.name
            language_code = 'uk'
            # print(pl_color)
            uk_attr_update = {
                # "name": uk_color,
                # "language_code": 'uk',
                # "product_type_id": product_type,
                # "attribute_id": attr_id.id
            }
            try:
                attribute = AttributeTranslation.objects.get(attribute_id=attr_id.id, language_code=language_code)
                for key, value in uk_attr_update.items():
                    setattr(attribute, key, value)
                attribute.save()
                # display_format = "\nAttribute, {}, has been edited."
                # print(display_format.format(attribute))
            except AttributeTranslation.DoesNotExist:
                try:
                    uk_color = translator.translate(uk_name, dest=language_code).text
                    uk_attr_create = {
                        "name": uk_color,
                        "language_code": language_code,
                        # "product_type_id": product_type,
                        "attribute_id": attr_id.id
                    }
                    uk_attr_create.update(uk_attr_update)
                    attribute = AttributeTranslation(**uk_attr_create)
                    attribute.save()
                    display_format = "\nAttribbute, {}, has been created."
                    print(display_format.format(attribute))
                except ValueError:  # includes simplejson.decoder.JSONDecodeError
                    print('Decoding JSON has failed UK', attribute.id)


            ############  Russian ##########################
            ru_name = attr_id.name
            language_code = 'ru'
            # print(pl_color)
            ru_attr_update = {
                # "name": ru_color,
                # "language_code": 'ru',
                # "product_type_id": product_type,
                # "attribute_id": attr_id.id
            }
            try:
                attribute = AttributeTranslation.objects.get(attribute_id=attr_id.id, language_code=language_code)
                for key, value in ru_attr_update.items():
                    setattr(attribute, key, value)
                attribute.save()
                # display_format = "\nAttribute, {}, has been edited."
                # print(display_format.format(attribute))
            except AttributeTranslation.DoesNotExist:
                try:
                    ru_color = translator.translate(ru_name, dest=language_code).text
                    ru_attr_create = {
                        "name": ru_color,
                        "language_code": language_code,
                        # "product_type_id": product_type,
                        "attribute_id": attr_id.id
                    }
                    ru_attr_create.update(ru_attr_update)
                    attribute = AttributeTranslation(**ru_attr_create)
                    attribute.save()
                    display_format = "\nAttribbute, {}, has been created."
                    print(display_format.format(attribute))
                except ValueError:  # includes simplejson.decoder.JSONDecodeError
                    print('Decoding JSON has failed RU', attribute.id)


        #######################################################################
        #                      Attribute Value Translation                    #
        #######################################################################

        attr_value_id = AttributeValue.objects.all()
        for attr_id in attr_value_id:

            ###########      Polska   ##############################
            pl_name = attr_id.name
            language_code = 'pl'
            # print(pl_color)
            pl_attr_update = {
                # "name": pl_color,
                # "language_code": 'pl',
                # "product_type_id": product_type,
                # "attribute_value_id": attr_id.id
            }
            try:
                attribute = AttributeValueTranslation.objects.get(attribute_value_id=attr_id.id, language_code=language_code)
                for key, value in pl_attr_update.items():
                    setattr(attribute, key, value)
                attribute.save()
                # display_format = "\nAttribute, {}, has been edited."
                # print(display_format.format(attribute))
            except AttributeValueTranslation.DoesNotExist:
                try:
                    pl_color = translator.translate(pl_name, dest=language_code).text
                    pl_attr_create = {
                        "name": pl_color,
                        "language_code": language_code,
                        # "product_type_id": product_type,
                        "attribute_value_id": attr_id.id
                    }
                    pl_attr_create.update(pl_attr_update)
                    attribute = AttributeValueTranslation(**pl_attr_create)
                    attribute.save()
                    display_format = "\nAttribbute, {}, has been created."
                    print(display_format.format(attribute))
                except ValueError:  # includes simplejson.decoder.JSONDecodeError
                    print('Decoding JSON has failed PL', attribute.id)


            ############  Ukrainian ##########################
            uk_name = attr_id.name
            language_code = 'uk'
            # print(pl_color)
            uk_attr_update = {
                # "name": uk_color,
                # "language_code": 'uk',
                # "product_type_id": product_type,
                # "attribute_value_id": attr_id.id
            }
            try:
                attribute = AttributeValueTranslation.objects.get(attribute_value_id=attr_id.id, language_code=language_code)
                for key, value in uk_attr_update.items():
                    setattr(attribute, key, value)
                attribute.save()
                # display_format = "\nAttribute, {}, has been edited."
                # print(display_format.format(attribute))
            except AttributeValueTranslation.DoesNotExist:
                try:
                    uk_color = translator.translate(uk_name, dest=language_code).text
                    uk_attr_create = {
                        "name": uk_color,
                        "language_code": language_code,
                        # "product_type_id": product_type,
                        "attribute_value_id": attr_id.id
                    }
                    uk_attr_create.update(uk_attr_update)
                    attribute = AttributeValueTranslation(**uk_attr_create)
                    attribute.save()
                    display_format = "\nAttribbute, {}, has been created."
                    print(display_format.format(attribute))
                except ValueError:  # includes simplejson.decoder.JSONDecodeError
                    print('Decoding JSON has failed UK', attribute.id)


            ############  Russian ##########################
            ru_name = attr_id.name
            language_code = 'ru'
            # print(pl_color)
            ru_attr_update = {
                # "name": ru_color,
                # "language_code": 'ru',
                # "product_type_id": product_type,
                # "attribute_value_id": attr_id.id
            }
            try:
                attribute = AttributeValueTranslation.objects.get(attribute_value_id=attr_id.id, language_code=language_code)
                for key, value in ru_attr_update.items():
                    setattr(attribute, key, value)
                attribute.save()
                # display_format = "\nAttribute, {}, has been edited."
                # print(display_format.format(attribute))
            except AttributeValueTranslation.DoesNotExist:
                try:
                    ru_color = translator.translate(ru_name, dest=language_code).text
                    ru_attr_create = {
                        "name": ru_color,
                        "language_code": language_code,
                        # "product_type_id": product_type,
                        "attribute_value_id": attr_id.id
                    }
                    ru_attr_create.update(ru_attr_update)
                    attribute = AttributeValueTranslation(**ru_attr_create)
                    attribute.save()
                    display_format = "\nAttribbute, {}, has been created."
                    print(display_format.format(attribute))
                except ValueError:  # includes simplejson.decoder.JSONDecodeError
                    print('Decoding JSON has failed RU', attribute.id)

    def handle(self, *args, **options):
        """
        Call the function to import data
        """
        self.make_colors()

