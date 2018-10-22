# coding: utf-8

from slackbot.bot import respond_to  # @botname: で反応するデコーダ
from slackbot.bot import listen_to  # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

import requests
import json
import re

# 今日の東京の天気：概要
@listen_to('今日の天気')
def respond_today_tokyo(message):
    respond(message, '130010', '東京', 0)

@listen_to('明日の天気')
def respond_tomorrow_tokyo(message):
    respond(message, '130010', '東京', 1)

@listen_to('詳しい天気')
def respond_description(message):
    respond_description_tokyo(message, '130010')

@respond_to('使い方')
def respond_manual(message):
    message.reply(
        'tenkibotを任意のチャンネルに招待すると、そのチャンネル内で指定のメッセージに対して反応します。\n'
        + '`今日の天気` 今日の天気、最高・最低気温を投稿します。\n'
        + '`明日の天気` 明日の天気、最高・最低気温を投稿します。\n'
        + '気温に関しては、時間帯により、気温が表示されないことがあります。\n'
        + '更に詳しい情報は、 https://github.com/haruspring-jokt/tenkibot を参照してください。')

def respond(message, city_id, city_name, date):
    url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city={}'.format(city_id)
    html = requests.get(url)
    json_file = json.loads(html.text)

    assert json_file is not None, '天気情報を正しく取得できませんでした'
    
    link = json_file['link']
    forecasts = json_file['forecasts'][date]
    telop = forecasts['telop']
    # 最高気温
    try:
        temperate_max = forecasts['temperature']['max']['celsius']
    except TypeError:
        temperate_max = '--'
    # 最低気温
    try:
        temperate_min = forecasts['temperature']['min']['celsius']
    except TypeError:
        temperate_min = '--'
    if date == 0:
        date_text = '今日'
    if date == 1:
        date_text = '明日'

    message.reply(
        date_text +'の' + city_name + 'は' + telop + 'です。\n'
        + '最高気温は' + temperate_max + '℃です。\n'
        + '最低気温は' + temperate_min + '℃です。\n'
        + ':information_source: 詳しくは、リンク先を参照してください。\n'
        + link)

def respond_description_tokyo(message, city_id):
    url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city={}'.format(city_id)
    html = requests.get(url)
    json_file = json.loads(html.text)

    assert json_file is not None, '天気情報を正しく取得できませんでした'

    title = json_file['title']
    description_text = json_file['description']['text']

    message.reply(
        title + 'です。\n'
        + description_text)
