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
    # message.send("```folio```")
    print('[info] listen to message. text=[{0}],'.format(message.body['text']))
    # message.send('{}'.format("FOLIOから資産概要を取得します…"))
    channel = message.body['channel']
    slack_messenger.post(
        "FOLIOから資産概要を取得します…",
        channel,
        as_user=False,
        icon_emoji=':moneybag:',
        username='foliobot')
    folio_service.send_folio_sammary(channel)
