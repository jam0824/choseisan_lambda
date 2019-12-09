# -*- coding: utf-8 -*-
import os
import logging
import json
import urllib.request
import urllib
import datetime
import re
import testerchan

# ログ設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    
    # 受信データをCloud Watchログに出力
    logging.info(json.dumps(event))

    # SlackのEvent APIの認証
    if "challenge" in event:
        return event["challenge"]
        
        
    token = get_token()

    dic_command = get_command(event.get("event").get("text"))
    kouho = get_date(dic_command["num"], dic_command["time"])
    chosei_url = get_chosei_url(token, dic_command["name"], kouho)
    
    # Slackにメッセージを投稿する
    serihu = testerchan.serihu() + "\n" + chosei_url
    post_message_to_channel(event.get("event").get("channel"), serihu)

    return 'OK'


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
    urllib.request.urlopen(req)

def is_verify_token(event):

    # トークンをチェック    
    token = event.get("token")
    if token != os.environ["SLACK_BOT_VERIFY_TOKEN"]:
        return False

    return True
    

def is_app_mention(event):
    return event.get("event").get("type") == "app_mention"
    
def get_token():
    url = 'https://chouseisan.com/'
    response = urllib.request.urlopen(url)
    for key, value in response.getheaders():
        if "chousei_token" in value:
            str_token = value
            break
    m = re.findall(r'chousei_token=.*?;', str_token)
    token = m[0].replace('chousei_token=', '')
    token = token.replace(';', '')
    return token



def get_chosei_url(token, name, kouho):
    url = 'https://chouseisan.com/schedule/newEvent/create'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {
        'name': name,
        'comment': '',
        'kouho': kouho,
        'chousei_token': token
    }
    params = urllib.parse.urlencode(params)
    req = urllib.request.Request(url, data=params.encode("utf-8"), method="POST", headers=headers)
    response = urllib.request.urlopen(req)
    get_url = response.geturl()
    get_url = get_url.replace('https://chouseisan.com/schedule/newEvent/complete', 'https://chouseisan.com/s')
    return get_url

def get_date(num_date, str_time):
    list_day = ["月","火","水","木","金","土","日"]
    str_dates = ""
    today = datetime.date.today()
    for i in range(num_date):
        target_date = today + datetime.timedelta(days=i+1)
        day = target_date.weekday()
        #土日以外を出力
        if day < 5:
            str_dates += target_date.strftime('%m/%d')
            str_dates += "（" + list_day[day] + "）" + str_time + "\n"
    return str_dates
    
def get_command(command):
    dic_command = {}
    list_command = command.split(",")
    dic_command["name"] = list_command[1]
    dic_command["num"] = int(list_command[2])
    dic_command["time"] = list_command[3]
    return dic_command