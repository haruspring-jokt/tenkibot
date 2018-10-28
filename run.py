# coding: utf-8

from slackbot.bot import Bot
import datetime
from template import tenkibot_template

def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    timestamp = datetime.datetime.now()
    print('[info] {0} tenkibot is running.'.format(timestamp))
    main()
