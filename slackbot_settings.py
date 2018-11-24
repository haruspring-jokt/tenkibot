# coding: utf-8

import os

# このbot宛のメッセージで、どの応答にも当てはまらない場合の応答文字列
DEFAULT_REPLY = "`tenki -h` で主な使い方を表示します。"

# プラグインスクリプトを置いてあるサブディレクトリ名のリスト
PLUGINS = ['template']

# ローカルで動かす場合はここにslackbotを利用するためのトークンを記述する
# Herokuにデプロイしているため環境変数から取得
# API_TOKEN = "hogehoge"
API_TOKEN = os.environ['SLACKBOT_API_TOKEN']

# テスト用チャネル（#9_test）
CHANNEL_9_TEST = 'CADLS0Y6N'

CHROME_BINARY_LOCATION = os.environ['CHROME_BINARY_LOCATION']

CHROME_DRIVER_PATH = os.environ['CHROME_DRIVER_PATH']

FOLIO_MAIL = os.environ['FOLIO_MAIL']

FOLIO_PASS = os.environ['FOLIO_PASS']
