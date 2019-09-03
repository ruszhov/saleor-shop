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

    def import_products(self):
    #     #!!!
        url = (requests.get('https://www.par.com.pl/en/api/products/', auth=('v.perekhaylo@akvarium.pro', 'AQWA22222'), stream = True)).text
    # #     # print(url)
        data_folder = os.path.join(PROJECT_ROOT, 'saleor','api_par_com', 'resources', 'json_file')
        xml_path = os.path.join(data_folder, 'products_en.xml')
        xml = open(xml_path, "w", errors='ignore')
        xml.writelines(url)
        xml.close()
        if xml.closed:
            print("products_en closed")
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

        url_stock = (requests.get('http://www.par.com.pl/api/stocks', auth=('v.perekhaylo@akvarium.pro', 'AQWA22222'), stream=True)).text
        xml_stock_path = os.path.join(data_folder, 'stocks.xml')
        stock = open(xml_stock_path, "w", errors='ignore')
        stock.writelines(url_stock)
        stock.close()
        if stock.closed:
            print("stocks closed")
            # iterate over the XML files in the folder
            for filename in os.listdir(data_folder):
                if filename.endswith(".xml"):
                    filename = xml_stock_path
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

        remaining_download_tries = 15
        while remaining_download_tries > 0:
            try:
                raw = (requests.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json')).text
                json_path = os.path.join(data_folder, 'currency.json')
                output_file = open(json_path, 'w')
                output_file.write(raw)
                output_file.close()
                if output_file.closed:
                    print('currency closed')
            except:
                print('error downloading currencies')
                remaining_download_tries = remaining_download_tries - 1
                continue
            else:
                break

        with open(os.path.join(data_folder, "currency.json"), encoding='utf-8',
                  errors='ignore') as currency_file:
            currency = json.loads(currency_file.read())
            for currency_object in currency:
                if currency_object['cc'] == 'EUR':
                    raw_rate_eur = currency_object['rate']
                    eur_rate = round(decimal.Decimal(raw_rate_eur), 3)
                elif currency_object['cc'] == 'PLN':
                    raw_rate_pln = currency_object['rate']
                    pln_rate = round(decimal.Decimal(raw_rate_pln * 1.23), 3)

                    with open(os.path.join(data_folder, "products_en.json"), encoding='utf-8') as data_file:
                        data = json.loads(data_file.read())
                        product_type = ProductType.objects.get(name="Сувенірна продукція").id
                        # print(product_type)
                        # if isinstance(product_type, int):
                        #     print("yes")
                        # else:
                        #     print("no")
                        # !!!
                        for data_object in data['products']['product']:
                            id = data_object.get('id', None)
                            name = data_object.get('nazwa', None)
                            description = data_object.get('opis', None)
                            description = description[:500]
                            raw_price = data_object.get('cena_eur', None)
                            dec_price = decimal.Decimal(raw_price)
                            raw_json = json.dumps({"blocks": [{"key": "", "data": {}, "text": description, "type": "unstyled", "depth": 0, "entityRanges": [], "inlineStyleRanges": []}], "entityMap": {}})
                            out_json = json.loads(raw_json)

                            products_update = {
                                # "id": id,
                                "name": name,
                                # "description": description,
                                # "price": Money(dec_price * eur_rate, DEFAULT_CURRENCY),
                                # "product_type_id": int(product_type),
                                # "attributes": out_mater_attr,
                                # "seo_description": description,
                                # "seo_title": name,
                                # "description_json": out_json
                            }
                            try:
                                obj = Product.objects.get(id=id)
                                for key, value in products_update.items():
                                    setattr(obj, key, value)
                                obj.save()
                                display_format = "\nProduct, {}, has been edited."
                                # print(display_format.format(obj))
                            except Product.DoesNotExist:
                                products_create = {
                                    "id": id,
                                    "name": name,
                                    "description": description,
                                    "price": Money(dec_price * eur_rate, DEFAULT_CURRENCY),
                                    "product_type_id": product_type,
                                    # "attributes": out_mater_attr,
                                    "seo_description": description,
                                    "seo_title": name,
                                    "description_json": out_json
                                }
                                products_create.update(products_update)
                                obj = Product(**products_create)
                                obj.save()
                                display_format = "\nProduct, {}, has been created."
                                print(display_format.format(obj))

                            #################################################################
                            ####            Product Variant creating                     ####
                            #################################################################
                            sku = data_object.get('kod', None)
                            color_name = data_object.get('kolor_podstawowy', None)
                            weight = data_object['opakowania']['karton_duzy']['waga_netto']

                            with open(os.path.join(data_folder, "stocks.json"), encoding='utf-8') as stock_file:
                                stock = json.loads(stock_file.read())
                                for stock_object in stock['produkty']['produkt']:
                                    # print(stock_object)
                                    if stock_object['id'] == id and stock_object['kod'] == sku:
                                        price_ov_raw = stock_object['cena_katalogowa']
                                        price_ov = decimal.Decimal(price_ov_raw)
                                        cost_price_raw = stock_object['cena_po_rabacie']
                                        cost_price = decimal.Decimal(cost_price_raw)
                                        quantity = stock_object['stan_magazynowy']

                                        if stock_object.get('ilosc_dostawy', 0) == None:
                                            quantity_allocated = 0
                                        else:
                                            quantity_allocated = stock_object.get('ilosc_dostawy', 0)

                                        stocks_update = {
                                            # "id": id,
                                            "sku": sku,
                                            "name": color_name,
                                            "price_override": Money(price_ov * pln_rate, DEFAULT_CURRENCY),
                                            "product_id": id,
                                            "cost_price": Money(cost_price * pln_rate, DEFAULT_CURRENCY),
                                            "quantity": quantity,
                                            "quantity_allocated": quantity_allocated,
                                            "track_inventory": False,
                                            "weight": weight
                                        }
                                        try:
                                            stock = ProductVariant.objects.get(sku=sku)
                                            for key, value in stocks_update.items():
                                                setattr(stock, key, value)
                                            stock.save()
                                            display_format = "\nStock, {}, has been edited."
                                            # print(display_format.format(stock))
                                        except ProductVariant.DoesNotExist:
                                            stocks_create = {
                                                # "id": id,
                                                "sku": sku,
                                                "name": color_name,
                                                "price_override": Money(price_ov * pln_rate, DEFAULT_CURRENCY),
                                                "product_id": id,
                                                "cost_price": Money(cost_price * pln_rate, DEFAULT_CURRENCY),
                                                "quantity": quantity,
                                                "quantity_allocated": quantity_allocated,
                                                "track_inventory": False,
                                                "weight": weight
                                            }
                                            stocks_update.update(stocks_update)
                                            stock = ProductVariant(**stocks_create)
                                            stock.save()
                                            display_format = "\nStock, {}, has been created."
                                            print(display_format.format(stock))

                                        price_update = Product.objects.get(id=id)
                                        price_update.price = Money(price_ov * pln_rate, DEFAULT_CURRENCY)
                                        price_update.save()

                            #################################################################
                            ####            m2m node-product adding                      ####
                            #################################################################

                            category_dict = data_object.get('kategorie', None)
                            # print(category_dict)
                            for cat, v in category_dict.items():
                                if type(v) is dict:
                                    # print(v)
                                    cat_id = v['@id']
                                    categ = Category.objects.get(id=cat_id)
                                    prod = Product.objects.get(id=id)
                                    m2m = prod.category.add(categ)

                                else:
                                    # print(v)
                                    for d in v:
                                        d['prod_id'] = id
                                        cat_id = d['@id']
                                        # print(cat_id, id)
                                        categ = Category.objects.get(id = cat_id)
                                        prod = Product.objects.get(id = id)
                                        m2m = prod.category.add(categ)

        #################################################################
        ####            m2m node-product adding                      ####
        #################################################################

        # with open(os.path.join(data_folder, "categories_en.json"), encoding='utf-8') as data_file:
        #     flc = json.loads(data_file.read())
        #     for data_object in flc['categories']['category']:
        #         first_level_cat_id = data_object.get('@id', None)
        #         node_object = data_object.get('node')
        #         # print(first_level_cat_id, type(node_object))
        #         for node in node_object:
        #             node_id = node.get('@id', None)
        #             # print(first_level_cat_id, node_id)
        #             node_product = Product.objects.filter(category=node_id)
        #             # print(node_product)
        #             for prod in Product.objects.filter(category=node_id):
        #                 # print(node_id, prod.id)
        #                 # print(first_level_cat_id, prod.id)
        #                 fl_cat = Category.objects.get(id=first_level_cat_id)
        #                 # m2m_fl = prod.category.add()
        #                 # print(fl_cat.id, prod.id)
        #                 m2m_fl = prod.category.add(fl_cat)

    def handle(self, *args, **options):
        """
        Call the function to import data
        """
        self.import_products()

