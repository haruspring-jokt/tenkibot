# coding: utf-8

import datetime
import slackbot_settings
from service.htb import htb_service
import os
from service import slack_messenger


def run():

    timestamp = datetime.datetime.now()
    print(f'[info] {timestamp} htb_daily is running.')

    # 投稿先チャンネル
    channel = '9_test'

    slack_messenger.post(
        "はてブのホッテントリを取得します",
        channel,
        as_user=False,
    )

    # 最新の日記をSlackに投稿する
    htb_service.send_htb_hotentry(channel)

if __name__ == '__main__':
    run()
