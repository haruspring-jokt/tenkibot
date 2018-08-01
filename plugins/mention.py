# coding: utf-8

from slackbot.bot import respond_to  # @botname: で反応するデコーダ
from slackbot.bot import listen_to  # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

import requests
import json


# 東京の天気（晴れとかだけ）
@respond_to('東京の天気')
def respond_simple_tenki_tokyo(message):
    # tenki APIから拾ってくる
    city_id = '130010'
    url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=' + city_id
    html = requests.get(url)
    json_file = json.loads(html.text)

    assert json_file is not None, '天気情報を正しく取得できませんでした'

    tenki_today = json_file['forecasts'][0]['telop']
    tenki_tomorrow = json_file['forecasts'][1]['telop']
    tenki_day_after_tomorrow = json_file['forecasts'][2]['telop']

    message.reply('今日の東京は{}です。'.format(tenki_today))
    message.reply('明日の東京は{}です。'.format(tenki_tomorrow))
    message.reply('明後日の東京は{}です。'.format(tenki_day_after_tomorrow))
