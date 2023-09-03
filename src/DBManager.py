import psycopg2
from src.parcer import HHParser
from tabulate import tabulate


class DBManager:
    def go_to_db(self):
        conn = psycopg2.connect(
            database="DBManager",
            user="postgres",
            password="sygm6DK?",
            host="localhost"
        )
        cur = conn.cursor()
        vacancies = HHParser()
        vacancies_data = vacancies.get_info()

        for vacancy_data in vacancies_data:
            employer_data = vacancy_data.get("employer", {})
            employer_id = None

            if employer_data:
                employer_id = self.get_or_update_employer(
                    cur,
                    employer_data.get("name", "Unknown Employer"),
                    employer_data.get("description", ""),
                    employer_data.get("industries", []),
                    employer_data.get("area", {}).get("name", "Unknown City")
                )

            vacancy_title = vacancy_data.get("name", "Unknown Title")
            salary_info = vacancy_data.get("salary", {})

            # Проверяем наличие данных о зарплате и их корректность
            salary = None
            if salary_info and "from" in salary_info and isinstance(salary_info["from"], (int, float)):
                salary = int(salary_info["from"])

            region = vacancy_data.get("area", {}).get("name", "Region Not Specified")
            description = vacancy_data.get("description", "")
            url = vacancy_data.get("url")

            cur.execute(
                "INSERT INTO vacancies (title, salary, region, description, url, employer_id) VALUES (%s, %s, %s, %s, %s, %s)",
                (vacancy_title, salary, region, description, url, employer_id)
            )

        conn.commit()
        cur.close()
        conn.close()

    def get_or_update_employer(self, cur, employer_name, description, industry, city):
        cur.execute(
            "SELECT id FROM employers WHERE name = %s",
            (employer_name,)
        )
        existing_id = cur.fetchone()
        if existing_id:
            # Работодатель с таким именем уже существует, можно выполнить операцию UPDATE
            employer_id = existing_id[0]
            cur.execute(
                "UPDATE employers SET description = %s, industry = %s, city = %s WHERE id = %s",
                (description, ", ".join(industry), city, employer_id)
            )
            return employer_id
        else:
            cur.execute(
                "INSERT INTO employers (name, description, industry, city) VALUES (%s, %s, %s, %s) RETURNING id",
                (employer_name, description, ", ".join(industry), city)
            )
            return cur.fetchone()[0]

    def add_employer(self, cur, employer_name, description, industry, city):
        cur.execute(
            "SELECT id FROM employers WHERE name = %s",
            (employer_name,)
        )
        existing_id = cur.fetchone()
        if existing_id:
            # Работодатель с таким именем уже существует
            return existing_id[0]
        else:
            cur.execute(
                "INSERT INTO employers (name, description, industry, city) VALUES (%s, %s, %s, %s) RETURNING id",
                (employer_name, description, ", ".join(industry), city)
            )
            return cur.fetchone()[0]

    def get_companies_and_vacancies_count(self):
        conn = psycopg2.connect(
            database="DBManager",
            user="postgres",
            password="sygm6DK?",
            host="localhost"
        )
        cur = conn.cursor()
        cur.execute("""
                SELECT e.name, COUNT(v.id) AS vacancy_count
                FROM employers AS e
                LEFT JOIN vacancies AS v ON e.id = v.employer_id
                GROUP BY e.name
            """)
        return cur.fetchall()

    def get_all_vacancies(self):
        conn = psycopg2.connect(
            database="DBManager",
            user="postgres",
            password="sygm6DK?",
            host="localhost"
        )
        cur = conn.cursor()
        cur.execute("""
                SELECT e.name AS employer_name, v.title AS vacancy_title, v.salary, v.url
                FROM employers AS e
                INNER JOIN vacancies AS v ON e.id = v.employer_id
            """)
        return cur.fetchall()

    def get_avg_salary(self):
        conn = psycopg2.connect(
            database="DBManager",
            user="postgres",
            password="sygm6DK?",
            host="localhost"
        )
        cur = conn.cursor()

        cur.execute("""
            SELECT salary
            FROM vacancies
        """)

        total_salary = 0
        count = 0

        for row in cur.fetchall():
            salary = row[0]
            if salary and salary != "Salary Not Specified" and salary != "[null]":
                try:
                    salary_value = float(salary)
                    total_salary += salary_value
                    count += 1
                except ValueError:
                    pass

        if count > 0:
            average_salary = total_salary / count
            return average_salary
        else:
            return "No valid salary data available"

    def get_vacancies_with_higher_salary(self):
        conn = psycopg2.connect(
            database="DBManager",
            user="postgres",
            password="sygm6DK?",
            host="localhost"
        )
        cur = conn.cursor()

        # Получаем среднюю зарплату
        avg_salary = self.get_avg_salary()

        # Выбираем все вакансии
        cur.execute("""
            SELECT e.name AS employer_name, v.title AS vacancy_title, v.salary, v.url
            FROM employers AS e
            INNER JOIN vacancies AS v ON e.id = v.employer_id
        """)

        valid_salary_vacancies = []

        for row in cur.fetchall():
            employer_name, vacancy_title, salary, url = row
            # Преобразуем зарплату в числовой формат, игнорируя "Salary Not Specified" и [null]
            try:
                if salary and salary != "Salary Not Specified" and salary != "[null]":
                    salary = float(salary)
                else:
                    continue
            except ValueError:
                continue

            # Сравниваем зарплату с средней
            if salary > avg_salary:
                valid_salary_vacancies.append((employer_name, vacancy_title, salary, url))

        if valid_salary_vacancies:
            return valid_salary_vacancies
        else:
            return "Нет вакансий с зарплатой выше средней."

    def get_vacancies_with_keyword(self, keyword):
        conn = psycopg2.connect(
            database="DBManager",
            user="postgres",
            password="sygm6DK?",
            host="localhost"
        )
        cur = conn.cursor()
        cur.execute("""
               SELECT e.name AS employer_name, v.title AS vacancy_title, v.salary, v.url
               FROM employers AS e
               INNER JOIN vacancies AS v ON e.id = v.employer_id
               WHERE v.title ILIKE %s
           """, ('%' + keyword + '%',))
        return cur.fetchall()
