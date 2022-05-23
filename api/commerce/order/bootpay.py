from bootpay import Bootpay


class BootpayMethods:
    def __init__(self):
        super().__init__()
        self.rest_application_id = '623d21ba2701800023f68706'
        self.rest_private_key = 'xANJyPvU+T8H3IWJIDsxWQukGnHuMNquyWYaR/GphmQ='
        self.bootpay = Bootpay(self.rest_application_id, self.rest_private_key)

    # 토큰 발급
    def get_token(self):
        result = self.bootpay.get_access_token()
        print(result)
        print(result['data']['token'])

    # 결제 검증
    def verification(self):
        receipt_id = '612df0250d681b001de61de6'
        result = self.bootpay.verify(receipt_id)
        print(result)

    # 결제 취소 (전액 취소 / 부분 취소)
    def cancel(self):
        receipt_id = '612df0250d681b001de61de6'
        result = self.bootpay.cancel(
            receipt_id,
        )
        print(result)

    # 서버 승인 요청
    def server_submit(self):
        result = self.bootpay.submit('')
        print(result)
