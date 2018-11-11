# coding: utf-8

from repository import folio_repository
from service import slack_messenger


def send_folio_sammary(channel):

    sammary = folio_repository.fetch_sammary()

    total = '{:,}'.format(sammary['total'])
    gains_amount = '{:,}'.format(sammary['gains']['amount'])
    gains_rate = '{:.2%}'.format(sammary['gains']['rate'])
    previous_amount = '{:,}'.format(sammary['previous_day']['amount'])
    previous_rate = '{:.2%}'.format(sammary['previous_day']['rate'])

    post_message = "資産概要の取得に成功しました!\n"
    post_message += "すべての資産: {}円\n".format(total)
    post_message += "含み損益: {} ({})\n".format(gains_amount, gains_rate)
    post_message += "前日比: {} ({})\n".format(sammary['previous_day']['amount'],
                                          sammary['previous_day']['rate'])
    if sammary['previous_day']['amount'] > 0:
        post_message += '前日比がプラスになっています!'
    else:
        post_message += '前日比がマイナスになっています…'

    slack_messenger.post(post_message, channel)
