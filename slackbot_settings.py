# coding: utf-8

import os

# このbot宛のメッセージで、どの応答にも当てはまらない場合の応答文字列
DEFAULT_REPLY = "`tenki -h` で主な使い方を表示します。"

# プラグインスクリプトを置いてあるサブディレクトリ名のリスト
PLUGINS = ['plugins']

# ローカルで動かす場合はここにslackbotを利用するためのトークンを記述する
# Herokuにデプロイしているため環境変数から取得
# API_TOKEN = "hogehoge"
API_TOKEN = os.environ['SLACKBOT_API_TOKEN']
