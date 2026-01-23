from unittest.mock import patch

import main


def test_init_db_call():
    """Покрываем функцию инициализации."""
    with patch('main.create_database') as mock_create:
        main.init_db('test_db', {})
        mock_create.assert_called_once()


def test_load_data_call():
    """Покрываем функцию загрузки."""
    with patch('main.get_data_from_hh') as mock_get, \
            patch('main.save_data_to_db') as mock_save:
        mock_get.return_value = []
        main.load_data('test_db', {})

        mock_get.assert_called_once()
        mock_save.assert_called_once()


@patch('builtins.input', side_effect=['0'])
@patch('main.DBManager')
def test_user_interaction_exit(mock_db, mock_input):
    """Покрываем меню (выход)."""
    main.user_interaction('test_db', {})
    assert mock_input.called
