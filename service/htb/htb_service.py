# encode: utf-8

from service import slack_messenger
from service import slack_uploader
from service import os_manager
import slackbot_settings as settings
import inspect
import urllib.parse as parser
import urllib.request as request
from bs4 import BeautifulSoup
import datetime


def send_htb_hotentry(channel):

    link = 'http://b.hatena.ne.jp/hotentry/all'

    # ホッテントリリストを取得する
    hotentry_list = fetch_hotentry_list(link)

    # NGエントリを除外する
    comp_list, ng_count = exclude_ng_entry(hotentry_list)

    # 投稿用attachmentsを作成する
    attachments = []
    attachment = make_attachment(comp_list, ng_count)
    attachments.append(attachment)

    # slackチャンネルに投稿する
    slack_messenger.post_attachment(attachments, channel, as_user=False)

    print(
        f'[info] finish service method. name=[{inspect.currentframe().f_code.co_name}]'
    )


def fetch_hotentry_list(link):

    response = request.urlopen(link)
    html = response.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")
    elements = soup.select('h3.entrylist-contents-title > a')

    hotentry_list = []

    for e in elements:
        entry = {}
        entry['href'] = e['href']
        entry['title'] = e['title']
        hotentry_list.append(entry)

    return hotentry_list


def exclude_ng_entry(entry_list):

    ng_list = ['togetter.com', 'diamond.jp', 'delete-all.hatenablog.com']

    ng_count = 0

    for e in entry_list:
        for ng in ng_list:
            if ng in e['href']:
                entry_list.remove(e)
                ng_count = ng_count + 1

    return entry_list, ng_count


def make_attachment(
        entry_list,
        ng_count,
        color='good',
        author_name='b.hatena.ne.jp',
        author_link='http://b.hatena.ne.jp/',
        author_icon='http://b.hatena.ne.jp/favicon.ico',
        title_link='http://b.hatena.ne.jp/hotentry/all',
        footer='created by https://github.com/haruspring-jokt/tenkibot',
        footer_icon='https://avatars0.githubusercontent.com/u/26742523?s=400&u=18055b920a2a9e20f62d0e443c96295fcc441811&v=4'
):

    # fieldsを作成する
    fields = []
    for e in entry_list:
        field = {'title': e['title'], 'value': e['href'], 'short': False}
        fields.append(field)

    dt = datetime.datetime.now().strftime("%m/%d %H:%M")

    # attachmentの編集
    attachment = {}

    attachment['fallback'] = f'{dt}のホットエントリ (除外: {ng_count}件)'
    attachment['color'] = color
    attachment['pretext'] = f'{ng_count}件のエントリがNG除外されました。'

    attachment['author_name'] = author_name
    attachment['author_link'] = author_link
    attachment['author_icon'] = author_icon

    attachment['title'] = f'{dt}のホットエントリ'
    attachment['title_link'] = title_link
    attachment['fields'] = fields
    attachment['footer'] = footer
    attachment['footer_icon'] = footer_icon

    return attachment
