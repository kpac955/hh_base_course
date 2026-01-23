import psycopg2


def create_database(db_name, params):
    """Создает базу данных и таблицы."""
    # 1. Подключаемся к системной базе 'postgres', чтобы создать новую БД
    db_params = params.copy()
    db_params['dbname'] = 'postgres'

    conn = psycopg2.connect(**db_params)
    conn.autocommit = True
    cur = conn.cursor()

    # Удаляем базу, если она есть, и создаем заново
    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    cur.close()
    conn.close()

    # 2. Подключаемся к созданной базе и создаем таблицы
    params['dbname'] = db_name
    conn = psycopg2.connect(**params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id SERIAL PRIMARY KEY,
                hh_id VARCHAR(20) UNIQUE NOT NULL,
                company_name VARCHAR(255) NOT NULL,
                url TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INTEGER REFERENCES employers(employer_id),
                title VARCHAR(255) NOT NULL,
                salary INTEGER,
                url TEXT
            )
        """)

    conn.commit()
    conn.close()
    print(f"База данных {db_name} и таблицы успешно созданы!")


def format_salary(salary_data):
    """
    Возвращает начальную зарплату или 0, если данные отсутствуют.
    """
    if salary_data and isinstance(salary_data.get('from'), int):
        return salary_data['from']
    return 0


def save_data_to_db(data, db_name, params):
    """Сохраняет данные о работодателях и вакансиях."""
    params['dbname'] = db_name
    conn = psycopg2.connect(**params)

    try:
        with conn.cursor() as cur:
            for item in data:
                employer = item['employer']
                vacancies = item['vacancies']

                cur.execute(
                    """
                    INSERT INTO employers (hh_id, company_name, url)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (hh_id) DO UPDATE SET company_name = EXCLUDED.company_name
                    RETURNING employer_id
                    """,
                    (employer['id'], employer['name'], employer['alternate_url'])
                )
                employer_db_id = cur.fetchone()[0]

                for vacancy in vacancies:
                    salary = format_salary(vacancy.get('salary'))

                    cur.execute(
                        """
                        INSERT INTO vacancies (employer_id, title, salary, url)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (employer_db_id, vacancy['name'], salary, vacancy['alternate_url'])
                    )

        conn.commit()
        print("Данные успешно сохранены в БД.")
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")
        conn.rollback()
    finally:
        conn.close()
