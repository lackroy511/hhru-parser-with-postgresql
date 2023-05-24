from utils.utils import create_database
from utils.utils import config_parser
from utils.utils import execute_sql_script
from utils.utils import db_hh_ru_fill_employers_table
from utils.utils import db_hh_ru_fill_vacancies_table
from head_hunter_api.head_hunter_api import HeadHunterAPI

import psycopg2

params = config_parser()

create_database(params)
execute_sql_script(params)

