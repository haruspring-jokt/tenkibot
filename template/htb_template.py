# coding: utf-8
import urllib.parse as parser
import urllib.request as request
from bs4 import BeautifulSoup

from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply
from service import slack_messenger
from service.htb import htb_service

@listen_to(r'^htb$')
@listen_to(r'^hatebu$')
@listen_to(r'^はて(ぶ|ブ|な|なブックマーク)$')
def post_htb_hotentry(message, *args):

    print(f'[info] listen to message. text=[{message.body["text"]}]')
    channel = message.body['channel']
    slack_messenger.post(
        "はてブのホッテントリを取得します",
        channel,
        as_user=False,
    )

    htb_service.send_htb_hotentry(channel)
