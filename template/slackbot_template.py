# coding: utf-8
"""
このslackbot自体についてのディスパッチ用テンプレート。
"""

from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply
from service import tenkibot_service, slack_messenger
import re

@respond_to('help', re.IGNORECASE)
@respond_to('使い方', re.IGNORECASE)
@respond_to('ヘルプ', re.IGNORECASE)
def post_slackbot_help(message):
    pass

