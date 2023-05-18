from src.hh_connector import Connector
from bs4 import BeautifulSoup
import json


class HeadHunterEmployer:
    """
    Класс получения данных о компании с API HH.ru
    """

    def __init__(self, employer_id: int):
        self._url = f'https://api.hh.ru/employers/{employer_id}'
        self._params = {'text': employer_id}
        self._employer_data = self._get_employer_data()
        self._employer_clean_data = {}
        self._get_clean_data(self._employer_data)

    @property
    def employers_data(self):
        return self._employer_clean_data

    def _get_employer_data(self):
        """
        Метод получает данные о компаниях и сохраняет их в словаре
        """
        connector = Connector(url=self._url, params=self._params)
        return connector.data_dict

    def _get_clean_data(self, data: dict):
        """
        Приводим в необходимый вид данные о компании
        """
        self._employer_clean_data["employer_id"] = data.get("id")
        self._employer_clean_data["company_name"] = data.get("name")
        self._employer_clean_data["hh_url"] = data.get("alternate_url")
        self._employer_clean_data["company_url"] = data.get("site_url")
        self._employer_clean_data["description"] = BeautifulSoup(data.get("description"), 'html.parser').get_text()

    def __repr__(self):
        return f'{json.dumps(self._employer_clean_data)}'
