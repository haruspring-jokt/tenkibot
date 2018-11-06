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
    # img_filepath = create_temp_only_gragh(element_list, city_name)

    # 気温と湿度のグラフを作成する
    img_filepath = create_temp_and_humid_graph(element_list, city_name)

    # TODO 気温（折れ線）と降水量（棒グラフ）のグラフを作成する
    # img_filepath = create_temp_and_rain_graph(data, city_name)

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
    plt.savefig(img_filepath, bbox_inches='tight')

    print('[info] graph image saved. filename=[{}]'.format(img_filepath))

    return img_filepath


def create_temp_and_humid_graph(element_list, city_name):
    """
    気温と湿度の2軸が共存するグラフを作成する。
    """

    # グラフ入力用データ
    # 日付のリスト作成
    dt_list = [i['dt'] for i in element_list]
    # 気温のリスト作成
    temp_list = [i['temp'] for i in element_list]
    # 湿度のリスト
    humid_list = [i['humidity'] for i in element_list]
    # 都市名
    city_name = city_name

    # 1つのグラフに二重のプロットを表示する
    plt.figure()
    fig, ax_temp = plt.subplots(figsize=(16, 9), dpi=150)

    # 1つめ、気温のグラフ
    color = 'tab:blue'
    ax_temp.set_xlabel('datetime')
    ax_temp.set_xticklabels(dt_list, rotation=45)
    ax_temp.set_ylabel('temperature (℃)', color=color)
    ax_temp.plot(dt_list, temp_list, label='temperature', marker='o', color=color)
    ax_temp.tick_params(axis='y', labelcolor=color)

    # 2つめ、湿度のグラフ
    ax_humid = ax_temp.twinx()
    color = 'tab:red'
    ax_humid.set_ylabel('humidity (%)', color=color)
    ax_humid.plot(dt_list, humid_list, label='humidity', marker='^', color=color)
    ax_humid.tick_params(axis='y', labelcolor=color)

    fig.tight_layout() # otherwise the right y-label is slightly clipped

    # グラフのヘッダーに表示するタイトルの設定
    plt.title("5 days forecast in {}".format(city_name))  # 都市名を入れる

    # グラフを.pngファイルとして保存する
    # 'tmp'フォルダを事前に作成しておく必要がある
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S_%f')
    img_filepath = './tmp/5_days_weather_graph_{}.png'.format(now)
    plt.savefig(img_filepath, bbox_inches='tight')

    print('[info] graph image saved. filename=[{}]'.format(img_filepath))

    return img_filepath
