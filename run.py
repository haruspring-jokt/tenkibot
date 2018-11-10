# coding: utf-8

from slackbot.bot import Bot
import datetime
from template import tenkibot_template
# import logging
# from logging import getLogger, StreamHandler, Formatter
# from service import logger_manager

def main():
    bot = Bot()
    bot.run()
    # logger test
    # logger = getLogger("logger")
    # logger_manager.conf_logger("logger", level=logging.DEBUG)
    # logger.debug("tenkibot is running.")


if __name__ == "__main__":
    timestamp = datetime.datetime.now()
    print('[info] {0} tenkibot is running.'.format(timestamp))
    main()
