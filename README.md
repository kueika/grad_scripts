# grad_scripts

卒業研究・制作のためのスクリプト 

## 使用した技術 Python
+ mongoDB (pymongo)
+ paho mqtt

## node-red環境構築
### node-red インストール
```
npm install -g --unsafe-perm node-red
```
### node-red起動
```
node-red
```
jsonでnode-redのソーススクリプトをインポート可能

動かすのに必要なnode-redライブラリ

+ node-red-contrib-aedes-broker

nodered上でWebSocketサーバ立ち上げており

```
http://127.0.0.1:1880/getsensor
```
でアクセスすることが可能。リアルタイムでセンサから収集したセンサ値を得られる
