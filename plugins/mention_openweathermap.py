# coding: utf-8

from slackbot.bot import respond_to  # @botname: で反応するデコーダ
from slackbot.bot import listen_to  # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

import requests
import json
import re
import os
import datetime

# openWeatherMapのAPI_KEYを環境変数から取得
owm_api_key = os.environ['OWM_API_KEY']
lang = 'ja'


@listen_to(r"^tenki\s-h|--help$")
def respond_help(message):
    """
    ヘルプメニューを表示する。
    コマンド: "tenki [-h|--help]"
    """
    print('[info] being called help command.')
    attachments = [{
        'fallback': 'tenkibot',
        'author_name': 'tenkibot',
        'author_link': 'https://openweathermap.org/',
        'text': 'ヘルプメニューを表示します',
        'color': '#59afe1'
    }]
    message.send_webapi('', json.dumps(attachments))


@listen_to(r"^tenki\s([^-]+|-c\s[^-]+|--current\s[^-]+)$")
def respond_current_weather_data(message, something):
    """
    指定された都市に関する現在の天気を表示する。
    コマンド: "@tenkibot [-c cityname|--current cityname]"
    """

    city_name = message.body['text'].split(" ")[-1]

    print('[info] being called current weather command about [{}].'.format(
        city_name))

    api = 'http://api.openweathermap.org/data/2.5/weather?units=metric&q={city}&APPID={API_KEY}&lang={LANG}'
    url = api.format(city=city_name, API_KEY=owm_api_key, LANG=lang)

    print('[info] url is {0}'.format(url))

    response = requests.get(url)
    data = json.loads(response.text)

    if data['cod'] == '404':
        message.send('```都市名が間違っています\n確認してください```')
    elif re.compile(data['name'], re.IGNORECASE).match(city_name):
        # loadしたjsonを渡して投稿用メッセージを作成する
        post_message = create_current_weather_message(data)
        message.send('{}'.format(post_message))


@listen_to(r"^tenki\s(-5\s[^-]+|--five\s[^-]+)$")
def respond_three_days_weather_data(message, something):
    """
    指定された都市に関する5日間天気を表示する。
    コマンド: "@tenkibot [-5 cityname|--five cityname]"
    """

    city_name = message.body['text'].split(" ")[-1]

    print('[info] being called five days weather command about [{}].'.format(
        city_name))

    api = 'http://api.openweathermap.org/data/2.5/forecast?units=metric&q={city}&APPID={API_KEY}&lang={LANG}'
    url = api.format(city=city_name, API_KEY=owm_api_key, LANG=lang)

    print('[info] url is {0}'.format(url))

    response = requests.get(url)
    data = json.loads(response.text)

    if data['cod'] == '404':
        message.send('```都市名が間違っています\n確認してください```')
    elif re.compile(data['city']['name'], re.IGNORECASE).match(city_name):
        message.send('```{}```'.format(data['city']))


def create_current_weather_message(json_loaded_data):
    """
    jsonでロードしたデータを読み、投稿用メッセージを作成する。
    """

    # jsonから取得
    weather = json_loaded_data['weather'][0]
    weather_main = weather['main']
    weather_description = weather['description']

    # TODO アイコンの貼り方
    # weather_icon = weather['icon']
    # weather_icon_img = 'https://openweathermap.org/img/w/{}.png'.format(
    #     weather_icon)

    main = json_loaded_data['main']
    main_temp = main['temp']
    main_pressure = main['pressure']
    main_humidity = main['humidity']

    wind = json_loaded_data['wind']
    wind_speed = wind['speed']
    wind_deg = wind['deg']

    clouds_all = json_loaded_data['clouds']['all']

    # TODO 日本時間になっているか要チェック
    dt_unix = json_loaded_data['dt']
    dt_formatted_utf = datetime.datetime.fromtimestamp(dt_unix).strftime(
        '%Y/%m/%d %H:%M:%S')

    city_name = json_loaded_data['name']
    city_id = json_loaded_data['id']

    # メッセージの作成
    post_message = """
{time}に取得した{city}の天気情報です。
天気: {main} （{des}）
気温: {temp} ℃
気圧: {pressure} hPa
湿度: {humid} %
風速と風向: {speed} m/s、{deg} 
雲量: {cloud} %
詳しくは https://openweathermap.org/city/{id} をご覧ください。
    """.format(
        time=dt_formatted_utf,
        city=city_name,
        main=weather_main,
        des=weather_description,
        temp=main_temp,
        pressure=main_pressure,
        humid=main_humidity,
        speed=wind_speed,
        deg=wind_deg,
        cloud=clouds_all,
        id=city_id)

    return post_message
