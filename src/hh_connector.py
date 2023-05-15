import requests


class Connector:
    """
    Класс созданий запросов к api HH
    """
    def __init__(self, url: str, params: dict):
        self._url = url
        self._headers = {'User-Agent': 'MyApp my-app-feedback@123123.com'}
        self._params = params
        self._data_dict = {}
        self._connect()

    def _connect(self):
        """
        Метод создает запрос к api сайта
        """
        try:
            r = requests.get(url=self._url, headers=self._headers, params=self._params)
            self._data_dict.update(r.json())
        except ConnectionError:
            print('Connection error!')
        except requests.HTTPError:
            print('HTTP error')
        except TimeoutError:
            print('Timeout error')
        return {}

    @property
    def data_dict(self):
        """
        Геттер полученных данных
        :return: json с данными
        """
        return self._data_dict
