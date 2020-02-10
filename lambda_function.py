# -*- coding: utf-8 -*-
import os
import logging
import json
import urllib
import urllib.request
import re
import testerchan
import choseisan
import qr_code

# ログ設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    
    # 受信データをCloud Watchログに出力
    logging.info(json.dumps(event))

    # SlackのEvent APIの認証
    if "challenge" in event:
        return event["challenge"]

    chosei_url = selector(event.get("event").get("text"))
    logging.info("**********chousei_url : " + chosei_url)
    
    # Slackにメッセージを投稿する
    message = testerchan.Testerchan().get_finish_message() + "\n" + chosei_url
    post_message_to_channel(event.get("event").get("channel"), message)

    return {
        'statusCode': 200,
        'body': json.dumps('kyunchan OK!')
    }
    
def selector(command):
    if "http" in command:
        return exec_qrcode(command)
    elif "choseisan" in command:
        return exec_choseisan(command)
    elif "chouseisan" in command:
        return exec_choseisan(command)
    else:
        return "えとえと……ごめんなさい、わかりませんっ＞＜"
    
def exec_choseisan(text):
    c = choseisan.Choseisan()
    token = c.get_token()
    dic_command = c.get_command(text)
    kouho = c.get_date(dic_command["num"], dic_command["time"])
    chosei_url = c.get_chosei_url(token, dic_command["name"], kouho)
    return chosei_url
    
def exec_qrcode(text):
    q = qr_code.Qrcode()
    return q.make_qr(text)
    

def post_message_to_channel(channel, message):
    url = "https://slack.com/api/chat.postMessage"
    logging.info(channel)
    logging.info(message)
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": "Bearer {0}".format(os.environ["SLACK_BOT_USER_ACCESS_TOKEN"])
    }
    data = {
        "token": os.environ["SLACK_BOT_VERIFY_TOKEN"],
        "channel": channel,
        "text": message,
    }

    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), method="POST", headers=headers)
    response = urllib.request.urlopen(req)
    logging.info("**********response : " + str(response.getcode()))
