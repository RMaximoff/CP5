import queries
import psycopg2
from src.db_connector import DBConnector
from src.hh_employer import HeadHunterEmployer
from src.hh_vacancy import HeadhunterVacancy
from src.db_manager import DBManager


def main():
    employers_list = {'Skyeng': 1122462, 'Keepcode': 3992497, 'Студия Кефир': 851138, 'Ланит': 733, 'Тензор': 67611,
                      'VK': 15478, 'CarPrice': 1532045, 'Aston': 6093775, 'Usetech': 681672, 'Сбер': 3529}
    print('Собираю данные по вакансиям...')
    employers_data = []
    for employer in employers_list:
        employers_data.append(HeadHunterEmployer(employers_list[employer]).employers_data)

    vacancies = HeadhunterVacancy(list(employers_list.values())).vacancies

    if len(vacancies) == 0:
        print('Вакансий не найдено')
        quit()

    db_name = 'hh_parsing_data'
    while True:
        user = input('Укажите имя пользователя как в PgAdmin: ')
        password = input('Укажите пароль как в PgAdmin: ')

        try:
            with DBConnector(db_name=db_name, user=user, password=password) as conn:
                print('\nПишу в базу данных ...\n')
                for data in employers_data:
                    conn.cursor.execute(queries.insert_employers_query, data)

                for data in vacancies:
                    conn.cursor.execute(queries.insert_vacancies_query, data)
        except psycopg2.OperationalError:
            print('Неправильно указан логин или пароль\n')
            pass
        db_manager = DBManager(db_name, user, password)
        while True:
            question = int(input('Укажите номер команды.\n'
                                 'Вот что я могу:\n'
                                 '1. Получить список всех компаний и количество вакансий у каждой компании\n'
                                 '2. Получить список всех вакансий с указанием названия компании, '
                                 'названия вакансии и зарплаты и ссылки на вакансию\n'
                                 '3. Получить среднюю зарплату по вакансиям\n'
                                 '4. Получить список всех вакансий, у которых '
                                 'зарплата выше средней по всем вакансиям\n'
                                 '5. Получить список всех вакансий, в названии которого содержится слово\n\n'
                                 '0. Выход\n'
                                 ': '))

            if question == 0:
                quit()
            elif question == 1:
                db_manager.get_companies_and_vacancies_count()
            elif question == 2:
                db_manager.get_all_vacancies()
            elif question == 3:
                db_manager.get_avg_salary()
            elif question == 4:
                db_manager.get_vacancies_with_higher_salary()
            elif question == 5:
                word = input("Какое слово ищем? ")
                db_manager.get_vacancies_with_keyword(word)
            else:
                print('Укажите число из списка выше')


if __name__ == '__main__':
    main()

