# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 18:12:45 2018

@author: linzino
"""
# server-side
from flask import Flask, request, abort

# line-bot
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

# package
import re
from datetime import datetime 

# customer module
import mongodb


app = Flask(__name__)

#line_bot_api = LineBotApi('RRQ+LmtuuSZzuCSEtkdYeEgAjSFXNabVPZ19J2KYeRbm1i1ewqk7anKv02JsNsPxc7kqs0Y/9a8tZ9iqcS1T5wPherdkUjZSDOhSkonQigc0htNxdBEptU9NbViHXcl4Dxp+CxdoCpcrKvlVJ3y/GQdB04t89/1O/w1cDnyilFU=')
#handler = WebhookHandler('f397ebb34a37e5f70bde617b84de7433')
line_bot_api = LineBotApi('cEvknKWJZuZSTlm/TxOA+HlhXPDT9YqN0x/ZBoQ3qzBe50BeqJ/YnWEHme5AKbADcNWoDSnroAu6XC2mPN+39G3qmwCbwA3/PQNyGuQvwpQyL5sTuxg0Va5gZ+U+BLyMr3/pd/IXcBcBa70+05zIFwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c5f5759e77922f50b3c2d7e73e7293f1')



@app.route("/callback", methods=['POST'])
def callback():

    
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(FollowEvent)
def handle_follow(event):
    '''
    當使用者加入時觸動
    '''
    # 取得使用者資料
    profile = line_bot_api.get_profile(event.source.user_id)
    name = profile.display_name
    uid = profile.user_id
    
    print(name)
    print(uid)
    # Udbddac07bac1811e17ffbbd9db459079
    if mongodb.find_user(uid,'users')<= 0: #使用者沒有在資料庫中
        # 整理資料
        dic = {'userid':uid,
               'username':name,
               'creattime':datetime.now(),
               'Note':'user',
               'ready':0}
        
        mongodb.insert_one(dic,'users')
   


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    '''
    當收到使用者訊息的時候
    '''
    message = event.message.text
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    return 0 


if __name__ == '__main__':
    app.run(debug=True)