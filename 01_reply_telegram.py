import telegram

# Use this token to access the HTTP API:
api_key = '1830582407:AAElfZrgBT637jcUT7LCJyIUBERYxHujuuc'
chat_id = '1772732703'
bot = telegram.Bot(token = api_key)

for item in bot.getUpdates():
    print(item)

bot.sendMessage(chat_id = chat_id, text = "test go")
bot.sendMessage(chat_id = chat_id, text = "hello!!!")