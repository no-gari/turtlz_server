import random
import string
import csv, io, json, os
from clayful import Clayful
import urllib.request as url_lib_request
from api.commerce.product.serializers import ClayfulOptionSerializer

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
    {'name': '옐로우', 'id': 'PTJ3UAT5R5DV'},
    {'name': '네이비', 'id': 'KU8KB7MKTQJ7'},
    {'name': '핑크', 'id': '6FVMGUW6FHPD'},
    {'name': '레드', 'id': 'MPFPX5F7A4VW'},
    {'name': '멀티', 'id': 'NNJCKNJWT8TP'},
    {'name': '베이지', 'id': 'MFAFSJT5UWW9'},
    {'name': '브라운', 'id': 'VN56J2HK6H4R'},
    {'name': '블루', 'id': '7T3C5VWXS3CX'},
    {'name': '그린', 'id': 'LMAGF9PBE2F7'},
    {'name': '오렌지', 'id': '69GXG8WEWZE8'},
    {'name': '실버', 'id': 'Z6MH5V5GNJF8'},
    {'name': '바이올렛', 'id': 'HLFRR4JSQQCJ'},
    {'name': '블랙', 'id': 'XBX7QN64NRWT'},
    {'name': '골드', 'id': 'NWR42BW5L8HQ'},
    {'name': '화이트', 'id': '55KHHK4R9PBE'},
    {'name': '그레이', 'id': 'FN8YGZQW7F2R'},
    {'name': '투명', 'id': 'ZHHR375W92FU'},
]


clayful_brand = Clayful.Brand
clayful_product = Clayful.Product
clayful_collection = Clayful.Collection

f = open('220623.csv', 'r', encoding='utf-8')
# wf = open('new_brand.csv', 'r', newline='', encoding='utf-8')
# wf2 = open('new_products.csv', 'w', newline='', encoding='utf-8')
# wf2 = open('colors.csv', 'w', newline='', encoding='utf-8')
rdr = csv.reader(f)
# wr = csv.writer(wf)
# wr2 = csv.writer(wf2)
brand_list = []
collection_list = []
products = []

options = {}
brand_code = ''
color_code = []

for line in rdr:
    if not line[41] == '-' and line[14] == 'instock' and int(line[25]) >= 49000:
        # 상품 슬러그 생성
        code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
        # 상품 브랜드 슬러그 구하기
        brand_name = line[41]
        with open("new_brand.csv") as f:
            for l, i in enumerate(f):
                data = i.split(",")
                if data[1] == brand_name+'\n':
                    brand_code = data[0]
        # 색상 슬러그 리스트로 구하기
        if line[59] != None and line[59] != '':
            product_colors = line[59].split(',')
            for product in product_colors:
                product_id = list(filter(lambda person: person['name'] == product, color_list))
                color_code.append(product_id[0]['id'])
        else:
            color_code = []

        # 카테고리의 슬러그 구하기
        category_id = list(filter(lambda person: person['name'] == line[27], category_list))
        color_code.append(category_id[0]['id'])
        total_category = color_code

        # 상품 이름
        name = line[4]

        # 상품 가격
        original_price, discount_price = int(line[26]), int(line[25])

        # 상품 상세
        description = line[9]

        # 상품 썸네일
        thumbnail_list = line[30].split(',')
        thumbnail_url = thumbnail_list[0]
        thumbnail_type = thumbnail_url.split('.')[-1]
        thumbnail_name = 'thumbnail.' + thumbnail_type
        img_open = url_lib_request.urlretrieve(thumbnail_url, thumbnail_name)

        clayful_image = Clayful.Image

        thumbnail = clayful_image.create({
            'model':  (None, 'Product'),
            'application':  (None, 'thumbnail'),
            'file': (
                thumbnail_name,
                open(thumbnail_name, 'rb'),
                'image/jpeg'
            ),
        }).data['_id']

        # 상품 옵션
        variants = []

        # 단일 상품인 경우
        if line[49] == None or line[49] == '':
            options = [
                {
                    'name': {
                        'ko': '옵션',
                    },
                    'priority': 0,
                    'variations': [
                        {
                            'value': {
                                'ko': name
                            },
                            'priority': 0
                        }
                    ]
                }
            ]
        else:
            raw_data = json.loads(line[49])
            data = ClayfulOptionSerializer(raw_data, many=True).data
            variations = []
            if len(raw_data) == 1:
                for i in range(len(raw_data[0]['options'])):
                    variations.append({
                        'value': {
                            'ko': raw_data[0]['options'][i]['name']
                        },
                        'priority': i
                    })
                options = [
                    {
                        'name': {
                            'ko': raw_data[0]['name'],
                        },
                        'priority': 0,
                        'variations': variations
                    }
                ]
            elif len(raw_data) == 2:
                for i in range(len(raw_data[1]['options'])):
                    # 슬러그가 'add'로 시작하는 경우 따로 옵션을 생성.
                    if raw_data[1]['options'][i]['slug'].isalpha():
                        variants.append({
                            'value': {
                                'ko': raw_data[1]['options'][i]['name']
                            },
                            'priority': i
                        })
                    # 슬러그가 숫자인 경우 종속성을 찾아서 옵션을 만들어준다.
                    else:
                        dependency_name = ''
                        has_depdendency_name = raw_data[1]['options'][i]['slug']
                        for item in raw_data[0]['options']:
                            if has_depdendency_name.startswith(item['slug']):
                                dependency_name = item['slug']
                                break
                        else:
                            pass

                        variations.append({
                            'value': {
                                'ko': dependency_name + ',' + has_depdendency_name
                            },
                            'priority': i
                        })

                options = [
                    {
                        'name': {
                            'ko': raw_data[0]['name'] + ', ' + raw_data[1]['name'],
                        },
                        'priority': 0,
                        'variations': variations
                    }
                ]

        clayful_response = clayful_product.create(
            {
                'slug': code,
                'type': 'tangible',
                'available': True,
                'bundled': False,
                'brand': brand_code,
                'collections': total_category,
                'catalogs': [
                    {
                        'title': {
                            'ko': None,
                        },
                        'description': {
                            'ko': None,
                        },
                        'image': None
                    }
                ],
                'thumbnail': thumbnail,
                'name': {
                    'ko': name,
                },
                'keywords': {
                    'ko': None,
                },
                'summary': {
                    'ko': None,
                },
                'description': {
                    'ko': description,
                },
                'manufacturer': None,
                'origin': {
                    'name': None
                },
                'price': {
                    'original': int(original_price),
                    'type': 'fixed'
                },
                'discount': {
                    'type': 'fixed',
                    'value': int(original_price) - int(discount_price)
                },
                'taxCategories': [
                    'JF3L3N6M55Y2'
                ],
                'shipping': {
                    'methods': [
                        'B6Q2MLNJ5RJ9'
                    ],
                    'calculation': 'bundled'
                },
                'options': options,
                'meta': {}
            },
            {}
        )
        os.remove(thumbnail_name)
        options = clayful_response.data['options']
        created_product_id = clayful_response.data['_id']
        sku = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
        # clayful_product.create_variant(
        #     created_product_id,
        #     {
        #         'available': True,
        #         'sku': sku,
        #         'thumbnail':  None,
        #         'downloadable': None,
        #         'types': [
        #             {
        #                 'option': String,
        #                 'variation': String
        #             }
        #         ],
        #         'price': Number,
        #         'discount': {
        #             'type': 'fixed',
        #             'value': Number
        #         },
        #         'quantity': None,
        #         'weight': None,
        #         'width': None,
        #         'height': None,
        #         'depth': None,
        #         'policy': {
        #             'count': None,
        #             'expires': {
        #                 'type':  None,
        #                 'value': None
        #             }
        #         }
        #     }
        # )


    break

# index = 0

# for product in products:
#     wr2.writerow([products[index]])
#     index += 1

f.close()
# wf.close()
# wf2.close()
