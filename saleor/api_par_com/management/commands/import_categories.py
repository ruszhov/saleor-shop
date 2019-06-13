"""
Import json data from JSON file to Datababse
"""
import os
import json
from ....product.models import Category, ProductType, Attribute
from ....menu.models import Menu, MenuItem
from django.core.management.base import BaseCommand
from datetime import datetime
from ....settings import PROJECT_ROOT
import requests
import xmltodict
from django.utils.text import slugify
from googletrans import Translator
from mptt.managers import TreeManager
from django.db.models import Max


class Command(BaseCommand):

    def import_categories(self):
        raw = (requests.get('https://www.par.com.pl/en/api/categories/', auth=('v.perekhaylo@akvarium.pro', 'AQWA22222'))).text
        # raw = r.text
        data_folder = os.path.join(PROJECT_ROOT, 'saleor','api_par_com', 'resources', 'json_file')
        # json_path = os.path.join(data_folder, 'categories.json')
        xml_path = os.path.join(data_folder, 'categories_en.xml')
        # print(xml_path)
        xml = open(xml_path, "w", encoding="utf-8")
        xml.write(raw)
        xml.close()
        if xml.closed:
            # print("ok")
            # iterate over the XML files in the folder
            for filename in os.listdir(data_folder):
                if filename.endswith(".xml"):
                    filename = xml_path
                    f = open(filename)

                    XML_content = f.read()

                    # parse the content of each file using xmltodict
                    x = xmltodict.parse(XML_content)
                    j = json.dumps(x)

                    # print(filename)

                    filename = filename.replace('.xml', '')
                    output_file = open(filename + '.json', 'w')
                    output_file.write(j)
                    output_file.close()
        else:
            print("no file *xml")
        menu_name = str('Меню')
        menu, created = Menu.objects.get_or_create(name=menu_name)
        if created:
            pass
        else:
            print('dont created')

        footer_name = str('Footer')
        footer, created = Menu.objects.get_or_create(name=footer_name)
        if created:
            pass
        else:
            print('dont created')

        product_type_create, created = ProductType.objects.get_or_create(name='Сувенірна продукція')
        if created:
            pass
        else:
            print('dont created')

        category_update = {
            'id': 1,
            'name': 'Catalogue',
            'slug': 'catalogue',
            'description': 'Catalogue',
            'seo_description': 'Catalogue',
            'seo_title': 'Catalogue',
            'description_json': {}
        }
        try:
            obj = Category.objects.get(id=1)
            for key, value in category_update.items():
                setattr(obj, key, value)
            obj.tree = TreeManager
            obj.save()
            display_format = "\nFirst level Categorie, {}, has been edited."
            print(display_format.format(obj))
        except Category.DoesNotExist:
            category_create = {
                'id': 1,
                'name': 'Catalogue',
                'slug': 'catalogue',
                'description': 'Catalogue',
                'seo_description': 'Catalogue',
                'seo_title': 'Catalogue',
                'description_json': {}
            }
            category_create.update(category_update)
            obj = Category(**category_create)
            obj.save()
            display_format = "\nFirst level Categorie, {}, has been created."
            print(display_format.format(obj))


        ############################################################
        # Menu creating
        ############################################################

        # name = menu_object.get('@name', None)
        # parent = menu_object.get('@parent', None)
        # mid = menu_object.get('@id', None)

        cat_ids = [1, 2]
        cat_menus = [Menu.objects.get(name="Меню").id, Menu.objects.get(name="Footer").id]

        for (id, menu_id) in zip(cat_ids, cat_menus):

            menu_update = {
                'id': id,
                'name': 'Catalogue',
                'menu_id': menu_id,
                'url': '#'
            }
            try:
                obj = MenuItem.objects.get(id=id)
                for key, value in menu_update.items():
                    setattr(obj, key, value)
                obj.save()
                display_format = "\nCatalogue, {}, has been edited."
                print(display_format.format(obj))
            except MenuItem.DoesNotExist:
                menu_create = {
                    'id': id,
                    'name': 'Catalogue',
                    'menu_id': menu_id,
                    'url': '#'
                }
                menu_create.update(menu_update)
                obj = MenuItem(**menu_create)
                obj.save()
                display_format = "\nCatalogue Menu, {}, has been created."
                print(display_format.format(obj))

        with open(os.path.join(data_folder, "categories_en.json"), encoding='utf-8') as data_file:
            data = json.loads(data_file.read())
            menu_id = Menu.objects.get(name="Меню").id
            # print(type(data))

            # !!!
            for data_object in data['categories']['category']:

                name = data_object.get('@name', None)
                parent = data_object.get('@parent', None)
                id = data_object.get('@id', None)
                category_slug = slugify(name)
                raw_json = json.dumps({"blocks": [{"key": "", "data": {}, "text": "", "type": "unstyled", "depth": 0, "entityRanges": [], "inlineStyleRanges": []}], "entityMap": {}})
                out_json = json.loads(raw_json)

                category_update = {
                    'id': id,
                    'name': name,
                    'slug': category_slug,
                    'description': name,
                    'seo_description': name,
                    'seo_title': name,
                    'description_json': out_json
                }
                try:
                    obj = Category.objects.get(id=id)
                    for key, value in category_update.items():
                        setattr(obj, key, value)
                    obj.tree = TreeManager
                    obj.save()
                    display_format = "\nFirst level Categorie, {}, has been edited."
                    print(display_format.format(obj))
                except Category.DoesNotExist:
                    category_create = {
                        'id': id,
                        'name': name,
                        'slug': category_slug,
                        'description': name,
                        'seo_description': name,
                        'seo_title': name,
                        'description_json': out_json
                    }
                    category_create.update(category_update)
                    obj = Category(**category_create)
                    obj.save()
                    display_format = "\nFirst level Categorie, {}, has been created."
                    print(display_format.format(obj))

            for menu_object in data['categories']['category']:

                name = menu_object.get('@name', None)
                parent = menu_object.get('@parent', None)
                mid = menu_object.get('@id', None)
                menu_update = {
                    'id': mid,
                    'name': name,
                    'menu_id': menu_id,
                    'category_id': mid,
                    'parent_id': 1
                }
                try:
                    obj = MenuItem.objects.get(id=mid)
                    for key, value in menu_update.items():
                        setattr(obj, key, value)
                    obj.save()
                    display_format = "\nFirst level Menu, {}, has been edited."
                    print(display_format.format(obj))
                except MenuItem.DoesNotExist:
                    menu_create = {
                        'id': mid,
                        'name': name,
                        'menu_id': menu_id,
                        'category_id': mid,
                        'parent_id': 1
                    }
                    menu_create.update(menu_update)
                    obj = MenuItem(**menu_create)
                    obj.save()
                    display_format = "\nFirst level Menu, {}, has been created."
                    print(display_format.format(obj))

            ###################################################################################
            ###                  Creating Product Type
            ####################################################################################

            # for product_type in data['categories']['category']:
            #
            #     id = product_type.get('@id', None)
            #     name = product_type.get('@name', None)
            #     prod_type_update = {
            #         'id': id,
            #         'name': name,
            #         'has_variants': True,
            #         'is_shipping_required': False,
            #         'tax_rate': 'standart',
            #         'weight': 0
            #     }
            #     try:
            #         obj = ProductType.objects.get(id=id)
            #         for key, value in prod_type_update.items():
            #             setattr(obj, key, value)
            #         obj.save()
            #         display_format = "\nProduct Type, {}, has been edited."
            #         print(display_format.format(obj))
            #     except ProductType.DoesNotExist:
            #         prod_type_create = {
            #             'id': id,
            #             'name': name,
            #             'has_variants': True,
            #             'is_shipping_required': False,
            #             'tax_rate': 'standart',
            #             'weight': 0
            #         }
            #         prod_type_create.update(prod_type_update)
            #         obj = ProductType(**prod_type_create)
            #         obj.save()
            #         display_format = "\nProduct Type, {}, has been created."
            #         print(display_format.format(obj))

                # #################################################################
                # ####            Product Material Attribute creating          ####
                # #################################################################
                #
                # product_type = ProductType.objects.get(name='Сувенірна продукція').id
                # attr_update = {
                #     "name": 'Матеріал',
                #     "slug": 'material',
                #     # "product_type_id": product_type,
                #     "product_type_id": product_type
                # }
                # try:
                #     attribute = Attribute.objects.get(product_type_id=product_type)
                #     for key, value in attr_update.items():
                #         setattr(attribute, key, value)
                #     attribute.save()
                #     display_format = "\nAttribute, {}, has been edited."
                #     print(display_format.format(attribute))
                # except Attribute.DoesNotExist:
                #     attr_create = {
                #         "name": 'Матеріал',
                #         "slug": 'material',
                #         # "product_type_id": product_type,
                #         "product_type_id": product_type
                #     }
                #     attr_update.update(attr_update)
                #     attribute = Attribute(**attr_create)
                #     attribute.save()
                #     display_format = "\nAttribbute, {}, has been created."
                #     print(display_format.format(attribute))

                # try:
                #     menu, created = MenuItem.objects.update_or_create(
                #         name=name, menu_id=menu_id, id=mid,
                #         defaults={'id': mid,
                #             'name': name,
                #             'menu_id': menu_id}
                #     )
                #     if menu:
                #         display_format = "\nFirst level Menu, {}, has been edited."
                #         print(display_format.format(menu))
                #     if created:
                #         display_format = "\nFirst level Menu, {}, has been created."
                #         print(display_format.format(created))
                # except Exception as ex:
                #     print(str(ex))
                #     msg = "\n\nSomething went wrong saving this movie: {}\n{}".format(name, str(ex))
                #     print(msg)


            for node in data['categories']['category']:
                subcat = node.get('node')
                for dict in subcat:
                    node_id = dict.get('@id', None)
                    node_name = dict.get('@name', None)
                    node_parent = dict.get('@parent', None)
                    node_slug = slugify(node_name)

                    category_node_update = {
                        'id': node_id,
                        'name': node_name,
                        'slug': node_slug,
                        'description': node_name,
                        'parent_id': node_parent,
                        'seo_description': node_name,
                        'seo_title': node_name,
                        'description_json': out_json
                    }
                    try:
                        obj = Category.objects.get(id=node_id)
                        for key, value in category_node_update.items():
                            setattr(obj, key, value)
                        obj.save()
                        display_format = "\nNode level Categorie, {}, has been edited."
                        print(display_format.format(obj))
                    except Category.DoesNotExist:
                        category_node_create = {
                            'id': node_id,
                            'name': node_name,
                            'slug': node_slug,
                            'description': node_name,
                            'parent_id': node_parent,
                            'seo_description': node_name,
                            'seo_title': node_name,
                            'description_json': out_json
                        }
                        category_node_create.update(category_node_update)
                        obj = Category(**category_node_create)
                        obj.save()
                        display_format = "\nNode level Categorie, {}, has been created."
                        print(display_format.format(obj))

            for node_menu in data['categories']['category']:
                # menu_id = Menu.objects.get(name="Меню").id
                # category_id = node_name.get('@id')
                subcat_menu = node_menu.get('node')
                for dict in subcat_menu:
                    node_id = dict.get('@id', None)
                    node_name = dict.get('@name', None)
                    node_parent = dict.get('@parent', None)

                    menu_node_update = {
                        'id': node_id,
                        'name': node_name,
                        'menu_id': menu_id,
                        'parent_id': node_parent,
                        'category_id': node_id
                    }
                    try:
                        obj = MenuItem.objects.get(id=node_id)
                        for key, value in menu_node_update.items():
                            setattr(obj, key, value)
                        obj.save()
                        display_format = "\nNode level Menu, {}, has been edited."
                        print(display_format.format(obj))
                    except MenuItem.DoesNotExist:
                        menu_node_create = {
                            'id': node_id,
                            'name': node_name,
                            'menu_id': menu_id,
                            'parent_id': node_parent,
                            'category_id': node_id
                        }
                        menu_node_create.update(menu_node_update)
                        obj = MenuItem(**menu_node_create)
                        obj.save()
                        display_format = "\nNode level Menu, {}, has been created."
                        print(display_format.format(obj))
                    # try:
                    #     node_menu, created = MenuItem.objects.update_or_create(
                    #         # title=title,
                    #         # url=url,
                    #         id = node_id,
                    #         # release_year=release_year,
                    #         # defaults={"id" : node_id}
                    #         defaults={'menu_id': menu_id}
                    #     )
                    #     if node_menu:
                    #         node_menu.id = node_id
                    #         node_menu.parent_id = node_parent
                    #         node_menu.category_id = node_parent
                    #         node_menu.name = node_name
                    #         node_menu.save()
                    #         display_format = "\nNode, {}, has been edited."
                    #         print(display_format.format(node_menu.name))
                    #     if created:
                    #         node_menu.save()
                    #         display_format = "\nNode, {}, has been saved."
                    #         print(display_format.format(node_menu.name))
                    # except Exception as ex:
                    #     print(str(ex))
                    #     msg = "\n\nSomething went wrong saving this node: {}\n{}".format(node.name, str(ex))
                    #     print(msg)
        footer_menu = Menu.objects.get(name="Footer").id
        footer_id = MenuItem.objects.get(menu_id = footer_menu, name="Catalogue").id
        menus = MenuItem.objects.filter(menu_id=Menu.objects.get(name="Меню").id)
        for menu in menus:
            if menu.name != 'Catalogue':
                if menu.parent_id == 1:
                    footer_update = {
                        # 'id':  MenuItem.objects.all().aggregate(Max('id'))['id__max'] + 1
                        'name': menu.name,
                        'menu_id': footer_menu,
                        'url':menu.url,
                        'parent_id': footer_id,
                        'category_id': menu.category_id
                    }
                    try:
                        obj = MenuItem.objects.get(menu_id = footer_menu, category_id=menu.category_id)
                        for key, value in footer_update.items():
                            setattr(obj, key, value)
                        obj.save()
                        display_format = "\nFooter Menu, {}, has been edited."
                        print(display_format.format(obj))
                    except MenuItem.DoesNotExist:
                        footer_create = {
                            'id':  MenuItem.objects.all().aggregate(Max('id'))['id__max'] + 1,
                            'name': menu.name,
                            'menu_id': footer_menu,
                            'url': menu.url,
                            'parent_id': footer_id,
                            'category_id': menu.category_id
                        }
                        footer_create.update(footer_update)
                        obj = MenuItem(**footer_create)
                        obj.save()
                        display_format = "\nFooter Menu, {}, has been created."
                        print(display_format.format(obj))
                    else:
                        footer_update = {
                            # 'id':  MenuItem.objects.all().aggregate(Max('id'))['id__max'] + 1
                            'name': menu.name,
                            'menu_id': footer_menu,
                            'url': menu.url,
                            'parent_id': 2,
                            'category_id': menu.category_id
                        }
                        try:
                            obj = MenuItem.objects.get(menu_id=footer_menu, category_id=menu.category_id)
                            for key, value in footer_update.items():
                                setattr(obj, key, value)
                            obj.save()
                            display_format = "\nFooter Menu, {}, has been edited."
                            print(display_format.format(obj))
                        except MenuItem.DoesNotExist:
                            footer_create = {
                                'id': MenuItem.objects.all().aggregate(Max('id'))['id__max'] + 1,
                                'name': menu.name,
                                'menu_id': footer_menu,
                                'url': menu.url,
                                'parent_id': 2,
                                'category_id': menu.category_id
                            }
                            footer_create.update(footer_update)
                            obj = MenuItem(**footer_create)
                            obj.save()
                            display_format = "\nFooter Menu, {}, has been created."
                            print(display_format.format(obj))

    def handle(self, *args, **options):
        """
        Call the function to import data
        """
        self.import_categories()

