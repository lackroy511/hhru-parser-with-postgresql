from src.base_class_for_DBManager import BaseClassForDBManager
from utils.utils import config_parser

import psycopg2


class DBManagerHhRu(BaseClassForDBManager):

    dbname = 'hh_ru'
    params = config_parser()

    @classmethod
    def get_companies_and_vacancies_count(cls) -> list[(), ()]:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        :return:
        """
        conn = psycopg2.connect(dbname=cls.dbname, **cls.params)
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute("""select employer_name, count(*) as open_vacancies
                           from employers
                           inner join vacancies using(employer_id)
                           group by employer_name;""")
            resulting_data = cur.fetchall()
        conn.close()
        return resulting_data

    @classmethod
    def get_all_vacancies(cls) -> list[(), ()]:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        :return:
        """
        conn = psycopg2.connect(dbname=cls.dbname, **cls.params)
        conn.autocommit = True

        with conn.cursor() as cur:

            cur.execute("""select employer_name, vacancy_name, vacancy_salary, vacancy_url
                           from employers
                           inner join vacancies using(employer_id);""")
            resulting_data = cur.fetchall()
        conn.close()
        return resulting_data

    @classmethod
    def get_avg_salary(cls) -> list[(), ()]:
        """
        Получает среднюю зарплату по вакансиям.
        :return:
        """
        conn = psycopg2.connect(dbname=cls.dbname, **cls.params)
        conn.autocommit = True

        with conn.cursor() as cur:

            cur.execute("""select avg(vacancy_salary) as avg_salary
                           from vacancies;""")
            resulting_data = cur.fetchall()
        conn.close()
        return resulting_data

    @classmethod
    def get_vacancies_with_higher_salary(cls) -> list[(), ()]:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return:
        """
        conn = psycopg2.connect(dbname=cls.dbname, **cls.params)
        conn.autocommit = True

        with conn.cursor() as cur:

            cur.execute("""select *
                           from vacancies
                           where vacancy_salary > (select avg(vacancy_salary)
                                                   from vacancies);""")
            resulting_data = cur.fetchall()
        conn.close()
        return resulting_data

    @classmethod
    def get_vacancies_with_keyword(cls, word_for_search='') -> list[(), ()]:
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
        :param word_for_search: Слово по которому будут найдены вакансии.
        :return:
        """
        conn = psycopg2.connect(dbname=cls.dbname, **cls.params)
        conn.autocommit = True

        with conn.cursor() as cur:

            cur.execute(f"""select *
                            from vacancies
                            where vacancy_name LIKE '%{word_for_search}%';""")
            resulting_data = cur.fetchall()
        conn.close()
        return resulting_data
