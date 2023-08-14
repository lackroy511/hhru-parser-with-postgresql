import psycopg2

from abc_classes.base_class_for_DBManager import BaseClassForDBManager


class DBManagerHhRu(BaseClassForDBManager):

    @classmethod
    def get_companies_and_vacancies_count(cls, cur: psycopg2) -> list:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        :param cur: Курсор, объект psycopg2.
        :return:
        """

        cur.execute("""select employer_name, count(*) as open_vacancies
                       from employers
                       inner join vacancies using(employer_id)
                       group by employer_name;""")
        resulting_data = cur.fetchall()

        return resulting_data

    @classmethod
    def get_all_vacancies(cls, cur: psycopg2) -> list:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        :param cur: Курсор, объект psycopg2.
        :return:
        """
        cur.execute("""select employer_name, vacancy_name, vacancy_salary, vacancy_url
                       from employers
                       inner join vacancies using(employer_id);""")
        resulting_data = cur.fetchall()

        return resulting_data

    @classmethod
    def get_avg_salary(cls, cur: psycopg2) -> list:
        """
        Получает среднюю зарплату по вакансиям.
        :param cur: Курсор, объект psycopg2.
        :return:
        """
        cur.execute("""select avg(vacancy_salary) as avg_salary
                       from vacancies;""")
        resulting_data = cur.fetchall()

        return resulting_data

    @classmethod
    def get_vacancies_with_higher_salary(cls, cur: psycopg2) -> list:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :param cur: Курсор, объект psycopg2.
        :return:
        """
        cur.execute("""select *
                       from vacancies
                       where vacancy_salary > (select avg(vacancy_salary)
                                               from vacancies);""")
        resulting_data = cur.fetchall()

        return resulting_data

    @classmethod
    def get_vacancies_with_keyword(cls, cur: psycopg2, word_for_search='') -> list:
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
        :param cur: Курсор, объект psycopg2.
        :param word_for_search: Слово по которому будут найдены вакансии.
        :return:
        """
        cur.execute(f"""select *
                        from vacancies
                        where vacancy_name
                        LIKE '%{word_for_search.lower()}%' or vacancy_name LIKE '%{word_for_search.title()}%';""")
        resulting_data = cur.fetchall()

        return resulting_data
