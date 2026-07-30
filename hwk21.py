# დავალება: Weather Checker API Client

# შექმენით Python პროგრამა, რომელიც მომხმარებლის მიერ შეყვანილი ქალაქის მიხედვით მიიღებს მიმდინარე ამინდის ინფორმაციას 
# Open-Meteo API-ის გამოყენებით.

# პროგრამამ უნდა გამოიყენოს Python-ის requests მოდული HTTP მოთხოვნების გასაგზავნად.

# API 1 — Geocoding API
# პირველ ეტაპზე საჭიროა ქალაქის სახელის მიხედვით მისი კოორდინატების (latitude, longitude) მიღება.

# გამოიყენეთ შემდეგი API endpoint:

# https://geocoding-api.open-meteo.com/v1/search

# გამოიყენეთ Query Parameters:
# name	ქალაქის სახელი
# count	რამდენი შედეგი გვინდა დაბრუნდეს

# მაგალითი:
# GET https://geocoding-api.open-meteo.com/v1/search?name=Tbilisi&count=1

# ამ მოთხოვნის შედეგად უნდა მიიღოთ:

# latitude
# longitude

# რომლებიც შემდეგ ეტაპზე დაგჭირდებათ.

# API 2 — Weather Forecast API

# მიღებული კოორდინატების გამოყენებით უნდა გამოიძახოთ ამინდის API.

# Endpoint:

# https://api.open-meteo.com/v1/forecast

# Query Parameters:
# latitude	ქალაქის განედი
# longitude	ქალაქის გრძედი
# current	რომელი მიმდინარე მონაცემები გვჭირდება
# timezone	დროის სარტყელი

# მაგალითად:
# params = {
#     "latitude": 52.52,
#     "longitude": 13.41,
#     "current": "temperature_2m,wind_speed_10m",
#     "timezone": "auto"
# }
# (რათქმაუნდა აქ კოორდინატები უნდა იყოს იმ ქალაქის, რომელსაც წინა მოთხოვნიდან მიიღებთ)
# ეს პარამეტრები გაატანეთ მოთხოვნას (params=params) სახით

# პროგრამის მუშაობის ეტაპები
# მომხმარებელმა უნდა შეიყვანოს ქალაქის სახელი.

# მაგალითი:

# Enter city name: Tbilisi

# საბოლოოდ გამოიტანეთ მხოლოდ:
# ქალაქის სახელი
# მიმდინარე ტემპერატურა
# ქარის სიჩქარე
# მიმდინარე დრო
# საბოლოო შედეგის მაგალითი
# City: Tbilisi
# Temperature: 22.1 °C
# Wind Speed: 6.8 km/h
# Time: 2026-07-18T23:00

# თუ მომხმარებელი შეიყვანს არასწორ ქალაქს, მაგალითად:
# Enter city name: Abcdxyz
# პროგრამამ უნდა დაბეჭდოს:
# City not found
# და არ უნდა დასრულდეს პროგრამა შეცდომით.

import requests

geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
weather_url = "https://api.open-meteo.com/v1/forecast"

def get_weather():

    city_name = input("Enter city name: ")

    geocoding_params = {
        "name": city_name,
        "count": 1
    }

    geocoding_response = requests.get(geocoding_url, params=geocoding_params)

    if geocoding_response.status_code != 200:
        print("Error fetching geocoding data")
        return

    geocoding_data = geocoding_response.json()

    if not geocoding_data.get('results'):
        print("City not found")
        get_weather()
        return
    
    latitude = geocoding_data['results'][0]['latitude']
    longitude = geocoding_data['results'][0]['longitude']

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
        "timezone": "auto"
    }

    weather_response = requests.get(weather_url, params=weather_params)

    if weather_response.status_code != 200:
        print("Error fetching weather data")
        return
    
    weather_data = weather_response.json()

    print(f"\n---------------------------------------------------------")
    print(f"City: {city_name}")
    print(f"Temperature: {weather_data['current']['temperature_2m']} °C")
    print(f"Wind Speed: {weather_data['current']['wind_speed_10m']} km/h")
    print(f"Time: {weather_data['current']['time']}")
    print(f"---------------------------------------------------------")

get_weather()