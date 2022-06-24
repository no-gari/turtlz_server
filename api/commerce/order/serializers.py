from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from api.commerce.cart.serializers import CartListSerializer


class OrderSerializer(serializers.Serializer):
    currency = serializers.SerializerMethodField()
    paymentMethod = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    request = serializers.SerializerMethodField()

    def get_currency(self, value):
        return 'KRW'

    def get_paymentMethod(self, value):
        return settings.CLAYFUL_PAYMENT_METHOD

    def get_address(self, value):
        postcode = value['address']['postal_code']
        name = value['address']['name']
        address = value['address']['big_address'].split(' ')
        city = address[0]
        address.pop(0)
        address1 = ' '.join(address)
        address2 = value['address']['small_address']
        mobile = value['address']['phone_number']

        return {
            'shipping': {'name': {'full': name}, 'postcode': postcode, 'country': "KR", 'city': city,
                         'address1': address1, 'address2': address2, 'mobile': mobile, 'phone': mobile},
            'billing': {'name': {'full': name}, 'postcode': postcode, 'country': "KR", 'city': city,
                        'address1': address1, 'address2': address2, 'mobile': mobile, 'phone': mobile}}

    def get_discount(self, value):
        try:
            discount = value['coupon']['_id']
            return {'cart': {'coupon': discount}}
        except:
            return None

    def get_request(self, value):
        request1 = value['request']['shipping_request'].get('content', '')
        request2 = str(value['request'].get('additional_request', ''))
        resonse = request1 + ' ' + request2
        return resonse


class QueryOptionSerializer(serializers.Serializer):
    products = serializers.SerializerMethodField()

    def get_products(self, value):
        product_string = ''
        for product in value:
            product_string += product['_id']
            if not product == value[-1]:
                product_string += ','
        return product_string


class PaymentSerializer(serializers.Serializer):
    merchant_uid = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()
    buyer_name = serializers.SerializerMethodField()
    buyer_tel = serializers.SerializerMethodField()
    buyer_email = serializers.SerializerMethodField()

    def get_merchant_uid(self, value):
        return value['_id']

    def get_name(self, value):
        return value['_id']

    def get_amount(self, value):
        return value['total']['price']['withTax']

    def get_currency(self, value):
        return value['currency']['base']['code']

    def get_buyer_name(self, value):
        return value['address']['shipping']['name']['full']

    def get_buyer_tel(self, value):
        return value['address']['shipping']['mobile']

    def get_buyer_email(self, value):
        return value['customer']['userId']


class MyOrderSerializer(serializers.Serializer):
    _id = serializers.CharField()
    order_date = serializers.SerializerMethodField()
    address_info = serializers.SerializerMethodField()
    customer_info = serializers.SerializerMethodField()
    items_info = serializers.SerializerMethodField()
    payment_info = serializers.SerializerMethodField()

    def get_order_date(self, value):
        return value['createdAt']['formatted']

    def get_address_info(self, value):
        city = value['address']['shipping'].get('city')
        address1 = value['address']['shipping'].get('address1', '')
        address2 = value['address']['shipping'].get('address2', '')
        return {'address': city + ' ' + address1 + ' ' + address2,
                'postcode': value['address']['shipping']['postcode']}

    def get_customer_info(self, value):
        return {'name': value['address']['shipping']['name']['full'],
                'mobile': value['address']['shipping']['mobile']}

    def get_items_info(self, value):
        fulfillments = value['fulfillments']
        shipped_list = []
        items_total = []


        if fulfillments is not []:
            for fulfillment in fulfillments:
                items = fulfillment['items']
                for item in items:
                    item_temp = CartListSerializer(item['item']).data
                    if value['done']:
                        item_temp['status'] = '주문 확정'
                    else:
                        item_temp['status'] = '배송 시작'
                    item_temp['tracking'] = fulfillment['tracking']
                    shipped_list.append(item_temp['_id'])
                    items_total.append(item_temp)

        for item in value['items']:
            if item['_id'] not in shipped_list:
                item_temp = CartListSerializer(item).data
                if value['done']:
                    item_temp['status'] = '주문 확정'
                else:
                    item_temp['status'] = '배송 준비'
                item_temp['tracking'] = {"company": None, "carrier": None, "uid": None, "url": None}
                items_total.append(item_temp)
        return items_total

    def get_payment_info(self, value):
        return {
            'total_original_price': value['total']['price']['original']['raw'],
            'total_sale_price': value['total']['price']['sale']['raw'],
            'total_discounted_price': value['total']['discounted']['raw'],
            'request': value['request']
        }
