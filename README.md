# chatbot_bert

### [배경]

- 사용자
  - 어려운 금융, 경제 용어들이 난무한 뉴스 기사를 읽기 어려운 사람들
  - 요약해서 빠르게 내용을 접하고 싶은 사람들
- 목표
  - AI가 뉴스 기사를 이해하고 사용자에게 쉽고 간단하게 정보 제공
  - 헷갈리는 내용이 있을 경우 질의 응답을 통해 해결



### [데이터 셋]

- 뉴스 신문기사 크롤링

### [개발 기간]

- 21.07.10 ~ 21.07.15
- 개인 프로젝트

### [**기술셋**]

1. 인공지능 모형 개발(뉴스 카테고리 분류/뉴스 내용 요약/뉴스 QA)
   - Pororo 라이브러리
   - Pytorch
   - Python-mecab-ko
   - cudatoolkit

2. 텔레그램 연동

   - DB sqlite3
   - AWS S3(boto3)

3. API 개발

   - Django API

   - AWS EC2



### [**아키텍처**]

![chatbot_architecture](https://user-images.githubusercontent.com/47164355/125904683-7d46a0aa-077b-42ae-8a2a-c890586cfb34.PNG)



사전 과정: S3에 자연어 데이터 적재

step1) AWS EC2 환경에서 분석가 표준 모델 개발

- pororo 자연어 라이브러리 활용하여, 특정 API 개발

step2) 챗봇 Client와 S3를 연동하여 데이터 불러오기

step3) 불러온 데이터를 input 값으로 활용, API 호출 시 결과 도출. Q&A의 지속적인 대화를 위해 original data를 불러와야 하고, sqlite3를 활용하여 데이터 임시 저장소 설정



### [구동 방법]

**사전 작업**

- Pororo 설치 및 사용법 확인

- Telegram 설치 및 파이썬 연동

- Sqlite3 설치 및 파이썬 연동
- S3 IAM 계정 생성 및 데이터 확보 후 csv 파일 저장
- Django 세팅

**실행 순서**

1. EC2기반 Pororo API 웹 서버 실행

   - https://github.com/kimjaejeong/pororoAPI/tree/main/pororo_api

   ```python
   python3 manage.py runserver 0.0.0.0:9000
   ```

2. 챗봇 실행

   - news_bot_AI.py 실행

##### 파일구조

- news_bot_AI.py
  - 메인 실행 소스

- s3_exercise 폴더

  - s3, python 연동

- telegram_exercise 폴더

  01) telegram reply 연습

  02) telgram send & reply 연습

  03) news data 크롤링 연습 



### [결과(텔레그램 캡처)]

![ai_result1](https://user-images.githubusercontent.com/47164355/127100372-e6d1664c-ef56-46f8-a847-b841d0fd0a74.PNG)
![ai_result2](https://user-images.githubusercontent.com/47164355/127100377-fb73afae-3750-4739-aab9-d249ce879791.PNG)



### [오류 및 해결]

- AttributeError: module 'telegram' has no attribute 'Bot'
  1. 파일명이 telegram 인지 확인
  2. pip uninstall wheel python-telegram-bot telegram
  3. pip install wheel python-telegram-bot telegram





### [참고자료]

##### **Web Server 소스**

- https://github.com/kimjaejeong/pororoAPI

**Pororo 라이브러리**

- https://kangaroo-dev.tistory.com/1 

  (라이브러리 설치 - 리눅스 환경에서 작업하는 것이 정신 건강에 좋습니다.)

- https://github.com/kakaobrain/pororo?fbclid=IwAR1QM9C-aXDJaZfx1zAXcSOI8aDn3BYHr8WvZVII6tHBZp37sSa29cTNKB4

  (활용 가이드)

- https://smilegate.ai/2021/02/10/kakaobrain-pororo/

  (다양한 Task)

##### Telegram

- https://py-son.tistory.com/8

  ([챗봇] 파이썬 텔레그램 챗봇, 이것만 따라하면 20분 완성 (코로나 알리미 봇))

- https://ddolcat.tistory.com/746
  - telegram 연동
- https://gabrielkim.tistory.com/entry/Telegram-Bot-Token-%EB%B0%8F-Chat-Id-%EC%96%BB%EA%B8%B0
  - chat_id 얻는 방법

##### S3

- IAM 계정생성

  - 정의

    - AWS 계정에서 하나 이상의 IAM 사용자를 만들 수 있습니다. 팀에 새로 합류하는 사람이 있거나 AWS에 대한 API 호출이 필요한 새 애플리케이션을 생성할 때 IAM 사용자를 생성합니다.

  - https://docs.aws.amazon.com/ko_kr/IAM/latest/UserGuide/getting-started_create-admin-group.html

    (IAM 관리자 및 사용자 그룹 생성)

    (따라하기 매우 좋음★★★★★★★★)

  - https://docs.aws.amazon.com/ko_kr/IAM/latest/UserGuide/getting-started_create-delegated-user.html

    (사용자 추가 방법)

- boto3 활용

  - https://ndb796.tistory.com/280

    (Python boto3을 이용하여 AWS S3과 연동하기)

    windows의 경우 cmd창에서 확인

  - https://dluo.me/s3databoto3

    (boto3 간단 사용법)

**sqlite**

- https://lee-mandu.tistory.com/449

  (설치 방법)

- https://iamthejiheee.tistory.com/47

  (sqlite3 문법정리 굿)

**github**

- https://cutemoomin.tistory.com/entry/Readme-%ED%8C%8C%EC%9D%BC%EC%97%90-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EB%84%A3%EA%B8%B0-%EB%A7%88%ED%81%AC%EB%8B%A4%EC%9A%B4-%EC%9D%B4%EB%AF%B8%EC%A7%80

  (이미지 업로드 방법)

