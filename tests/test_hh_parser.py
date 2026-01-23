from unittest.mock import patch

from hh_parser import get_data_from_hh


@patch('requests.get')
def test_get_data_from_hh(mock_get):
    """Тестируем, что парсер корректно собирает структуру данных."""

    # Эмулируем ответ от API для компании и для вакансий
    mock_get.return_value.json.side_effect = [
        {'id': '123', 'name': 'Test Company', 'alternate_url': 'url1'},  # Ответ для работодателя
        {'items': [{'name': 'Dev', 'salary': None, 'alternate_url': 'url2'}]}  # Ответ для вакансий
    ]

    result = get_data_from_hh(['123'])

    # Проверяем структуру
    assert len(result) == 1
    assert result[0]['employer']['name'] == 'Test Company'
    assert len(result[0]['vacancies']) == 1
    assert result[0]['vacancies'][0]['name'] == 'Dev'
