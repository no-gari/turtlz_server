import csv
import time
import random
import string
from clayful import Clayful

Clayful.config({
    'language': 'ko',
    'currency': 'KRW',
    'time_zone': 'Asia/Seoul',
    'debug_language': 'ko',
    'client': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjFlNzYzZDc4NTA2YTJiYmM3Y2NmZTcwMmM0ZWI3M2ExMzkyNjI2MTFmYjU4MzdiY2U0YzdiOTUxNGRkZmMwNzQiLCJyb2xlIjoiY2xpZW50IiwiaWF0IjoxNjU1ODA2NDMyLCJzdG9yZSI6IlpDSjRQOENaSDJVUi5HWjVRTFZIUVk1WFEiLCJzdWIiOiJORUY1VFdFNU1FRUwifQ.OT7C_v_38T3-ZR0AdQEpRi4OonnI18bev4G_os7ne40'
})

category_list = [
    {'name': '화로/스토브', 'id': 'CSQMZK7U8WGE'},
    {'name': '테이블/체어', 'id': 'R82P7P4ZX4PL'},
    {'name': '텐트/타프', 'id': '5PS23XC7RSTH'},
    {'name': '기타캠핑용품', 'id': 'MJ6CPYNUQ7GP'},
    {'name': '냉난방', 'id': 'NKKKB9V73HVU'},
    {'name': '침낭/매트', 'id': 'K53M3B3RABWD'},
    {'name': '키친/식기','id': '9FZ884Z2VX48'},
    {'name': '조명/랜턴', 'id': 'YGLYFLLDF63T'},
    {'name': '캠핑소품', 'id': 'VWLAH5XCDFSY'},
]

color_list = [
    {'name': '옐로우', 'id': '9O80C09YI5CE'},
    {'name': '네이비', 'id': 'ZK75JKXSEXRI'},
    {'name': '핑크', 'id': 'RWWGPYRPT0JU'},
    {'name': '레드', 'id': 'EQJ622YESOWA'},
    {'name': '멀티', 'id': 'GD2ZU3SMF4MX'},
    {'name': '베이지', 'id': 'V32LLMZVIPMG'},
    {'name': '브라운', 'id': '9FZ884Z2VX48'},
    {'name': '블루', 'id': 'J8T65XLZYS63'},
    {'name': '그린', 'id': 'CVD79B0XJ793'},
    {'name': '오렌지', 'id': '4WMBHCWMSDFA'},
    {'name': '실버', 'id': 'VUU7D9I7O6ZW'},
    {'name': '바이올렛', 'id': 'OHDITMDLWZ5S'},
    {'name': '블랙', 'id': '02YCN2B9EVL0'},
    {'name': '골드', 'id': 'F77Z1HU4MN6S'},
    {'name': '화이트', 'id': 'TUTFMB504SXH'},
    {'name': '그레이', 'id': 'V85YY2ZZHB54'},
    {'name': '투명', 'id': '5FQBUE2TTB3L'},
]


clayful_brand = Clayful.Brand
clayful_product = Clayful.Product
clayful_collection = Clayful.Collection

f = open('220623.csv', 'r', encoding='utf-8')
# wf = open('new_brand.csv', 'r', newline='', encoding='utf-8')
# wf2 = open('new_products.csv', 'w', newline='', encoding='utf-8')
wf2 = open('colors.csv', 'w', newline='', encoding='utf-8')
rdr = csv.reader(f)
# wr = csv.writer(wf)
wr2 = csv.writer(wf2)
brand_list = []
collection_list = []
products = []
color_list = set()

options = {}
brand_code = ''
color_code = 'ZNPMJMG3EMDK'

for line in rdr:
    if not line[41] == '-' and line[14] == 'instock' and int(line[25]) >= 49000 and line[59] != None and line[59] != '':
        new_color = line[59].split(',')
        color_list.update(new_color)
new_color_list = list(color_list)

        # 상품 슬러그 생성
        # code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
        # 상품 브랜드 슬러그 구하기
        # brand_name = line[41]
        # with open("new_brand.csv") as f:
        #     for l, i in enumerate(f):
        #         data = i.split(",")
        #         if data[1] == brand_name+'\n':
        #             brand_code = data[0]

        # 카테고리의 슬러그 구하기
        # category_id = list(filter(lambda person: person['name'] == line[27], id_list))
        # print(brand_code)
        # print(category_id[0]['id'])
        # print(category_id)

        # clayful_product.create(
        #     {
        #         'slug': code,
        #         'type': 'tangible',
        #         'available': True,
        #         'bundled': False,
        #         'brand': brand_code,
        #         'collections': [
        #             String
        #         ],
        #         'catalogs': [
        #             {
        #                 'title': {
        #                     '{lang}': String or None,
        #                     ...
        #                 },
        #                 'description': {
        #                     '{lang}': String or None,
        #                     ...
        #                 },
        #                 'image': String or None
        #             }
        #         ],
        #         'thumbnail': String or None,
        #         'name': {
        #             '{lang}': String or None,
        #             ...
        #         },
        #         'keywords': {
        #             '{lang}': String or None,
        #             ...
        #         },
        #         'summary': {
        #             '{lang}': String or None,
        #             ...
        #         },
        #         'description': {
        #             '{lang}': String or None,
        #             ...
        #         },
        #         'manufacturer': String or None,
        #         'origin': {
        #             'name': String or None
        #         },
        #         'notices': [
        #             {
        #                 'slug': String,
        #                 'title': {
        #                     '{lang}': String or None,
        #                     ...
        #                 },
        #                 'items': [
        #                     {
        #                         'title': {
        #                             '{lang}': String or None,
        #                             ...
        #                         },
        #                         'description': {
        #                             '{lang}': String or None,
        #                             ...
        #                         }
        #                     }
        #                 ]
        #             }
        #         ],
        #         'price': {
        #             'original': Number,
        #             'type': String or 'fixed' or 'dynamic'
        #         },
        #         'discount': {
        #             'type': 'percentage' or 'fixed' or None,
        #             'value': Number or None
        #         },
        #         'taxCategories': [
        #             String
        #         ],
        #         'shipping': {
        #             'methods': [
        #                 String
        #             ],
        #             'calculation': String or 'bundled' or 'separated' or None
        #         },
        #         'options': [
        #             {
        #                 'name': {
        #                     '{lang}': String or None,
        #                     ...
        #                 },
        #                 'priority': Number,
        #                 'variations': [
        #                     {
        #                         'value': {
        #                             '{lang}': String or None,
        #                             ...
        #                         },
        #                         'priority': Number
        #                     }
        #                 ]
        #             }
        #         ],
        #         'bundles': [
        #             {
        #                 'required': Boolean,
        #                 'name': {
        #                     '{lang}': String or None,
        #                     ...
        #                 },
        #                 'items': [
        #                     {
        #                         'product': String,
        #                         'variant': String
        #                     }
        #                 ]
        #             }
        #         ],
        #         'meta': Object
        #     },
        #     {}
        # )

        # brand_list.append(line[41])
        # collection_list.append(line[27])
        # products.append(line[4])
    # break

# new_brand_list = list(set(brand_list))
# new_collection_list = list(set(collection_list))
# new_brand_list.sort()
# collection_list.sort()
# index = 0
#
# for collection in new_collection_list:
#     code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
#     wr.writerow([code, new_brand_list[index]])
#
#     clayful_brand.create(
#         {
#             'slug': code,
#             'name': {
#                 'ko': new_brand_list[index]
#             },
#             'thumbnail': None,
#             'logo': None,
#         },
#         {}
#     )
#     wr.writerow()
#     print(collection)
#     time.sleep(0.5)
#     index += 1

# index = 0

# for product in products:
#     wr2.writerow([products[index]])
#     index += 1

f.close()
# wf.close()
wf2.close()

[
    {
        "type":"select",
        "name":"사이즈",
        "options":
            [
                {"slug":"0","name":"아이보리 L사이즈 의자 2개","price":"0"},
                {"slug":"1","name":"그린 L사이즈 의자 2개","price":"0"},
                {"slug":"2","name":"아이보리 XL사이즈 의자 2개","price":"0"},
                {"slug":"3","name":"그린 XL사이즈 의자 2개","price":"0"},
                {"slug":"4","name":"블랙 L사이즈 의자 2개","price":"0"},
                {"slug":"5","name":"블랙 XL사이즈 의자 2개","price":"0"}
            ],"slug":"first"},
    {"type":"select",
     "name":"사은품",
     "options":
         [
             {"slug":"00","name":"원목스툴","price":"0"},
             {"slug":"01","name":"보냉백","price":"0"},
             {"slug":"10","name":"원목스툴","price":"0"},
             {"slug":"11","name":"보냉백","price":"0"},
             {"slug":"20","name":"원목스툴","price":"10000"},
             {"slug":"21","name":"보냉백","price":"10000"},
             {"slug":"30","name":"원목스툴","price":"10000"},
             {"slug":"31","name":"보냉백","price":"10000"},
             {"slug":"40","name":"원목스툴","price":"0"},
             {"slug":"41","name":"보냉백","price":"0"},
             {"slug":"50","name":"원목스툴","price":"10000"},
             {"slug":"51","name":"보냉백","price":"10000"}],
     "slug":"second"}
]


[
    {
        "type":"select",
        "name":"컬러",
        "options":
            [
                {"slug":"0",
                 "name":"블랙(기본상판)",
                 "price":"0"},
                {"slug":"1","name":"화이트(기본상판)","price":"0"},
                {"slug":"2","name":"블랙(우드상판)","price":"5500"},
                {"slug":"3","name":"화이트(우드상판)","price":"5500"},
                {"slug":"4","name":"카키(일반상판)","price":"0"},
                {"slug":"5","name":"탄(일반상판)","price":"0"},
                {"slug":"add0","name":"(추가구매상품) 우드 상판 단품 ","price":"-7400"}],
        "slug":"first"
    }
]