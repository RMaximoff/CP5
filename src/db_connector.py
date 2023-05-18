import psycopg2
import queries


class DBConnector:
    """
    Класс с основными методами взаимодействия с БД
    """
    def __init__(self, db_name: str, user: str, password: str):
        self._db_name = db_name
        self._user = user
        self._password = password
        self._host = 'localhost'
        self._port = 5432

        self._connection = None
        self._cursor = None

        self._check_db()

    @property
    def cursor(self):
        return self._cursor

    def _connect(self):
        """Подключение к БД"""
        self._connection = psycopg2.connect(database=self._db_name,
                                            user=self._user,
                                            password=self._password,
                                            host=self._host,
                                            port=self._port)
        self._cursor = self._connection.cursor()

    def _disconnect(self):
        """Отключение от БД"""
        if self._connection:
            self._connection.commit()
            self.cursor.close()
            self._connection.close()

    def _check_db(self):
        """Проверка существования БД"""
        try:
            self._connect()
            self._disconnect()

        except (Exception, psycopg2.Error) as error:
            self._create_db()
            self._create_table()

        finally:
            self._check_table()

    def _check_table(self):
        """Проверяем существование таблиц"""
        self._connect()

        tables = ['employers', 'vacancies']
        response = []
        for name in tables:
            try:
                self._cursor.execute(f"SELECT EXISTS ("
                                     f"SELECT 1 "
                                     f"FROM information_schema.tables "
                                     f"WHERE table_name = '{name}')")

                response.append(self._cursor.fetchone()[0])

            except psycopg2.Error:
                pass

        if len(response) < 2:
            self._disconnect()
            self._create_table()
        else:
            pass

    def _create_db(self):
        """Создание БД"""
        db_name = self._db_name
        self._db_name = 'postgres'
        self._connect()
        self._connection.autocommit = True
        self._cursor.execute(f"CREATE DATABASE {db_name};")

        self._connection.autocommit = False
        self._disconnect()
        self._db_name = db_name

    def _create_table(self):
        """Создание таблиц в БД"""
        self._connect()
        self._cursor.execute("DROP TABLE IF EXISTS  vacancies, employers;")
        self._cursor.execute(f"CREATE TABLE employers" \
                             f"(employer_id int unique," \
                             f"company_name varchar not null," \
                             f"hh_url varchar not null," \
                             f"company_url varchar," \
                             f"description text);" \
                            
                             f"CREATE TABLE vacancies" \
                             f"(vacancy_id int unique," \
                             f"employer_id int references employers(employer_id) not null," \
                             f"vacancy_name varchar," \
                             f"requirement varchar," \
                             f"responsibility varchar," \
                             f"salary_from real," \
                             f"salary_to real," \
                             f"salary_currency varchar," \
                             f"url varchar)")
        self._disconnect()

    def __enter__(self):
        self._check_db()
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._disconnect()
