# coding: utf-8
"""
Slackへ画像をアップロードするモジュール
"""

from slackclient import SlackClient
import os

slack_token = os.environ['SLACKBOT_API_TOKEN']


def upload_image(filepath,
                 channels,
                 initial_comment=None,
                 title='uploaded image',
                 as_user=True,
                 username='tenkibot',
                 icon_emoji=':rainbow:'):
    """
    受け取ったファイルパスの画像をSlackチャネルにアップロードする。
    filepath: 投稿する画像のファイルパス
    channels: 投稿先チャネルのIDまたは'#'以降のチャネル名
    initial_comment: 画像を投稿する前に投稿するメッセージ
    title: ファイル上部に表示されるタイトル
    """
    sc = SlackClient(slack_token)

    with open(filepath, 'rb') as img_content:
        # 画像アップロード
        result = sc.api_call(
            "files.upload",
            channels=channels,
            file=img_content,
            title=title,
            initial_comment=initial_comment,
            as_user=as_user,
            username=username,
            icon_emoji=icon_emoji)

    if result['ok'] == True:
        print(f'[info] image uploaded. channel=[{channels}], image=[{filepath}]')
    else:
        return False
