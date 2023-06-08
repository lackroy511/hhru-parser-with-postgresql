from configparser import ConfigParser
import json

import psycopg2
from tqdm import tqdm


def config_parser(filename: str = 'database.ini', section: str = "postgresql") -> dict:
    """
    Читает .ini файл с параметрами для подключения к БД.
    :param filename: Имя файла / путь до файла.
    :param section: Выбор параметров.
    :return: Словарь с параметрами для подключения к БД.
    """
    parser = ConfigParser()
    parser.read(filename)
    db = {}

    if parser.has_section(section):
        params = parser.items(section)

        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db


def create_database(params: dict, db_name: str) -> None:
    """
    Создает базу данных hh_ru.
    :param db_name: Название базы данных.
    :param params: Словарь с параметрами для подключения к БД.
    """
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True

    with conn.cursor() as cur:
        cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cur.execute(f"CREATE DATABASE {db_name}")
    conn.close()


def json_reader(path_to_file: str) -> dict:
    """
    Читает данные из json файла.
    :param path_to_file: Путь до файла.
    :return: Cловарь python.
    """
    with open(path_to_file, 'r') as file:
        data = json.load(file)
    return data


def execute_sql_script(cur: psycopg2, path_to_sql_script: str) -> None:
    """
    Выполняет скрипт из sql файла.
    :param cur: Курсор модуля psycopg2.
    :param path_to_sql_script: Путь до sql файла со скриптом.
    """
    with open(path_to_sql_script, 'r') as file:
        sql_script = file.read()
    cur.execute(sql_script)


def create_pbar(iterable: list or any) -> tqdm:
    """
    Для красоты и наглядности создает в консоли шкалу загрузки данных и заполнения таблиц.
    :param iterable: Любой итерируемый объект.
    :return: Объект pbar.
    """
    pbar = tqdm(iterable,
                leave=True,
                ncols=60,
                colour='#747671',
                bar_format='Заполнение таблиц:|{bar}|Emp.count|{n_fmt}/{total_fmt}'
                )

    return pbar


def print_rows(rows) -> None:
    """
    Печатает в консоль дынные из SQL таблицы.
    :param rows: Данные из SQL таблицы
    """
    for row in rows:
        print(row)
    input('\nВернуться в меню - "Enter": ')


def print_rows_with_counter(rows) -> None:
    """
    Печатает в консоль дынные из SQL таблицы.
    :param rows: Данные из SQL таблицы
    """
    counter = 1
    for row in rows:
        print(f'№{counter} {row}')
        counter += 1
    input('\nВернуться в меню - "Enter": ')
