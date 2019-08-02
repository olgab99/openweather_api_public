import requests
import json
import os

from abstract_api import ApiBase


class OpenWeatherApi(ApiBase):
    def __init__(self, appid):
        if appid is None:
            raise Exception("Invalid APPID")
        self.appid = appid

        package_dir = os.path.dirname(os.path.abspath(__file__))
        dir = os.path.join(package_dir, 'openweather_api_data')
        self.lists = os.path.join(dir, 'lists')

        with open(os.path.join(dir, 'openweather_mapping.json')) as f:
            self.mappings = json.load(f)

    def get_weather_by_cityid(self, params, optional_params=None):
        '''
        Get weather by city-id
        :param id: city id
        :param units: metric or imperial
        :return: mapped json result
        '''
        if id is None:
            raise Exception("Parameter id is missing")
        payload = self.common_params(optional_params)
        payload['id'] = params['id']
        return self.call_api(payload)

    def get_weather_by_city(self, params, optional_params=None):
        '''

        :param city: city name
        :param country: country code
        :param units: metric or imperial
        :return: mapped json result
        '''
        if 'city' not in params or params['city'] is None:
            raise Exception("Parameter city is missing")

        payload = self.common_params(optional_params)

        if 'country' in params and params['country'] is not None:
            payload['q'] = '%s,%s' % (params['city'], params['country'].lower())
        else:
            payload['q'] = params['city']
        return self.call_api(payload)

    def get_weather_by_zipcode(self, params, optional_params=None):
        '''
        Get weather by zip code
        :param zipcode:  zip code
        :param id: city id
        :param units: metric or imperial
        :return: mapped json result
        '''
        if 'zip' not in params or params['zip'] is None:
            raise Exception("Parameter zipcode is missing")
        payload = self.common_params(optional_params)
        payload['zip'] = params['zip']
        return self.call_api(payload)

    def get_weather_by_coords(self, params, optional_params=None):
        '''
        Get weather by coordinates
        :param lat: latitude
        :param lon: longitude
        :param id: city id
        :param units: metric or imperial
        :return: mapped json result
        '''
        if 'lat' not in params or params['lat'] is None or 'lon' not in params or params['lon'] is None:
            raise Exception("Parameter lat or lon is missing")
        payload = self.common_params(optional_params)
        payload['lat'] = params['lat']
        payload['lon'] = params['lon']
        return self.call_api(payload)

    def call_api(self, payload):
        '''
        Call open weather API
        :param payload: call payload
        :return: mapped json result
        '''
        r = requests.get('http://api.openweathermap.org/data/2.5/weather', params=payload)
        if r.status_code == 200:
            mapped = self.map_result(r.json())
            return {"status": 'OK', "status_code": r.status_code, 'data': mapped}
        else:
            # {"cod":"404","message":"city not found"}
            return {"status": 'FAIL', "status_code": r.status_code, 'message': 'Error processing request'}

    # Create query string for API call
    # params - passed-in parameters
    def common_params(self, params=None):
        result = {'APPID': self.appid}
        if params is not None:
            for name, val in params.iteritems():
                if val is not None:
                    result[name] = val
        return result

    def map_result(self, response):
        # [ { category_title: "...", data: [{title:"...", value:"..."},... ]}, .... ]
        result = []
        for item in self.mappings:
            data = self.append_values(response, item["key"], item["title"], item["fields"])
            if data is not None:
                result.append(data)

        return result

    def append_values(self, response, category, category_title, fields):
        '''
        Helper function to append parameters
        :param response: json data
        :param category: category name
        :param category_title: category caption
        :param fields: array of category fields to read
        :return:
        '''
        if category in response:
            section = {'category_title': category_title, "data": []}

            for item in fields:
                # we have field values
                data = response[category][0] if isinstance(response[category], list) else response[category]
                if item['key'] in data:
                    section["data"].append({"title": item['title'], "value": data[item['key']]})

            return section
        return None

    ### get data for website
    def get_countries(self):
        '''
        Get list of countries and codes for displaying on front-end
        :return: json array of countries names/codes
        '''
        try:
            with open(os.path.join(self.lists, 'country_list.json')) as f:
                countries = json.load(f)
                sorted_countries = sorted(countries, key=lambda k: k['country'])
                return sorted_countries
        except:
            return None

    def get_cities_by_country(self, country_code):
        '''
        Get list of city names/ids by country
        :param country_code:  country code
        :return:  json array of cities names/ids
        '''
        fname = "%s.json" % country_code
        try:
            with open(os.path.join(self.lists, fname)) as f:
                cities = json.load(f)
            sorted_cities = sorted(cities, key=lambda k: k['city'])
            return sorted_cities
        except:
            return None
