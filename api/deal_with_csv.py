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

clayful_brand = Clayful.Brand

f = open('220623.csv', 'r', encoding='utf-8')
wf = open('new_brand.csv', 'w', newline='', encoding='utf-8')
# wf2 = open('new_products.csv', 'w', newline='', encoding='utf-8')
rdr = csv.reader(f)
wr = csv.writer(wf)
# wr2 = csv.writer(wf2)
brand_list = []
# products = []

options = {}

for line in rdr:
    if not line[41] == '-' and line[14] == 'instock' and int(line[25]) >= 49000:
        brand_list.append(line[41])
        # products.append(line[4])
    else:
        pass
new_brand_list = list(set(brand_list))
new_brand_list.sort()
index = 0

for brand in new_brand_list:
    code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
    wr.writerow([code, new_brand_list[index]])

    clayful_brand.create(
        {
            'slug': code,
            'name': {
                'ko': new_brand_list[index]
            },
            'thumbnail': None,
            'logo': None,
        },
        {}
    )
    time.sleep(0.5)
    index += 1

index = 0

# for product in products:
#     wr2.writerow([products[index]])
#     index += 1

f.close()
wf.close()
wf2.close()
