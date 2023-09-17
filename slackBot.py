import json
import logging
import urllib.request
import os
import openai
import re
import requests

print('Loading function... ')
logger = logging.getLogger()
logger.setLevel(logging.INFO)



def openAIapi(text):
    # APIクライアントをセットアップ
    openai.api_key = os.environ['OPENAI_KEY']
    # ChatGPT-3.5 Turboを使用してPythonコードを生成
    response = openai.Completion.create(
        engine="text-davinci-003",  # GPT-3.5 Turboエンジンを使用
        prompt=text,
        max_tokens=1000,  # 生成テキストの最大トークン数を指定
        n = 1
    )
    # 生成されたPythonコードを取得
    generated_code = response.choices[0].text
    #print(generated_code)
    return generated_code

def mentionremove(text):
    # メンションのパターンを正規表現で検出
    mention_pattern = r"<@[^>]+>"
    mentions = re.findall(mention_pattern, text)
    # メンションを取り除いたメッセージを生成
    cleaned_message = text
    for mention in mentions:
        cleaned_message = cleaned_message.replace(mention, '')#メッセージ
    return cleaned_message


def handler(event, context):
    #getenv
    OAUTH_TOKEN = os.environ['OAUTH_TOKEN']
    BOT_TOKEN = os.environ['BOT_TOKEN']

    #受信したjsonをLogsに出力
    logging.info(json.dumps(event))

    print (type(event))
    # json処理
    if 'body' in event:
        body = json.loads(event.get('body'))
    elif 'token' in event:
        body = event
    else:
        logger.error('unexpected event format')
        return {'statusCode': 500, 'body': 'error:unexpected event format'}

    #url_verificationイベントに返す
    if 'challenge' in body:
        challenge = body.get('challenge')
        logging.info('return challenge key %s:', challenge)
        return {
            'isBase64Encoded': 'true',
            'statusCode': 200,
            'headers': {},
            'body': challenge
        }
    
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer {0}'.format(BOT_TOKEN)
    }
    # 受信したメッセージのtimestamp (ts)
    message_ts = body.get('event').get('ts')
    
    # メッセージ送信先のユーザーID
    user_id = body.get('event').get('user')
    
    #チャンネルID
    channel_id = body.get('event').get('channel')
    # 受信したメッセージテキスト
    received_message = body.get('event').get('text')
    
    cleaned_message = mentionremove(received_message)
    

    #過去メッセージ取得
    """
    thread_messages = get_thread_messages(BOT_TOKEN, channel_id, message_ts)
    return_text = ""
    if thread_messages:
        for message in thread_messages:
            return_text += "{}:{}   ".format('chatGPT' if message['user'] == 'U05SLAM3H37' else 'ユーザ', mentionremove(message['text']))
    """
    #chatGPTへ
    return_text = openAIapi(cleaned_message)
    
    
    
    data = {
        'token': OAUTH_TOKEN,
        'channel': channel_id,
        'text': '<@{}> {}'.format(user_id,return_text),#
        'thread_ts': message_ts  # スレッド内の返信として指定
        #'username': 'chatAPI'
    }
    # POST処理　
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), method='POST', headers=headers)
    res = urllib.request.urlopen(req)
    logger.info('post result: %s', res.msg)
    return {'statusCode': 200, 'body': 'ok'}
