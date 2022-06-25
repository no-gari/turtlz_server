import random
import string
import csv
import time
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

rdr = csv.reader(f)
wr = csv.writer(wf)

brand_list = []

for line in rdr:
    if not line[41] == '-' and line[14] == 'instock' and int(line[25]) >= 49000:
        brand_list.append(line[41])
    else:
        pass
new_brand_list = list(set(brand_list))
new_brand_list.sort()

index = 0
count = 0

for brand in new_brand_list:
    code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))

    response = clayful_brand.create(
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
    wr.writerow([response.data['_id'], new_brand_list[index]])

    index +=1
    count +=1

    if count == 13:
        time.sleep(0.3)
        count = 0

f.close()
wf.close()

[
    {
        'name': {'ko': '[4천원쿠폰] 2022 지라프 구이바다 세라믹 아이보리 에디션 M'},
        'priority': 0,
        'variations':
            [
                {'value': {'ko': '본품'}, 'priority': 0, '_id': 'LN2YHUMPED7G'},
                {'value': {'ko': '지라프 소나무 손잡이 2p'}, 'priority': 1, '_id': 'NCBRSSRUXU2R'}
            ],
        '_id': 'MTWXKY6CP759'
    }
]
