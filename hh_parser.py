import requests


def get_data_from_hh(employer_ids):
    """
    Получает данные о работодателях и их вакансиях с API hh.ru.
    """

    data = []

    for employer_id in employer_ids:
        # Получаем данные о компании
        employer_url = f"https://api.hh.ru/employers/{employer_id}"
        employer_response = requests.get(employer_url).json()

        # Получаем вакансии компании
        vacancies_url = f"https://api.hh.ru/vacancies?employer_id={employer_id}&per_page=20"
        vacancies_response = requests.get(vacancies_url).json()

        data.append({
            'employer': employer_response,
            'vacancies': vacancies_response.get('items', [])
        })
        print(f"Получены данные для: {employer_response.get('name')}")

    return data
