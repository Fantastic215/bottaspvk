import requests
import wikipedia #Модуль Википедии
wikipedia.set_lang("RU")
import vk_api
import os
from pdf2jpg import pdf2jpg
while True:
    try:
        vk_session = vk_api.VkApi(token="29a19f8c539a7ad2ff7ed2c8df51328fbc5473097d60a55dd5a40132ab664ed50610428c78f98e5c3ddd0",scope="messages")

        from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

        longpoll = VkBotLongPoll(vk_session, "194277538")
        vk = vk_session.get_api()


        def get_rasp():
            url = 'http://rasp.kolledgsvyazi.ru/spo.pdf'
            f = open(r'rasp.pdf', "wb")  # открываем файл для записи, в режиме wb
            ufr = requests.get(url)  # делаем запрос
            f.write(ufr.content)  # записываем содержимое в файл; как видите - content запроса
            return f
            f.close()
            


        def get_rasp2():
            url = 'http://rasp.kolledgsvyazi.ru/npo.pdf'
            f = open(r'rasp2.pdf', "wb")  # открываем файл для записи, в режиме wb
            ufr = requests.get(url)  # делаем запрос
            f.write(ufr.content)  # записываем содержимое в файл; как видите - content запроса
            retutn f
            f.close()

        def send(massage, peer_id):
            vk.messages.send(  # Отправляем собщение
                    peer_id=peer_id,
                    message=massage, random_id=123456)
            vk.messages.deleteConversation(peer_id=peer_id, group_id=194277538)

        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.object['text']:
                s = event.object['text']
                # Слушаем longpoll, если пришло сообщение то:
                peer_id = event.obj['peer_id']
                if s == '/user info':  # Если написали заданную фразу
                    if peer_id<2000000000:
                        send('ваш id- ' + str(peer_id), peer_id)
                    else:
                        send("работает только в лс",peer_id)
                elif s == '/search wiki':  # Если написали заданную фразу
                    send('введите запрос ', peer_id)
                    try:
                        for event in longpoll.listen():
                            if event.type == VkBotEventType.MESSAGE_NEW and event.object['text']:
                                send('Вот что я нашёл: \n' + str(wikipedia.summary(event.object['text'])), peer_id)
                                break
                    except Exception as exe:
                        send("error\nнеправильный запрос", peer_id)
                        if peer_id == 165974848:
                            send(str(exe), peer_id)


                elif s == '/info':
                    send('бота написал\n'
                         'https://vk.com/fantasticfeed\n'
                         '____________________________\n'
                         'список команд:\n'
                         '/user info\n/search wiki\n/rasp\n/info\n'
                         'разрабатываются новые возможности.', peer_id)

                elif s == '/🖕🏻':
                    if peer_id == 165974848:
                        send('🖕🏻иди нах🖕🏻', peer_id)
                    else:
                        send("нет доступа")

                elif s == '/rasp':
                    get_rasp()
                    get_rasp2()
                    try:
                        try:
                            a = vk_session.method("photos.getMessagesUploadServer")
                            b = requests.post(a['upload_url'],
                                              files={'photo': open(get_rasp(), 'rb')}).json()
                            c = vk_session.method('photos.saveMessagesPhoto',
                                                  {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
                            d = "photo{}_{}".format(c["owner_id"], c["id"])
                            b2 = requests.post(a['upload_url'],
                                               files={'photo': open(get_rasp2, 'rb')}).json()
                            c2 = vk_session.method('photos.saveMessagesPhoto',
                                                   {'photo': b2['photo'], 'server': b2['server'], 'hash': b2['hash']})[0]
                            d2 = "photo{}_{}".format(c2["owner_id"], c2["id"])
                            vk.messages.send(  # Отправляем собщение
                                    peer_id=peer_id,
                                    attachment=[d,d2], random_id=123456
                                )
                            vk.messages.deleteConversation(peer_id=peer_id, group_id=194277538)
                        except:
                            send("error\n " + str(E), peer_id)
                            vk.messages.deleteConversation(peer_id=peer_id, group_id=194277538)

                    except Exception as E:
                        send("error\n " + str(E), peer_id)
                        vk.messages.deleteConversation(peer_id=peer_id, group_id=194277538)


                elif s[0]=='/':
                    send('нет такой команды\n'
                         'попробуйте написать "/info"', peer_id)
    except Exception as ec:
        print(ec)
