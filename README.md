# grad_scripts

卒業研究・制作のためのスクリプト

## 使用した機材 ラズベリーパイ

- RaspberryPi3 Model B+
- grave sensor hat raspberrypi
- adafruit MQ9 Gas Sensor (CO gas sensor)

## 使用した機材 M5Stack

- M5Stack FIRE
- M5Stack PaHub-Unit
- M5Stack ENV2-Unit

## 使用した技術 Python 以外

- node-red
- mongoDB (NoSQL)
- WebSocket

## 使用した技術 Python

- mongoDB (pymongo)
- paho mqtt

## node-red 環境構築

### node-red インストール

```
npm install -g --unsafe-perm node-red
```

### node-red 起動

```
node-red
```

json で node-red のソーススクリプトをインポート可能

動かすのに必要な node-red ライブラリ

- node-red-contrib-aedes-broker

nodered 上で WebSocket サーバ立ち上げており

```
http://127.0.0.1:1880/getsensor
```

でアクセスすることが可能。リアルタイムでセンサから収集したセンサ値を得られる
