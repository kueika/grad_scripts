import math
import json
import paho.mqtt.client as mqtt
from time import sleep
from pymongo import ASCENDING
from pymongo import DESCENDING
from pymongo import MongoClient


class MongoFindClass(object):

    def __init__(self, dbName, collectionName):
        self.client = MongoClient()
        self.db = self.client[dbName]  # DB名を設定
        self.collection = self.db.get_collection(collectionName)

    def find_one(self, projection=None, filter=None, sort=None):
        return self.collection.find_one(projection=projection, filter=filter, sort=sort)

    def find(self, projection=None, filter=None, sort=None):
        return self.collection.find(projection=projection, filter=filter, sort=sort)

# 長さの取得 mongo.find.count()


def main():
    client = mqtt.Client()                 # クラスのインスタンス(実体)の作成
    client.on_connect = on_connect         # 接続時のコールバック関数を登録
    client.on_disconnect = on_disconnect   # 切断時のコールバックを登録
    client.on_publish = on_publish         # メッセージ送信時のコールバック
    client.connect("localhost", 1883, 60)  # 接続先は自分自身
    mongo = MongoFindClass('sotuken', 'm5stack01_test')
    mongo_MQ9 = MongoFindClass('sotuken', 'MQ9')
    last_tail_id_m5 = ""
    count = 0
    find = mongo.find()
    findMQ9 = mongo_MQ9.find()
    client.loop_start()    # subはloop_forever()だが，pubはloop_start()で起動だけさせる
    mes = json.dumps({"message": "Please take a rest"})
    while True:
        # ここからは永久ループ入るように
        print('====m5要素====')
        tail_m501 = find[find.count()-1]
        tail_id = str(tail_m501['_id'])
        temp = tail_m501['temp']
        hum = tail_m501['hum']
        # wbgtの値は小数点切り上げで計算
        wbgt_val = math.ceil(wbgt(temp, hum))
        print(wbgt_val)
        print(tail_m501)
        # id違う→新しいデータなので、熱中症のカウント処理をすること
        if last_tail_id_m5 != tail_id:
            last_tail_id_m5 = tail_id
            count += judge_count_wbgt(wbgt_val)
        # 一定回数のカウント処理を行った後に休憩メッセージを飛ばし、カウントを初期化する
        if count > 5:
            client.publish("sub/M5stack", mes)
            count = 0
        print("this is the count : ", count)
        print('====MQ9====')
        tail_MQ9 = findMQ9[findMQ9.count()-1]
        print(tail_MQ9)
        sleep(1)

# 熱中症指数wbgtの近似計算式


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

# ブローカーに接続できたときの処理


def on_connect(client, userdata, flag, rc):
    print("Connected with result code " + str(rc))

# ブローカーが切断したときの処理


def on_disconnect(client, userdata, flag, rc):
    if rc != 0:
        print("Unexpected disconnection.")

# publishが完了したときの処理


def on_publish(client, userdata, mid):
    print("publish: {0}".format(mid))


if __name__ == "__main__":
    main()
