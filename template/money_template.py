# coding: utf-8
"""メンションで受け取った（またはチャンネルに投稿された）メッセージから判断し、
実行するサービスをディスパッチする。
お金や資産に関するテンプレート
"""

from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply
from service import folio_service, slack_messenger


@listen_to(r"^folio$")
def post_folio_summary(message):
    """FOLIOのWebページから資産概要を取得し表示する。

    Arguments:
        message {message} -- Slack上で取得したメッセージなど
    """
    print('[info] listen to message. text=[{0}],'.format(message.body['text']))
    channel = message.body['channel']
    slack_messenger.post(
        "FOLIOから資産概要を取得します…",
        channel,
        as_user=False,
        icon_emoji=':moneybag:',
        username='foliobot')
    folio_service.send_folio_sammary(channel)


@listen_to(r"^folio\s(-g|--graph)$")
def post_dolio_detail(message, option):
    """FOLIOのWebページからすべてのテーマ・おまかせ投資それぞれのグラフの画像を取得し表示する。
    コマンド: "folio [-g|--graph]"

    Arguments:
        message {message} -- Slack上で取得したmessage
        option {str} -- オプション文字列
    """
    print('[info] listen to message. text=[{0}],'.format(message.body['text']))
    channel = message.body['channel']
    slack_messenger.post(
        "FOLIOから資産推移のグラフを取得します…",
        channel,
        as_user=False,
        icon_emoji=':moneybag:',
        username='foliobot'
    )
    folio_service.send_folio_detail(channel)
