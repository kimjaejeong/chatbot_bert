import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request as req
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


######## 크롤링 관련 함수 ########
def covid_num_crawling():
    code = req.urlopen(
        "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%ED%99%95%EC%A7%84%EC%9E%90")
    soup = BeautifulSoup(code, "html.parser")
    info_num = soup.select("div.status_today em")
    result = int(info_num[0].string) + int(info_num[1].string)
    return result


def covid_news_crawling():
    code = req.urlopen("https://search.naver.com/search.naver?where=news&sm=tab_jum&query=%EC%BD%94%EB%A1%9C%EB%82%98")
    soup = BeautifulSoup(code, "html.parser")
    title_list = soup.select("a.news_tit")
    output_result = ""
    for i in title_list:
        title = i.text
        news_url = i.attrs["href"]
        output_result += title + "\n" + news_url + "\n\n"
        if title_list.index(i) == 2:
            break
    return output_result


def covid_image_crawling(image_num=5):
    if not os.path.exists("./코로나이미지"):
        os.mkdir("./코로나이미지")

    browser = webdriver.Chrome("./chromedriver")
    browser.implicitly_wait(3)
    wait = WebDriverWait(browser, 10)

    browser.get(
        "https://search.naver.com/search.naver?where=image&section=image&query=%EC%BD%94%EB%A1%9C%EB%82%98&res_fr=0&res_to=0&sm=tab_opt&color=&ccl=0&nso=so%3Ar%2Cp%3A1d%2Ca%3Aall&datetype=1&startdate=&enddate=&gif=0&optStr=d&nq=&dq=&rq=&tq=")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.photo_group._listGrid div.thumb img")))
    img = browser.find_elements_by_css_selector("div.photo_group._listGrid div.thumb img")
    for i in img:
        img_url = i.get_attribute("src")
        req.urlretrieve(img_url, "./코로나이미지/{}.png".format(img.index(i)))
        if img.index(i) == image_num - 1:
            break
    browser.close()


####################################

######## 텔레그램 관련 코드 ########
api_key = "1830582407:AAElfZrgBT637jcUxxxxxxxx"
chat_id = "1772xxxxx"

bot = telegram.Bot(api_key)
info_message = '''- 오늘 확진자 수 확인 : "코로나" or "ㅋㄹㄴ" 입력
- 코로나 관련 뉴스 : "뉴스" or "ㄴㅅ" 입력
- 코로나 관련 이미지 : "이미지" or "ㅇㅁㅈ" 입력'''
bot.sendMessage(chat_id=chat_id, text=info_message)

updater = Updater(token=api_key, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling()


### 챗봇 답장
def handler(update, context):
    user_text = update.message.text  # 사용자가 보낸 메세지를 user_text 변수에 저장합니다.
    # 오늘 확진자 수 답장
    if (user_text == "코로나") or (user_text == "ㅋㄹㄴ"):
        covid_num = covid_num_crawling()
        bot.send_message(chat_id=chat_id, text="오늘 확진자 수 : {} 명".format(covid_num))
        bot.sendMessage(chat_id=chat_id, text=info_message)
    # 코로나 관련 뉴스 답장
    elif (user_text == "뉴스") or (user_text == "ㄴㅅ"):
        covid_news = covid_news_crawling()
        bot.send_message(chat_id=chat_id, text=covid_news)
        bot.sendMessage(chat_id=chat_id, text=info_message)
    # 코로나 관련 이미지 답장
    elif (user_text == "이미지") or (user_text == "ㅇㅁㅈ"):
        bot.send_message(chat_id=chat_id, text="최신 이미지 크롤링 중...")
        covid_image_crawling(image_num=10)
        # 이미지 한장만 보내기
        # bot.send_photo(chat_id=id, photo=open("./코로나이미지/0.png", 'rb'))
        # 이미지 여러장 묶어서 보내기
        photo_list = []
        for i in range(len(os.walk("./코로나이미지").__next__()[2])):  # 이미지 파일 개수만큼 for문 돌리기
            photo_list.append(telegram.InputMediaPhoto(open("./코로나이미지/{}.png".format(i), "rb")))
        bot.sendMediaGroup(chat_id=chat_id, media=photo_list)
        bot.sendMessage(chat_id=chat_id, text=info_message)


echo_handler = MessageHandler(Filters.text, handler)
dispatcher.add_handler(echo_handler)
####################################