<!-- TOC -->

- [about](#about)
- [使用している技術](#使用している技術)
    - [Python](#python)
    - [Slackbotフレームワーク](#slackbotフレームワーク)
    - [ライブラリ](#ライブラリ)
    - [Heroku](#heroku)
        - [buildpack](#buildpack)
        - [addon](#addon)
    - [機能](#機能)
        - [天気情報に関する機能](#天気情報に関する機能)
            - [使用できるコマンド](#使用できるコマンド)
            - [都市名について](#都市名について)
        - [お金に関する機能](#お金に関する機能)
            - [コマンド](#コマンド)
- [利用方法](#利用方法)

<!-- /TOC -->

# about

受け取ったメッセージに従って天気の情報をはじめ作者が欲しい情報を表示・通知してくれるslackbotです。

# 使用している技術

## Python

```bash
python-3.7.0
```

## Slackbotフレームワーク

- [slackbot](https://github.com/lins05/slackbot)
    - メッセージの受け取り、サービスへのディスパッチに使用
- [python-slackclient](https://github.com/slackapi/python-slackclient)
    - botからのメッセージ送信、画像のアップロードなどに使用

## ライブラリ

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
selenium==3.141.0
six==1.11.0
slackbot==0.5.3
slackclient==1.3.0
slacker==0.9.65
urllib3==1.24
websocket-client==0.44.0
wrapt==1.10.11
yapf==0.24.0
```

## Heroku

### buildpack

以下のbuildpackを使用しています。

- heroku/python
- https://github.com/heroku/heroku-buildpack-google-chrome.git
- https://github.com/heroku/heroku-buildpack-chromedriver.git

### addon

- Heroku Scheduler Standard
    - 定期的な通知をするために使用しています。

## 機能

### 天気情報に関する機能

#### 使用できるコマンド

- `tenki <cityname（都市名）>`
    - その都市に関する現在の天気情報を表示します。`tenki -c <cityname（都市名）>`でもOKです。また、`-c`の代わりに`--current`を使用することもできます。
    - ![](img/2018-11-07-23-37-04.png)
- `tenki [-5 | --five] <cityname（都市名）>`
    - その都市に関する5日間の天気情報を表示します。
    - ![](img/2018-11-07-23-40-52.png)
- `tenki [-g | --graph] <cityname（都市名）>`
    - その都市に関する5日間の気温と降水量をグラフで表示します。
    - ![](img/2018-11-07-23-41-59.png)

#### 都市名について

天気情報は [OpenWeatherMap](https://openweathermap.org/)から取得しています。そのため、都市名はここに登録されている表記で入力する必要があります。ただし、`chiba`と`chiba-shi`はどちらも千葉市を取得してくれたりと様々なようです。

### お金に関する機能

#### コマンド

- `folio`
    - [FOLIO](https://folio-sec.com/)から資産状況を取得して通知してくれます。
    - ![](img/2018-11-11-17-58-38.png)

# 利用方法

現在のところ個人もしくは所属組織にて使用する目的で作成しているため、第三者による使用はできません。
