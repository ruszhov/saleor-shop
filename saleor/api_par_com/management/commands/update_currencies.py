"""
Import json data from URL to Datababse
"""
import requests
import json
import os
from ....product.models import ProductVariant
from django.core.management.base import BaseCommand
from datetime import datetime
from ....settings import PROJECT_ROOT
from prices import Money
import decimal

class Command(BaseCommand):
    def import_currencies(self):
        raw = (requests.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json')).text
        data_folder = os.path.join(PROJECT_ROOT, 'saleor','api_par_com', 'resources', 'json_file')
        json_path = os.path.join(data_folder, 'currency.json')
        output_file = open(json_path, 'w')
        output_file.write(raw)
        output_file.close()

        #################################################################
        ####            Variant Currencies values updating           ####
        #################################################################

        with open(os.path.join(data_folder, "currency.json"), encoding='utf-8', errors='ignore') as currency_file:
            currency = json.loads(currency_file.read())
            for currency_object in currency:
                if currency_object['cc'] == 'PLN':
                    raw_rate = currency_object['rate']
                    rate = round(decimal.Decimal(raw_rate), 3)
                    print(type(rate))

                    #################################################################
                    ####            Product Variant creating                     ####
                    #################################################################

                    with open(os.path.join(data_folder, "stocks.json"), encoding='utf-8') as stock_file:
                        stock = json.loads(stock_file.read())
                        for stock_object in stock['produkty']['produkt']:
                            # print(stock_object)
                            # if stock_object['id'] == id:
                            price_ov_raw = stock_object['cena_katalogowa']
                            price_ov = decimal.Decimal(price_ov_raw)
                            cost_price_raw = stock_object['cena_po_rabacie']
                            cost_price = decimal.Decimal(cost_price_raw)
                            sku = stock_object['kod']
                            print(price_ov * rate)
                            print(cost_price * rate)
                            stocks_update = {
                                "price_override": Money(price_ov * rate, 'UAH'),
                                "cost_price": Money(cost_price * rate, 'UAH'),
                            }
                            stock = ProductVariant.objects.get(sku=sku)
                            for key, value in stocks_update.items():
                                setattr(stock, key, value)
                            stock.save()
                            display_format = "\nCurrency, {}, has been edited."
                            print(display_format.format(stock))

    def handle(self, *args, **options):
        """
        Makes a GET request to the  API.
        """
        self.import_currencies()
