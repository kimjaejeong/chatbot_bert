# chatbot_bert
bert, telegram 연동



### Telegram

telegram 연동

- https://ddolcat.tistory.com/746

chat_id 얻는 방법

- https://gabrielkim.tistory.com/entry/Telegram-Bot-Token-%EB%B0%8F-Chat-Id-%EC%96%BB%EA%B8%B0



### 오류 해결

##### Error message 해결

- AttributeError: module 'telegram' has no attribute 'Bot'
  1. 파일명이 telegram 인지 확인
  2. pip uninstall wheel python-telegram-bot telegram
  3. pip install wheel python-telegram-bot telegram