# about

[https://github.com/lins05/slackbot](https://github.com/lins05/slackbot)を使っています。

## 注意

`slackbot_settings.py`は自分で用意してください。

```python
# coding: utf-8

# botアカウントのトークンを指定
API_TOKEN = "{トークンをコピペ}"

# このbot宛のメッセージで、どの応答にも当てはまらない場合の応答文字列
DEFAULT_REPLY = "`@tenkibot 使い方` でコマンド一覧を表示します。"

# プラグインスクリプトを置いてあるサブディレクトリ名のリスト
PLUGINS = ['plugins']
```

## 対応地域

会社のSlackチャネルで使用することを前提にしているため、現在は東京にしか対応していません。

順次全国の天気を取得できるような機能追加を考えています。