# coding: utf-8
"""
Slackへメッセージを投稿するモジュール
"""

from slackclient import SlackClient
import os

SLACK_TOKEN = os.environ['SLACKBOT_API_TOKEN']


def post(message, channel):
    """
    Slackチャネルにテキストメッセージを投稿する。
    """
    sc = SlackClient(SLACK_TOKEN)

    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=message,
        as_user=True)
