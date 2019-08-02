from unittest import TestCase
import flask
from flask import Flask, request, jsonify
import mock
from mock import patch
import weather_api
from apis.openweather_api import OpenWeatherApi


class TestWeatherApp(TestCase):
    ## test get_by_cityid
    @patch.object(flask, "request")
    @patch.object(weather_api, 'get_params', return_value={})
    @patch.object(OpenWeatherApi, 'get_weather_by_cityid', return_value={})
    def test_get_weather_bycityid(self, mock_get_by_cityid, mock_get_params, mock_request):
        mock_get_params.return_value = {'id': 1234, 'units': None}
        res = weather_api.get_weather(mock_request)
        mock_get_by_cityid.assert_called()
        mock_get_by_cityid.reset_mock()
        mock_get_params.reset_mock()
        mock_get_params.return_value = {'city': 'London', 'units': 'metric'}
        res = weather_api.get_weather(mock_request)
        mock_get_by_cityid.assert_not_called()

    ## test get_by_city
    @patch.object(flask, "request")
    @patch.object(weather_api, 'get_params', return_value={})
    @patch.object(OpenWeatherApi, 'get_weather_by_city', return_value={})
    def test_get_weather_bycity(self, mock_get_by_city, mock_get_params, mock_request):
        mock_get_params.return_value = {'id': 1234, 'units': None}
        res = weather_api.get_weather(mock_request)
        mock_get_by_city.assert_not_called()

        mock_get_params.reset_mock()
        mock_get_params.return_value = {'city': 'London', 'units': 'metric'}
        res = weather_api.get_weather(mock_request)
        mock_get_by_city.assert_called()

    ## test get_by_coords
    @patch.object(flask, "request")
    @patch.object(weather_api, 'get_params', return_value={})
    @patch.object(OpenWeatherApi, 'get_weather_by_coords', return_value={})
    def test_get_weather_bycity(self, mock_get_by_coords, mock_get_params, mock_request):
        mock_get_params.return_value = {'id': 1234, 'units': None}
        res = weather_api.get_weather(mock_request)
        mock_get_by_coords.assert_not_called()

        mock_get_params.reset_mock()
        mock_get_params.return_value = {'lat': 12365, 'lon': 12345}
        res = weather_api.get_weather(mock_request)
        mock_get_by_coords.assert_called()

    ## test get_by_zip
    @patch.object(flask, "request")
    @patch.object(weather_api, 'get_params', return_value={})
    @patch.object(OpenWeatherApi, 'get_weather_by_zipcode', return_value={})
    def test_get_weather_bycity(self, mock_get_by_zipcode, mock_get_params, mock_request):
        mock_get_params.return_value = {'id': 1234, 'units': None}
        res = weather_api.get_weather(mock_request)
        mock_get_by_zipcode.assert_not_called()

        mock_get_params.reset_mock()
        mock_get_params.return_value = {'zip': 12365}
        res = weather_api.get_weather(mock_request)
        mock_get_by_zipcode.assert_called()

    def test_send_result(self):
        data = {'a': 'b'}
        result = weather_api.send_result(data)
        expected = {'status': 'OK', 'status_code': 200, 'data': {'a': 'b'}}
        self.assertEquals(result, expected, "Error in send_result")

        result = weather_api.send_result({})
        expected = {"status": "ERROR", "code": 404, "message": "Data is missing"}
        self.assertEquals(result, expected, "Error in send_result")


