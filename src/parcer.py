import requests


# класс для парсинга сайта hh.ru
class HHParser:
    def __init__(self, keyword=None):
        self.base_url = 'https://api.hh.ru/vacancies'
        self.keyword = keyword

    # получает информацию с сайта через API
    def get_info(self):
        companies = [
            "Яндекс",
            "Mail.ru Group",
            "Сбер",
            "Google",
            "Ярославль-Электроавтоматика",
            "Wildberries",
            "Роснефть",
            "EPAM Systems",
            "Kaspersky Lab",
            "Avito"
        ]
        for company in companies:
            print(f"Вакансии от компании {company}:\n")
            vacancies = self.get_vacancies(company)

            if vacancies:
                for vacancy in vacancies:
                    print(f"Название: {vacancy['name']}")
                    print(f"Зарплата: {vacancy.get('salary', 'Не указана')}")
                    print(f"Регион: {vacancy.get('area', {}).get('name', 'Не указан')}")
                    print(f"Описание: {vacancy.get('description', 'Отсутствует')}")
                    print(f"Ссылка: {vacancy['url']}\n")

            else:
                print("Нет доступных вакансий от этой компании.\n")

    def get_vacancies(self, company_name):
        params = {
            "text": f'компания:"{company_name}"',  # Поиск вакансий по названию компании
            "per_page": 10  # Количество вакансий для отображения
        }

        response = requests.get(self.base_url, params=params)

        if response.status_code == 200:
            vacancies = response.json()
            return vacancies
        else:
            print(f"Не удалось получить данные о вакансиях от компании {company_name}.")
            return []
