#!/usr/bin/env python
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json

# initialization
import api_factory as api_factory

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['APPID'] = 'XXXXXXX' # IMPORTANT! Please replace with your APPID

# allow from localhost - replace with your domain
app.config["ORIGIN_ALLOWED"] = "http://localhost:port"
cors = CORS(app, resources={r"/api/*": {"origins": app.config["ORIGIN_ALLOWED"]}})
weather_api = api_factory.get_api('openweather', app.config['APPID'])


@app.route('/api/countries', endpoint='countries', methods=['GET'])
@app.route('/api/cities', endpoint='cities', methods=['GET'])
@app.route('/api/weather', endpoint='weather', methods=['POST', 'GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def get_weather_api():
    result = None
    if request.endpoint == 'countries':
        result = get_supported_countries()
    if request.endpoint == 'cities':
        result = get_cities(request)
    if request.endpoint == 'weather':
        result = get_weather(request)

    if result is not None:
        return jsonify(result)

    return jsonify({"status": "ERROR", "code": 404, "message": "Invalid request"})


def get_weather(r):
    '''
    Call api to get weather by city, optional country or by city id
    :param r: should include ('city') or ('city', 'country') or ('id') or ('lat', 'lon')
    :return: json response
    '''
    names = ['city', 'country', 'id', 'lat', 'lon', 'zip']
    params = get_params(r, names)
    optional_names = ['units']
    params_optional = get_params(r, optional_names)
    # prioritize parameters
    if 'id' in params and params['id'] is not None:
        try:
            return weather_api.get_weather_by_cityid(params, params_optional)
        except Exception, e:
            return return_error(e.message)

    if 'city' in params and params['city'] is not None:
        try:
            return weather_api.get_weather_by_city(params, params_optional)
        except Exception, e:
            return return_error(e.message)

    if 'lat' in params and 'lon' in params and params['lat'] is not None and params['lon'] is not None:
        try:
            return weather_api.get_weather_by_coords(params, params_optional)
        except Exception, e:
            return return_error(e.message)

    if 'zip' in params and params['zip'] is not None:
        try:
            return weather_api.get_weather_by_zipcode(params, params_optional)
        except Exception, e:
            return return_error(e.message)


def get_params(r, names):
    '''
    Get dict of query parameters from request
    :param r:  - request
    :param names:  names of parameters to get
    :return:  dict of parameters
    '''
    params = {}
    if r.method == 'POST':
        for name in names:
            params[name] = r.json.get(name)
    else:
        for name in names:
            params[name] = r.args.get(name)
    return params


def get_supported_countries():
    '''
    Returns list of supported countries
    :return:  json array of countries name and codes
    '''
    return send_result(weather_api.get_countries())


def get_cities(r):
    '''
     Returns list of supported cities by country
    :param r: request, must contain 'country' parameter (country code)
    :return: json array of cities name and ids
    '''
    country_code = r.args.get('country')
    if country_code is None:
        return return_error("Country parameter is missing.")
    return send_result(weather_api.get_cities_by_country(country_code))


def send_result(result):
    if not result or result is None:
        return return_error("Data is missing")
    else:
        return {"status": "OK", "status_code": 200, "data": result}


def return_error(msg):
    return {"status": "ERROR", "code": 404, "message": msg}


if __name__ == '__main__':
    app.run(debug=True)
