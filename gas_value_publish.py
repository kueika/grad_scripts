#!usr/bin/env python
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt     # MQTTのライブラリをインポート
import math
import sys
from grove.adc import ADC
import json


class GroveGasSensorMQ9:

    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def MQ9(self):
        value = self.adc.read(self.channel)
        return value


def on_connect(client, userdata, flag, rc):
    print("Connected with result code " + str(rc))


def on_disconnect(client, userdata, flag, rc):
    if rc != 0:
        print("Unexpected disconnection.")


def on_publish(client, userdata, mid):
    print("publish: {0}".format(mid))


def main():
    client = mqtt.Client()                 # クラスのインスタンス(実体)の作成
    client.on_connect = on_connect         # 接続時のコールバック関数を登録
    client.on_disconnect = on_disconnect   # 切断時のコールバックを登録
    client.on_publish = on_publish         # メッセージ送信時のコールバック
    sensor = GroveGasSensorMQ9(0)          # MQ-9ガスセンサとA0の部分に接続すること

    client.connect("localhost", 1883, 60)  # 接続先は自分自身

    # 通信処理スタート
    client.loop_start()    # subはloop_forever()だが，pubはloop_start()で起動だけさせる

    t = json.dumps({"gas_sensor_value": sensor.MQ9})
    client.publish("pub/gas", t)    # トピック名とメッセージを決めて送信
    print(t)


if __name__ == '__main__':          # importされないときだけmain()を呼ぶ
    main()    # メイン関数を呼び出す
