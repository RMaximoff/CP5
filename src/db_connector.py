import psycopg2


class DBConnector:
    """
    Класс с основными методами взаимодействия с БД
    """
    def __init__(self, db_name, user, password):
        self._db_name = db_name
        self._default_db_name = 'postgres'
        self._user = user
        self._password = password
        self._host = 'localhost'
        self._port = 5432
        self._employers_table_name = 'employers'
        self._vacancies_table_name = 'vacancies'

        self._connection = None
        self.cursor = None

        if not self._check_db():
            self._create_db()
            self._create_table()

    def _connect(self, db_name):
        """Подключение к БД"""
        self._connection = psycopg2.connect(database=db_name,
                                            user=self._user,
                                            password=self._password,
                                            host=self._host,
                                            port=self._port)
        self.cursor = self._connection.cursor()

    def _disconnect(self):
        """Отключение от БД"""
        if self._connection:
            self._connection.commit()
            self.cursor.close()
            self._connection.close()

    def _check_db(self):
        """Проверка существования БД"""
        try:
            self._connect(self._db_name)
            self._disconnect()

            return True

        except (Exception, psycopg2.Error) as error:
            return False

    def _create_db(self):
        """Создание БД"""
        self._connect(self._default_db_name)
        self._connection.autocommit = True
        self.cursor.execute(f"CREATE DATABASE {self._db_name};")

        self._connection.autocommit = False
        self._disconnect()

    def _create_table(self):
        """Создание таблиц в БД"""
        self._connect(self._db_name)
        self.cursor.execute(f"CREATE TABLE {self._employers_table_name}" \
                            f"(id SERIAL PRIMARY KEY," \
                            f"hh_id int," \
                            f"company_name varchar not null," \
                            f"hh_url varchar not null," \
                            f"company_url varchar," \
                            f"description text);" \
                            f"CREATE TABLE {self._vacancies_table_name}" \
                            f"(id SERIAL PRIMARY KEY," \
                            f"hh_id int not null," \
                            f"employer_id int references {self._employers_table_name}(id) not null," \
                            f"vacancy_name varchar," \
                            f"requirement varchar," \
                            f"responsibility varchar," \
                            f"salary_from real," \
                            f"salary_to real," \
                            f"salary_currency varchar," \
                            f"url varchar)")
        self._disconnect()



