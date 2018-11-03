# coding: utf-8
"""
Slackへメッセージを投稿するモジュール
"""

from slackclient import SlackClient
import os

slack_token = os.environ['SLACKBOT_API_TOKEN']


def post(message, channel):
    """
    Slackチャネルにテキストメッセージを投稿する。
    """
    sc = SlackClient(slack_token)

    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=message,
        as_user=True)
