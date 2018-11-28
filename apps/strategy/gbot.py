import requests
from django.conf import settings


class Client(object):
    def __init__(self, host, port):

        self.host = host
        self.port = port
        self.headers = {
            'auth_key': settings.SECRET_KEY,
            'Content-Type': 'application/json',
        }

    def close_orders(self, order_type='all'):
        url = ''.join([self.host, ':', self.port, '/close_orders'])
        response = requests.put(url, json={'type': order_type}, headers=self.headers)
        return response
