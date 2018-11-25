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


def make_current_weather_attachments(city_name):

    # openweathermapから現在の天気データを取得する
    data = openweathermap.fetch_current_weather_data(city_name)

    # attachmentsの編集
    attachments = []

    # 天気データを投稿用メッセージに編集
    # 雨または雪の場合は降水量、降雪量を追加する
    attachment = create_current_weather_attachments(data)

    attachments.append(attachment)

    # attachmentsのリターン
    return attachments


def create_current_weather_attachments(data):

    attachment = {}

    if cod_check(data) == '404':
        attachment['text'] = '```都市名が間違っています!```'
        attachment['mrkdwn_in'] = ['text']
        return attachment

    # jsonから取得
    weather = data['weather'][0]
    weather_id = str(weather['id'])
    weather_main = weather['main']
    weather_description = weather['description']

    # サムネイル用アイコンの取得
    icon = weather['icon']
    thumb_url = f'https://openweathermap.org/img/w/{icon}.png'

    # 温度・湿度
    main = data['main']
    main_temp = main['temp']
    main_humidity = main['humidity']

    # 天気データの取得日次
    dt_unix = data['dt']
    dt_formatted_utf = datetime.datetime.fromtimestamp(dt_unix).strftime(
        '%m/%d %H:%M:%S')

    # 都市に関する情報
    city_name = data['name']
    city_id = data['id']

    # 投稿用textの編集
    text = f'天気: {weather_description}\n気温: {main_temp}℃\n湿度: {main_humidity}%\n'

    # 雨の場合はtextに降水量を追加
    if 'rain' in data:
        rain_3h = round(data['rain']['3h'], 2)
        text += f'降水量（3時間あたり）: {rain_3h}％'

    # 雪の場合はtextに降雪量を追加
    if 'snow' in data:
        snow_3h = round(data['snow']['3h'], 2)
        text += f'降雪量（3時間あたり）: {snow_3h}％'

    # condition codeからattachmentのcolorを選択
    # condirion codeについては https://openweathermap.org/weather-conditions を参照
    code = weather_id[0]
    # 晴天
    if weather_id == '800':
        color = '#FF9900'
    # 曇り
    elif code == '7' or code == '8':
        color = '#BEC3C8'
    # 雷
    elif code == '2':
        color = '#FAF500'
    # 雨（霧雨含む）
    elif code == '3' or code == '5':
        color = '#0041FF'
    # 雪
    elif code == '6':
        color = '#C800FF'

    # 固定のattachment要素
    author_name = 'openweathermap.org'
    author_link = 'https://openweathermap.org/'
    author_icon = 'https://openweathermap.org/themes/openweathermap/assets/vendor/owm/img/icons/favicon.ico'
    created_by = 'https://github.com/haruspring-jokt/tenkibot'
    footer_icon = 'https://avatars0.githubusercontent.com/u/26742523?s=400&u=18055b920a2a9e20f62d0e443c96295fcc441811&v=4'

    # attachmentの編集
    attachment['fallback'] = f'{city_name}の天気: {weather_description}'
    attachment['color'] = f'{color}'
    attachment['pretext'] = f'現在の *{city_name}* の天気を表示します。'
    attachment['author_name'] = author_name
    attachment['author_link'] = author_link
    attachment['author_link'] = author_icon
    attachment[
        'title'] = f'Current weather in {city_name} (acquired at {dt_formatted_utf})'
    attachment['title_link'] = f'https://openweathermap.org/city/{city_id}'
    attachment['text'] = text
    attachment['thumb_url'] = f'https://openweathermap.org/img/w/{icon}.png'
    attachment['footer'] = f'created by {created_by}'
    attachment['footer_icon'] = footer_icon
    attachment['mrkdwn_in'] = ['pretext', 'text']

    return attachment
