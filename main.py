from hh_parser import get_data_from_hh
from utils import create_tables, save_data_to_db
from db_manager import DBManager


def main():
    print("Привет! Это программа для работы с вакансиями HH.ru")
    # Начало работы программы, здесь мы вызываем создание таблиц
    # 1. Создание таблиц
    print("1. Создаем таблицы в БД...")
    create_tables()

    # 2. Получение данных и заполнение БД
    user_input = input("Хотите загрузить свежие данные с HH.ru? (да/нет): ").lower()
    if user_input in ['да', 'yes', 'y']:
        print("Загружаем данные, подождите...")
        data = get_data_from_hh()
        save_data_to_db(data)

    # 3. Работа с DBManager
    db_manager = DBManager()

    while True:
        print("\nВыберите действие:")
        print("1 - Список всех компаний и количество вакансий")
        print("2 - Список всех вакансий")
        print("3 - Средняя зарплата")
        print("4 - Вакансии с зарплатой выше средней")
        print("5 - Поиск вакансий по ключевому слову")
        print("0 - Выход")

        choice = input("Ваш выбор: ")

        if choice == '1':
            companies = db_manager.get_companies_and_vacancies_count()
            for company in companies:
                print(f"{company[0]}: {company[1]} вакансий")

        elif choice == '2':
            vacancies = db_manager.get_all_vacancies()
            for vac in vacancies:
                print(f"Компания: {vac[0]} | Вакансия: {vac[1]} | ЗП: {vac[2]} | Ссылка: {vac[3]}")

        elif choice == '3':
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата: {avg_salary} руб.")

        elif choice == '4':
            vacancies = db_manager.get_vacancies_with_higher_salary()
            for vac in vacancies:
                print(f"Вакансия: {vac[2]} | ЗП: {vac[3]}")

        elif choice == '5':
            keyword = input("Введите слово для поиска: ")
            vacancies = db_manager.get_vacancies_with_keyword(keyword)
            for vac in vacancies:
                print(f"Найдено: {vac[2]} | ЗП: {vac[3]}")

        elif choice == '0':
            print("До свидания!")
            break
        else:
            print("Неверный ввод, попробуйте еще раз.")


if __name__ == '__main__':
    main()