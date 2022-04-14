from rest_framework.pagination import PageNumberPagination
from django.utils.deconstruct import deconstructible
import datetime
import uuid
import os

@deconstructible
class FilenameChanger(object):
    def __init__(self, base_path):
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.base_path = f'{base_path}/{str(date)}'

    def __call__(self, instance, filename, *args, **kwargs):
        ext = filename.split('.')[-1].lower()
        filename = f'{uuid.uuid4()}.{ext}'
        path = os.path.join(self.base_path, filename)
        return path

    def __eq__(self, other):
        return self.base_path


class StandardResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 10
    page_size = 10


def new_list(datas):
    new_product_list = []
    for data in datas:
        index = next((index for (index, d) in enumerate(new_product_list) if d.get('id') == data['brand_id']), None)
        if index is None:
            new_product_list.append({
                'id': data['brand_id'],
                'name': data['brand_name'],
                'least_price': data['brand_least_price'],
                'shipping_price': data['brand_shipping_price'],
                'products': [
                    {
                        'name': data['product']['name'],
                        'banner_img': data['product']['banner_img'],
                        'discount_price': data['product']['discount_price'],
                        'quantity': data['quantity'],
                        'variant_id': data['variant_id'],
                        'variant_name': data['variant_name'],
                    }
                ]
            })
        else:
            new_product_list[index]['products'].append(
                {
                    'name': data['product']['name'],
                    'banner_img': data['product']['banner_img'],
                    'discount_price': data['product']['discount_price'],
                    'quantity': data['quantity'],
                    'variant_id': data['variant_id'],
                    'variant_name': data['variant_name'],
                }
            )
    return new_product_list
