# coding: utf-8

from repository import folio_repository
from service import slack_messenger


def send_folio_sammary(channel):

    sammary = folio_repository.fetch_sammary()

    if sammary['status'] == 'NG':
        post_message = '```データの取得に失敗しました```'
        slack_messenger.post(post_message, channel)

    total = '{:,}'.format(sammary['total'])
    gains_amount = '{:,}'.format(sammary['gains']['amount'])
    gains_rate = '{:.2%}'.format(sammary['gains']['rate'])
    previous_amount = '{:,}'.format(sammary['previous_day']['amount'])
    previous_rate = '{:.2%}'.format(sammary['previous_day']['rate'])

    post_message = "資産概要の取得に成功しました!\n"
    post_message += "すべての資産: {}円\n".format(total)
    post_message += "含み損益: {} ({})\n".format(gains_amount, gains_rate)
    post_message += "前日比: {} ({})\n".format(previous_amount, previous_rate)
    if sammary['previous_day']['amount'] > 0:
        post_message += '前日比がプラスになっています!\n'
    else:
        post_message += '前日比がマイナスになっています…\n'
    post_message += '詳しくは: https://folio-sec.com/mypage/assets'

    slack_messenger.post(
        post_message,
        channel,
        as_user=False,
        icon_emoji=':moneybag:',
        username='foliobot')

    print('[info] message is posted. ch:[{ch}] message:[{me}]'.format(
        ch=channel, me=post_message[:10]))
