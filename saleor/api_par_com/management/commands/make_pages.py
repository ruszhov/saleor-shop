"""
Import json data from JSON file to Datababse
"""
from ....page.models import Page, PageTranslation
from ....menu.models import Menu, MenuItem, MenuItemTranslation
from django.core.management.base import BaseCommand
from googletrans import Translator

class Command(BaseCommand):

    def pages(self):
        page_slugs = ['payment-and-delivery', 'about-us', 'contact']
        page_titles = ['Payment and delivery', 'About us', 'Contacts']
        menu_id = Menu.objects.get(name="Меню").id

        for (slug, title) in zip(page_slugs, page_titles):

            page_update = {
                'slug': slug,
                'title': title,
                # 'content': content,
                # 'seo_description': content,
                'seo_title': title,
                'content_json': {}
            }
            try:
                page = Page.objects.get(slug=slug)
                for key, value in page_update.items():
                    setattr(page, key, value)
                page.save()
                display_format = "\nPage, {}, has been edited."
                print(display_format.format(page))
            except Page.DoesNotExist:
                page_create = {
                    'slug': slug,
                    'title': title,
                    # 'content': content,
                    # 'seo_description': content,
                    'seo_title': title,
                    'content_json': {}
                }
                page_create.update(page_update)
                page = Page(**page_create)
                page.save()
                display_format = "\nPage, {}, has been created."
                print(display_format.format(page))

            ###########################################
            langs = ['pl', 'uk', 'ru']
            for lang in langs:
                page_translation_update = {
                    # 'seo_title': title,
                    # 'seo_description': content,
                    'language_code': lang,
                    # 'title': trans_title,
                    # 'content': content,
                    'page_id': page.id,
                    'content_json': {}
                }
                try:
                    obj = PageTranslation.objects.get(page_id=page.id, language_code=lang)
                    for key, value in page_translation_update.items():
                        setattr(obj, key, value)
                    obj.save()
                    display_format = "\nPageTranslation, {}, has been edited."
                    print(display_format.format(obj))
                except PageTranslation.DoesNotExist:
                    try:
                        translator = Translator(service_urls=[
                            'translate.google.com',
                            'translate.google.co.kr',
                        ])
                        trans_title = translator.translate(page.title, dest=lang).text
                        page_translation_create = {
                            'seo_title': title,
                            # 'seo_description': content,
                            'language_code': lang,
                            'title': trans_title,
                            # 'content': content,
                            'page_id': page.id,
                            'content_json': {}
                        }
                        page_translation_create.update(page_translation_update)
                        obj = PageTranslation(**page_translation_create)
                        obj.save()
                        display_format = "\nPageTranslation, {}, has been created."
                        print(display_format.format(obj))
                    except ValueError:  # includes simplejson.decoder.JSONDecodeError
                        print('Decoding JSON has failed UK', page.id)

            ###############Menu Creating#######################################
            menu_item_update = {
                # 'name': name,
                'menu_id': menu_id,
                'page_id': page.id
            }
            try:
                menu_item = MenuItem.objects.get(page_id=page.id)
                for key, value in menu_item_update.items():
                    setattr(menu_item, key, value)
                menu_item.save()
                display_format = "\nMenuItem, {}, has been edited."
                print(display_format.format(menu_item))
            except MenuItem.DoesNotExist:
                menu_item_create = {
                    'name': title,
                    'menu_id': menu_id,
                    'page_id': page.id
                }
                menu_item_create.update(menu_item_update)
                menu_item = MenuItem(**menu_item_create)
                menu_item.save()
                display_format = "\nMenuItem, {}, has been created."
                print(display_format.format(menu_item))

            ###########################################
            langs = ['pl', 'uk', 'ru']
            for lang in langs:
                menu_item_translation_update = {
                    'language_code': lang,
                    'menu_item_id': menu_item.id
                }
                try:
                    obj = MenuItemTranslation.objects.get(menu_item_id=menu_item.id, language_code=lang)
                    for key, value in menu_item_translation_update.items():
                        setattr(obj, key, value)
                    obj.save()
                    display_format = "\nMenuItemTranslation, {}, has been edited."
                    print(display_format.format(obj))
                except MenuItemTranslation.DoesNotExist:
                    try:
                        translator = Translator(service_urls=[
                            'translate.google.com',
                            'translate.google.co.kr',
                        ])
                        trans_name = translator.translate(menu_item.name, dest=lang).text
                        menu_item_translation_create = {
                            'language_code': lang,
                            'name': trans_name,
                            'menu_item_id': menu_item.id
                        }
                        menu_item_translation_create.update(menu_item_translation_update)
                        obj = MenuItemTranslation(**menu_item_translation_create)
                        obj.save()
                        display_format = "\nMenuItemTranslation, {}, has been created."
                        print(display_format.format(obj))
                    except ValueError:  # includes simplejson.decoder.JSONDecodeError
                        print('Decoding JSON has failed UK', menu_item.id)


    def handle(self, *args, **options):
        """
        Call the function to import data
        """
        self.pages()

