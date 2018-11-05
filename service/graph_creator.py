# coding: utf-8
"""
matplotlibをつかってグラフを作成するモジュール
"""

import matplotlib.pyplot as plt
import datetime


def create_5_days_weather_graph(data):
    """
    5日間の天気予報データをグラフ化する。
    作成した画像のファイルパスを出力値として返す。
    """

    # jsonから気温データを取得してリスト化する
    forecast_list = data['list']
    # print(len(forecast_list))
    element_list = []

    for forecast in forecast_list:
        element = {}
        element['dt'] = datetime.datetime.fromtimestamp(
            forecast['dt']).strftime('%m/%d %H') + ':00'
        element['temp'] = round(forecast['main']['temp'], 1)
        element['humidity'] = forecast['main']['humidity']
        element_list.append(element)

    city_name = data['city']['name']

    # 気温のみのグラフを作成する
    img_filepath = create_temp_only_gragh(element_list, city_name)

    # 気温と湿度のグラフを作成する
    # img_filepath = create_temp_and_humid_graph(element_list, city_name)

    return img_filepath


def create_temp_only_gragh(element_list, city_name):
    """
    気温のみのグラフを作成し保存する。
    """

    # グラフ入力用データ
    # 日付のリスト作成
    dt_list = [i['dt'] for i in element_list]
    # 気温のリスト作成
    temp_list = [i['temp'] for i in element_list]

    # グラフの新規作成（初期化）
    plt.figure(figsize=(16, 9), dpi=150)

    color = 'tab:blue'
    # データ入力
    plt.plot(dt_list, temp_list, label="temperature", marker='o', color=color)
    # グラフのヘッダーに表示するタイトルの設定
    plt.title("5 days forecast in {}".format(city_name))  # 都市名を入れる
    # x軸のラベル名の設定
    plt.xlabel("datetime")
    plt.tick_params(axis='y', labelcolor=color)
    plt.xticks(rotation=45)
    # # y軸のラベル名の設定
    plt.ylabel("temperature (℃)", color=color)
    # 凡例の設定
    plt.legend()
    # グリッド
    plt.grid(which='major',color='#CEECEF',linestyle='-',)
    plt.grid(which='minor',color='#CEECEF',linestyle='-')

    # グラフを.pngファイルとして保存する
    # TODO 'tmp'フォルダが無かったら作成するくらい気を効かせたい
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S_%f')
    img_filepath = './tmp/5_days_weather_graph_{}.png'.format(now)
    plt.savefig(img_filepath)

    print('[info] graph image saved. filename=[{}]'.format(img_filepath))

    return img_filepath


def create_temp_and_humid_graph(element_list, city_name):
    """
    気温と湿度の2軸が共存するグラフを作成する。
    """

    img_filepath = ''
    return img_filepath
