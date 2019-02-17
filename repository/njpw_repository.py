# coding: utf-8

from selenium.common.exceptions import NoSuchElementException
from service.util import selenium_service
import slackbot_settings as settings
import time
import datetime
import requests
import shutil


def setup_webdriver():
    driver = selenium_service.setup_webdriver(is_mobile=True)
    return driver


def login(driver, mailadress, password):
    # ログイン処理
    element = driver.find_element_by_xpath(
        '//*[@id="mw_wp_form_mw-wp-form-61300"]/form/div/dl[1]/dd/input')
    element.send_keys(mailadress)

    element = driver.find_element_by_xpath(
        '//*[@id="mw_wp_form_mw-wp-form-61300"]/form/div/dl[2]/dd/input')
    element.send_keys(password)

    element = driver.find_element_by_xpath(
        '//*[@id="mw_wp_form_mw-wp-form-61300"]/form/div/p/input')
    element.click()

    # ログイン確認
    element = driver.find_element_by_xpath(
        '//*[@id="join"]/h2'
    )
    assert element.text == 'ログイン完了' , 'Error! ログイン失敗'


def fetch_daily_data():
    driver = setup_webdriver()
    time.sleep(1)

    driver.get('https://sp.njpw.jp/payment/credit/login.php')

    time.sleep(3)

    login(driver, settings.NJPW_MAIL, settings.NJPW_PASS)

    time.sleep(1)

    # トップページへ
    driver.get('https://sp.njpw.jp/')

    # 日記の一番上（最新）へ
    element = driver.find_element_by_xpath('//*[@id="home"]/div[4]/div[2]')
    element.click()

    # 日記テキストを取得
    element = driver.find_element_by_xpath(
        '//*[@id="diary"]/div[1]/article/p[1]')
    text = element.text

    # 枚数分だけ画像ダウンロード
    index = 1
    thumb_paths = []
    while True:
        try:
            thumb_element = driver.find_element_by_xpath(
                f'//*[@id="diary"]/div[1]/article/p[1]/img[{index}]')
            thumb_url = thumb_element.get_attribute('src')

            # 画像の保存
            res = requests.get(thumb_url, stream=True)
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            path = f'./tmp/njpw_daily_{today}_thumb_{index}.jpg'
            with open(path, 'wb') as f:
                shutil.copyfileobj(res.raw, f)
            thumb_paths.append(path)

            index = index + 1
        # 画像が取得できなくなったら終了する
        except NoSuchElementException:
            break

    driver.quit()

    return text, thumb_paths
