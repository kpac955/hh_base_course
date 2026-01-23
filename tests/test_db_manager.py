from unittest.mock import patch

from db_manager import DBManager


def test_db_manager_init():
    """Тестируем, что менеджер правильно принимает параметры."""
    params = {'user': 'postgres', 'password': '123'}
    db_name = 'test_db'
    db = DBManager(db_name, params)

    assert db.params['dbname'] == 'test_db'
    assert db.params['user'] == 'postgres'


def test_db_manager_params_copy():
    """Проверяем, что менеджер не портит исходный словарь"""
    params = {'user': 'postgres'}
    DBManager('new_db', params)
    assert 'dbname' not in params


@patch('psycopg2.connect')
def test_db_manager_other_methods(mock_connect):
    mock_cursor = mock_connect.return_value.cursor.return_value.__enter__.return_value

    # Настраиваем возвращаемые значения для разных методов
    mock_cursor.fetchone.return_value = (50000.0,)
    mock_cursor.fetchall.return_value = [('Vac', 60000)]

    db = DBManager('test_db', {'user': 'admin'})

    db.get_all_vacancies()
    db.get_avg_salary()
    db.get_vacancies_with_higher_salary()
    db.get_vacancies_with_keyword('python')

    assert mock_cursor.execute.call_count == 4


@patch('psycopg2.connect')
def test_db_manager_get_companies(mock_connect):
    """Тест получения компаний."""
    mock_conn = mock_connect.return_value
    mock_cur = mock_conn.cursor.return_value.__enter__.return_value
    mock_cur.fetchall.return_value = [('Yandex', 5), ('Ozon', 10)]

    db = DBManager('test_db', {'user': 'admin'})
    results = db.get_companies_and_vacancies_count()

    assert len(results) == 2
    assert results[0][0] == 'Yandex'
