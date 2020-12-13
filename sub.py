#!usr/bin/env python
# -*- coding: utf-8 -*-
import json
import paho.mqtt.client as mqtt     # MQTTのライブラリをインポート

import math

topic: str = "pub/M5stack"


# topic = "pub/gas"

# ブローカーに接続できたときの処理


def on_connect(client, userdata, flag, rc):
    print("Connected with result code " + str(rc))  # 接続できた旨表示
    client.subscribe(topic)  # subするトピックを設定

# ブローカーが切断したときの処理


def on_disconnect(client, userdata, flag, rc):
    if rc != 0:
        print("Unexpected disconnection.")

# メッセージが届いたときの処理


def on_message(client, userdata, msg):
    # msg.topicにトピック名が，msg.payloadに届いたデータ本体が入っている
    # print("Received message '" + str(msg.payload) +
    #       "' on topic '" + msg.topic + "' with QoS " + str(msg.qos)+"msg type is:"+str(json.loads(msg.payload)))
    # gas sensor 用の処理
    # data = json.loads(msg.payload)
    # gas_value = data["gas_sensor_value"]
    # print("gassensor is:", gas_value)
    # M5Stack Sensor
    data = json.loads(msg.payload)
    tmp: float = data["env_temperature"]
    hum: float = data["humidity"]
    body: float = data["body_temperature"]
    number: int = data["deviceID"]
    val: int = math.ceil(wbgt(tmp, hum))
    print("wbgt value is:", val)

    '''
    wbgtの基準
    注意　２５未満
    警戒　２５以上〜２８未満
    厳重警戒　２８以上〜３１未満
    危険　３１以上
    '''
    count += judge_count_wbgt(val)
    print("now count is: ", count)


def wbgt(tmp, hmd) -> float:
    return (hmd - 20) * (math.pow(tmp - 40, 2) * -0.00025 + 0.185) + (11 / 15) * (tmp - 25) + 17.8


def judge_count_wbgt(value) -> int:
    te = 0
    if value >= 25 and value < 28:
        te = 2
    elif value >= 28 and value < 31:
        te = 3
    elif value >= 31:
        te = 4
    else:
        te = 1
    return te


def judge(count) -> int:
    if count > 10:
        # 休憩指示
        return 1
    else:
        return 0

# def judge():


# MQTTの接続設定
def main():
    client = mqtt.Client()                 # クラスのインスタンス(実体)の作成
    client.on_connect = on_connect         # 接続時のコールバック関数を登録
    client.on_disconnect = on_disconnect   # 切断時のコールバックを登録
    client.on_message = on_message         # メッセージ到着時のコールバック

    client.connect("localhost", 1883, 60)  # 接続先は自分自身

    client.loop_forever()                  # 永久ループして待ち続ける


if __name__ == "__main__":
    main()
