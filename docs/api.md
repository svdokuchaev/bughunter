API сервера
===========

Получение всего графа с аттрибутами
-----------------------------------

GET /network

Response:
    {
        'directed': False,
        'multigraph': True,
        'graph': {},
        'nodes': [{
            'url': 'http: //online.sbis.ru',
            'title': None,
            'id': 1
        }],
        'links': [{
            'source': 0,
            'target': 226,
            'key': 0
        }]
    }

Добавление состояния
--------------------

POST /state

data = {
    'url': 'http://test-online.sbis.ru/',
    'title': 'Разводящая',
    'screenshot': 'скриншот_страницы_в_base64',
    'console': '{все_записи_из_консоли_в_формате_json}',
    'http_requests': 'HTTP запросы в формате HAR'
}

Ответ: 54 - идентификатор состояния в БД

Добавление перехода
-------------------

POST /transition

data = {
    'source': '54',
    'target': '55',
    'action': 'click'
}

Ответ: 44 - идентификатор перехода

События
-------

Все события реализованы как broadcast, т.е. прилетают сразу всем подключенным.

1. 'state' - появление нового состояния
    {
        'url': 'http://test-online.sbis.ru/',
        'title': 'Разводящая',
        'id': '54'
    }

2. 'transition' - появление нового перехода
    {
        'source': '54',
        'target': '55',
        'action': 'click'
    }