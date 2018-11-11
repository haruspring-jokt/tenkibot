# coding: utf-8
"""
Slackへメッセージを投稿するモジュール
"""

from slackclient import SlackClient
import os

SLACK_TOKEN = os.environ['SLACKBOT_API_TOKEN']


def post(message, channel, as_user=True, username='tenkibot', icon_emoji=':rainbow:'):
    """
    Slackチャネルにテキストメッセージを投稿する。
    """
    sc = SlackClient(SLACK_TOKEN)

    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=message,
        as_user=as_user,
        username=username,
        icon_emoji=icon_emoji)
