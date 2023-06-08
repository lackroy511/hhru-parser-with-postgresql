from utils.utils import create_pbar
from utils.utils import json_reader
from utils.utils import config_parser
from utils.utils import print_rows
from utils.utils import print_rows_with_counter
from utils.user_interaction import print_main_menu
from utils.user_interaction import try_execute_sql_script
from utils.user_interaction import try_fill_employers_and_vacancies_table
from utils.user_interaction import choosing_whether_to_create_db


from db_classes.DBManagerHhRu import DBManagerHhRu

from os.path import join

import psycopg2
import psycopg2.errors


def main():

    path_to_sql_script = join('create_db.sql')
    path_to_employers_ids = join('data', 'employers_ids.json')
    db_name = 'hh_ru'
    params = config_parser()  # <-В аргументы ввести путь до .ini файла с параметрами для подключения к БД и select.

    choosing_whether_to_create_db(params, db_name)

    # Цикл меню, где можно проверить работу кода в проекте.
    # Навигация путем ввода цифр, соответствующих пунктам меню.
    conn = psycopg2.connect(dbname=db_name, **params)
    conn.autocommit = True
    with conn.cursor() as cur:
        while True:

            print_main_menu()
            user_input = input('Номер действия: ')

            # Создать таблицы "employers" и "vacancies" в БД "hh_ru"'
            if user_input == "1":
                try_execute_sql_script(cur, path_to_sql_script)

            elif user_input == "2":
                employers_ids = json_reader(path_to_employers_ids)['employers_ids']
                pbar = create_pbar(employers_ids)
                try_fill_employers_and_vacancies_table(cur, pbar)

            elif user_input == "3":
                rows = DBManagerHhRu.get_companies_and_vacancies_count(cur)
                print_rows(rows)

            elif user_input == "4":
                rows = DBManagerHhRu.get_all_vacancies(cur)
                print_rows_with_counter(rows)

            elif user_input == "5":
                rows = DBManagerHhRu.get_avg_salary(cur)
                print_rows(rows)

            elif user_input == "6":
                rows = DBManagerHhRu.get_vacancies_with_higher_salary(cur)
                print_rows(rows)

            elif user_input == "7":
                word_for_search = input(
                    'Введите слово для поиска вакансий в базе данных, название которых, его включает: ')
                rows = DBManagerHhRu.get_vacancies_with_keyword(cur, word_for_search)
                print_rows(rows)

            elif user_input == "0":
                break

            else:
                input('Нет такого действия! Нажмите Enter, что бы попробовать еще раз: ')
    conn.close()


if __name__ == '__main__':
    main()
