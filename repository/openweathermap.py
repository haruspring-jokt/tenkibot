# coding: utf-8
"""
openweathemapのweb APIを利用する
"""

import requests
import json
import re
import os

OWM_API_KEY = os.environ['OWM_API_KEY']


def fetch_current_weather_data(city_name, lang='ja', units='metric'):
    """
    現在の天気データをjson形式で取得する。
    """
    url = 'http://api.openweathermap.org/data/2.5/weather?units={units}&q={q}&APPID={appid}&lang={lang}'.format(
        units=units, q=city_name, appid=OWM_API_KEY, lang=lang)

    print('[info] url is {0}'.format(url))

    response = requests.get(url)
    data = json.loads(response.text)

    return data


def fetch_5_days_weather_data(city_name, lang='ja', units='metric'):
    """
    5日分の天気データをjson形式で取得する。
    """
    url = 'http://api.openweathermap.org/data/2.5/forecast?units={units}&q={q}&APPID={appid}&lang={lang}'.format(
        units=units, q=city_name, appid=OWM_API_KEY, lang=lang)

    print('[info] url is {0}'.format(url))

    response = requests.get(url)
    data = json.loads(response.text)

    return data
