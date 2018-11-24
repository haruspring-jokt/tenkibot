# coding: utf-8

from repository import folio_repository
from service import slack_messenger, slack_uploader, os_manager
import slackbot_settings as settings


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


def send_folio_theme(channel):
    """テーマの資産の通知
    """

    theme = folio_repository.fetch_theme()

    if theme['status'] == 'NG':
        post_message = '```データの取得に失敗しました```'
        slack_messenger.post(post_message, channel)

    total = '{:,}'.format(theme['deposit'])
    gains_amount = '{:,}'.format(theme['gains']['amount'])
    gains_rate = '{:.2%}'.format(theme['gains']['rate'])
    previous_amount = '{:,}'.format(theme['previous_day']['amount'])
    previous_rate = '{:.2%}'.format(theme['previous_day']['rate'])

    post_message = "テーマの資産の取得に成功しました!\n"
    post_message += "お預かり資産: {}円\n".format(total)
    post_message += "含み損益: {} ({})\n".format(gains_amount, gains_rate)
    post_message += "前日比: {} ({})\n".format(previous_amount, previous_rate)
    if theme['previous_day']['amount'] > 0:
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


def send_folio_roboad(channel):
    """おまかせの資産の通知
    """

    roboad = folio_repository.fetch_roboad()

    if roboad['status'] == 'NG':
        post_message = '```データの取得に失敗しました```'
        slack_messenger.post(post_message, channel)

    deposit = '{:,}'.format(roboad['deposit'])
    gains_amount = '{:,}'.format(roboad['gains']['amount'])
    gains_rate = '{:.2%}'.format(roboad['gains']['rate'])
    previous_amount = '{:,}'.format(roboad['previous_day']['amount'])
    previous_rate = '{:.2%}'.format(roboad['previous_day']['rate'])

    post_message = "おまかせの資産の取得に成功しました!\n"
    post_message += "お預かり資産: {}円\n".format(deposit)
    post_message += "含み損益: {} ({})\n".format(gains_amount, gains_rate)
    post_message += "前日比: {} ({})\n".format(previous_amount, previous_rate)
    if roboad['previous_day']['amount'] > 0:
        post_message += '前日比がプラスになっています!\n'
    else:
        post_message += '前日比がマイナスになっています…\n'
    post_message += '詳しくは: https://folio-sec.com/mypage/assets/omakase'

    slack_messenger.post(
        post_message,
        channel,
        as_user=False,
        icon_emoji=':moneybag:',
        username='foliobot')

    print('[info] message is posted. ch:[{ch}] message:[{me}]'.format(
        ch=channel, me=post_message[:10]))


def send_folio_detail(channel):
    """FOLIO グラフ画像の通知

    Arguments:
        channel {str} -- チャンネルID
    """

    print('[info] called service method. name=[send_folio_detail]')

    # 投稿する画像をそれぞれ取得して保存する
    # ファイルパスを辞書型で返してもらう
    result = folio_repository.fetch_graph_images()

    if result['status'] == 'NG':
        post_message = '```データの取得に失敗しました```'
        slack_messenger.post(post_message, channel)

    # 画像を投稿する（テーマの資産）
    slack_uploader.upload_image(
        result['path']['theme'],
        channel,
        initial_comment='取得元: https://folio-sec.com/mypage/assets',
        title='transition graph about theme assets.',
        as_user=False,
        icon_emoji=':moneybag:',
        username='foliobot')

    # 画像を投稿する（おまかせの資産）
    slack_uploader.upload_image(
        result['path']['roboad'],
        channel,
        initial_comment='取得元: https://folio-sec.com/mypage/assets/omakase',
        title='transition graph about roboad assets.',
        as_user=False,
        icon_emoji=':moneybag:',
        username='foliobot')

    # アップロード完了後画像を削除する
    os_manager.remove_file(result['path']['theme'])
    os_manager.remove_file(result['path']['roboad'])

    print('[info] finish service method. name=[send_folio_detail]')


def post_daily_folio_notify(channel):

    icon_emoji = ':moneybag:'
    username = 'foliobot'

    # 開始メッセージを投稿する
    slack_messenger.post(
        "【定期】FOLIOから資産概要を取得します…",
        channel,
        as_user=False,
        icon_emoji=icon_emoji,
        username=username)

    # FOLIOサイトから一連のデータを取得
    sammary, theme, roboad = folio_repository.fetch_daily_data()

    # それぞれメッセージを作成
    sammary_message = make_sammary_message(sammary)
    theme_message = make_theme_message(theme)
    roboad_message = make_roboad_message(roboad)

    # 資産概要を投稿する
    slack_messenger.post(
        sammary_message,
        channel,
        as_user=False,
        icon_emoji=icon_emoji,
        username=username)

    # テーマの資産状況を投稿する
    slack_messenger.post(
        theme_message,
        channel,
        as_user=False,
        icon_emoji=icon_emoji,
        username=username)

    # おまかせの資産状況を投稿する
    slack_messenger.post(
        roboad_message,
        channel,
        as_user=False,
        icon_emoji=icon_emoji,
        username=username)


def make_sammary_message(sammary):

    total = '{:,}'.format(sammary['total'])
    gains_amount = '{:,}'.format(sammary['gains']['amount'])
    gains_rate = '{:.2%}'.format(sammary['gains']['rate'])
    previous_amount = '{:,}'.format(sammary['previous_day']['amount'])
    previous_rate = '{:.2%}'.format(sammary['previous_day']['rate'])

    post_message = "資産概要の取得に成功しました!\n"
    post_message += f"すべての資産: {total}円\n"
    post_message += f"含み損益: {gains_amount} ({gains_rate})\n"
    post_message += f"前日比: {previous_amount} ({previous_rate})\n"
    if sammary['previous_day']['amount'] > 0:
        post_message += '前日比がプラスになっています!\n'
    else:
        post_message += '前日比がマイナスになっています…\n'
    post_message += '詳しくは: https://folio-sec.com/mypage/assets'

    return post_message


def make_theme_message(theme):

    total = '{:,}'.format(theme['deposit'])
    gains_amount = '{:,}'.format(theme['gains']['amount'])
    gains_rate = '{:.2%}'.format(theme['gains']['rate'])
    previous_amount = '{:,}'.format(theme['previous_day']['amount'])
    previous_rate = '{:.2%}'.format(theme['previous_day']['rate'])

    post_message = "テーマの資産の取得に成功しました!\n"
    post_message += f"お預かり資産: {total}円\n"
    post_message += f"含み損益: {gains_amount} ({gains_rate})\n"
    post_message += f"前日比: {previous_amount} ({previous_rate})\n"
    if theme['previous_day']['amount'] > 0:
        post_message += '前日比がプラスになっています!\n'
    else:
        post_message += '前日比がマイナスになっています…\n'
    post_message += '詳しくは: https://folio-sec.com/mypage/assets'

    return post_message


def make_roboad_message(roboad):

    deposit = '{:,}'.format(roboad['deposit'])
    gains_amount = '{:,}'.format(roboad['gains']['amount'])
    gains_rate = '{:.2%}'.format(roboad['gains']['rate'])
    previous_amount = '{:,}'.format(roboad['previous_day']['amount'])
    previous_rate = '{:.2%}'.format(roboad['previous_day']['rate'])

    post_message = "おまかせの資産の取得に成功しました!\n"
    post_message += f"お預かり資産: {deposit}円\n"
    post_message += f"含み損益: {gains_amount} ({gains_rate})\n"
    post_message += f"前日比: {previous_amount} ({previous_rate})\n"
    if roboad['previous_day']['amount'] > 0:
        post_message += '前日比がプラスになっています!\n'
    else:
        post_message += '前日比がマイナスになっています…\n'
    post_message += '詳しくは: https://folio-sec.com/mypage/assets/omakase'

    return post_message
