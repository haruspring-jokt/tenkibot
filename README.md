# about

受け取ったメッセージに従って天気の情報を表示してくれるslackbotです。

## Slackbotフレームワーク

- [slackbot](https://github.com/lins05/slackbot)
    - メッセージの受け取り、サービスへのディスパッチに使用
- [python-slackclient](https://github.com/slackapi/python-slackclient)
    - botからのメッセージ送信、画像のアップロードなどに使用

## 使用できるコマンド

- `tenki <cityname（都市名）>`
    - その都市に関する現在の天気情報を表示します。`tenki -c <cityname（都市名）>`でもOKです。また、`-c`の代わりに`--current`を使用することもできます。
    - ![](img/2018-11-07-23-37-04.png)
- `tenki [-5 | --five] <cityname（都市名）>`
    - その都市に関する5日間の天気情報を表示します。
    - ![](img/2018-11-07-23-40-52.png)
- `tenki [-g | --graph] <cityname（都市名）>`
    - その都市に関する5日間の気温と降水量をグラフで表示します。
    - ![](img/2018-11-07-23-41-59.png)

### 都市名について

天気情報は [OpenWeatherMap](https://openweathermap.org/)から取得しています。そのため、都市名はここに登録されている表記で入力する必要があります。ただし、`chiba`と`chiba-shi`はどちらも千葉市を取得してくれたりと様々なようです。
