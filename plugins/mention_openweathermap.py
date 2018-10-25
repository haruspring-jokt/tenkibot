# coding: utf-8

from slackbot.bot import respond_to  # @botname: で反応するデコーダ
from slackbot.bot import listen_to  # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

import requests
import json
import re
import os

# openWeatherMapのAPI_KEYを環境変数から取得
owm_api_key = os.environ['OWM_API_KEY']


@listen_to(r"^tenki\s-h|--help$")
def respond_help(message):
    """
    ヘルプメニューを表示する。
    コマンド: "tenki [-h|--help]"
    """
    print('[info] being called help command.')
    attachments = [
        {
            'fallback': 'tenkibot',
            'author_name': 'tenkibot',
            'author_link': 'https://openweathermap.org/',
            'text': 'ヘルプメニューを表示します',
            'color': '#59afe1'
        }
    ]
    message.send_webapi('', json.dumps(attachments))


@listen_to(r"^tenki\s([^-]+|-c\s[^-]+|--current\s[^-]+)$")
def respond_current_weather_data(message, something):
    """
    指定された都市に関する現在の天気を表示する。
    コマンド: "@tenkibot [-c cityname|--current cityname]"
    """

    city_name = message.body['text'].split(" ")[-1]

    print('[info] being called current weather command about [{}].'.format(city_name))

    api = 'http://api.openweathermap.org/data/2.5/weather?units=metric&q={city}&APPID={API_KEY}'
    url = api.format(city = city_name, API_KEY = owm_api_key)

    print('[info] url is {0}'.format(url))
    
    response = requests.get(url)
    data = json.loads(response.text)

    if data['cod'] == '404':
        message.send('```都市名が間違っています\n確認してください```')
    elif re.compile(data['name'],re.IGNORECASE).match(city_name):
        message.send('```{}```'.format(data))


@listen_to(r"^tenki\s(-5\s[^-]+|--five\s[^-]+)$")
def respond_three_days_weather_data(message, something):
    """
    指定された都市に関する5日間天気を表示する。
    コマンド: "@tenkibot [-5 cityname|--five cityname]"
    """

    city_name = message.body['text'].split(" ")[-1]

    print('[info] being called five days weather command about [{}].'.format(city_name))

    api = 'http://api.openweathermap.org/data/2.5/forecast?units=metric&q={city}&APPID={API_KEY}'
    url = api.format(city = city_name, API_KEY = owm_api_key)

    print('[info] url is {0}'.format(url))
    
    response = requests.get(url)
    data = json.loads(response.text)

    if data['cod'] == '404':
        message.send('```都市名が間違っています\n確認してください```')
    elif re.compile(data['city']['name'],re.IGNORECASE).match(city_name):
        message.send('```{}```'.format(data['city']))
