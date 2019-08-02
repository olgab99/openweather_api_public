from apis.openweather_api import OpenWeatherApi


def get_api(name, appid):
    name = name.lower()
    if name == 'openweather':
        return OpenWeatherApi(appid)

    raise Exception("Api not implemented", 400)