# APIドキュメント

## Current weather data

### Weather parameters in API respond

#### sample

以下のリクエストで取得。`?units=metric`とすることで、複数種類のデータに関して単位を変更している。（例：気温＝摂氏、風速＝m/秒など）

ちなみに取得方法はcityのIDでも名前でも色々ある模様。複数都市のデータを取得することもできるみたい

```
http://api.openweathermap.org/data/2.5/weather?units=metric&q=tokyo&APPID={xxxxxxxxxxxxxxx}
```

```json
{
    "coord": {
        "lon": 139.76,
        "lat": 35.68
    },
    "weather": [{
        "id": 701,
        "main": "Mist",
        "description": "mist",
        "icon": "50d"
    }],
    "base": "stations",
    "main": {
        "temp": 19.29,
        "pressure": 1007,
        "humidity": 94,
        "temp_min": 17,
        "temp_max": 21
    },
    "visibility": 10000,
    "wind": {
        "speed": 3.1,
        "deg": 180
    },
    "clouds": {
        "all": 75
    },
    "dt": 1540603800,
    "sys": {
        "type": 1,
        "id": 7505,
        "message": 0.0074,
        "country": "JP",
        "sunrise": 1540587465,
        "sunset": 1540626685
    },
    "id": 1850147,
    "name": "Tokyo",
    "cod": 200
}
```

>  - coord
>     - coord.lon **経度**
>     - coord.lat **緯度**
> - weather (more info Weather condition codes)
>     - weather.id Weather condition id **cityのID。**
>     - weather.main Group of weather parameters (Rain, Snow, Extreme etc.) **天気の概要的な？**
>     - weather.description Weather condition within the group **もう少し詳しい天気**
>     - weather.icon Weather icon id **アイコンのID**
> - base Internal parameter **内部のパラメータ**
> - main
>     - main.temp Temperature. Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit. **温度**
>     - main.pressure Atmospheric pressure (on the sea level, if there is no sea_level or grnd_level data), hPa **気圧**
>     - main.humidity Humidity, % **湿度**
>     - main.temp_min Minimum temperature at the moment. This is deviation from current temp that is possible for large cities and megalopolises geographically expanded (use these parameter optionally). Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit. **最低気温（オプションとして使用するのが適切らしい）**
>     - main.temp_max Maximum temperature at the moment. This is deviation from current temp that is possible for large cities and megalopolises geographically expanded (use these parameter optionally). Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit. **最高気温（これもオプション）**
>     - main.sea_level Atmospheric pressure on the sea level, hPa **海面の気圧**
>     - main.grnd_level Atmospheric pressure on the ground level, hPa **地面の気圧**
> - wind
>     - wind.speed Wind speed. Unit Default: meter/sec, Metric: meter/sec, Imperial: miles/hour. **風速**
>     - wind.deg Wind direction, degrees (meteorological) **風の方向**
> - clouds
>     - clouds.all Cloudiness, % **雲面積の割合？**
> - rain
>     - rain.3h Rain volume for the last 3 hours **直近3時間の降水量**
> - snow
>     - snow.3h Snow volume for the last 3 hours **直近3時間の降雪量**
> - dt Time of data calculation, unix, UTC **UTC形式での時間（UNIX時間）**
> - sys
>     - sys.type Internal parameter **内部のパラメータ**
>     - sys.id Internal parameter **内部のパラメータ**
>     - sys.message Internal parameter **内部のパラメータ**
>     - sys.country Country code (GB, JP etc.) **国コード**
>     - sys.sunrise Sunrise time, unix, UTC **日の出時間（UTC、UNIX）**
>     - sys.sunset Sunset time, unix, UTC **日の入り時間（UTC、UNIX）**
> - id City ID **cityのID**
> - name City name **cityのname**
> - cod Internal parameter **HTTPステータスコード**

> - visibility 
>     - visibility.value Visibility, meter **視程**

## 5 day / 3 hour forecast data

以下のリクエストで取得。

```
http://api.openweathermap.org/data/2.5/forecast?units=metric&q={city}&APPID={API_KEY}
```

### jsonの読み方

jsonサンプルは .\sanple\5_day_3_hour_forecast_data.json を参照

### リストの件数

36件の天気予報がリストとして含まれていて、これをすべて表示するのはなんか違う気がする。1個取得したら2個飛ばすくらいの感じで良いかな～

#### 何時の天気を取得しているのか

- 0, 3, 6, 12, 15, 18, 21時の天気を取得する
- リストの先頭には取得時点の次の時間の天気が入る
    - 15時半にリクエストすると、18時の予報が先頭に入る

