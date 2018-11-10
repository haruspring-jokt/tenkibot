# coding: utf-8
"""
サービスを実装する
"""

import datetime
from repository import openweathermap
from service import graph_creator
from service import slack_uploader
from service import slack_messenger
from service import os_manager
import json


def make_help_message():
    attachments = [{
        'fallback': 'tenkibot',
        'author_name': 'tenkibot',
        'author_link': 'https://openweathermap.org/',
        'text': 'ヘルプメニューを表示します',
        'color': '#59afe1'
    }]
    return json.dumps(attachments)


def cod_check(data):
    """
    ステータスをチェックする。
    """
    return data['cod']


def make_current_weather_message(city_name):
    """
    現在の天気メッセージを作成する。
    """
    data = openweathermap.fetch_current_weather_data(city_name)
    post_message = create_current_weather_message(data)
    return post_message


def make_5_days_weather_message(city_name):
    """
    5日間予報のメッセージを取得する。
    """
    data = openweathermap.fetch_5_days_weather_data(city_name)
    post_message = create_5_days_forecast_message(data)
    return post_message


def upload_5_days_weather_graph(city_name, channels):
    """
    5日間予報のグラフ付きメッセージを取得する。
    city_name: 天気データを取得する都市名
    channels: 投稿するチャネルのID
    """

    print('[info] called service method. name=[upload_5_days_weather_graph]')

    # OWMのAPIから天気予報JSONデータを取得する
    data = openweathermap.fetch_5_days_weather_data(city_name)

    # 取得結果チェック
    if cod_check(data) != '200':
        slack_messenger.post('```天気データが正しく取得できませんでした```', channels)
        return False

    # データを渡してグラフ画像のファイルパスをもらう
    img_filepath = graph_creator.create_5_days_weather_graph(data)

    # 画像を投稿する
    up_result = slack_uploader.upload_image(
        img_filepath,
        channels,
        initial_comment='uploaded forecast graph in {}'.format(city_name),
        title='5 days forecast in {}'.format(city_name))

    # 結果を取得
    if up_result == False:
        slack_messenger.post('```天気データが正しく取得できませんでした```', channels)
        return False

    # アップロード完了後画像を削除する
    os_manager.remove_file(img_filepath)

    print('[info] finish service method. name=[upload_5_days_weather_graph]')

    return True


def create_current_weather_message(data):
    """
    jsonをロードしたデータを読み、投稿用メッセージを作成する。
    """

    if cod_check(data) == '404':
        return '```都市名が間違っています```'

    # jsonから取得
    weather = data['weather'][0]
    weather_main = weather['main']
    weather_description = weather['description']

    # TODO アイコンの貼り方
    # weather_icon = weather['icon']
    # weather_icon_img = 'https://openweathermap.org/img/w/{}.png'.format(
    #     weather_icon)

    main = data['main']
    main_temp = main['temp']
    main_pressure = main['pressure']
    main_humidity = main['humidity']

    wind = data['wind']
    wind_speed = wind['speed']
    wind_deg = wind['deg']

    clouds_all = data['clouds']['all']

    dt_unix = data['dt']
    dt_formatted_utf = datetime.datetime.fromtimestamp(dt_unix).strftime(
        '%Y/%m/%d %H:%M:%S')

    city_name = data['name']
    city_id = data['id']

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


def create_5_days_forecast_message(data):
    """
    jsonをロードしたデータを読み、投稿用メッセージを作成する。
    """

    if cod_check(data) == '404':
        return '```都市名が間違っています```'

    # jsonから取得
    full_list = data['list']
    post_list = []

    # full_listから1個飛ばし（6時間毎）で予報を取得し、投稿用の予報リストに格納する
    for i, forecast in enumerate(full_list):
        if i % 2 == 0:
            continue
        # 格納処理
        post = {}
        post['dt'] = datetime.datetime.fromtimestamp(
            forecast['dt']).strftime('%m/%d %H') + '時'
        post['temp'] = round(forecast['main']['temp'], 1)
        post['weather'] = forecast['weather'][0]['description']
        if 'rain' in forecast and '3h' in forecast['rain']:
            post['rain'] = round(forecast['rain']['3h'], 2)
        else:
            post['rain'] = ''
        post_list.append(post)

    # 投稿用メッセージの作成
    city_name = data['city']['name']
    post_message = "{}に関する5日間の天気予報です。\ndatetime | temp(℃) | weather | rain(mm)\n".format(
        city_name)

    # 投稿用の予報リストをメッセージに追加
    for post in post_list:
        post_message += str(post['dt'])
        post_message += ' | '
        post_message += str(post['temp'])
        post_message += ' | '
        post_message += str(post['weather'])
        post_message += ' | '
        post_message += str(post['rain'])
        post_message += '\n'

    # リンクの追加
    city_id = data['city']['id']
    post_message += '詳しくはhttps://openweathermap.org/city/{id} をご覧ください。'.format(
        id=city_id)

    return post_message
