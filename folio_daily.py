# coding: utf-8
"""日次でFOLIOのWebサイトから資産状況を取得しSlackに投稿する。
"""

import datetime
from service import folio_service, slack_messenger
import slackbot_settings


def run():
    """日次FOLIO通知サービスを呼び出す。
    """
    # test
    timestamp = datetime.datetime.now()
    print('[info] {0} foliodaily is running.'.format(timestamp))

    channel = slackbot_settings.CHANNEL_9_TEST

    folio_service.post_daily_folio_notify(channel)


if __name__ == '__main__':
    run()
