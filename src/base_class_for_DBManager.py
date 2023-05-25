from abc import ABC, abstractmethod


class BaseClassForDBManager(ABC):
    """Абстрактный класс DBManager"""

    @abstractmethod
    def get_companies_and_vacancies_count(self, cur):
        pass

    @abstractmethod
    def get_all_vacancies(self, cur):
        pass

    @abstractmethod
    def get_avg_salary(self, cur):
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self, cur):
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, cur, word_for_search):
        pass
