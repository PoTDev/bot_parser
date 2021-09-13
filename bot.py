import telebot
import requests
from bs4 import BeautifulSoup


from database import database


#инициализация бота
token = ''
bot = telebot.TeleBot(token)


#команда старт
@bot.message_handler(commands=['start','help'])  
def start_command(message):  

    text_hi = 'Привет😊\n'
    text_hi += 'Я бот, который может определить, что изображено на картинке.\n'
    

    bot.send_message(message.chat.id, text_hi)


#обработка картинки
@bot.message_handler(content_types=['photo'])
def handle(message):
  #вызов проверки пользователя
  us_id = message.from_user.id
  us_name = message.from_user.first_name
  us_sname = message.from_user.last_name
  username = message.from_user.username
  us_chat_id = message.chat.id


  db = database()
  check = 0
  #подключение и проверка  базы данных
  check = db.check_connection(check)

  if check:
    print('СОЕДИНЕНИЕ С БАЗОЙ ДАННОЙ УСТАНОВЛЕНО')
    #обработка пользователя
    check_user = db.user_identity(us_id, us_chat_id, us_name, us_sname, username)
    #db.user_identity(us_id)

    #запрос лога
    #log_request(message)

    #получение ссылки изображения
    image_name = save_image_from_message(message)


    #отправка ccсылки на изображение и результат

    result = parser(image_name)
    

    #вывод результата

    # send classification results
    output = 'Похоже, что на этом изображении:\n'
    output += '\n'

    for data in result:
      output += data.text
      output += '\n'

    
    bot.reply_to(message, output)



  else:
    output = 'Ошибка бота. Обратитесь к администратору'
    bot.reply_to(message, output)
  
     



# ----------- Функции ---------------


#def log_request(message):
#  file = open('.data/logs.txt', 'a') #append to file 
#  file.write("{0} - {1} {2} [{3}]\n".format(datetime.datetime.now(), message.from_user.first_name, message.from_user.last_name, message.from_user.id)) 
 # print("{0} - {1} {2} [{3}]".format(datetime.datetime.now(), message.from_user.first_name, message.from_user.last_name, message.from_user.id))
 # file.close() 
# ----------- #

def get_image_id_from_message(message):
  # there are multiple array of images, check the biggest
  return message.photo[len(message.photo)-1].file_id
# ----------- #

def save_image_from_message(message):
    cid = message.chat.id

    image_id = get_image_id_from_message(message)

    bot.send_message(cid, '🔥 Анализирую изображение, подождите чуть-туть ! 🔥')

    # prepare image for downlading
    file_path = bot.get_file(image_id).file_path

    # generate image download url
    image_url = "https://api.telegram.org/file/bot{0}/{1}".format(token, file_path)
    print(image_url)
  
  
    return image_url


def parser(image_ulr):

    prepared_url = r'https://yandex.ru/images/search?source=collections&rpt=imageview&url='
    url = prepared_url + image_ulr
    
    print(url)

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    soup.prettify()
    print(page.status_code)

    similar = soup.find('section', class_='CbirItem CbirTags').find_all('span')

    for item in similar:
      print(item.text)

    return similar

bot.polling(none_stop=True, interval=0)
