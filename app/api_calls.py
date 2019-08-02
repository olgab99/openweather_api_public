import requests


def get_weather(appid, params):
    # api.openweathermap.org/openweather_api_data/2.5/weather?q=London,uk&APPID=c94b9a772a00fc2f807900891313151b
    payload = assemble_params(appid, params)
    return call_api(payload)


def call_api(payload):
    r = requests.get('http://api.openweathermap.org/data/2.5/weather', params=payload)
    if r.status_code == 200:
        return {"status": 'OK', "status_code": r.status_code, 'openweather_api_data': r.json()}
    else:
        # {"cod":"404","message":"city not found"}
        return {"status": 'FAIL', "status_code": r.status_code, 'message': r.json()['message']}


def assemble_params(appid, params):
    if appid is None:
        return None
    if params['id'] is not None:
        return {'id': params['id'], 'APPID': appid}

    if params['city'] is None:
        return None

    if params['country'] is None:
        return {'q': '%s,%s' % (params['city'], params['country'].lower()), 'APPID': appid}
    else:
        return {'q': params['city'], 'APPID': appid}
