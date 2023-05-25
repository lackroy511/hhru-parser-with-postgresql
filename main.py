from utils.utils import create_database
from utils.utils import json_reader
from utils.utils import config_parser
from utils.utils import execute_sql_script
from utils.utils import db_hh_ru_fill_employers_table
from utils.utils import db_hh_ru_fill_vacancies_table
from head_hunter_api.head_hunter_api import HeadHunterAPI
from DBManager.DBManager import DBManagerHhRu

from os.path import join

from tqdm import tqdm
import psycopg2
import psycopg2.errors


def main():

    path_to_sql_script = join('create_db.sql')  # Путь до sql скрипта для создания таблиц.
    path_to_employers_ids = join('data', 'employers_ids.json')  # Путь до файла с айди компаний.
    db_name = 'hh_ru'  # Имя БД которая  будет создана.
    params = config_parser()  # <-В аргументы ввести путь до .ini файла с параметрами для подключения к БД и select.

    # Выбор, создать БД или не делать ничего.
    print('\n\n\n\n')
    print('1. Создать(удалить и пересоздать, если существует) БД hh_ru.')
    print('"Enter" ничего не делать и продолжить.\n')
    user_input = input("Ваш выбор: ")
    if user_input == '1':
        create_database(params, db_name)

    # Цикл меню, где можно проверить работу кода в проекте.
    # Навигация путем ввода цифр, соответствующих пунктам меню.
    conn = psycopg2.connect(dbname=db_name, **params)
    conn.autocommit = True
    with conn.cursor() as cur:
        while True:
            print('\n\n\n')
            print('1. Создать таблицы "employers" и "vacancies" в БД "hh_ru"')
            print('2. Заполнить таблицы данными работодателей, id которых хранятся в data/employers_ids.json')
            print('3. Потестить метод DBManagerHhRu "get_companies_and_vacancies_count()"')
            print('4. Потестить метод DBManagerHhRu "get_all_vacancies()"')
            print('5. Потестить метод DBManagerHhRu "get_avg_salary()"')
            print('6. Потестить метод DBManagerHhRu "get_vacancies_with_higher_salary()"')
            print('7. Ввести слово и потестить метод DBManagerHhRu "get_vacancies_with_keyword()"')
            print('0. Выкл.')
            print()
            user_input = input('Номер действия: ')

            # Создать таблицы "employers" и "vacancies" в БД "hh_ru"'
            if user_input == "1":
                try:
                    execute_sql_script(cur, path_to_sql_script)
                except psycopg2.errors.DependentObjectsStillExist:
                    input('Таблицы уже существуют! Нажмите Enter:')

            # Заполнить таблицы "employers" и "vacancies" данными.
            elif user_input == "2":
                employers_ids = json_reader(path_to_employers_ids)['employers_ids']

                pbar = tqdm(employers_ids,
                            leave=True,
                            ncols=60,
                            colour='#747671',
                            bar_format='Заполнение таблиц:|{bar}|Emp.count|{n_fmt}/{total_fmt}'
                            )
                try:
                    for employer_id in pbar:
                        hh_ru_api = HeadHunterAPI(employer_id)

                        employer_data = hh_ru_api.get_employer_data()
                        employer_data_of_vacancies = hh_ru_api.get_vacancies_data_of_employer()

                        db_hh_ru_fill_employers_table(cur, employer_data)
                        db_hh_ru_fill_vacancies_table(cur, employer_data_of_vacancies)

                    input("\nТаблицы успешно заполнены, нажмите Enter: ")
                except psycopg2.errors.UniqueViolation:
                    print()
                    input('Данные уже есть в таблицах. Вернуться в меню - "Enter": ')
                except psycopg2.errors.UndefinedTable:
                    print()
                    input('Таблицы не созданы. Вернуться в меню - "Enter": ')

            # Вывод результата, который возвращает метод get_companies_and_vacancies_count() класса DBManagerHhRu
            elif user_input == "3":
                rows = DBManagerHhRu.get_companies_and_vacancies_count(cur)
                for row in rows:
                    print(row)
                input('\nВернуться в меню - "Enter": ')

            # Вывод результата, который возвращает get_all_vacancies() класса DBManagerHhRu
            elif user_input == "4":
                rows = DBManagerHhRu.get_all_vacancies(cur)
                counter = 1
                for row in rows:
                    print(f'№{counter} + {row}')
                    counter += 1
                input('\nВернуться в меню - "Enter": ')

            # Вывод результата, который возвращает get_avg_salary() класса DBManagerHhRu
            elif user_input == "5":
                rows = DBManagerHhRu.get_avg_salary(cur)
                for row in rows:
                    print(round(row[0], 3))
                input('\nВернуться в меню - "Enter": ')

            # Вывод результата, который возвращает get_vacancies_with_higher_salary() класса DBManagerHhRu
            elif user_input == "6":
                rows = DBManagerHhRu.get_vacancies_with_higher_salary(cur)
                for row in rows:
                    print(row)
                input('\nВернуться в меню - "Enter": ')

            # Вывод результата, который возвращает get_vacancies_with_keyword() класса DBManagerHhRu
            elif user_input == "7":
                word_for_search = input(
                    'Введите слово для поиска вакансий в базе данных, название которых, его включает: '
                )
                rows = DBManagerHhRu.get_vacancies_with_keyword(cur, word_for_search)
                for row in rows:
                    print(row)
                input('\nВернуться в меню - "Enter": ')

            # Выход из программы
            elif user_input == "0":
                break

            else:
                input('Нет такого действия! Нажмите Enter, что бы попробовать еще раз: ')
    conn.close()


if __name__ == '__main__':
    main()
