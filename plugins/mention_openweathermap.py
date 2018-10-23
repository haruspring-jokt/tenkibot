# coding: utf-8

from slackbot.bot import respond_to  # @botname: で反応するデコーダ
from slackbot.bot import listen_to  # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

import requests
import json
import re
import os

owm_api_key = os.environ['OWM_API_KEY']

# API keyを取得
# def get_API_KEY():
#     with open('openWeatherMap', encoding='utf-8') as API_KEY:
#         return API_KEY.read()

@listen_to(r"^tenki\s-h|--help")
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
            'text': 'ヘルプメニュー',
            'color': '#59afe1'
        }
    ]
    message.send_webapi('', json.dumps(attachments))

@listen_to(r"^tenki\s[^-]+")
def respond_current_weather_data_tokyo(message):
    """
    現在の天気を表示する。
    コマンド: "tenki [city]"
    """
    # api_key = get_API_KEY()
    
    city_name = message.body['text'].split(" ")[1]

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
