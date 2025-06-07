import pytest
from sigmas import create_app
from unittest.mock import patch

@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_regular_simulation_no_exposure_time(client):
    test_data = {
        'mode': 'lss_l',
        'source': 'simple_gal',
        'exposure_time': ''
    }
    response = client.post('/regular_simulation', data=test_data)
    assert response.status_code == 200
    assert b'Please enter an exposure time!' in response.data

def test_regular_simulation_valid(client):
    with patch('sigmas.Yaml_Simulate') as mock_sim:
        mock_sim.return_value = True
        test_data = {
            'mode': 'lss_l',
            'source': 'simple_gal',
            'exposure_time': '300'
        }
        response = client.post('/regular_simulation', data=test_data)
        assert response.status_code == 200
        mock_sim.assert_called_once()

def test_display_fits_not_found(client):
    response = client.get('/display_fits')
    assert response.status_code == 200