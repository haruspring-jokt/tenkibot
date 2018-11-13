# coding: utf-8
"""日次でFOLIOのWebサイトから資産状況を取得しSlackに投稿する。
"""

import datetime
from service import folio_service, slack_messenger
import slackbot_settings


def post_daily_folio_notify():
    """FOLIOのWebサイトから資産概要と個別資産の状況を通知する。
    """
    # test
    timestamp = datetime.datetime.now()
    print('[info] {0} foliodaily is running.'.format(timestamp))

    # 現状は投稿するチャネルを固定 設定ファイルから取得
    channel = slackbot_settings.CHANNEL_9_TEST

    # 資産概要を取得し投稿する
    # メッセージが途切れないように
    slack_messenger.post(
        "【定期】FOLIOから資産概要を取得します…",
        channel,
        as_user=False,
        icon_emoji=':moneybag:',
        username='foliobot')

    folio_service.send_folio_sammary(channel)

    # 個別の状況：テーマの資産
    slack_messenger.post(
        "テーマの資産を取得します…",
        channel,
        as_user=False,
        icon_emoji=':moneybag:',
        username='foliobot')

    folio_service.send_folio_theme(channel)

    # 個別の状況：おまかせ（ロボアドバイザー）の資産
    slack_messenger.post(
        "おまかせの資産を取得します…",
        channel,
        as_user=False,
        icon_emoji=':moneybag:',
        username='foliobot')

    folio_service.send_folio_roboad(channel)


if __name__ == '__main__':
    post_daily_folio_notify()
