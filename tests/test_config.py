from unittest.mock import patch

from config import config


@patch('configparser.ConfigParser.read')
@patch('configparser.ConfigParser.has_section', return_value=True)
@patch('configparser.ConfigParser.items', return_value=[('user', 'postgres')])
def test_config(mock_items, mock_has, mock_read):
    assert mock_items is not None
    assert mock_has is not None
    assert mock_read is not None
    res = config()
    assert res['user'] == 'postgres'
