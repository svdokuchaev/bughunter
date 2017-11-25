# _*_ coding = utf-8 _*_

from model import State, Element, Transition, Bot, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import networkx as nx
from networkx.readwrite import json_graph
import time
import matplotlib.pyplot as plt

class _State:
    """Класс, описывающий состояние страницы"""

    def __init__(self, url='', elements=''):
        self.url = url
        self.elements = elements[:]


class _Element:
    """Отдельный элемент на странице
    Нужно его уметь максимально точно идентифицировать по собранным данным:
      * text
      * size
      * location (?)
      * screentshot
      * atributes (e.g. innerHTML)"""

    def __init__(self, html):
        self.html = html


class Network:
    """Сеть в памяти и в БД и весь функционал с ней связанный"""

    def __init__(self, db):
        """Выгружаем из БД id состояний и переходы в память"""
        self.engine = create_engine('sqlite:///%s' % db, connect_args={'check_same_thread': False})
        Base.metadata.bind = self.engine
        DBSession = sessionmaker(bind=self.engine)
        self.session = scoped_session(DBSession)

    def yaml(self):
        """Выгрузка данных о сети из БД в yaml"""
        nx.write_yaml(self.MG, 'test.yaml')

    def json(self):
        """Выгрузка данных о сети из БД в json"""
        return json_graph.node_link_data(self.MG)

    def add_state(self, bot_id, url, title=None, screenshot=None, state_hash=None, console=None, http_requests=None, request_count=None, has_bug=None):
        """Добавляем новое состояние.
        Здесь же идёт и изменение объекта в памяти и все записи в БД"""
        if screenshot == '':
            screenshot = b''
        if isinstance(screenshot, str):
            screenshot = screenshot.encode('utf-8')
        exists_state = self.get_state(state_hash=state_hash)
        if self.get_state(state_hash=state_hash):
            return exists_state['id']
        state = State(url, title, screenshot, console, has_bug, http_requests, state_hash, request_count)
        self.update_bot(bot_id, state.id, has_bug=None)
        self.session.add(state)
        self.session.commit()
        return state.id

    def get_state(self, state_id=None, state_hash=None):
        """Возвращаем метаданные состояния по его идентификатору"""
        try:
            if state_id:
                return self.session.query(State).filter(State.id == state_id).first().as_dict()
            elif state_hash:
                return self.session.query(State).filter(State.state_hash == state_hash).first().as_dict()
        except:
            return False

    def get_bugs_num(self):
        return self.session.query(State).filter(State.has_bug == True).count()

    def get_states_id(self):
        states = self.session.query(State.id).all()
        states_ids = [id[0] for id in states]
        return states_ids

    def get_edges_id(self):
        return self.session.query(Transition.state_from_id, Transition.state_to_id).all()

    def add_transition(self, source, target, action):
        """Добавляем новый переход"""
        transition = Transition(source, target, action)
        self.session.add(transition)
        self.session.commit()
        return transition.id

    def get_transition(self, transition_id):
        """Возвращаем метаданные переходе по его идентификатору"""
        dict = self.session.query(Transition).filter(Transition.id == transition_id).first().as_dict()
        return dict

    def shortest_path(self):
        """Выдаёт путь от одного состояния до другого"""
        pass

    def find_state(self):
        """Находим в сети нужное состояние"""
        pass

    def get_errors(self):
        """Базовый метод для нахождения ошибок в сети.
        Вынесен отдельно, т.к. будет запускаться отдельно от основной работы ботов.
        Список паттернов на реализацию:
        1. Ошибки в консоли
        2. Пустыае страницы
        3. Ошибки в http запросах
        4. Окно с сообщением об ошибке"""
        pass

    def add_bot(self):
        """Добавляем/обновляем существующего бота"""
        start_time = int(time.time())
        bot = Bot(start_time, 0, 0)
        self.session.add(bot)
        self.session.commit()
        #self.session.refresh(bot)
        return bot.id

    def get_bot(self, bot_id):
        """Находим бота по id"""
        return self.session.query(Bot).filter(Bot.id == bot_id).first()

    def update_bot(self, bot_id, state_id, has_bug=None):
        """Обновление бота"""
        bot = self.get_bot(bot_id)
        print(bot.id)
        bot.state_id = state_id
        bot.states_count += 1
        if (has_bug):
            bot.bugs_count += 1
        self.session.commit()

    def delete_bot(self, bot_id):
        """Удаление бота по id"""
        self.session.query(Bot).filter(Bot.id == bot_id).delete()
        self.session.commit()

    def delete_all_bots(self):
        """Удаление всех ботов"""
        self.session.query(Bot).delete()
        self.session.commit()

    def get_bots_id(self):
        """Возвращает список id активных ботов"""
        bots = self.session.query(Bot.id).all()
        bots_ids = [id[0] for id in bots]
        return bots_ids


if __name__ == '__main__':
    net = Network('network.db')
    # print(net.json())
    import random, string
    urls = ['https://test-online.sbis.ru/fregistry.html?region_left=registry-RegistryOutgoing#region_left=registry-RegistryOutgoing',
            'https://test-online.sbis.ru/fregistry.html',
            'https://test-online.sbis.ru/calendar.html',
            'https://test-online.sbis.ru/test.html',
            'https://test-online.sbis.ru/ver.html',
            'https://test-online.sbis.ru/admin.html',
            'https://test-online.sbis.ru/all.html',
            'https://test-online.sbis.ru/task.html',
            'https://test-online.sbis.ru/salary.html',
            'https://test-online.sbis.ru/welldie.html',
            'https://test-online.sbis.ru/box.html',
            ]
    for i in range(100):
        url = "http://online.sbis.ru/%s" % random.choice(urls)
        net.add_state(url, 'Заголовок', b'', '', False, '')
        actions = ['click', 'type_in', 'mouse_over']
    for i in range(150):
        net.add_transition(random.choice(net.get_states_id()),
                           random.choice(net.get_states_id()),
                           random.choice(actions))