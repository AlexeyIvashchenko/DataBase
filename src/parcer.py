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

        vacancies = []

        for company in companies:
            company_id = self.get_company_id(company)
            if company_id:
                vacancies.extend(self.get_vacancies(company_id))
        return vacancies

    def get_company_id(self, company_name):
        params = {
            "text": f'компания:"{company_name}"',
            "per_page": 1
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            vacancies = response.json()
            if vacancies and 'items' in vacancies and vacancies['items']:
                return vacancies['items'][0]['employer']['id']
            else:
                return None
        return None

    def get_vacancies(self, company_id):
        params = {
            "employer_id": company_id,
            "per_page": 10
        }

        response = requests.get(self.base_url, params=params)

        if response.status_code == 200:
            vacancies = response.json().get('items', [])
            formatted_vacancies = []

            for vacancy in vacancies:
                title = vacancy.get('name', 'Unknown Title')
                description = vacancy.get('description', '')
                region = vacancy.get('area', {}).get('name', 'Region Not Specified')
                url = vacancy.get('url')

                salary_info = vacancy.get('salary', {})
                salary_from = salary_info.get('from')
                salary_to = salary_info.get('to')

                # Проверяем данные о зарплате и преобразуем их в числовой формат
                if isinstance(salary_from, (int, float)) and isinstance(salary_to, (int, float)):
                    # Если оба значения доступны, берем среднее
                    salary = (salary_from + salary_to) / 2
                elif isinstance(salary_from, (int, float)):
                    # Если есть только одно значение
                    salary = salary_from
                elif isinstance(salary_to, (int, float)):
                    # Если есть только одно значение
                    salary = salary_to
                else:
                    # Если данных о зарплате нет или они некорректны
                    salary = None

                formatted_vacancies.append({
                    'title': title,
                    'description': description,
                    'region': region,
                    'url': url,
                    'salary': salary
                })

            return formatted_vacancies
        else:
            return []
