import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import boto3
import pandas as pd
import requests
from datetime import datetime
import pytz
import sqlite3


# ############# S3 연동 키 ############################
# AWS_ACCESS_KEY_ID = 'AKIATY67EXXXXXXXXXXX'
# AWS_ACCESS_KEY_SECRET = 'qzj1JFCdXVuZDER3XXXXXXXXXXX'
# region_name = 'ap-noXXXXXXXXXXX'
#
########텔레그램 연동 키##############
api_key = ''
chat_id = ''

# S3 버킷에 있는 데이터 불러오기
def load_data_s3():
    client = boto3.client('s3')  # low-level functional API
    resource = boto3.resource('s3')  # high-level object-oriented API

    # for bucket in resource.buckets.all():
    #     bucket_name = bucket.name
    bucket_name = 'kb-bucket-test-01'
    file_name = 'naver_news_multi_tuning.csv'
    # obj = client.get_object(Bucket=bucket_name, Key='test.csv')
    # obj = client.get_object(Bucket=bucket_name, Key='news_articles.csv')
    # obj = client.get_object(Bucket=bucket_name, Key='news_articles_bin3.csv')
    obj = client.get_object(Bucket=bucket_name, Key=file_name)
    grid_sizes = pd.read_csv(obj['Body'])

    return grid_sizes

# news_qa API 호출
def news_qa_analysis(question, original_news_data):
    # from konlpy.tag import Okt  # 예시: 광주광역시가 7월 1일에 시행하는 것은?
    #
    # okt = Okt()

    url = "http://172.16.50.4:9000/qa_analysis"

    payload = {'question': question,
               'original_news_data': original_news_data,
               }
    answer_sentence = requests.request("POST", url, data=payload)

    # after_tuning_answer_words = ' '.join(okt.phrases(answer_sentence.text))

    return answer_sentence.text

##################### 후에 class로 변환 ####################################
# sqlite3 활용
def select_db():
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    
    # 추후 코드 변경
    for row in cur.execute('SELECT * FROM news ORDER BY DATE DESC'):
        return row[1] # original_news_data만 추출

def insert_db(original_news_data):
    con = sqlite3.connect('example.db')
    cur = con.cursor()

    date = datetime.now(pytz.timezone('Asia/Seoul')).strftime("%Y%m%d%H%M%S")

    # 테이블 존재하지 않으면 생성
    cur.execute("CREATE TABLE IF NOT EXISTS news(DATE text PRIMARY KEY, CONTENT text)")  # AUTOINCREMENT

    # 데이터 삽입
    cur.execute("INSERT INTO news (DATE,CONTENT) VALUES(?,?)", (date, original_news_data))

    con.commit()

def delete_db():
    con = sqlite3.connect('example.db')
    cur = con.cursor()

    cur.execute("DELETE FROM news").rowcount

    con.commit()

######################################################################################


### 챗봇 답장
def handler(update, context):
    user_text = update.message.text  # 사용자가 보낸 메세지를 user_text 변수에 저장합니다.
    
    # 경제 내용 요약
    if (user_text in ["경제", "IT/과학", "정치", "사회", "생활/문화", "스포츠"]):
        bot.send_message(chat_id=chat_id, text= user_text + " 관련 최신 뉴스 전달 드립니다\n" + "(AI가 {} 기사로 분류했습니다.)".format(user_text))
        # 해당 뉴스 불러오기
        grid_sizes = load_data_s3()
        # dropna_grid_sizes = grid_sizes[grid_sizes.CONTENT.notnull()]
        dropna_grid_sizes = grid_sizes[grid_sizes.content.notnull()]
        # top1_df = dropna_grid_sizes[dropna_grid_sizes.CATEGORY == user_text].sort_values("WRITEDATE", ascending=False).head(1)
        top1_df = dropna_grid_sizes[dropna_grid_sizes.CATEGORY == user_text].head(1)
        # title_message = "[뉴스 제목] \n" + top1_df.TITLE.iloc[0]
        title_message = "[뉴스 제목] \n" + top1_df.title.iloc[0]
        # url_message = top1_df.URL.iloc[0]
        url_message = top1_df.url.iloc[0]
        AI_message = "[AI 분석 요약] \n" + " " + top1_df.SUMMARY_CONTENT.iloc[0]
        bot.send_message(chat_id=chat_id, text=title_message + '\n\n' + AI_message + '\n\n' + url_message)
        bot.send_message(chat_id=chat_id, text="해당 뉴스에서 궁금한 사항이 있으면 입력해주세요." + "\n없으면 '종료'를 입력해주세요")

        # 해당 관련 DB 저장 - original_news_data / date
        # insert_db(top1_df.CONTENT.iloc[0])
        insert_db(top1_df.content.iloc[0])
        
    elif (user_text == "종료"):
        # athena DB 내용 삭제
        delete_db()
        bot.send_message(chat_id=chat_id, text="다른 분야가 궁금하시면 입력해주세요.\n\n" + '''"경제", "IT/과학", "정치", \n "사회", "생활/문화", "스포츠"''')
    
    else: # 질문 관련 내용
        # DB에서 내용 최신 순으로 조회 후, news_qa analysis에 호출
        #// 아무것도 없을 때 exceptio 처리 해야 함.
        original_news_data = select_db()
        answer_message = news_qa_analysis(user_text, original_news_data)

        bot.send_message(chat_id=chat_id, text=answer_message)

if __name__ == "__main__":
    bot = telegram.Bot(api_key)
    info_message = '''[원하는 뉴스 분야 입력] \n\n '"경제", "IT/과학", "정치", \n"사회", "생활/문화", "스포츠"'''
    bot.sendMessage(chat_id=chat_id, text=info_message)

    updater = Updater(token=api_key, use_context=True)
    dispatcher = updater.dispatcher
    updater.start_polling()

    echo_handler = MessageHandler(Filters.text, handler)
    dispatcher.add_handler(echo_handler)






