BugHunter - web-application tester bot
======================================

Проект для хакатона "Стипендия Тензор".
Предназначен для нахождения типовых ошибок через UI и их последующей
визуализации.

Что лежит в проекте
-------------------
    \client - интерфейсная часть визуализации
    \docs - документация по проекту
    \server - реализация бота, сети и API
    \tests - тесты проекта
    readme.md - ты сейчас читаешь этот документ

Как установить
--------------
Устанавливаем все python модули:

    pip install networkx
    pip install requests
    pip install matplotlib
    pip install selenium
    pip install flask
    pip install flask_restful
    pip install flask-socketio
    pip install sqlalchemy
    pip install flask-cors
Качаем и настраиваем chromedriver:
https://sites.google.com/a/chromium.org/chromedriver/getting-started
Запускаем сервер:

    cd /d ./server
    py -3 main.py

Требования
----------

TODO

Что делаем (сервер)
-------------------

Программа минимум:
1. Работа с конфигом
2. [Сеть] состояния и связи вынести в БД, в графе=в памяти хранить только id
3. [Сеть] реализовать механизм поиска состояний
4. [Бот] генератор элементов - правила + проверки
5. [Бот] идентификация элементов
6. [Сеть] механизм определения того, что перед нами ошибка
7. [Сеть] API для ботов и для фронтенда
8. [Бот] инкапсулировать в метод логику работы
9. [Бот] реализовать runner для запуска ботов
10. [Бот][Сеть] считывание текущего состояния
11. [Бот] реализовать логику движения бота по сети
12. [Бот] определение окончания изменений на странице

Программа максимум:
1. Реализация макро-паттернов
2. Контекстные действия
3. Нахождение проблем безопасности и производительности