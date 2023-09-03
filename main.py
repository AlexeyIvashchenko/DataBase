from src.DBManager import DBManager
from tabulate import tabulate
if __name__ == "__main__":
    manage = DBManager()

    print("Здравствуйте! Что бы вы хотели сделать?")
    print("1. Получить список всех компаний и количество вакансий у каждой компании")
    print("2. Получить список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию")
    print("3. Получить среднюю зарплату по вакансиям")
    print("4. Получить список всех вакансий, у которых зарплата выше средней")
    print("5. Получить вакансии по ключевому слову")

    choice = input("Введите номер выбранной опции: ")

    if choice == "1":
        companies_and_vacancies = manage.get_companies_and_vacancies_count()
        print(tabulate(companies_and_vacancies, headers=["Company Name", "Vacancy Count"]))
    elif choice == "2":
        all_vacancies = manage.get_all_vacancies()
        print(tabulate(all_vacancies, headers=["Company Name", "Vacancy Title", "Salary", "Vacancy URL"]))
    elif choice == "3":
        avg_salary = manage.get_avg_salary()
        print(f"Средняя зарплата по вакансиям: {avg_salary}")
    elif choice == "4":
        high_salary_vacancies = manage.get_vacancies_with_higher_salary()
        if high_salary_vacancies:
            print(tabulate(high_salary_vacancies, headers=["Company Name", "Vacancy Title", "Salary", "Vacancy URL"]))
        else:
            print("Нет вакансий с зарплатой выше средней.")
    elif choice == "5":
        keyword = input("Введите ключевое слово для поиска вакансий: ")
        vacancies_by_keyword = manage.get_vacancies_with_keyword(keyword)
        if vacancies_by_keyword:
            print(tabulate(vacancies_by_keyword, headers=["Company Name", "Vacancy Title", "Salary", "Vacancy URL"]))
        else:
            print(f"Нет вакансий с ключевым словом '{keyword}'.")
    else:
        print("Некорректный выбор. Пожалуйста, выберите существующий вариант (1-5).")
