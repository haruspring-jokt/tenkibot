from slackclient import SlackClient
import os
import slackbot_settings as settings

SLACK_TOKEN = settings.API_TOKEN

sc = SlackClient(SLACK_TOKEN)

attachments = []

attachment = {
    'fallback': 'tokyoの天気: 晴れ',
    "color": 'danger',
    'pretext': '現在の *tokyo* の天気を表示します。',
    'author_name': 'tenkibot from openweathermap',
    'author_link': 'https://openweathermap.org/',
    'author_icon': 'https://openweathermap.org/themes/openweathermap/assets/vendor/owm/img/icons/favicon.ico',
    'title': 'Current weather in tokyo',
    'title_link': 'https://openweathermap.org/city/tokyo',
    'text': '天気: 雨\n気温: 13.9℃\n湿度: 57%\n降水量: 1mm\n降雪量: 0.1mm',
    'thumb_url': 'http://openweathermap.org/img/w/09d.png',
    'footer': 'created by https://github.com/haruspring-jokt/tenkibot',
    'footer_icon': 'https://avatars0.githubusercontent.com/u/26742523?s=400&u=18055b920a2a9e20f62d0e443c96295fcc441811&v=4',
    'mrkdwn_in': ['pretext']
}

attachments.append(attachment)

sc.api_call(
    'chat.postMessage',
    channel='CADLS0Y6N',
    attachments = attachments
)
