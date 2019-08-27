"""
Import imges to Datababse
"""
import os
from urllib.parse import urlparse
import json
from io import StringIO, BytesIO
import urllib
from PIL import Image
from ....product.models import Product, ProductImage
from ....menu.models import Menu, MenuItem
from django.core.management.base import BaseCommand
from datetime import datetime
from ....settings import PROJECT_ROOT
import requests
from django.db.models import Q
import xmltodict
from django.utils.text import slugify


class Command(BaseCommand):
    def import_images(self):
        data_folder = os.path.join(PROJECT_ROOT, 'saleor','api_par_com', 'resources', 'json_file')
        img_folder = os.path.join(PROJECT_ROOT, 'media', 'products')
        # print(img_folder)
        par_url = 'https://www.par.com.pl'
        with open(os.path.join(data_folder, "products_en.json"), encoding='utf-8') as data_file:
            data = json.loads(data_file.read())
            for data_object in data['products']['product']:
                # print(data_object)

                zdjecia = data_object.get('zdjecia', None)
                # print(zdjecia)
                pid = data_object.get('id', None)
                # print(pid)
                # product_id = Product.objects.get(id=pid)
                # print(type(zdjecia))
                for k,v in zdjecia.items():
                    if type(v) is list:
                        for im_url in v:
                            url = par_url + im_url
                            im_name = os.path.basename(urlparse(url).path)
                            full_path = str(os.path.join(img_folder, im_name))
                            # print(full_path)
                            try:
                                if not os.path.exists(full_path):
                                    # resource = urllib.request.urlopen(url)
                                    # output = open(full_path, 'wb')
                                    # output.write(resource.read())
                                    # output.close()
                                    with open(full_path, 'wb') as fout:
                                        response = requests.get(url, stream=True)
                                        response.raise_for_status()
                                        # Write response data to file
                                        for block in response.iter_content(4096):
                                            fout.write(block)
                            except EOFError:
                                print(EOFError)

                            image = ('products/'+im_name)
                            # print(image, pid)
                            # print(pid)
                            products_update = {
                                # "id": product_id,
                                "image": image,
                                "alt": '',
                                "product_id": pid
                            }
                            outobj = ProductImage.objects.filter(image=image, product_id=pid)
                            if outobj.exists():
                                for obj in outobj:
                                    try:
                                        # obj = ProductImage.objects.get(product_id=product_id)
                                        for key, value in products_update.items():
                                            setattr(obj, key, value)
                                        obj.save()
                                        # display_format = "\nProductImage, {}, has been edited."
                                        # print(display_format.format(obj.product_id))
                                    except ProductImage.DoesNotExist:
                                        products_create = {
                                            # "id": product_id,
                                            "image": image,
                                            "alt": '',
                                            "product_id": pid
                                        }
                                        products_create.update(products_update)
                                        obj = ProductImage(**products_create)
                                        obj.save()
                                        # display_format = "\nProductImage, {}, has been created."
                                        # print(display_format.format(obj))
                            else:
                                products_create = {
                                    # "id": product_id,
                                    "image": image,
                                    "alt": '',
                                    "product_id": pid
                                }
                                products_create.update(products_update)
                                obj = ProductImage(**products_create)
                                obj.save()
                                display_format = "\nProductImage, {},has been created."
                                print(display_format.format(obj))



                    else:
                        url = par_url + v
                        im_name = os.path.basename(urlparse(url).path)
                        full_path = str(os.path.join(img_folder, im_name))
                        # print(full_path)

                        try:
                            if not os.path.exists(full_path):
                                # resource = urllib.request.urlopen(url)
                                # output = open(full_path, 'wb')
                                # output.write(resource.read())
                                # output.close()
                                with open(full_path, 'wb') as fout:
                                    response = requests.get(url, stream=True)
                                    response.raise_for_status()
                                    # Write response data to file
                                    for block in response.iter_content(4096):
                                        fout.write(block)
                        except EOFError:
                            print(EOFError)
                        image = ('products/' + im_name)
                        # print(image)
                        products_update = {
                            # "id": product_id,
                            "image": image,
                            "alt": '',
                            "product_id": pid
                        }
                        try:
                            obj = ProductImage.objects.get(product_id=pid)
                            for key, value in products_update.items():
                                setattr(obj, key, value)
                            obj.save()
                            # display_format = "\nProduct, {}, has been edited."
                            # print(display_format.format(obj))
                        except ProductImage.DoesNotExist:
                            products_create = {
                                # "id": product_id,
                                "image": image,
                                "alt": '',
                                "product_id": pid
                            }

                            products_create.update(products_update)
                            obj = ProductImage(**products_create)
                            obj.save()
                            # display_format = "\nImage, {}, does not exests."
                            # print(display_format.format(obj))


    def handle(self, *args, **options):
        """
        Call the function to import data
        """
        self.import_images()

