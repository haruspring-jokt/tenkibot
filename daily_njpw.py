# coding: utf-8
"""新日本プロレスのモバイルサイトから最新の日記を取得する
"""

import datetime
import slackbot_settings
from service.njpw import njpw_service as njpw
import os

RUN_FLUG = True


def run():

    timestamp = datetime.datetime.now()
    print(f'[info] {timestamp} njpw_daily is running.')

    # 投稿先チャンネル
    channel = slackbot_settings.NJPW_POST_CHANNEL

    # 最新の日記をSlackに投稿する
    njpw.post_njpw_daily(channel)


if __name__ == '__main__':
    if RUN_FLUG:
        run()
