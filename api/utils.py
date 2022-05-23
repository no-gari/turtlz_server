from rest_framework.pagination import PageNumberPagination
from django.utils.deconstruct import deconstructible
from firebase_admin import messaging
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


def list_converter(datas):
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


# 개인한테 보내기
def send_to_individual():
    registration_token = '클라이언트의 FCM 토큰'

    message = messaging.Message(
    notification=messaging.Notification(
        title='안녕하세요 타이틀 입니다',
        body='안녕하세요 메세지 입니다',
    ),
    token=registration_token,
    )

    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)


def send_to_all():
    messages = [
        messaging.Message(
            notification=messaging.Notification('Price drop', '5% off all electronics'),
            token=registration_token,
        ),
        # ...
        messaging.Message(
            notification=messaging.Notification('Price drop', '2% off all books'),
            topic='readers-club',
        ),
    ]

    response = messaging.send_all(messages)
    # See the BatchResponse reference documentation
    # for the contents of response.
    print('{0} messages were sent successfully'.format(response.success_count))