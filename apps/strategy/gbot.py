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
        self._url = '{host}:{port}/{method}'

    def close_orders(self, order_type='all'):
        """
        This method close opened orders, if order_type `all`, it close strategy at all
        :param order_type: str
        :return: Response
        """
        method = 'close_orders'
        url = self._url.format(host=self.host, port=self.port, method=method)

        response = requests.put(url, json={'type': order_type}, headers=self.headers)

        return response

    def get_orders(self):
        """
        Get list of opened orders
        :return: # TODO:
        """
        method = 'orders'
        url = self._url.format(host=self.host, port=self.port, method=method)

        response = requests.get(url, headers=self.headers)

        return response

    def get_history(self):
        """
        Get executed orders
        :return:
        """
        method = 'history'
        url = self._url.format(host=self.host, port=self.port, method=method)

        response = requests.get(url, headers=self.headers)

        return response

    def pause(self, status=None):
        """
        Get or Set bot status
        :param status:
        :return:
        """
        method = 'status'
        url = self._url.format(host=self.host, port=self.port, method=method)
        if status is not None:
            response = requests.put(url, json={'pause': status}, headers=self.headers)
        else:
            response = requests.get(url, headers=self.headers)

        return response
