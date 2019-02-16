# coding: utf-8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import slackbot_settings as settings


def setup_webdriver(is_headless=True, is_mobile=False):

    options = Options()
    options.binary_location = settings.CHROME_BINARY_LOCATION

    # headlessにする場合は以下の2行についてコメントアウトを外します
    if is_headless:
        options.add_argument('--headless')
        options.add_argument('--start-maximized')

    if is_mobile:
        mobile_emulation = {"deviceName": "Pixel 2"}
        options.add_experimental_option('mobileEmulation', mobile_emulation)

    options.add_argument('disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(
        options=options, executable_path=settings.CHROME_DRIVER_PATH)

    # ドライバが設定されるまでの待ち時間を設定
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(60)

    return driver
