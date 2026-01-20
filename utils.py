import psycopg2
from config import config


def create_tables():
    """Создает таблицы employers и vacancies в базе данных PostgreSQL."""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS employers (
            employer_id SERIAL PRIMARY KEY,
            hh_id VARCHAR(20) UNIQUE NOT NULL,
            company_name VARCHAR(255) NOT NULL,
            url TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            employer_id INTEGER REFERENCES employers(employer_id),
            title VARCHAR(255) NOT NULL,
            salary INTEGER,
            url TEXT
        )
        """
    )

    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
        print("База данных готова к работе!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def save_data_to_db(data):
    """Сохраняет данные о работодателях и вакансиях в базу данных."""
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        for item in data:
            employer = item['employer']
            vacancies = item['vacancies']

            # Вставляем данные о работодателе
            cur.execute(
                """
                INSERT INTO employers (hh_id, company_name, url)
                VALUES (%s, %s, %s)
                RETURNING employer_id
                """,
                (employer['id'], employer['name'], employer['alternate_url'])
            )
            # Получаем сгенерированный ID работодателя в нашей БД
            employer_db_id = cur.fetchone()[0]

            for vacancy in vacancies:
                # Обработка зарплаты (берем 'from', если есть, иначе 0)
                salary = 0
                if vacancy['salary'] and vacancy['salary']['from']:
                    salary = vacancy['salary']['from']

                cur.execute(
                    """
                    INSERT INTO vacancies (employer_id, title, salary, url)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (employer_db_id, vacancy['name'], salary, vacancy['alternate_url'])
                )

        conn.commit()
        cur.close()
        print("Данные успешно сохранены в БД.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()