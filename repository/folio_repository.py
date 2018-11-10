# coding: utf-8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

CHROME_BINARY_LOCATION = os.environ['CHROME_BINARY_LOCATION']
CHROME_DRIVER_PATH = os.environ['CHROME_DRIVER_PATH']
FOLIO_MAIL = os.environ['FOLIO_MAIL']
FOLIO_PASS = os.environ['FOLIO_PASS']


def fetch_sammary():

    # webdriverをセットアップしブラウザを起動する。
    driver = setup_webdriver()
    time.sleep(2)
    #トップ画面に遷移する
    driver.get('https://folio-sec.com/')
    # ログインして会員用トップ画面に遷移する
    login(driver, FOLIO_MAIL, FOLIO_PASS)
    time.sleep(2)
    # 財産管理トップ画面へ遷移する。
    driver.get('https://folio-sec.com/mypage/assets')


def setup_webdriver():

    options = Options()
    options.binary_location = CHROME_BINARY_LOCATION
    # headlessにする場合は以下の2行についてコメントアウトを外します
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(
        options=options, executable_path=CHROME_DRIVER_PATH)

    # ドライバが設定されるまでの待ち時間を設定
    driver.implicitly_wait(10)

    return driver


def login(driver, mailadress, password):
    element = driver.find_element_by_xpath(
        '//*[@id="portal-target"]/header/div/div[2]/button')
    element.click()

    # メールアドレスとパスワードを入力
    element = driver.find_element_by_xpath(
        '//*[@id="portal-target"]/header/section/div/div/section/form/label[1]/div[2]/input'
    )
    element.send_keys(mailadress)

    element = driver.find_element_by_xpath(
        '//*[@id="portal-target"]/header/section/div/div/section/form/label[2]/div[2]/input'
    )
    element.send_keys(password)

    # ログインボタンをクリック
    element = driver.find_element_by_xpath(
        '//*[@id="portal-target"]/header/section/div/div/section/form/div[2]/button'
    )
    element.click()
