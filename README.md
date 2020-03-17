# TweetRemover
一定時間経過したツイートを削除するやつ。3200ツイートまでしか削除できない。

## 必要なもの
* Twitterの開発者登録
* ↑で得たアクセストークンその他諸々
* ↑を保存するsettings.py
```python:settings.py
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
TARGET = "" # 削除対象アカウントのscreen_name（@から先の文字列）
DAYS = 30   # 何日より古いツイートを削除するか
```