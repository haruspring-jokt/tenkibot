# coding: utf-8

from repository import folio_repository
from service import slack_messenger


def send_folio_sammary(channel):

    sammary = folio_repository.fetch_sammary()
    post_message = "資産概要の取得に成功しました!\n"
    post_message += "すべての資産: {}\n".format(sammary['total'])
    post_message += "含み損益: {} {}\n".format(sammary['gains']['amount'],
                                           sammary['gains']['rate'])
    post_message += "前日比: {} {}\n".format(sammary['previous_day']['amount'],
                                          sammary['previous_day']['rate'])

    slack_messenger.post(post_message, channel)
