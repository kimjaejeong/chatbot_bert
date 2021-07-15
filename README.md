# chatbot_bert

### [배경]

- 뉴스 기사를 읽기 어려운 사람들
- 요약해서 빠르게 내용을 접하고 싶은 사람들
- AI가 사용자를 기사를 이해하고 사용자를 이해시키는 것이 핵심



### [데이터 셋(AI허브 데이터)]

- 뉴스 신문기사



### [**기술셋**]

1. 인공지능 모형 개발(뉴스 카테고리 분류/뉴스 내용 요약/뉴스 QA)
   - Pororo 라이브러리
   - Pytorch
   - python-mecab-ko
   - cudatoolkit

2. 텔레그램 연동

   - DB sqlite3
   - AWS S3

3. API 개발

   - Django API

   - AWS EC2



### [**아키텍처**]



사전 과정: S3에 자연어 데이터 적재

step1) AWS EC2 환경에서 분석가 표준 모델 개발

- pororo 자연어 라이브러리 활용하여, 특정 API 개발

step2) 챗봇 Client와 S3를 연동하여 데이터 불러오기

step3) 불러온 데이터를 input 값으로 활용, API 호출 시 결과 도출. Q&A의 지속적인 대화를 위해 original data를 불러와야 하고, sqlite3를 활용하여 데이터 임시 저장소 설정





### [결과(텔레그램 캡처)]





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