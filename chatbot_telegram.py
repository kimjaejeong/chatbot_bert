import telegram

# Use this token to access the HTTP API:
api_key = '1830582407:AAElfZrgBT637jcUT7LCJyxxxxxxx'
chat_id = '17727xxxxxxx'
bot = telegram.Bot(token = api_key)

for item in bot.getUpdates():
    print(item)

bot.sendMessage(chat_id = chat_id, text = "잘 지내니?")
bot.sendMessage(chat_id = chat_id, text = "그런데 너 앞으로 뭐 먹고 살거냐?")