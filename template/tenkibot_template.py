# coding: utf-8
"""
メンションで受け取った（またはチャンネルに投稿された）メッセージから判断し
実行するサービスをディスパッチする。
"""

from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply
from service import tenkibot_service


@listen_to(r"^tenki\s-h|--help$")
def post_help(message):
    """
    ヘルプメニューを表示する。
    """
    print('[info] being called help command.')
    attachments = tenkibot_service.make_help_message()
    message.send_webapi('', attachments)
    

def post_not_found_city(message):
    message.send("```都市名が間違っています```")


@listen_to(r"^tenki\s(-c\s|--current\s)(.*)$")
def post_current_weather_data_with_option(message, option, city_name):
    """
    指定された都市に関する現在の天気を表示する。
    コマンド: "@tenkibot [-c cityname|--current cityname]"
    """
    post_message = tenkibot_service.make_current_weather_message(city_name)
    message.send('{}'.format(post_message))


@listen_to(r"^tenki\s([^-].*)$")
def post_current_weather_data(message, city_name):
    """
    指定された都市に関する現在の天気を表示する。
    コマンド: "@tenkibot [cityname]"
    """
    post_message = tenkibot_service.make_current_weather_message(city_name)
    message.send('{}'.format(post_message))


@listen_to(r"^tenki\s(-5\s|--five\s)(.*)$")
def post_five_days_weather_data(message, option, city_name):
    """
    指定された都市に関する5日間の天気予報を表示する。
    コマンド: "@tenkibot [-5 cityname|--five cityname]"
    """
    post_message = tenkibot_service.make_5_days_weather_message(city_name)
    message.send('{}'.format(post_message))