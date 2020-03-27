import config
import telebot
import irbis64
import datetime

bot = telebot.TeleBot(config.token)


def findbook(message):
    answer=''
    message_list = message.split(' ')
    del message_list[0]
    
    message = ''
    for word in message_list:
        message += '+"K=' + word + '$"'
    message = '(' + message + ')'
    answer = irbis64.irbis_search(message)
    return answer


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Приветствую Вас! Я Книжный бот
Я могу помочь вам найти интересующие книги в Электронном каталоге библиотеки.
Давайте нечнем!
Если вы хотите найти книгу, то напишите слово "*/Найти*", а после него укажите автора или слова из названия
Все слова, которые Вы введете после команды "*/Найти*", будут восприниматься как ключевые слова
В скором времени планируется добавить следующий функционал:
"*/записаться*" - регистрация в библиотеке
"*/формуляр*" -  просмотр своего электронного формуляра
"*/продлить*" продление книг
"*/заказать*" заказ книг
"*/новинки10* - список из 10 последних книг, поступивших в библиотеку
\
""", parse_mode="Markdown")


def log(userid,text,who): 
    with open(''.join(['users/', str(userid)]) + '.log', 'a') as f:
        if who == 1:
            who = 'bot'
        else:
            who = userid
        f.write(str(datetime.date.today()) + ': ' + who + ': ' + text + '\n')

        


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    log(str(message.chat.id),message.text,0)
    command = message.text.split(' ', 1)[0].lower()

    if ((command == '/найти') or (command == 'найти')):
        answer = findbook(message.text)
    elif ((command == '/помощь') or (command == 'помощь')):
        answer = 'Если вы хотите найти книгу, то напишите команду "*/Найти*", а после него укажите автора или слова из названия'
    elif (command == '/id'):
        answer = message.chat.id
    elif (command == '/формуляр'):
        answer = 'Тут будет вывод данных о вашем формуляре'
    else:
        answer = 'К сожалению, я не понял вашего запроса'

    bot.send_message(message.chat.id, answer , parse_mode="Markdown")
    log(str(message.chat.id),answer,1)
    

    
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)

            # ConnectionError and ReadTimeout because of possible timout of the requests library
            # TypeError for moviepy errors
            # maybe there are others, therefore Exception
        except Exception as e:
            #logger.error(e)
            print('Error - ' + str(e))
            time.sleep(15)





