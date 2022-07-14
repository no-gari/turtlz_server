import csv, time, json
from api.commerce.product.serializers import ClayfulOptionSerializer

f = open('220623.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
products = []
brand_list = []
collection_list = []

index = 0
options = {}
brand_code = ''
color_code = []

for line in rdr:
    if not line[41] == '-' and line[14] == 'instock' and int(line[25]) >= 49000:
        try:
            # 단일 상품인 경우
            if line[49] == None or line[49] == '':
                pass
            else:
                raw_data = json.loads(line[49])
                data = ClayfulOptionSerializer(raw_data, many=True).data
                variations = []
                if len(raw_data) == 1:
                    pass
                elif len(raw_data) == 2:
                    for i in range(len(raw_data[1]['options'])):
                        # 슬러그가 'add'로 시작하는 경우 따로 옵션을 생성.
                        if raw_data[1]['options'][i]['slug'].startswith('add'):
                            pass
                        else:
                            print(line[4])
        except:
            pass

f.close()
