import requests
import os
from django.conf import settings

class PayStack:
    # PayStack_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    TEST_PayStack_SECRET_KEY = settings.TEST_PAYSTACK_SECRET_KEY
    base_url = 'https://api.paystack.co/'

    # print(settings.TEST_PAYSTACK_SECRET_KEY)

    def verify_payment(self, ref, *args, **kwargs):
        self.ref = ref

        headers = {
            # 'Authorization' : f'Bearer sk_test_1ad78ea96eb747b1525831175d7adf585339cb85',
            # 'Authorization' : f'Bearer {self.PayStack_SECRET_KEY}',
            'Authorization' : f'Bearer {self.TEST_PayStack_SECRET_KEY}',
            'Content_type' : 'application/json',
        }

        path = f'transaction/verify/{ref}'

        url = self.base_url + path

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['data']
        
        response_data = response.json()
        return response_data['status'], response_data['message']