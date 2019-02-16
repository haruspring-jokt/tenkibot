# encode: utf-8

from repository import njpw_repository
from service import slack_messenger
from service import slack_uploader
from service import os_manager
import slackbot_settings as settings
import inspect


def post_njpw_daily(channel, img=True):

    # 開始メッセージを投稿する
    slack_messenger.post('本日の日記を取得します…', channel, as_user=False)

    # 日記テキストと画像を取得
    text, thumb_paths = njpw_repository.fetch_daily_data()

    # テキストを投稿
    slack_messenger.post(f'>>> {text}', channel, as_user=False)

    # thumbnailを投稿（枚数分だけ）
    for i, thumb_path in enumerate(thumb_paths):
        slack_uploader.upload_image(
            thumb_path, channel, initial_comment=f'thumbnail {i+1}')

    # アップロード完了後画像を削除する
    for thumb_path in thumb_paths:
        os_manager.remove_file(thumb_path)

    print(
        f'[info] finish service method. name=[{inspect.currentframe().f_code.co_name}]'
    )
