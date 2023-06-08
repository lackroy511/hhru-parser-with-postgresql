from head_hunter_api.head_hunter_api import HeadHunterAPI
from utils.utils import execute_sql_script, create_database
from db_classes.DBFiller import DBFiller


import psycopg2
import psycopg2.errors
from tqdm import tqdm


def choosing_whether_to_create_db(params: dict, db_name: str) -> None:
    """
    Создает базу данных hh_ru.
    :param db_name: Название базы данных.
    :param params: Словарь с параметрами для подключения к БД.
    """

    print('\n\n\n\n')
    print('1. Создать(удалить и пересоздать, если существует) БД hh_ru.')
    print('"Enter" ничего не делать и продолжить.\n')
    user_input = input("Ваш выбор: ")
    if user_input == '1':
        create_database(params, db_name)
        input('\nБаза данных успешно создана, нажмите "Enter": ')


def print_main_menu() -> None:
    """
    Вывести в консоль главное меню.
    """
    print('\n\n\n')
    print('1. Создать таблицы "employers" и "vacancies" в БД "hh_ru"')
    print('2. Заполнить таблицы данными работодателей, id которых хранятся в data/employers_ids.json')
    print('3. Потестить метод db_classes "get_companies_and_vacancies_count()"')
    print('4. Потестить метод db_classes "get_all_vacancies()"')
    print('5. Потестить метод db_classes "get_avg_salary()"')
    print('6. Потестить метод db_classes "get_vacancies_with_higher_salary()"')
    print('7. Ввести слово и потестить метод db_classes "get_vacancies_with_keyword()"')
    print('0. Выкл.')
    print()


def try_execute_sql_script(cur: psycopg2, path_to_sql_script: str) -> None:
    """
    Выполняет скрипт из sql файла.
    :param cur: Курсор модуля psycopg2.
    :param path_to_sql_script: Путь до sql файла со скриптом.
    """
    try:
        execute_sql_script(cur, path_to_sql_script)
        input('\nТаблицы успешно созданы, нажмите "Enter": ')
    except psycopg2.errors.DependentObjectsStillExist:
        input('Таблицы уже существуют! Нажмите Enter:')


def try_fill_employers_and_vacancies_table(cur: psycopg2, pbar: tqdm) -> None:
    """
    Заполняет таблицу Employers и Vacancies данными, которые были получены с hh.ru
    :param cur: Курсор psycopg2
    :param pbar: Объект tqdm,
    :return:
    """
    try:
        for employer_id in pbar:
            hh_ru_api = HeadHunterAPI(employer_id)

            employer_data = hh_ru_api.get_employer_data()
            employer_data_of_vacancies = hh_ru_api.get_vacancies_data_of_employer()

            DBFiller.fill_employers_table(cur, employer_data)
            DBFiller.fill_vacancies_table(cur, employer_data_of_vacancies)

        input('\nТаблицы успешно заполнены, нажмите "Enter": ')
    except psycopg2.errors.UniqueViolation:
        print()
        input('Данные уже есть в таблицах. Вернуться в меню - "Enter": ')
    except psycopg2.errors.UndefinedTable:
        print()
        input('Таблицы не созданы. Вернуться в меню - "Enter": ')

