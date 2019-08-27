"""
Import json data from JSON file to Datababse
"""
import json
from ....product.models import Category, Product, ProductTranslation, \
    ProductVariant, ProductVariantTranslation
from ....menu.models import MenuItem, MenuItemTranslation
from ....product.models import CategoryTranslation
from django.core.management.base import BaseCommand
from googletrans import Translator
from mptt.managers import TreeManager


class Command(BaseCommand):

    def trans(self):
        # cat = Category.objects.get(name="Catalogue").id
        # raw_json = json.dumps({"blocks": [
        #     {"key": "", "data": {}, "text": "", "type": "unstyled", "depth": 0, "entityRanges": [],
        #      "inlineStyleRanges": []}], "entityMap": {}})
        # out_json = json.loads(raw_json)
        #
        # category_update = {
        #     'id': 1,
        #     'name': 'Katalog',
        #     'language_code': 'pl',
        #     'description': 'Katalog',
        #     'seo_description': 'Katalog',
        #     'seo_title': 'Katalog',
        #     'description_json': out_json,
        #     'category_id': cat
        # }
        # try:
        #     obj = CategoryTranslation.objects.get(id=1)
        #     for key, value in category_update.items():
        #         setattr(obj, key, value)
        #     obj.tree = TreeManager
        #     obj.save()
        #     display_format = "\nFirst level Categorie, {}, has been translated."
        #     print(display_format.format(obj))
        # except CategoryTranslation.DoesNotExist:
        #     category_create = {
        #         'id': 1,
        #         'name': 'Katalog',
        #         'language_code': 'pl',
        #         'description': 'Katalog',
        #         'seo_description': 'Katalog',
        #         'seo_title': 'Katalog',
        #         'description_json': out_json,
        #         'category_id': cat
        #     }
        #     category_create.update(category_update)
        #     obj = CategoryTranslation(**category_create)
        #     obj.save()
        #     display_format = "\nFirst level Categorie, {}, has been translated."
        #     print(display_format.format(obj))
        #
        # menu_id = MenuItem.objects.get(name="Catalogue").id
        # menu_update = {
        #     'id': 1,
        #     'language_code': 'pl',
        #     'name': 'Katalog',
        #     'menu_item_id': menu_id
        # }
        # try:
        #     obj = MenuItemTranslation.objects.get(name='Katalog', language_code='pl')
        #     for key, value in menu_update.items():
        #         setattr(obj, key, value)
        #     obj.save()
        #     display_format = "\nTranslation for Catalogue, {}, has been edited."
        #     print(display_format.format(obj))
        # except MenuItemTranslation.DoesNotExist:
        #     menu_create = {
        #         'id': 1,
        #         'language_code': 'pl',
        #         'name': 'Katalog',
        #         'menu_item_id': menu_id
        #     }
        #     menu_create.update(menu_update)
        #     obj = MenuItemTranslation(**menu_create)
        #     obj.save()
        #     display_format = "\nTranslation for Catalogue, {}, has been created."
        #     print(display_format.format(obj))

        #######################################################################
        #                           Translation                               #
        #######################################################################

        translator = Translator(service_urls=[
            'translate.google.com',
            'translate.google.co.kr',
        ])

        #######################################################################
        #                           Menu  Translation                         #
        #######################################################################

        menus = MenuItem.objects.all()
        for menu in menus:

            menu_item_id = menu.id

            ###########      Polska   ##############################
            language_code = 'pl'
            pl_menu_update = {
                'language_code': language_code,
                # 'name': pl_name,
                'menu_item_id': menu_item_id,
            }
            try:
                menu = MenuItemTranslation.objects.get(
                    menu_item_id=menu_item_id, language_code='pl')
                for key, value in pl_menu_update.items():
                    setattr(menu, key, value)
                menu.save()
                display_format = "\nTranslation for menu, {}, has been edited."
                # print(display_format.format(menu))
            except MenuItemTranslation.DoesNotExist:
                try:
                    pl_name = translator.translate(menu.name, dest='pl').text
                    pl_menu_create = {
                        'language_code': language_code,
                        'name': pl_name,
                        'menu_item_id': menu_item_id,
                    }
                    pl_menu_create.update(pl_menu_update)
                    menu = MenuItemTranslation(**pl_menu_create)
                    menu.save()
                    display_format = "\nTranslation for menu, {}, has been created."
                    print(display_format.format(menu))
                except ValueError:  # includes simplejson.decoder.JSONDecodeError
                    print('Decoding JSON has failed PL', menu.id)

            ###########      Ukrainian    ##############################
            language_code = 'uk'
            uk_menu_update = {
                'language_code': language_code,
                # 'name': uk_name,
                'menu_item_id': menu_item_id,
            }
            try:
                uk_menu = MenuItemTranslation.objects.get(
                    menu_item_id=menu_item_id, language_code='uk')
                for key, value in uk_menu_update.items():
                    setattr(menu, key, value)
                uk_menu.save()
                disukay_format = "\nTranslation for menu, {}, has been edited."
                # print(disukay_format.format(menu))
            except MenuItemTranslation.DoesNotExist:
                try:
                    uk_name = translator.translate(menu.name, dest='uk').text
                    uk_menu_create = {
                        'language_code': language_code,
                        'name': uk_name,
                        'menu_item_id': menu_item_id,
                    }
                    uk_menu_create.update(uk_menu_update)
                    uk_menu = MenuItemTranslation(**uk_menu_create)
                    uk_menu.save()
                    disukay_format = "\nTranslation for menu, {}, has been created."
                    print(disukay_format.format(menu))
                except ValueError:  # includes simplejson.decoder.JSONDecodeError
                    print('Decoding JSON has failed UK', menu.id)

            ###########      Russian    ##############################
            language_code = 'ru'

            ru_menu_update = {
                'language_code': language_code,
                # 'name': ru_name,
                'menu_item_id': menu_item_id,
            }
            try:
                menu = MenuItemTranslation.objects.get(
                    menu_item_id=menu_item_id, language_code='ru')
                for key, value in ru_menu_update.items():
                    setattr(menu, key, value)
                menu.save()
                disruay_format = "\nTranslation for menu, {}, has been edited."
                # print(disruay_format.format(menu))
            except MenuItemTranslation.DoesNotExist:
                try:
                    ru_name = translator.translate(menu.name, dest='ru').text
                    ru_menu_create = {
                        'language_code': language_code,
                        'name': ru_name,
                        'menu_item_id': menu_item_id,
                    }
                    ru_menu_create.update(ru_menu_update)
                    menu = MenuItemTranslation(**ru_menu_create)
                    menu.save()
                    disruay_format = "\nTranslation for menu, {}, has been created."
                    print(disruay_format.format(menu))
                except ValueError:  # includes simplejson.decoder.JSONDecodeError
                    print('Decoding JSON has failed RU', menu.id)

        #######################################################################
        #                           Categorie  Translation                    #
        #######################################################################

        categories = Category.objects.all()
        for category in categories:
            category_id = category.id
            json_description = category.description_json

            ###########      Polska   ##############################
            # pl_seo_title = translator.translate(category.seo_title, dest='pl').text
            # pl_seo_description = translator.translate(category.description, dest='pl').text
            language_code = 'pl'

            pl_category_update = {
                # 'seo_title': pl_seo_title,
                # 'seo_description': pl_seo_description,
                # 'language_code': language_code,
                # 'name': pl_name,
                # 'description': pl_description,
                # 'category_id': category_id,
                # 'description_json': json_description
            }
            try:
                category = CategoryTranslation.objects.get(
                    category_id=category_id, language_code='pl')
                for key, value in pl_category_update.items():
                    setattr(category, key, value)
                category.save()
                display_format = "\nTranslation for category, {}, has been edited."
                # print(display_format.format(category))
            except CategoryTranslation.DoesNotExist:
                try:
                    pl_name = translator.translate(category.name,
                                                   dest='pl').text
                    pl_description = translator.translate(category.description,
                                                          dest='pl').text
                    pl_category_create = {
                        'seo_title': pl_name,
                        'seo_description': pl_description,
                        'language_code': language_code,
                        'name': pl_name,
                        'description': pl_description,
                        'category_id': category_id,
                        'description_json': json_description
                    }
                    pl_category_create.update(pl_category_update)
                    category = CategoryTranslation(**pl_category_create)
                    category.save()
                    display_format = "\nTranslation for category, {}, has been created."
                    print(display_format.format(category))
                except ValueError:  # includes simplejson.decoder.JSONDecodeError
                    print('Decoding JSON has failed PL', category.id)

            ############  Ukrainian ##########################
            # uk_seo_title = translator.translate(category.seo_title, dest='uk').text
            # uk_seo_description = translator.translate(category.description, dest='uk').text
            language_code = 'uk'
            uk_category_update = {
                # 'seo_title': uk_seo_title,
                # 'seo_description': uk_seo_description,
                # 'language_code': language_code,
                # 'name': uk_name,
                # 'description': uk_description,
                # 'category_id': category_id,
                # 'description_json': json_description
            }
            try:
                category = CategoryTranslation.objects.get(
                    category_id=category_id, language_code='uk')
                for key, value in uk_category_update.items():
                    setattr(category, key, value)
                category.save()
                disukay_format = "\nTranslation for category, {}, has been edited."
                # print(disukay_format.format(category))
            except CategoryTranslation.DoesNotExist:
                try:
                    uk_name = translator.translate(category.name,
                                                   dest='uk').text
                    uk_description = translator.translate(category.description,
                                                          dest='uk').text
                    uk_category_create = {
                        'seo_title': uk_name,
                        'seo_description': uk_description,
                        'language_code': language_code,
                        'name': uk_name,
                        'description': uk_description,
                        'category_id': category_id,
                        'description_json': json_description
                    }
                    uk_category_create.update(uk_category_update)
                    category = CategoryTranslation(**uk_category_create)
                    category.save()
                    disukay_format = "\nTranslation for category, {}, has been created."
                    print(disukay_format.format(category))
                except ValueError:  # includes simplejson.decoder.JSONDecodeError
                    print('Decoding JSON has failed UK', category.id)

            # ############  Russian  ############################
            # ru_seo_title = translator.translate(category.seo_title, dest='ru').text
            # ru_seo_description = translator.translate(category.description, dest='ru').text
            language_code = 'ru'
            # print(category_id)
            ru_category_update = {
                # 'seo_title': ru_seo_title,
                # 'seo_description': ru_seo_description,
                # 'language_code': language_code,
                # 'name': ru_name,
                # 'description': ru_description,
                # 'category_id': category_id,
                # 'description_json': json_description
            }
            try:
                category = CategoryTranslation.objects.get(
                    category_id=category_id, language_code='ru')
                for key, value in ru_category_update.items():
                    setattr(category, key, value)
                category.save()
                disruay_format = "\nTranslation for category, {}, has been edited."
                # print(disruay_format.format(category))
            except CategoryTranslation.DoesNotExist:
                try:
                    ru_name = translator.translate(category.name,
                                                   dest='ru').text
                    ru_description = translator.translate(category.description,
                                                          dest='ru').text
                    ru_category_create = {
                        'seo_title': ru_name,
                        'seo_description': ru_description,
                        'language_code': language_code,
                        'name': ru_name,
                        'description': ru_description,
                        'category_id': category_id,
                        'description_json': json_description
                    }
                    ru_category_create.update(ru_category_update)
                    category = CategoryTranslation(**ru_category_create)
                    category.save()
                    disruay_format = "\nTranslation for category, {}, has been created."
                    print(disruay_format.format(category))
                except ValueError:  # includes simplejson.decoder.JSONDecodeError
                    print('Decoding JSON has failed RU', category.id)

        #######################################################################
        #                           Product  Translation                      #
        #######################################################################

        products = Product.objects.all()
        for product in products:

            ###########      Polska   ##############################
            language_code = 'pl'
            product_id = product.id
            pl_product_update = {
                # 'seo_title': pl_seo_title,
                # 'seo_description': pl_seo_description,
                # 'language_code': language_code,
                # 'name': pl_name,
                # 'description': pl_description,
                # 'product_id': product_id,
                # 'description_json': pl_out_json
            }
            try:
                product = ProductTranslation.objects.get(product_id=product_id,
                                                         language_code='pl')
                for key, value in pl_product_update.items():
                    setattr(product, key, value)
                product.save()
                display_format = "\nTranslation for product, {}, has been edited."
                # print(display_format.format(product))
            except ProductTranslation.DoesNotExist:
                try:
                    pl_name = translator.translate(product.name,
                                                   dest='pl').text
                    pl_description = translator.translate(product.description,
                                                          dest='pl').text[:600]
                    pl_raw_json = json.dumps({"blocks": [
                        {"key": "", "data": {}, "text": pl_description,
                         "type": "unstyled", "depth": 0,
                         "entityRanges": [],
                         "inlineStyleRanges": []}], "entityMap": {}})
                    pl_out_json = json.loads(pl_raw_json)
                    pl_product_create = {
                        'seo_title': pl_name,
                        'seo_description': pl_description,
                        'language_code': language_code,
                        'name': pl_name,
                        'description': pl_description,
                        'product_id': product_id,
                        'description_json': pl_out_json
                    }
                    pl_product_create.update(pl_product_update)
                    product = ProductTranslation(**pl_product_create)
                    product.save()
                    display_format = "\nTranslation for product, {}, has been created."
                    print(display_format.format(product))

                except ValueError:  # includes simplejson.decoder.JSONDecodeError
                    print('Decoding JSON has failed PL', product.id)

            # # ###########      Ukrainian   ##############################
            language_code = 'uk'
            uk_product_update = {
                # 'seo_title': uk_seo_title,
                # 'seo_description': uk_seo_description,
                # 'language_code': language_code,
                # 'name': uk_name,
                # 'description': uk_description,
                # 'product_id': product_id,
                # 'description_json': uk_out_json
            }
            try:
                product = ProductTranslation.objects.get(product_id=product_id,
                                                         language_code='uk')
                for key, value in uk_product_update.items():
                    setattr(product, key, value)
                product.save()
                disukay_format = "\nTranslation for product, {}, has been edited."
                # print(disukay_format.format(product))
            except ProductTranslation.DoesNotExist:
                try:
                    uk_name = translator.translate(product.name,
                                                   dest='uk').text
                    uk_description = translator.translate(product.description,
                                                          dest='uk').text[:600]
                    uk_raw_json = json.dumps({"blocks": [
                        {"key": "", "data": {}, "text": uk_description,
                         "type": "unstyled", "depth": 0,
                         "entityRanges": [],
                         "inlineStyleRanges": []}], "entityMap": {}})
                    uk_out_json = json.loads(uk_raw_json)
                    uk_product_create = {
                        'seo_title': uk_name,
                        'seo_description': uk_description,
                        'language_code': language_code,
                        'name': uk_name,
                        'description': uk_description,
                        'product_id': product_id,
                        'description_json': uk_out_json
                    }
                    uk_product_create.update(uk_product_update)
                    product = ProductTranslation(**uk_product_create)
                    product.save()
                    disukay_format = "\nTranslation for product, {}, has been created."
                    print(disukay_format.format(product))
                except ValueError:  # includes simplejson.decoder.JSONDecodeError
                    print('Decoding JSON has failed UK', product.id)

            ############      Russian   ##############################
            language_code = 'ru'
            ru_product_update = {
                # 'seo_title': ru_name,
                # 'seo_description': ru_description,
                # 'language_code': language_code,
                # 'name': ru_name,
                # 'description': ru_description,
                # 'product_id': product_id,
                # 'description_json': ru_out_json
            }
            try:
                product = ProductTranslation.objects.get(product_id=product_id,
                                                         language_code='ru')
                for key, value in ru_product_update.items():
                    setattr(product, key, value)
                product.save()
                disruay_format = "\nTranslation for product, {}, has been edited."
                # print(disruay_format.format(product))
            except ProductTranslation.DoesNotExist:
                try:
                    ru_name = translator.translate(product.name,
                                                   dest='ru').text
                    ru_description = translator.translate(product.description,
                                                          dest='ru').text[:600]
                    ru_raw_json = json.dumps({"blocks": [
                        {"key": "", "data": {}, "text": ru_description,
                         "type": "unstyled", "depth": 0,
                         "entityRanges": [],
                         "inlineStyleRanges": []}], "entityMap": {}})
                    ru_out_json = json.loads(ru_raw_json)
                    ru_product_create = {
                        'seo_title': ru_name,
                        'seo_description': ru_description,
                        'language_code': language_code,
                        'name': ru_name,
                        'description': ru_description,
                        'product_id': product_id,
                        'description_json': ru_out_json
                    }
                    ru_product_create.update(ru_product_update)
                    product = ProductTranslation(**ru_product_create)
                    product.save()
                    disruay_format = "\nTranslation for product, {}, has been created."
                    print(disruay_format.format(product))
                except ValueError:  # includes simplejson.decoder.JSONDecodeError
                    print('Decoding JSON has failed RU', product.id)

        #######################################################################
        #                    ProductVariant  Translation                      #
        #######################################################################

        variants = ProductVariant.objects.all()
        for variant in variants:

            ###########      Polska   ##############################
            language_code = 'pl'
            variant_id = variant.id
            pl_variant_update = {
                # 'seo_title': pl_seo_title,
                # 'seo_description': pl_seo_description,
                # 'language_code': language_code,
                # 'name': pl_name,
                # 'description': pl_description,
                # 'product_id': product_id,
                # 'description_json': pl_out_json
            }
            try:
                variant = ProductVariantTranslation.objects.get(
                    product_variant_id=variant_id, language_code=language_code)
                for key, value in pl_variant_update.items():
                    setattr(variant, key, value)
                variant.save()
                display_format = "\nPL translation for variant, {}, has been edited."
                # print(display_format.format(product))
            except ProductVariantTranslation.DoesNotExist:
                try:
                    pl_name = translator.translate(variant.name,
                                                   dest=language_code).text
                    pl_variant_create = {
                        'language_code': language_code,
                        'name': pl_name,
                        'product_variant_id': variant_id,
                    }
                    pl_variant_create.update(pl_variant_update)
                    variant = ProductVariantTranslation(**pl_variant_create)
                    variant.save()
                    display_format = "\nPL translation for variant, {}, has been created."
                    print(display_format.format(variant))

                except ValueError:  # includes simplejson.decoder.JSONDecodeError
                    print('Decoding JSON has failed PL', variant.id)

            ############      Ukrainian   ##############################
            language_code = 'uk'
            uk_variant_update = {
                # 'seo_title': pl_seo_title,
                # 'seo_description': pl_seo_description,
                # 'language_code': language_code,
                # 'name': pl_name,
                # 'description': pl_description,
                # 'product_id': product_id,
                # 'description_json': pl_out_json
            }
            try:
                variant = ProductVariantTranslation.objects.get(
                    product_variant_id=variant_id, language_code=language_code)
                for key, value in uk_variant_update.items():
                    setattr(variant, key, value)
                variant.save()
                display_format = "\nUK translation for variant, {}, has been edited."
                # print(display_format.format(product))
            except ProductVariantTranslation.DoesNotExist:
                try:
                    uk_name = translator.translate(variant.name,
                                                   dest=language_code).text
                    uk_variant_create = {
                        'language_code': language_code,
                        'name': uk_name,
                        'product_variant_id': variant_id,
                    }
                    uk_variant_create.update(uk_variant_update)
                    variant = ProductVariantTranslation(**uk_variant_create)
                    variant.save()
                    display_format = "\nUK translation for variant, {}, has been created."
                    print(display_format.format(variant))

                except ValueError:  # includes simplejson.decoder.JSONDecodeError
                    print('Decoding JSON has failed UK', variant.id)

            ############      Russian   ##############################
            language_code = 'ru'
            ru_variant_update = {
                # 'seo_title': pl_seo_title,
                # 'seo_description': pl_seo_description,
                # 'language_code': language_code,
                # 'name': pl_name,
                # 'description': pl_description,
                # 'product_id': product_id,
                # 'description_json': pl_out_json
            }
            try:
                variant = ProductVariantTranslation.objects.get(
                    product_variant_id=variant_id, language_code=language_code)
                for key, value in ru_variant_update.items():
                    setattr(variant, key, value)
                variant.save()
                display_format = "\nRU translation for variant, {}, has been edited."
                # print(display_format.format(product))
            except ProductVariantTranslation.DoesNotExist:
                try:
                    ru_name = translator.translate(variant.name,
                                                   dest=language_code).text
                    ru_variant_create = {
                        'language_code': language_code,
                        'name': ru_name,
                        'product_variant_id': variant_id,
                    }
                    ru_variant_create.update(ru_variant_update)
                    variant = ProductVariantTranslation(**ru_variant_create)
                    variant.save()
                    display_format = "\nRU translation for variant, {}, has been created."
                    print(display_format.format(variant))

                except ValueError:  # includes simplejson.decoder.JSONDecodeError
                    print('Decoding JSON has failed RU', variant.id)

        # with open(os.path.join(data_folder, "categories_pl.json"), encoding='utf-8') as data_file:
        #     data = json.loads(data_file.read())
        #
        #     for data_object in data['categories']['category']:
        #
        #         name = data_object.get('@name', None)
        #         id = data_object.get('@id', None)
        #         raw_json = json.dumps({"blocks": [{"key": "", "data": {}, "text": "", "type": "unstyled", "depth": 0, "entityRanges": [], "inlineStyleRanges": []}], "entityMap": {}})
        #         out_json = json.loads(raw_json)
        #
        #         category_update = {
        #             'seo_title': name,
        #             'seo_description': name,
        #             'language_code': 'pl',
        #             'name': name,
        #             'description': name,
        #             'category_id': id,
        #             'description_json': out_json
        #         }
        #         try:
        #             obj = CategoryTranslation.objects.get(category_id=id, language_code='pl')
        #             for key, value in category_update.items():
        #                 setattr(obj, key, value)
        #             obj.tree = TreeManager
        #             obj.save()
        #             display_format = "\nTranslation for Categorie, {}, has been edited."
        #             print(display_format.format(obj))
        #         except CategoryTranslation.DoesNotExist:
        #             category_create = {
        #                 'seo_title': name,
        #                 'seo_description': name,
        #                 'language_code': 'pl',
        #                 'name': name,
        #                 'description': name,
        #                 'category_id': id,
        #                 'description_json': out_json
        #             }
        #             category_create.update(category_update)
        #             obj = CategoryTranslation(**category_create)
        #             obj.save()
        #             display_format = "\nTranslation for Categorie, {}, has been created."
        #             print(display_format.format(obj))
        #
        #     for menu_object in data['categories']['category']:
        #
        #         name = menu_object.get('@name', None)
        #         mid = menu_object.get('@id', None)
        #         menu_update = {
        #             'language_code': 'pl',
        #             'name': name,
        #             'menu_item_id': mid,
        #         }
        #         try:
        #             obj = MenuItemTranslation.objects.get(menu_item_id=mid, language_code='pl')
        #             for key, value in menu_update.items():
        #                 setattr(obj, key, value)
        #             obj.save()
        #             display_format = "\nTranslation for First level Menu, {}, has been edited."
        #             print(display_format.format(obj))
        #         except MenuItemTranslation.DoesNotExist:
        #             menu_create = {
        #                 'language_code': 'pl',
        #                 'name': name,
        #                 'menu_item_id': mid,
        #             }
        #             menu_create.update(menu_update)
        #             obj = MenuItemTranslation(**menu_create)
        #             obj.save()
        #             display_format = "\nTranslation for First level Menu, {}, has been created."
        #             print(display_format.format(obj))
        #
        #
        #     for node in data['categories']['category']:
        #         subcat = node.get('node')
        #         for dict in subcat:
        #             node_id = dict.get('@id', None)
        #             node_name = dict.get('@name', None)
        #
        #             category_node_update = {
        #                 'seo_title': node_name,
        #                 'seo_description': node_name,
        #                 'language_code': 'pl',
        #                 'name': node_name,
        #                 'description': node_name,
        #                 'category_id': node_id,
        #                 'description_json': out_json
        #             }
        #             try:
        #                 obj = CategoryTranslation.objects.get(category_id=node_id, language_code='pl')
        #                 for key, value in category_node_update.items():
        #                     setattr(obj, key, value)
        #                 obj.save()
        #                 display_format = "\nTranslation for Node level Categorie, {}, has been edited."
        #                 print(display_format.format(obj))
        #             except CategoryTranslation.DoesNotExist:
        #                 category_node_create = {
        #                     'seo_title': node_name,
        #                     'seo_description': node_name,
        #                     'language_code': 'pl',
        #                     'name': node_name,
        #                     'description': node_name,
        #                     'category_id': node_id,
        #                     'description_json': out_json
        #                 }
        #                 category_node_create.update(category_node_update)
        #                 obj = CategoryTranslation(**category_node_create)
        #                 obj.save()
        #                 display_format = "\nTranslation for Node level Categorie, {}, has been created."
        #                 print(display_format.format(obj))
        #
        #     for node_menu in data['categories']['category']:
        #         subcat_menu = node_menu.get('node')
        #         for dict in subcat_menu:
        #             node_id = dict.get('@id', None)
        #             node_name = dict.get('@name', None)
        #
        #             menu_node_update = {
        #                 'language_code': 'pl',
        #                 'name': node_name,
        #                 'menu_item_id': node_id,
        #             }
        #             try:
        #                 obj = MenuItemTranslation.objects.get(menu_item_id=node_id, language_code='pl')
        #                 for key, value in menu_node_update.items():
        #                     setattr(obj, key, value)
        #                 obj.save()
        #                 display_format = "\nTranslation for Node level Menu, {}, has been edited."
        #                 print(display_format.format(obj))
        #             except MenuItemTranslation.DoesNotExist:
        #                 menu_node_create = {
        #                     'language_code': 'pl',
        #                     'name': node_name,
        #                     'menu_item_id': node_id,
        #                 }
        #                 menu_node_create.update(menu_node_update)
        #                 obj = MenuItemTranslation(**menu_node_create)
        #                 obj.save()
        #                 display_format = "\nTranslation for Node level Menu, {}, has been created."
        #                 print(display_format.format(obj))

    def handle(self, *args, **options):
        """
        Call the function to import data
        """
        self.trans()
