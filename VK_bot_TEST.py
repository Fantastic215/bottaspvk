import requests
import wikipedia #Модуль Википедии
wikipedia.set_lang("RU")
import vk_api
from vk_api import VkUpload 
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import os
from pdf2jpg import pdf2jpg
from vk_api.utils import get_random_id
from io import BytesIO
while True:
    try:
        session = requests.Session()
        token_vk=os.environ.get('BOT_TOKEN')
        vk_session = vk_api.VkApi(token=str(token_vk),scope="message")

        from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

        longpoll = VkBotLongPoll(vk_session, "194277538")
        vk = vk_session.get_api()
        def key_b(peer_id):
            if peer_id<2000000000:
                try:
                    keyboard = VkKeyboard(one_time=True, inline=False)
                    keyboard.add_button("/info", color=VkKeyboardColor.POSITIVE, payload=None)
                    keyboard.add_button("/search wiki", color=VkKeyboardColor.PRIMARY, payload=None)
                    keyboard.add_button("/rasp", color=VkKeyboardColor.NEGATIVE, payload=None)
                    vk.messages.send(  # Отправляем собщение
                                    peer_id=peer_id,
                                    keyboard=keyboard.get_keyboard(),message='  ', random_id=get_random_id())

                except Exception as ecc:
                    vk.messages.send(  # Отправляем собщение
                            peer_id=peer_id,
                            message=str(ecc), random_id=get_random_id())
                
        def get_rasp():
            url = 'http://rasp.kolledgsvyazi.ru/spo.pdf'
            f = open(r'rasp.pdf', "wb")  # открываем файл для записи, в режиме wb
            ufr = requests.get(url)  # делаем запрос
            f.write(ufr.content)  # записываем содержимое в файл; как видите - content запроса
            f.close()
            from pdf2jpg import pdf2jpg
            inputpath = r"rasp.pdf"
            outputpath = r""
            # to convert all pages
            result = pdf2jpg.convert_pdf2jpg(inputpath, outputpath, pages="ALL")
            
            old_image = open('rasp.pdf_dir\0_rasp.pdf.jpg', 'r').read()
            # Создаем новый файл
            new_image = open('0_rasp.pdf.jpg', 'w')
            # Сохраняем данные старой картинки в новую
            new_image.write(old_image)
            new_image.close()
            
            print(result)


        def get_rasp2():
            url = 'http://rasp.kolledgsvyazi.ru/npo.pdf'
            f = open(r'rasp2.pdf', "wb")  # открываем файл для записи, в режиме wb
            ufr = requests.get(url)  # делаем запрос
            f.write(ufr.content)  # записываем содержимое в файл; как видите - content запроса
            f.close()
            inputpath = r"rasp2.pdf"
            outputpath = r""
            # to convert all pages
            result = pdf2jpg.convert_pdf2jpg(inputpath, outputpath, pages="ALL")
            
            old_image = open('rasp2.pdf_dir\0_rasp2.pdf.jpg', 'r').read()
            # Создаем новый файл
            new_image = open('0_rasp2.pdf.jpg', 'w')
            # Сохраняем данные старой картинки в новую
            new_image.write(old_image)
            new_image.close()
            
            print(result)

        def send(massage, peer_id):
            vk.messages.send(  # Отправляем собщение
                    peer_id=peer_id,
                    message=massage, random_id=get_random_id())
            

        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.object['text']:
                
                s = event.object['text']
                # Слушаем longpoll, если пришло сообщение то:
                peer_id = event.obj['peer_id']
                if s[0]=='/':
                    key_b(peer_id)
                if s == '/user info' or s=='@club194277538 /user info':  # Если написали заданную фразу
                    if peer_id<2000000000:
                        send('ваш id- ' + str(peer_id), peer_id)
                    else:
                        send("работает только в лс",peer_id)
                elif s == '/search wiki' or s=='@club194277538 /search wiki':  # Если написали заданную фразу
                    send('введите запрос ', peer_id)
                    try:
                        for event in longpoll.listen():
                            if event.type == VkBotEventType.MESSAGE_NEW and event.object['text']:
                                key_b(peer_id)
                                send('Вот что я нашёл: \n' + str(wikipedia.summary(event.object['text'])), peer_id)
                                
                                break
                    except Exception as exe:
                        key_b(peer_id)
                        send("error\nнеправильный запрос", peer_id)
                        
                        if peer_id == 165974848:
                            send(str(exe), peer_id)


                elif s == '/info' or s=='@club194277538 (Расписание) /info':
                    send('бота написал\n'
                         'https://vk.com/fantasticfeed\n'
                         '____________________________\n'
                         'список команд:\n'
                         '/user info\n/search wiki\n/rasp(сломана)\n/info\n/game(в разработке)\n'
                         'разрабатываются новые возможности.', peer_id)
                    
                elif s == '/game':
                    send('разработка...', peer_id)

                
                elif s == '/rasp' or s=='@club194277538 (Расписание) /rasp':
                    try:
                        files = [('file', ('0_rasp.pdf.jpg', open('0_rasp.pdf.jpg', 'rb')))]
                        a = vk_session.method("photos.getMessagesUploadServer")
                        b = requests.post(a['upload_url'],
                                              files={'photo': files, 'rb'))}).json()
                        c = vk_session.method('photos.saveMessagesPhoto',
                                                  {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
                        d = "photo{}_{}".format(c["owner_id"], c["id"])
                        vk.messages.send(
                                peer_id=peer_id,
                                attachment=d,
                                 random_id=get_random_id()
                            )

                    except Exception as E:
                        send("error\n " + str(E), peer_id)
                        


                elif s[0]=='/':
                    send('нет такой команды\n'
                         'попробуйте написать "/info"', peer_id)
    except Exception as ec:
        print(ec)
