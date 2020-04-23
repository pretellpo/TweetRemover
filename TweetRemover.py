# -*- coding:utf-8 -*-
import json
import requests
from requests_oauthlib import OAuth1Session
import settings
import datetime
import pytz
import sys

# setting.pyから読み込み
CONSUMER_KEY = settings.CONSUMER_KEY
CONSUMER_SECRET = settings.CONSUMER_SECRET
ACCESS_TOKEN = settings.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = settings.ACCESS_TOKEN_SECRET
TARGET = settings.TARGET
DAYS = settings.DAYS

# Twitter
twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET,
                        ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# ツイート数を取得
url_show = "https://api.twitter.com/1.1/users/show.json"
params = {"screen_name": TARGET}
req_result_show = twitter.get(url_show, params=params)
if req_result_show.status_code == 200:
	user = json.loads(req_result_show.text)
	statuses_count = user["statuses_count"]
	max_id = user["status"]["id"] + 1 # max_idを暫定的に最新ツイート+1にする
else:
	print("ERROR: %d" % req_result_show.status_code)
	sys.exit()

# ループ回数を計算
tweets = min(3200,statuses_count)
roop = tweets // 200
if (tweets % 200) != 0:
	roop += 1


# 削除対象ツイートの判定
now_time = datetime.datetime.now(pytz.utc) # タイムゾーン付きなのでpytz
delta = datetime.timedelta(days=DAYS)
target_time = now_time - delta
delete_target = []

# ツイートを3200件まで掘り返す
exist_tweet = 0
delete_tweet = 0
url_timeline = "https://api.twitter.com/1.1/statuses/user_timeline.json"
delete_list = []
for i in range(roop):
	params = {'screen_name': TARGET, "count": 200, "exclude_replies": False, "include_rts": True, "max_id": max_id}
	req_result_tl = twitter.get(url_timeline, params=params)
	if req_result_tl.status_code == 200:
		user_timeline = json.loads(req_result_tl.text)
		for i in user_timeline:
			if max_id > i["id"]:
				max_id = i["id"] - 1	# max_idを古いものに更新していく
			tweet_id = i["id"]
			created_at = datetime.datetime.strptime(i["created_at"], '%a %b %d %H:%M:%S %z %Y')
			if created_at < target_time:	# 対象期間より古いツイートなら削除リストに入れる
				print(i["text"])
				delete_list.append(tweet_id)
				delete_tweet += 1
			exist_tweet += 1
			
	else:
		print("ERROR: %d" % req_result_tl.status_code)
		break


# 削除
for i in delete_list:
	url_delete = "https://api.twitter.com/1.1/statuses/destroy/" + str(i) + ".json"
	req_result_del = twitter.post(url_delete)
	if req_result_del.status_code != 200:
		print("何かエラーが起きました:",req_result_del.status_code)
		break

print("既存ツイート:",exist_tweet,"件")
print("削除対象ツイート:",delete_tweet,"件")