import psycopg2


class DBFiller:

    @classmethod
    def fill_employers_table(cls, cur: psycopg2, employers_data: dict) -> None:
        """
        Заполняет таблицу employers данными.
        :param cur: Курсор модуля psycopg2.
        :param employers_data: Данные, которыми будет заполнена таблица.
        """

        cur.execute("""
        INSERT INTO employers (employer_id, 
                               employer_name, 
                               employer_industry, 
                               employer_city, 
                               employer_url, 
                               employer_open_vacancies) 
        VALUES (%s, %s, %s, %s, %s, %s) """, (
            employers_data['id'],
            employers_data['name'],
            employers_data['industries'][0]['name'],
            employers_data['area']['name'],
            employers_data['site_url'],
            employers_data['open_vacancies'])
                    )

    @classmethod
    def fill_vacancies_table(cls, cur: psycopg2, vacancy_data: dict) -> None:
        """
        Заполняет таблицу vacancies данными.
        :param cur: Курсор модуля psycopg2.
        :param vacancy_data: Данные, которыми будет заполнена таблица.
        """

        vacancies = vacancy_data['items']

        for vacancy in vacancies:
            # Приведение зарплаты "от" и "до" к одному значению.
            vacancy_salary = cls.__get_salary(vacancy)

            cur.execute("""
            INSERT INTO vacancies (vacancy_id, 
                                   vacancy_name,
                                   vacancy_city,
                                   vacancy_url,
                                   vacancy_salary,
                                   published_at,
                                   employer_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""", (
                vacancy['id'],
                vacancy['name'],
                vacancy['area']['name'],
                vacancy['alternate_url'],
                vacancy_salary,
                vacancy['published_at'],
                vacancy['employer']['id'])
                        )

    @classmethod
    def __get_salary(cls, vacancy: dict) -> str or None:
        """
        Приводит зарплату из значений "От" и "До" к одному значению.
        :param vacancy: Данные вакансии.
        :return: Значение зарплаты.
        """
        vacancy_salary = None
        if vacancy['salary']:
            if vacancy['salary']["from"] and vacancy['salary']["to"]:
                vacancy_salary = (vacancy['salary']["from"] + vacancy['salary']["to"]) / 2

            elif vacancy['salary']["from"] is not None:
                vacancy_salary = vacancy['salary']["from"]

            elif vacancy['salary']["to"] is not None:
                vacancy_salary = vacancy['salary']["to"]
        return vacancy_salary
