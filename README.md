<!-- TOC -->autoauto- [1. about](#1-about)auto- [2. 使用している技術](#2-使用している技術)auto    - [2.1. Python](#21-python)auto    - [2.2. Slackbotフレームワーク](#22-slackbotフレームワーク)auto    - [2.3. ライブラリ](#23-ライブラリ)auto    - [2.4. Heroku](#24-heroku)auto        - [2.4.1. buildpack](#241-buildpack)auto        - [2.4.2. addon](#242-addon)auto    - [2.5. 機能](#25-機能)auto        - [2.5.1. 天気情報に関する機能](#251-天気情報に関する機能)auto            - [2.5.1.1. 使用できるコマンド](#2511-使用できるコマンド)auto            - [2.5.1.2. 都市名について](#2512-都市名について)auto        - [2.5.2. お金に関する機能](#252-お金に関する機能)auto            - [2.5.2.1. コマンド](#2521-コマンド)auto- [3. 利用方法](#3-利用方法)autoauto<!-- /TOC -->

# 1. about

受け取ったメッセージに従って天気の情報をはじめ作者が欲しい情報を表示・通知してくれるslackbotです。

# 2. 使用している技術

## 2.1. Python

```bash
python-3.7.0
```

## 2.2. Slackbotフレームワーク

- [slackbot](https://github.com/lins05/slackbot)
    - メッセージの受け取り、サービスへのディスパッチに使用
- [python-slackclient](https://github.com/slackapi/python-slackclient)
    - botからのメッセージ送信、画像のアップロードなどに使用

## 2.3. ライブラリ

```bash
astroid==2.0.4
certifi==2018.10.15
chardet==3.0.4
colorama==0.4.0
cycler==0.10.0
idna==2.7
isort==4.3.4
kiwisolver==1.0.1
lazy-object-proxy==1.3.1
matplotlib==3.0.1
mccabe==0.6.1
numpy==1.15.3
pylint==2.1.1
pyparsing==2.3.0
python-dateutil==2.7.5
requests==2.20.0
selenium==3.8.0
six==1.11.0
slackbot==0.5.3
slackclient==1.3.0
slacker==0.9.65
urllib3==1.24
websocket-client==0.44.0
wrapt==1.10.11
yapf==0.24.0
```

## 2.4. Heroku

### 2.4.1. buildpack

以下のbuildpackを使用しています。

- heroku/python
- https://github.com/heroku/heroku-buildpack-google-chrome.git
- https://github.com/heroku/heroku-buildpack-chromedriver.git

### 2.4.2. addon

- [Heroku Scheduler Standard](https://elements.heroku.com/addons/scheduler)
    - 定期的な通知をするために使用しています。

## 2.5. 機能

### 2.5.1. 天気情報に関する機能

#### 2.5.1.1. 使用できるコマンド

- `tenki <cityname（都市名）>`
    - その都市に関する現在の天気情報を表示します。`tenki -c <cityname（都市名）>`でもOKです。また、`-c`の代わりに`--current`を使用することもできます。
    - **new!** [attachments](https://api.slack.com/docs/message-attachments)を使った表示ができるようになりました。
    - ![](img/2018-11-26-23-46-30.png)
- `tenki [-o | --old] <cityname（都市名）>`
    - その都市に関する現在の天気情報を表示します。
    - **attachments表示の前に使用した形式なので、今後削除予定のコマンドです。**
    - ![](img/2018-11-26-23-49-57.png)
- `tenki [-5 | --five] <cityname（都市名）>`
    - その都市に関する5日間の天気情報を表示します。
    - ![](img/2018-11-07-23-40-52.png)
- `tenki [-g | --graph] <cityname（都市名）>`
    - その都市に関する5日間の気温と降水量をグラフで表示します。
    - ![](img/2018-11-07-23-41-59.png)

#### 2.5.1.2. 都市名について

天気情報は [OpenWeatherMap](https://openweathermap.org/)から取得しています。そのため、都市名はここに登録されている表記で入力する必要があります。ただし、`chiba`と`chiba-shi`はどちらも千葉市を取得してくれたりと様々なようです。

### 2.5.2. お金に関する機能

#### 2.5.2.1. コマンド

- `folio`
    - [FOLIO](https://folio-sec.com/)から資産状況を取得して通知してくれます。
    - ![](img/2018-11-11-17-58-38.png)
- `folio [-g | --graph]`
    - [FOLIO](https://folio-sec.com/)から資産推移グラフの画像を取得して通知してくれます。
    - ![](img/2018-11-26-23-58-48.png)
- スケジューラ
    - 1日に1回、[FOLIO](https://folio-sec.com/)から資産状況を通知してくれます。

# 3. 利用方法

現在のところ個人もしくは所属組織にて使用する目的で作成しているため、第三者による使用はできません。
