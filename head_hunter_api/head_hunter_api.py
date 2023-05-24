from src.base_class_for_api import BaseClassForAPI

import requests


class HeadHunterAPI(BaseClassForAPI):
    """Класс для работы с API Head Hunter"""

    def __init__(self, employer_id: str) -> None:
        """
        Конструктор класса
        :param employer_id: id работодателя на ресурсе hh.ru.
        """
        self.url_for_employer = 'https://api.hh.ru/employers/'

        self.employer_id = employer_id
        self.employer_info = self.get_employer_data()

        self.url_for_employer_vacancies = self.employer_info['vacancies_url']

    def get_employer_data(self) -> dict:
        """
        Получает информацию о работодателе
        :return: Словарь с данными о работодателе
        """
        url = f'{self.url_for_employer}{self.employer_id}'

        response = requests.get(url)
        employer_data = response.json()

        return employer_data

    def get_vacancies_data_of_employer(self) -> dict:
        """
        Получает информацию о вакансиях работодателя
        :return: Словарь информацией о вакансиях работодателя
        """

        params = {
            'employer_id': self.employer_id,
            'per_page': 100,
            'page': 0
        }
        vacancies_data = {'items': []}

        while True:
            response = requests.get(self.url_for_employer_vacancies, params=params)
            data = response.json()

            vacancies_data['items'].extend(data['items'])

            params['page'] += 1
            if data['pages'] - 1 == data['page']:
                break

        vacancies_data['number of vacancies'] = data['found']

        return vacancies_data



