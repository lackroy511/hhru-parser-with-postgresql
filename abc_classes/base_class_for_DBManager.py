from abc import ABC, abstractmethod

import psycopg2


class BaseClassForDBManager(ABC):
    """Абстрактный класс db_classes"""

    @abstractmethod
    def get_companies_and_vacancies_count(self, cur: psycopg2) -> list[(), ()]:
        pass

    @abstractmethod
    def get_all_vacancies(self, cur: psycopg2) -> list[(), ()]:
        pass

    @abstractmethod
    def get_avg_salary(self, cur: psycopg2) -> list[(), ()]:
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self, cur: psycopg2) -> list[(), ()]:
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, cur: psycopg2, word_for_search: str) -> list[(), ()]:
        pass
