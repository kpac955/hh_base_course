from config import config
from db_manager import DBManager
from hh_parser import get_data_from_hh
from utils import create_database, save_data_to_db


def init_db(db_name, params):
    """Инициализация базы данных и создание таблиц."""
    print(f"Инициализация базы данных {db_name}...")
    create_database(db_name, params)


def load_data(db_name, params):
    """Сбор данных через API и сохранение в БД."""
    print("Начинаю сбор данных с HeadHunter...")

    # Список ID компаний
    employer_ids = [
        '1740',  # Яндекс
        '3529',  # Сбер
        '7863',  # Тинькофф
        '2748',  # Ростелеком
        '3776',  # МТС
        '3127',  # МегаФон
        '15478',  # VK
        '80',  # Альфа-Банк
        '2180',  # Ozon
        '232402'  # Skyeng
    ]

    # Получаем данные
    data = get_data_from_hh(employer_ids)

    print("Сохранение данных в базу...")
    save_data_to_db(data, db_name, params)


def user_interaction(db_name, params):
    """Интерфейс взаимодействия с пользователем."""
    db_manager = DBManager(db_name, params)

    while True:
        print("\n--- Меню управления ---")
        print("1 - Список компаний и количество вакансий")
        print("2 - Список всех вакансий")
        print("3 - Средняя зарплата по вакансиям")
        print("4 - Вакансии с зарплатой выше средней")
        print("5 - Поиск вакансий по ключевому слову")
        print("0 - Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            results = db_manager.get_companies_and_vacancies_count()
            for row in results:
                print(f"{row[0]}: {row[1]} вакансий")
        elif choice == "2":
            results = db_manager.get_all_vacancies()
            for row in results:
                print(f"Компания: {row[0]}, Вакансия: {row[1]}, ЗП: {row[2]}, Ссылка: {row[3]}")
        elif choice == "3":
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата: {avg_salary}")
        elif choice == "4":
            results = db_manager.get_vacancies_with_higher_salary()
            for row in results:
                print(f"Вакансия: {row[0]}, ЗП: {row[1]}")
        elif choice == "5":
            keyword = input("Введите слово для поиска: ")
            results = db_manager.get_vacancies_with_keyword(keyword)
            for row in results:
                print(f"Вакансия: {row[0]}, ЗП: {row[1]}")
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Некорректный ввод. Попробуйте еще раз.")


def main():
    # Настройки
    db_name = 'hh_course'
    params = config()

    # Инициализация (Создание БД и таблиц)
    init_db(db_name, params)

    # Загрузка данных (API -> DB)
    load_data(db_name, params)

    # Взаимодействие (Меню)
    user_interaction(db_name, params)


if __name__ == "__main__":
    main()
