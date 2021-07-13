import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import urllib.request as req
import os
import boto3
import pandas as pd

############# S3 연동 키 ############################
AWS_ACCESS_KEY_ID = 'AKIATY67EXXXXXXXXXXX'
AWS_ACCESS_KEY_SECRET = 'qzj1JFCdXVuZDER3XXXXXXXXXXX'
region_name = 'ap-noXXXXXXXXXXX'

############# 텔레그램 연동 키 ############################
api_key = "1830582407:AAElfZrgBT637jcUxxxxxxxx"
chat_id = "1772xxxxx"

# S3 버킷에 있는 데이터 불러오기
def load_data_s3():
    client = boto3.client('s3')  # low-level functional API
    resource = boto3.resource('s3')  # high-level object-oriented API

    for bucket in resource.buckets.all():
        bucket_name = bucket.name
    # obj = client.get_object(Bucket=bucket_name, Key='test.csv')
    obj = client.get_object(Bucket=bucket_name, Key='news_articles.csv')
    grid_sizes = pd.read_csv(obj['Body'])

    return grid_sizes

def news_qa_analysis(sentence):

    url = "API URL 입력"

    summary_sentence = ""

    return summary_sentence

### 챗봇 답장
def handler(update, context):
    user_text = update.message.text  # 사용자가 보낸 메세지를 user_text 변수에 저장합니다.
    
    # 경제 내용 요약
    if (user_text == "경제"):
        grid_sizes = load_data_s3()
        dropna_grid_sizes = grid_sizes[grid_sizes.CONTENT.notnull()]
        top1_df = dropna_grid_sizes.sort_values("WRITEDATE", ascending = False).head(1)
        AI_message = "AI 분석 요약 : " + "경제 관련 된 이야기입니다."
        bot.send_message(chat_id=chat_id, text=top1_df.TITLE.iloc[0] + '\n\n' + AI_message + '\n\n' + top1_df.URL.iloc[0])
        bot.send_message(chat_id=chat_id, text="해당 뉴스에서 궁금한 사항이 있으면 입력해주세요." + "없으면 '종료'를 입력해주세요")

        user2_text = update.message.text  # 사용자가 보낸 메세지를 user_text 변수에 저장합니다.
        while (user2_text != "없음"):
            # API 연계 관련 내용
            summary_sentence = news_qa_analysis(top1_df.TITLE.iloc[0])
            bot.send_message(chat_id=chat_id, text=summary_sentence)
        bot.send_message(chat_id=chat_id, text="많이 애용해주세요. 감사합니다^^")
    else:
        bot.send_message(chat_id=chat_id, text="해당 카테고리는 존재하지 않습니다.")

if __name__ == "__main__":
    bot = telegram.Bot(api_key)
    info_message = '''- 원하는 뉴스 카테고리 입력 : '"스포츠", "사회", "정치", "경제", "생활/문화", "IT/과학"'''
    bot.sendMessage(chat_id=chat_id, text=info_message)

    updater = Updater(token=api_key, use_context=True)
    dispatcher = updater.dispatcher
    updater.start_polling()

    echo_handler = MessageHandler(Filters.text, handler)
    dispatcher.add_handler(echo_handler)





