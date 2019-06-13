"""
Import json data from URL to Datababse
"""
import requests
import json
import os
from ....settings import LANGUAGE_CODE as language_code
from ....product.models import Category, CategoryTranslation, Product, ProductTranslation, ProductVariantTranslation, ProductVariant
from ....menu.models import Menu, MenuItem, MenuItemTranslation
from django.core.management.base import BaseCommand
import xmltodict
from ....settings import PROJECT_ROOT
from ....core.utils.translations import TranslationProxy
# from google.cloud import translate
from googletrans import Translator


class Command(BaseCommand):
    def translate(self):

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
            print(menu_item_id)

            ###########      Polska   ##############################
            language_code = 'pl'
            pl_menu_update = {
                'language_code': language_code,
                # 'name': pl_name,
                'menu_item_id': menu_item_id,
            }
            try:
                menu = MenuItemTranslation.objects.get(menu_item_id=menu_item_id, language_code='pl')
                print(menu.name)
                for key, value in pl_menu_update.items():
                    setattr(menu, key, value)
                menu.save()
                display_format = "\nTranslation for menu, {}, has been edited."
                print(display_format.format(menu))
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
                    print('Decoding JSON has failed', menu.id)


                    # pl_menu_create = {
                    #     'language_code': language_code,
                    #     'name': pl_name,
                    #     'menu_item_id': menu_item_id,
                    # }
                    # pl_menu_create.update(pl_menu_update)
                    # menu = MenuItemTranslation(**pl_menu_create)
                    # menu.save()
                    # display_format = "\nTranslation for menu, {}, has been created."
                    # print(display_format.format(menu))

            ###########      Ukrainian    ##############################
            # language_code = 'uk'
            # uk_menu_update = {
            #     'language_code': language_code,
            #     # 'name': uk_name,
            #     'menu_item_id': menu_item_id,
            # }
            # try:
            #     uk_menu = MenuItemTranslation.objects.get(menu_item_id=menu_item_id, language_code='uk')
            #     for key, value in uk_menu_update.items():
            #         setattr(menu, key, value)
            #     uk_menu.save()
            #     disukay_format = "\nTranslation for menu, {}, has been edited."
            #     print(disukay_format.format(menu))
            # except MenuItemTranslation.DoesNotExist:
            #     try:
            #         uk_name = translator.translate(menu.name, dest='uk').text
            #     except ValueError:  # includes simplejson.decoder.JSONDecodeError
            #         print('Decoding JSON has failed', menu.id)
            #         uk_menu_create = {
            #             'language_code': language_code,
            #             'name': uk_name,
            #             'menu_item_id': menu_item_id,
            #         }
            #         uk_menu_create.update(uk_menu_update)
            #         uk_menu = MenuItemTranslation(**uk_menu_create)
            #         uk_menu.save()
            #         disukay_format = "\nTranslation for menu, {}, has been created."
            #         print(disukay_format.format(menu))

            ###########      Russian    ##############################
            # language_code = 'ru'
            # # ru_name = translator.translate(menu.name, dest='ru').text
            #
            # ru_menu_update = {
            #     'language_code': language_code,
            #     # 'name': ru_name,
            #     'menu_item_id': menu_item_id,
            # }
            # try:
            #     menu = MenuItemTranslation.objects.get(menu_item_id=menu_item_id, language_code='ru')
            #     for key, value in ru_menu_update.items():
            #         setattr(menu, key, value)
            #     menu.save()
            #     disruay_format = "\nTranslation for menu, {}, has been edited."
            #     print(disruay_format.format(menu))
            # except MenuItemTranslation.DoesNotExist:
            #     try:
            #         ru_name = translator.translate(menu.name, dest='uk').text
            #     except ValueError:  # includes simplejson.decoder.JSONDecodeError
            #         print('Decoding JSON has failed', menu.id)
            #         ru_menu_create = {
            #             'language_code': language_code,
            #             'name': ru_name,
            #             'menu_item_id': menu_item_id,
            #         }
            #         ru_menu_create.update(ru_menu_update)
            #         menu = MenuItemTranslation(**ru_menu_create)
            #         menu.save()
            #         disruay_format = "\nTranslation for menu, {}, has been created."
            #         print(disruay_format.format(menu))

    def handle(self, *args, **options):
        """
        Makes a GET request to the  API.
        """
        # headers = {'Content-Type': 'application/json'}
        # response = requests.get(
        #     url=IMPORT_URL,
        #     headers=headers,
        # )
        #
        # response.raise_for_status()
        # data = response.json()
        #
        # for data_object in data:
        self.translate()
