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
