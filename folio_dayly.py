# coding: utf-8

import datetime
from service import folio_service, slack_messenger

# test
timestamp = datetime.datetime.now()
print('[info] {0} foliodaily is running.'.format(timestamp))

channel = 'CADLS0Y6N'

slack_messenger.post(
        "【定期】FOLIOから資産概要を取得します…",
        channel,
        as_user=False,
        icon_emoji=':moneybag:',
        username='foliobot')
folio_service.send_folio_sammary(channel)
