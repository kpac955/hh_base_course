from utils import format_salary


def test_format_salary_integer():
    """Проверяем, что функция корректно возвращает число."""
    assert format_salary({'from': 50000}) == 50000


def test_format_salary_none_value():
    """Проверяем случай, когда значение зарплаты None."""
    assert format_salary({'from': None}) == 0


def test_format_salary_missing_key():
    """Проверяем случай, когда ключа 'from' нет в словаре."""
    assert format_salary({'to': 100000}) == 0


def test_format_salary_not_a_dict():
    """Проверяем случай, когда вместо словаря пришло что-то другое (None или список)."""
    assert format_salary(None) == 0
    assert format_salary([]) == 0


def test_format_salary_string():
    """Проверяем защиту от строк (если API пришлет текст вместо числа)."""
    assert format_salary({'from': "50000"}) == 0
