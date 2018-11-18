# coding: utf-8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
import re
import datetime

CHROME_BINARY_LOCATION = os.environ['CHROME_BINARY_LOCATION']
CHROME_DRIVER_PATH = os.environ['CHROME_DRIVER_PATH']
FOLIO_MAIL = os.environ['FOLIO_MAIL']
FOLIO_PASS = os.environ['FOLIO_PASS']


def fetch_sammary():
    """資産概要を辞書型で返す
    """

    sammary = {}

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

    sammary['total'] = get_total(driver)
    sammary['gains'] = get_gains(driver)
    sammary['previous_day'] = get_previous_day(driver)

    sammary['status'] = 'OK'
    print('[info] fetched summary data: '.format(sammary))

    driver.quit()

    return sammary


def fetch_theme():
    """テーマの資産に関するデータを辞書型で返す
    """

    theme = {}

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

    theme['deposit'] = get_theme_deposit(driver)
    theme['gains'] = get_theme_gains(driver)
    theme['previous_day'] = get_theme_previous_day(driver)

    theme['status'] = 'OK'
    print('[info] fetched theme data: '.format(theme))

    driver.quit()

    return theme


def fetch_roboad():
    """おまかせの資産に関するデータを辞書型で返す
    """

    roboad = {}

    # webdriverをセットアップしブラウザを起動する。
    driver = setup_webdriver()
    time.sleep(2)
    #トップ画面に遷移する
    driver.get('https://folio-sec.com/')
    # ログインして会員用トップ画面に遷移する
    login(driver, FOLIO_MAIL, FOLIO_PASS)
    time.sleep(2)
    # おまかせの資産画面へ遷移する。
    driver.get('https://folio-sec.com/mypage/assets/omakase')

    roboad['deposit'] = get_roboad_deposit(driver)
    roboad['gains'] = get_roboad_gains(driver)
    roboad['previous_day'] = get_roboad_previous_day(driver)

    roboad['status'] = 'OK'
    print('[info] fetched roboad data: {}'.format(roboad))

    driver.quit()

    return roboad


def fetch_graph_images():
    """テーマの資産・おまかせの資産の推移グラフ画像を取得し保存する
    """

    result = {'path': {}, 'status': ''}

    # webdriberのセットアップ
    driver = setup_webdriver()
    time.sleep(1)
    # トップ画面に遷移する
    driver.get('https://folio-sec.com/')
    # ログインして会員用トップ画面に遷移する
    login(driver, FOLIO_MAIL, FOLIO_PASS)
    time.sleep(1)

    # 財産管理トップ画面へ遷移する。
    driver.get('https://folio-sec.com/mypage/assets')
    # グラフの画像を保存する。
    result['path']['theme'] = capture_screenshot_by_xpath(
        driver, '//*[@id="portal-target"]/main/section/section[1]')

    # おまかせの資産画面へ遷移する。
    driver.get('https://folio-sec.com/mypage/assets/omakase')
    # グラフの画像を保存する。
    result['path']['roboad'] = capture_screenshot_by_xpath(
        driver, '//*[@id="portal-target"]/main/section/section[1]')

    result['status'] = 'OK'
    print('[info] fetched roboad transition graph: '.format(result))

    driver.quit()

    return result


def setup_webdriver():

    options = Options()
    options.binary_location = CHROME_BINARY_LOCATION

    # headlessにする場合は以下の2行についてコメントアウトを外します
    options.add_argument('--headless')
    options.add_argument('--start-maximized')

    options.add_argument('disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(
        options=options, executable_path=CHROME_DRIVER_PATH)

    # ドライバが設定されるまでの待ち時間を設定
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(60)

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


def get_total(driver):
    element = driver.find_element_by_xpath(
        '//*[@id="portal-target"]/header[2]/div/div[1]/div/div[1]/div[2]/span')
    total = int(re.sub(r'[¥|,]', '', element.text))
    return total


def get_gains(driver):
    gains = {}
    element = driver.find_element_by_xpath(
        '//*[@id="portal-target"]/header[2]/div/div[1]/div/div[2]/div[1]/span')
    rate = float(re.sub(r'[（|）|%]', '', element.text)) / 100
    gains['rate'] = rate

    element = driver.find_element_by_xpath(
        '//*[@id="portal-target"]/header[2]/div/div[1]/div/div[2]/div[2]/span[2]'
    )
    amount = int(re.sub(r'[¥|,]', '', element.text))
    gains['amount'] = amount

    return gains


def get_previous_day(driver):
    previous_day = {}
    element = driver.find_element_by_xpath(
        '//*[@id="portal-target"]/header[2]/div/div[1]/div/div[3]/div[1]/span')
    rate = float(re.sub(r'[（|）|%]', '', element.text)) / 100
    previous_day['rate'] = rate

    element = driver.find_element_by_xpath(
        '//*[@id="portal-target"]/header[2]/div/div[1]/div/div[3]/div[2]/span[2]'
    )
    amount = int(re.sub(r'[¥|,]', '', element.text))
    previous_day['amount'] = amount

    return previous_day


def get_theme_deposit(driver):
    element = driver.find_element_by_xpath(
        '//*[@id="portal-target"]/main/section/section[1]/div/div[1]/div/div[1]/p'
    )
    deposit = int(re.sub(r'[¥|,]', '', element.text))
    return deposit


def get_theme_gains(driver):
    gains = {}
    element = driver.find_element_by_xpath(
        '//*[@id="portal-target"]/main/section/section[1]/div/div[1]/div/div[2]/h3/span'
    )
    rate = float(re.sub(r'[（|）|%]', '', element.text)) / 100
    gains['rate'] = rate

    element = driver.find_element_by_xpath(
        '//*[@id="portal-target"]/main/section/section[1]/div/div[1]/div/div[2]/p'
    )
    amount = int(re.sub(r'[¥|,]', '', element.text))
    gains['amount'] = amount

    return gains


def get_theme_previous_day(driver):
    previous_day = {}
    element = driver.find_element_by_xpath(
        '//*[@id="portal-target"]/main/section/section[1]/div/div[1]/div/div[3]/h3/span'
    )
    rate = float(re.sub(r'[（|）|%]', '', element.text)) / 100
    previous_day['rate'] = rate

    element = driver.find_element_by_xpath(
        '//*[@id="portal-target"]/main/section/section[1]/div/div[1]/div/div[3]/p'
    )
    amount = int(re.sub(r'[¥|,]', '', element.text))
    previous_day['amount'] = amount

    return previous_day


def get_roboad_deposit(driver):
    element = driver.find_element_by_xpath(
        '//*[@id="portal-target"]/main/section/section[1]/div/div[1]/div[1]/p')
    deposit = int(re.sub(r'[¥|,]', '', element.text))
    return deposit


def get_roboad_gains(driver):
    gains = {}
    element = driver.find_element_by_xpath(
        '//*[@id="portal-target"]/main/section/section[1]/div/div[1]/div[2]/h3/span'
    )
    rate = float(re.sub(r'[（|）|%]', '', element.text)) / 100
    gains['rate'] = rate

    element = driver.find_element_by_xpath(
        '//*[@id="portal-target"]/main/section/section[1]/div/div[1]/div[2]/p')
    amount = int(re.sub(r'[¥|,]', '', element.text))
    gains['amount'] = amount

    return gains


def get_roboad_previous_day(driver):
    previous_day = {}
    element = driver.find_element_by_xpath(
        '//*[@id="portal-target"]/main/section/section[1]/div/div[1]/div[3]/h3/span'
    )
    rate = float(re.sub(r'[（|）|%]', '', element.text)) / 100
    previous_day['rate'] = rate

    element = driver.find_element_by_xpath(
        '//*[@id="portal-target"]/main/section/section[1]/div/div[1]/div[3]/p')
    amount = int(re.sub(r'[¥|,]', '', element.text))
    previous_day['amount'] = amount

    return previous_day


def capture_screenshot_by_xpath(driver, xpath):

    now = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S_%f')
    filepath = './tmp/selenium_screenshot_{}.png'.format(now)

    png = driver.find_element_by_xpath(xpath).screenshot_as_png
    with open(filepath, 'wb') as f:
        f.write(png)

    return filepath
