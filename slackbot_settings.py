# coding: utf-8

import os

# このbot宛のメッセージ（@メンション）で、どの応答にも当てはまらない場合の応答文字列
DEFAULT_REPLY = "`tenki -h` で主な使い方を表示します。"

# slackbotのプラグインスクリプトを置いてあるサブディレクトリ名のリスト
PLUGINS = ['template']

# slackbotを利用するためのトークンを記述する
# トークンは https://{ワークスペース}.slack.com/apps/manage/custom-integrations で確認できる
API_TOKEN = os.environ['SLACKBOT_API_TOKEN']

# テスト用チャネル（#9_test）
# 定期投稿などで使用する
DEFAULT_CHANNEL = 'CADLS0Y6N'

# https://openweathermap.org/ のAPIキー
OWM_API_TOKEN = os.environ['OWM_API_KEY']

# tenkibot: デフォルトの都市
DEFAULT_CITY = 'tokyo'

# seleniumで使用するChromeバイナリのパス
CHROME_BINARY_LOCATION = os.environ['CHROME_BINARY_LOCATION']

# seleniumで使用するChrome Web Driverのパス
CHROME_DRIVER_PATH = os.environ['CHROME_DRIVER_PATH']

# https://folio-sec.com/ ログイン用メールアドレス
FOLIO_MAIL = os.environ['FOLIO_MAIL']

# https://folio-sec.com/ ログイン用パスワード
FOLIO_PASS = os.environ['FOLIO_PASS']

# 新日本プロレス関係の投稿先チャンネル
NJPW_POST_CHANNEL = 'njpw'

# 新日本プロレスモバイルサイト ログイン用メールアドレス
NJPW_MAIL = os.environ['NJPW_MAIL']

# 新日本プロレスモバイルサイト ログイン用パスワード
NJPW_PASS = os.environ['NJPW_PASS']
