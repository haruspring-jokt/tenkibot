# coding: utf-8

import logging
from logging import getLogger, StreamHandler, Formatter

# TODO ログ出力設定をここでまとめたい
def conf_logger(logger_name, level=logging.INFO):
    """loggerを設定し返却
    
    Keyword Arguments:
        level {[type]} -- loggingレベル (default: {logging.INFO})
    
    Returns:
        logger -- loggerを返却
    """
    logger = getLogger(logger_name).getChild("sub")

    logger.parent.setLevel(level)

    stream_handler = StreamHandler()

    stream_handler.setLevel(logging.DEBUG)

    handler_format = Formatter(
        '[%(asctime)s] [%(name)s] [%(levelname)s] [%(module)s] %(message)s')
    stream_handler.setFormatter(handler_format)

    # loggerにhandlerをセット
    logger.parent.addHandler(stream_handler)

    logger.debug("finish logger config")
