from rest_framework.exceptions import ValidationError
from django.conf import settings
from clayful import Clayful

Clayful.config({
    'language': 'ko',
    'currency': 'KRW',
    'time_zone': 'Asia/Seoul',
    'debug_language': 'ko',
    'client': settings.CLAYFUL_BACKEND_TOKEN
})


class ClayfulCustomerClient:
    def __init__(self):
        super().__init__()
        self.customer = Clayful.Customer

    def clayful_register(self, **kwargs):
        customer = self.customer
        payload = {'connect': True, 'userId': kwargs['email'], 'name': {'full': kwargs['nickname']}}
        try:
            response = customer.create(payload)
            return response
        except Exception as e:
            return ValidationError({'error_msg': [e.args]})

    def clayful_login(self, **kwargs):
        customer = self.customer
        payload = {'userId': kwargs['email']}
        try:
            response = customer.authenticate(payload)
            return response
        except Exception as e:
            return ValidationError({'error_msg': [e.args]})

    def clayful_customer_delete(self, **kwargs):
        customer = self.customer
        options = {'customer': kwargs['clayful']}
        try:
            response = customer.delete_me(options)
            return response
        except Exception as e:
            return ValidationError({'error_msg': [e.args]})

    def clayful_customer_get_me(self, **kwargs):
        customer = self.customer
        options = {'customer': kwargs['clayful']}
        try:
            response = customer.get_me(options)
            return response
        except Exception as e:
            return ValidationError({'error_msg': [e.args]})

    def clayful_customer_coupons_list(self, **kwargs):
        customer = self.customer
        options = {'customer': kwargs['clayful'], 'query': {'limit': 120}}
        try:
            response = customer.list_coupons_for_me(options)
            return response
        except Exception as e:
            return ValidationError({'error_msg': [e.args]})

    def clayful_customer_add_coupon(self, **kwargs):
        customer = self.customer
        payload = {'coupon': kwargs['coupon_id']}
        options = {}
        try:
            response = customer.add_coupon(kwargs['customer_id'], payload, options)
            return response
        except Exception as e:
            return ValidationError({'error_msg': [e.args]})


class ClayfulProductClient:
    def __init__(self):
        super().__init__()
        self.product = Clayful.Product

    def get_related_products(self, **kwargs):
        try:
            options = {
                'query': {
                    'brand': kwargs['brand_id'],
                    'available': True,
                    'limit': 120,
                }
            }
            response = self.product.list(options)
            return response
        except Exception as err:
            return ValidationError({'error_msg': [err.message]})

    def list_catalog_products(self, **kwargs):
        try:
            options = {
                'query': {
                    'collection': kwargs.get('collection', 'any'),
                    'limit': 120
                }
            }
            response = self.product.list(options)
            return response
        except Exception as err:
            return ValidationError({'error_msg': [err.message]})

    def search_products_count(self, **kwargs):
        try:
            options = {
                'query': {
                    'q': kwargs['keyword'],
                    'search': 'name.ko,keywords.ko',
                    'searchMatch': 'partial'
                }
            }
            response = self.product.count(options)
            return response
        except Exception as err:
            return ValidationError({'error_msg': [err.message]})

    def search_products(self, **kwargs):
        try:
            options = {
                'query': {
                    'q': kwargs['keyword'],
                    'search': 'name.ko,keywords.ko',
                    'searchMatch': 'partial',
                    'limit': 10,
                    'page': kwargs.get('page', 1)
                }
            }
            response = self.product.list(options)
            return response
        except Exception as err:
            return ValidationError({'error_msg': [err.message]})

    def list_products(self, **kwargs):
        try:
            options = {
                'query': {
                    'collection': kwargs.get('collection', 'any'),
                    'limit': 10,
                    'available': True,
                    'page': kwargs.get('page', 1),
                    'sort': kwargs.get('sort', '-createdAt'),
                    'brand': kwargs.get('brand', 'any')
                }
            }
            response = self.product.list(options)
            return response
        except Exception as err:
            return ValidationError({'error_msg': [err.message]})

    def get_detail(self, **kwargs):
        try:
            product_id = kwargs['id']
            options = {'query': {'embed': '+brand.logo'}}
            response = self.product.get(product_id, options)
            return response
        except Exception as err:
            return ValidationError({'error_msg': [err.message]})

    def count_products(self, **kwargs):
        try:
            options = {'query': {'collection': kwargs.get('collection', 'any'), 'brand': kwargs.get('brand', 'any')}}
            response = self.product.count(options)
            return response
        except Exception as err:
            return ValidationError({'error_msg': [err.message]})


class ClayfulBrandClient:
    def __init__(self):
        self.brand = Clayful.Brand

    def get_brand(self, **kwargs):
        try:
            brand_id = kwargs['brand_id']
            response = self.brand.get(brand_id)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def get_brand_list(self, **kwargs):
        try:
            options = {
                'query': {
                    'limit': 10,
                    'page': kwargs.get('page' ,1)
                }
            }
            response = self.brand.list(options)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def get_brand_count(self, **kwargs):
        try:
            options = {}
            response = self.brand.count(options)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def search_brands(self, **kwargs):
        try:
            options = {
                'query': {
                    'q': kwargs['keyword'],
                    'search': 'name.ko',
                    'searchMatch': 'partial',
                    'limit': 10,
                    'page': kwargs.get('page', 1)
                }
            }
            response = self.brand.list(options)
            return response
        except Exception as err:
            return ValidationError({'error_msg': [err.message]})


class ClayfulCollectionClient:
    def __init__(self):
        self.collection = Clayful.Collection

    def get_collections(self, **kwargs):
        try:
            parent = kwargs.get('parent', None)
            options = {'query': {'parent': 'none', 'limit': 120}} if parent is None else {
                'query': {'parent': parent, 'limit': 120}}
            response = self.collection.list(options)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def get_collection(self, **kwargs):
        try:
            parent = kwargs.get('parent')
            response = self.collection.get(parent)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})


class ClayfulReviewClient:
    def __init__(self, auth_token):
        self.review = Clayful.Review
        if auth_token is not None:
            self.options = {'customer': auth_token}

    def reviews_count(self, **kwargs):
        try:
            options = {'query': {'product': kwargs['product']}}
            response = self.review.count(options)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def reviews_list(self, **kwargs):
        try:
            options = {
                'query':
                    {
                        'limit': 10,
                        'product': kwargs['product'],
                        'page': kwargs['page'],
                        'sort': '-id',
                        'published': False
                    }
            }
            response = self.review.list(options)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def get_review(self, **kwargs):
        try:
            review_id = kwargs['review_id']
            response = self.review.get(review_id, self.options)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def create_review(self, **kwargs):
        try:
            payload = ({'order': kwargs['order'], 'product': kwargs['product'], 'body': kwargs['body']})
            response = self.review.create_for_me(payload, self.options)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def delete_review(self, **kwargs):
        try:
            review_id = kwargs['review_id']
            response = self.review.delete_for_me(review_id, self.options)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})


class ClayfulReviewCommentClient:
    def __init__(self):
        self.review_comment = Clayful.ReviewComment

    def get_comments(self, **kwargs):
        try:
            options = {'query': {'review': kwargs['review_id']}}
            response = self.review_comment.list(options)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})


class ClayfulCartClient:
    def __init__(self, auth_token):
        self.cart = Clayful.Cart
        self.options = {'customer': auth_token}

    def get_cart(self):
        try:
            response = self.cart.get_for_me({}, self.options)
            return response
        except Exception as err:
            raise ValidationError({'error_msg': [err.message]})

    def add_item(self, **kwargs):
        try:
            payload = {'product': kwargs['product_id'], 'variant': kwargs['variant'],
                       'shippingMethod': settings.CLAYFUL_SHIPPING_ID, 'quantity': kwargs['quantity']}
            response = self.cart.add_item_for_me(payload, self.options)
            return response
        except Exception as err:
            raise ValidationError({'add_item': [err.message]})

    def delete_item(self, **kwargs):
        try:
            response = self.cart.delete_item_for_me(kwargs['item_id'], self.options)
            return response
        except Exception as err:
            raise ValidationError({'delete_item': [err.message]})

    def empty_cart(self):
        try:
            response = self.cart.empty_for_me(self.options)
            return response
        except Exception as err:
            return ValidationError({'empty_cart': [err.message]})

    def count_items_cart(self, **kwargs):
        try:
            resposne = self.cart.count_items_for_me(self.options)
            return resposne
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def checkout_cart(self, **kwargs):
        try:
            payload = kwargs['payload']
            if payload['discount']['cart']['coupon'] is None or payload['discount'] is None:
                payload.pop('discount')
            options = self.options
            options['query'] = {'items': kwargs['items']['products']}
            resposne = self.cart.checkout_for_me('order', payload, self.options)
            return resposne
        except Exception as err:
            if err.message == '결제 방식이 필요하지 않습니다.':
                payload.pop('paymentMethod')
                resposne = self.cart.checkout_for_me('order', payload, self.options)
                ㅁ=1
                return resposne
            else:
                raise ValidationError({'error_msg': '결제 에러 발생.'})


class ClayfulOrderClient:
    def __init__(self, auth_token):
        self.order = Clayful.Order
        if auth_token == None:
            self.options = {}
        else:
            self.options = {'customer': auth_token}

    def get_order_list(self, **kwargs):
        try:
            options = self.options
            options['query'] = {'limit': 10, 'page': kwargs['page'], 'status': 'paid'}
            response = self.order.list_for_me(options)
            return response
        except Exception as err:
            return ValidationError({'error_msg': [err.message]})

    def get_cancel_list(self, **kwargs):
        try:
            options = self.options
            options['query'] = {'limit': 10, 'page': kwargs['page'], 'raw': False, 'status': 'cancelled,refunded'}
            response = self.order.list_for_me(options)
            return response
        except Exception as err:
            return ValidationError({'error_msg': [err.message]})

    def order_cancel(self, **kwargs):
        try:
            payload = kwargs['payload']
            order_id = kwargs['order_id']
            response = self.order.cancel_for_me(order_id, payload, self.options)
            return response
        except Exception as err:
            return ValidationError({'error_msg': [err.message]})

    def get_order(self, **kwargs):
        try:
            options = {}
            options['query'] = {'raw': False, 'displayLanguage': 'order'}
            response = self.order.get_for_me(kwargs['order_id'], options)
            return response
        except Exception as err:
            return ValidationError({'error_msg': [err.message]})

    def get_order_webhook(self, **kwargs):
        try:
            options = self.options
            options['query'] = {'raw': False}
            response = self.order.get(kwargs['order_id'], options)
            return response
        except Exception as err:
            return ValidationError({'error_msg': [err.message]})

    def order_count(self, **kwargs):
        try:
            response = self.order.count(self.options)
            return response
        except Exception as err:
            return ValidationError({'error_msg': [err.message]})

    def order_done(self, **kwargs):
        try:
            response = self.order.mark_as_done(kwargs['order_id'], self.options)
            return response
        except Exception as err:
            return ValidationError({'error_msg': [err.message]})

    def request_refund(self, **kwargs):
        try:
            payload = {
                'reason': kwargs['reason'],
                'items': [{'item': kwargs['item'], 'quantity': kwargs['quantity']}],
                'shipments': [settings.CLAYFUL_SHIPPING_ID]
            }
            response = self.order.request_refund_for_me(kwargs['order_id'], payload, self.options)
            return response
        except Exception as err:
            return ValidationError({'error_msg': [err.message]})


class ClayfulCouponClient:
    def __init__(self):
        self.coupon = Clayful.Coupon

    def coupon_list(self, **kwargs):
        try:
            response = self.coupon.list({'query': {'active': True}})
            return response
        except Exception as err:
            return ValidationError({'error_msg': '쿠폰 목록을 불러오는데 실패했습니다.'})

    def coupon_detail(self, **kwargs):
        try:
            response = self.coupon.get(kwargs['coupon_id'])
            return response
        except Exception as err:
            return ValidationError({'error_msg': '쿠폰을 불러오는데 실패했습니다.'})

    def coupon_count(self, **kwargs):
        try:
            options = {'query': {'active': True}}
            response = self.coupon.count(options)
            return response
        except Exception as e:
            return ValidationError({'error_msg': [e.args]})
