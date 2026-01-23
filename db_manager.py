import psycopg2


class DBManager:
    """
    Класс для управления подключением к БД и выполнения запросов.
    """

    def __init__(self, db_name, params):
        self.params = params.copy()
        self.params['dbname'] = db_name

    def get_companies_and_vacancies_count(self) -> list:
        conn = psycopg2.connect(**self.params)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT company_name, COUNT(vacancies.vacancy_id) 
                FROM employers 
                LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id 
                GROUP BY company_name
            """)
            result = cur.fetchall()
        conn.close()
        return result

    def get_all_vacancies(self) -> list:
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        conn = psycopg2.connect(**self.params)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT employers.company_name, vacancies.title, vacancies.salary, vacancies.url 
                FROM vacancies 
                JOIN employers ON vacancies.employer_id = employers.employer_id
            """)
            result = cur.fetchall()
        conn.close()
        return result

    def get_avg_salary(self) -> float:
        """
        Получает среднюю зарплату по вакансиям.
        """
        conn = psycopg2.connect(**self.params)
        with conn.cursor() as cur:
            cur.execute("SELECT AVG(salary) FROM vacancies WHERE salary > 0")
            result = cur.fetchone()[0]
        conn.close()
        return round(float(result), 2) if result is not None else 0.0

    def get_vacancies_with_higher_salary(self) -> list:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        conn = psycopg2.connect(**self.params)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM vacancies 
                WHERE salary > (SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL)
            """)
            result = cur.fetchall()
        conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword: str) -> list:
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова.
        """
        conn = psycopg2.connect(**self.params)
        with conn.cursor() as cur:
            # Используем параметризованный запрос для безопасности (защита от SQL-инъекций)
            query = "SELECT * FROM vacancies WHERE lower(title) LIKE %s"
            cur.execute(query, ('%' + keyword.lower() + '%',))
            result = cur.fetchall()
        conn.close()
        return result
