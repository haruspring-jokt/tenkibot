# coding: utf-8
"""
Slackへメッセージを投稿するモジュール
"""

from slackclient import SlackClient
import os
import slackbot_settings as settings

SLACK_TOKEN = settings.API_TOKEN


def post(message,
         channel,
         as_user=True,
         username='秘書',
         icon_emoji=':secretary:'):
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


def post_attachment(attachments,
                    channel,
                    as_user=True,
                    username='秘書',
                    icon_emoji=':secretary:'):
    """Slackチャネルにattachment形式で投稿する。
    """
    sc = SlackClient(SLACK_TOKEN)

    sc.api_call(
        'chat.postMessage',
        channel=channel,
        attachments=attachments,
        as_user=as_user,
        username=username,
        icon_emoji=icon_emoji)
