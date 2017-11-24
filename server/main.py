# _*_ coding = utf-8 _*_
# TODO: реализовать нахождение состояния в графе

from selenium import webdriver
import requests
import re
import json
import copy
import networkx as nx
import time
import random
from matplotlib import pyplot as plt

import reqs

# Пока настроек немного, храним прямо тут
site = 'test-online.sbis.ru'
login = 'Демо_тензор'
password = 'Демо123'


class State:
    """Класс, описывающий состояние страницы"""
    
    def __init__(self, url, elements):
        self.url = url
        self.elements = elements[:]


class Element:
    """Отдельный элемент на странице
    Нужно его уметь максимально точно идентифицировать по собранным данным:
      * text
      * size
      * location (?)
      * screentshot
      * atributes (e.g. innerHTML)"""

    def __init__(self, html):
        self.html = html


class Bot:
    
    def __init__(self, network):
        self.network = network
        self.driver = webdriver.Chrome()
        self.current_state = None
        self.basement_state = None
        
    def open(self, url):
        self.driver.get(url)
    
    def auth(self, login, password):
        temp_auth = copy.deepcopy(reqs.auth)
        temp_auth['params']['data']['d'][0] = login
        temp_auth['params']['data']['d'][1] = password
        r = requests.post(' http://%s/auth/service/sbis-rpc-service300.dll' % site,
                          headers=reqs.headers, data=json.dumps(temp_auth))
        sid = re.search('sid=(.+?);', r.headers['Set-Cookie']).groups()[0]
        cps = re.search('CpsUserId=(.+?);', r.headers['Set-Cookie']).groups()[0]
        self.driver.add_cookie({'name': 'sid', 'value': sid, 'path': '/', 'secure': False})
        self.driver.add_cookie({'name': 'CpsUserId', 'value': cps, 'path': '/', 'secure': False})
        
    def get_state(self):
        url = self.driver.current_url
        # здесь требуется уточнить механизм выбора элементов
        elements = self.driver.find_elements('css selector', '[data-component^="SBIS3.CONTROLS"]')
        filtered_elements = []
        success = False
        while not success:
            try:
                for element in elements:
                    if element.size['height']*element.size['width'] > 10 and \
                                    element.text != '' and \
                            'Конфигурация' not in element.text:
                        elm = Element(element.get_attribute('innerHTML'))
                        filtered_elements.append(elm)
                        success = True
            except:
                pass
        state = State(url, filtered_elements)
        self.network.add_state(state)
        # убрать это позорище, как можно скорее
        if self.current_state:
            self.network.MG.add_edge(self.current_state, state)
        self.current_state = state
        plt.clf()
        nx.draw(self.network.MG)
        plt.savefig('current_network.png')
        return state

    def set_basement(self):
        self.basement_state = self.current_state

    def wait(self):
        time.sleep(5)

    def move(self):
        # будем пробовать, пока не получится
        success = False
        while not success:
            # крайне сложный выбор элемента с которым мы будем взаимодействовать
            elm = random.choice(self.current_state.elements)
            # т.к. PoC заморачиваться с эффективностью и уникальными программными локаторами мы не будем
            for element in self.driver.find_elements('css selector', '[data-component^="SBIS3.CONTROLS"]'):
                try:
                    if element.get_attribute('innerHTML') == elm.html:
                        element.click()
                        success = True
                except:
                    continue

    def move_to_basement(self):
        """здесь нужно реализовать базовый механизм перемещения к нужному состоянию"""
        self.driver.get('http://test-online.sbis.ru/')
        self.current_state = self.basement_state


class Network:

    def __init__(self):
        self.MG = nx.MultiGraph()

    def add_state(self, state):
        self.MG.add_node(state)
        print('Число нод: {0}, число связей: {1}'.format(self.states_number(),
                                                         self.transition_number()))

    def states_number(self):
        return self.MG.number_of_nodes()

    def transition_number(self):
        return self.MG.number_of_edges()

    def distanse(self, first_state, second_state):
        return nx.shortest_path_length(self.MG, first_state, second_state)


if __name__ == '__main__':
    # создвем сеть, с которой дальше будем общаться
    net = Network()
    # создаём бота
    bot = Bot(net)
    # открываем первую страницу
    bot.open('http://test-online.sbis.ru')
    # проходим аутентификацию
    bot.auth(login, password)
    bot.open('http://test-online.sbis.ru')
    # получаем состояние и записываем его в граф
    bot.get_state()
    # фиксируем текущее состояние как базовую точку
    bot.set_basement()
    while True:
        # выбираем наиболее подходящее действие и выполняем его
        bot.move()
        # дожидаемся окончания телодвижений
        bot.wait()
        # получаем состояние, ищем в графе, если находим - соединяем, если нет - создаем
        state = bot.get_state()

        if net.distanse(bot.basement_state, state) > 3:
            bot.move_to_basement()