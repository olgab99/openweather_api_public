This is an example of client for OpenWeather API (https://openweathermap.org/) free-tie service
=========

The code is written in Python 2.7 with using Flask library and Bootstrap for HTML front end.

Installation
------------
After cloning, create a virtual environment and install the requirements. For Linux and Mac users:

    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt

If you are on Windows, then use the following commands instead:

    $ virtualenv venv
    $ venv\Scripts\activate
    (venv) $ pip install -r requirements.txt

Running
-------
To run the server use the following command:

    (venv) $ python app/weather_api.py
     * Running on http://127.0.0.1:5000/
     * Restarting with reloader
     
To run the front-end - open file frontend/weather.html in your browser

Notes:
in weather.js file SERVER_URL set to deault localhost backend URL - replace if you use different server url  
in weather_api.py file replace app.config['APPID'] to your OpenWeatherAPI id

API Documentation
-----------------

- GET **/api/countries**

    Get JSON-formatted data array of country names and codex:
```json
[
  {
    "country": "Afghanistan",
    "code": "AF"
  },
  {
    "country": "Albania",
    "code": "AL"
  }
]
```
On success a status code 200 is returned

- GET **/api/cities?country={country_code}**

    Get JSON-formatted data array of city names and ids:
```json
[
  {
    "city": "Morden",
    "id": 6078447
  },
  {
    "city": "Laval",
    "id": 6050612
  }
]
```
On success a status code 200 is returned

- GET **/api/weather?id=12345**
or
- POST **/api/weather** with json data:
```json
{"id": 12345}
```
    On success a status code 200 is returned. The body of the response contains a JSON object with weather information.<br>
    On failure status code 400 (bad request) is returned.
Possibel parameters:

```text
One of:
id - city id, 
city - city name with optional country - country name
lat, lon - latitude and longitude 
zip - zip code

Optional:
uinits - one of 'metrics' or 'imperial'

```

Example curl command:
```text
curl:
$ curl -H "Content-Type: application/json" -X GET http://127.0.0.1:5000/api/city?id=2172797
```

To run unit tests:
```text
python -m unittest discover app
```