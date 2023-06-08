from abc import ABC, abstractmethod


class BaseClassForAPI(ABC):
    """Базовый класс для API сайтов с вакансиями"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_employer_data(self):
        pass

    @abstractmethod
    def get_vacancies_data_of_employer(self):
        pass
