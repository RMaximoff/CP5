from src.connector import Connector


class HeadhunterVacancy:
    """
    Класс вакансий полученных с апи хх.ру
    """

    def __init__(self, employers_id: list):
        self._url = 'https://api.hh.ru/vacancies'
        self._params = {'employer_id': employers_id}
        self._vacancies_data = self._get_vacancies()
        self._vacancies_clean_data = {}
        self._get_clean_data(self._vacancies_data)

    def _get_vacancies(self):
        """
        Метод получает данные о компаниях и сохраняет их в словаре
        """
        connector = Connector(url=self._url, params=self._params)
        return connector.data_dict

    def _get_clean_data(self, data: dict):
        """
        Приводим в необходимый вид данные вакансий
        """
        for vacancy in data['items']:
            salary = vacancy.get("salary")
            self._vacancies_clean_data[vacancy.get("id")] = {'employer_id': vacancy.get('employer').get("id"),
                                                             'name': vacancy.get("name"),
                                                             'requirement': vacancy.get("snippet").get("requirement"),
                                                             'responsibility': vacancy.get('snippet').get("responsibility"),
                                                             'salary_from': salary.get("from") if salary else 0,
                                                             'salary_to': salary.get("to") if salary else 0,
                                                             'salary_currency': salary.get("currency") if salary else None,
                                                             'url': vacancy.get("alternate_url")}

    def __repr__(self):
        return f'{self._vacancies_clean_data}'

