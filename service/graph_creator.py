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
        element_list.append(element)

    # print(element_list)
    # print(len(element_list))

    # 気温のグラフ作成
    dt_list = [i['dt'] for i in element_list]
    temp_list = [i['temp'] for i in element_list]
    # print(temp_list)

    city_name = data['city']['name']

    # グラフの新規作成（初期化）
    plt.figure()

    plt.plot(dt_list, temp_list)
    plt.title("5 days forecast in {}".format(city_name))  # 都市名を入れる
    plt.xlabel("datetime")
    plt.ylabel("temperature (℃)")
    # plt.show()

    now = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S_%f')
    img_filepath = './tmp/5_days_weather_graph_{}.png'.format(now)

    # グラフを.pngファイルとして保存する
    # 'tmp'フォルダを事前に作成しておくこと
    plt.savefig(img_filepath)
    print('[info] graph image saved. filename=[{}]'.format(img_filepath))

    return img_filepath
