import psycopg2
from src.db_connector import DBConnector


class DBManager:

    def __init__(self, db_name, user, password):
        self._db_name = db_name
        self._user = user
        self._password = password

    def _connect(self, query):
        with DBConnector(self._db_name, self._user, self._password) as conn:
            conn.cursor.execute(query)
            results = conn.cursor.fetchall()
            for i in results:
                print(i)

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        query = """SELECT e.company_name,
                          count(v.vacancy_id) as num_vacancies
                   FROM employers e 
                   FULL JOIN vacancies v on v.employer_id = e.employer_id
                   GROUP BY e.company_name"""
        self._connect(query)

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        query = """SELECT e.company_name, 
                          v.vacancy_name,
                          case when v.salary_to = 0 then v.salary_from else v.salary_to end as salary,
                          v.url
                    FROM vacancies v
                    LEFT JOIN employers e on v.employer_id = e.employer_id"""
        self._connect(query)

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        query = """SELECT avg(case when v.salary_to = 0 then v.salary_from else v.salary_to end)
                   FROM vacancies v
                   WHERE v.salary_to > 0 or v.salary_from > 0 """
        self._connect(query)

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        query = """SELECT e.company_name, 
                          v.vacancy_name,
                          case when v.salary_to = 0 then v.salary_from else v.salary_to end as salary,
                          v.url
                   FROM vacancies v
                   LEFT JOIN employers e on v.employer_id = e.employer_id
                   WHERE CASE WHEN v.salary_to = 0 THEN v.salary_from ELSE v.salary_to END > 
                   (SELECT avg(case when v.salary_to = 0 then v.salary_from else v.salary_to end)
                   FROM vacancies v
                   WHERE v.salary_to > 0 or v.salary_from > 0)"""
        self._connect(query)

    def get_vacancies_with_keyword(self, word):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        query = """SELECT e.company_name, 
                          v.vacancy_name,
                          case when v.salary_to = 0 then v.salary_from else v.salary_to end as salary,
                          v.url
                   FROM vacancies v
                   LEFT JOIN employers e on v.employer_id = e.employer_id
                   WHERE v.vacancy_name LIKE %s"""
        keyword = '%'+word+'%'
        with DBConnector(self._db_name, self._user, self._password) as conn:
            conn.cursor.execute(query, (keyword,))
            results = conn.cursor.fetchall()
            if len(results) == 0:
                print(f"В названиях вакансий слова '{word}' не найдено\n")
            else:

                for i in results:
                    print(i)
