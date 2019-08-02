class ApiBase:
    '''
    Base class for API clients. Contains methods that API client must implement
    '''

    def __init__(self, appid):
        pass

    def get_countries(self):
        raise NotImplementedError('users must define get_countries to use this base class')

    def get_cities_by_country(self, country_code):
        raise NotImplementedError('users must define get_cities_by_country to use this base class')

    def get_weather_by_cityid(self, id, units=None):
        raise NotImplementedError('users must define get_weather_by_cityid to use this base class')

    def get_weather_by_city(self, city, country=None, units=None):
        raise NotImplementedError('users must define get_weather_by_city to use this base class')

    def get_weather_by_zipcode(self, zipcode, units=None):
        raise NotImplementedError('users must define get_weather_by_zipcode to use this base class')

    def get_weather_by_coords(self, lat, lon, units=None):
        raise NotImplementedError('users must define get_weather_by_coords to use this base class')
