from unittest import TestCase
import json
import os
import requests
from requests.models import Response
import mock
from mock import patch

from openweather_api import OpenWeatherApi


class TestOpenWeatherApi(TestCase):

    def setUp(self):
        package_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_data_dir = os.path.join(package_dir, 'test_data')


    @patch.object(requests, 'get')
    def test_get_weather_by_cityid(self, get_mock):
        api = OpenWeatherApi(121212)
        api.get_weather_by_cityid({'id': 1234})
        get_mock.assert_called()
        get_mock.reset_mock()
        api.get_weather_by_cityid({'id': 1234}, {'units': 'metric'})
        get_mock.assert_called()

    @patch.object(requests, 'get')
    def test_get_weather_by_city(self, get_mock):
        api = OpenWeatherApi(121212)
        api.get_weather_by_city({'city': "London"})
        get_mock.assert_called()
        get_mock.reset_mock()
        api.get_weather_by_city({'city': "London"},  {'units': 'metric'})
        get_mock.assert_called()

    @patch.object(requests, 'get')
    def test_get_weather_by_coords(self, get_mock):
        api = OpenWeatherApi(121212)
        api.get_weather_by_coords({'lat': 236, 'lon': 1234})
        get_mock.assert_called()
        get_mock.reset_mock()
        api.get_weather_by_coords({'lat': 236, 'lon': 1234}, {'units': 'imperial'})
        get_mock.assert_called()

    @patch.object(requests, 'get')
    def test_get_weather_by_zipcode(self, get_mock):
        api = OpenWeatherApi(121212)
        api.get_weather_by_zipcode({'zip': 1236})
        get_mock.assert_called()
        get_mock.reset_mock()
        api.get_weather_by_zipcode({'zip': 1236}, {'units': 'metric'})
        get_mock.assert_called()

    def test_common_params(self):
        api = OpenWeatherApi(121212)
        params = {'units': 'metric'}
        result = api.common_params(params)
        expected = {'units': 'metric', 'APPID': 121212}
        self.assertEquals(result, expected, "Error in assembling params")

        result = api.common_params()
        expected = {'APPID': 121212}
        self.assertEquals(result, expected, "Error in assembling params")

    @patch.object(requests, 'get')
    def test_call_api(self, get_mock):
        api = OpenWeatherApi(121212)
        r = Response()
        r.status_code = 200
        r._content = b'{}'
        get_mock.return_value = r
        result = api.call_api({})
        self.assertEquals(200, result['status_code'])

        r.status_code = 404
        result = api.call_api({})
        self.assertEquals(404, result['status_code'])

        get_mock.side_effect = Exception("Some error")
        with self.assertRaises(Exception):
            result = api.call_api({})

    def test_map_result(self):
        api = OpenWeatherApi(121212)
        with open(os.path.join(self.test_data_dir, "response.json")) as f:
            response = json.load(f)
        with open(os.path.join(self.test_data_dir,  "expected_result.json")) as f:
            expected = json.load(f)

        result = api.map_result(response)
        self.assertEquals(result, expected, "Mapping does not match")

    def test_get_countries(self):
        api = OpenWeatherApi(121212)
        package_dir = os.path.dirname(os.path.abspath(__file__))
        api.lists = os.path.join(package_dir, 'test_data')
        result = api.get_countries()

        with open(os.path.join(self.test_data_dir, "country_list.json")) as f:
            expected = json.load(f)

        self.assertEquals(result, expected, "Country list does not match")

    def test_get_cities_by_country(self):
        api = OpenWeatherApi(121212)
        package_dir = os.path.dirname(os.path.abspath(__file__))
        api.lists = os.path.join(package_dir, 'test_data')

        with open(os.path.join(self.test_data_dir,  "CA_expected.json")) as f:
            expected = json.load(f)

        result = api.get_cities_by_country('CA')
        self.assertEquals(result, expected, "City list does not match")
