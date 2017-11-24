# -*- coding: utf-8 -*-
"""
| Модуль содержит в себе базовый класс для моделирования всех элементов
| и класс для работы с дочерними элементами.
"""
import time
import hashlib
import functools
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
import config


def wait(action, wait_time=True):
    """Метод в качестве параметра получает функцию action

    Ждет wait_max время пока функция не вернет True
    Если не возвращает, то вернет в конце результат выполнения функции.

    :param action: действие которое ожиданем
    """
    if wait_time is True:
        end_time = time.time() + config.wait_element
    else:
        end_time = time.time() + wait_time
    tmp_err = None
    res = False
    while True:
        try:
            res = action()
            if res is not False:
                return res
            tmp_err = None
        except Exception as error:
            tmp_err = error
        if time.time() > end_time:
            break
        time.sleep(0.1)

    if not res and tmp_err is None:
        return False
    else:
        return tmp_err


def find_elements(how, locator, webelement):
    """Обертка для поиска элементов в элементах

    :param how: стратегия поиска
    :param locator: локатор
    :param webelement: если ищем в родительском элементе
    """
    return webelement.find_elements(how, locator)


def highlight_action(element):
    """Подсветка элемента

    :param element: инициализированный экземпляр с драйвером atf.elements.element.Element
    """
    try:
        driver = element.driver
        driver.execute_script(
            "arguments[0].style.border = '3px solid red'", element.webelement()
        )
        time.sleep(0.2)
        driver.execute_script(
            "arguments[0].style.border = ''", element.webelement()
        )
    except WebDriverException:
        pass


def before_after(f):
    """Декоратор выполнения действий до/после action

    :param f: выполняемый action
    """
    @functools.wraps(f)
    def tmp(*args, **kwargs):
        """
        :param args: список параметров метода f
        :param kwargs: словарь параметров метода f
        """

        if config.highlight_action:
            highlight_action(args[0])
        # выполнение действия
        return f(*args, **kwargs)
    return tmp


class Element:
    """Базовый класс для всех элементов

    | Содержит в себе методы, которые актуальны для большинства наследников.
    | При этом сам может быть использован для моделирования в коде объектов,
    | которые не подходят ни под одного наследника. Типичные примеры:

    * блок страницы с картинкой
    * div, появления которого нужно просто дождаться

    :param how: локатор нахождения webelement
    :param locator: локатор нахождения webelement
    """

    def __init__(self, driver, locator, how=By.CSS_SELECTOR):
        # список методов для поиска элементов
        self._webelements = [lambda webelement: find_elements(how, locator, webelement)]
        self.driver = driver
        self._current_webelement = self.driver  # нужен для поиска вложенных
        self.how = how
        self.locator = locator

    @staticmethod
    def _wait_property(action):
        """Ожидание выполнения свойства"""

        result = False
        wait_time = config.wait_element
        while time.time() < wait_time + time.time():
            try:
                config.wait_element = 0
                result = action()
            except NoSuchElementException:
                break
            except WebDriverException:
                pass
            finally:
                config.wait_element = wait_time
                return result

    def webelement(self, methods_list=None, return_list=False):
        """Вычисляем webelement по заданному локатору и стратегии поиска

        Метод пытается найти webelement self._config.WAIT_ELEMENT_LOAD секунд.
        Если webelement не найден за указанное время,
        вызовет NoSuchElementException
        :param methods_list: если передан список методов получения webelement'ов, то берем его, а не self._webelements
        :param return_list: возвращать список webelement или 1 webelement
        """
        if not methods_list:
            methods_list = self._webelements
        webelements = []  # чтобы PyCharm не ругался
        end_time = time.time() + config.wait_element
        while True:
            assert self.driver, 'Не передан драйвер элементу! Проверьте правильность инициализации Page/Region'
            self._current_webelement = self.driver
            # перебираем всю цепочку локаторов
            for method in methods_list:
                try:  # страница может измениться и элемент пропадет
                    # для совместимости, не везде нужен driver в параметрах
                    webelements = method(self._current_webelement)
                    if len(webelements) > 0:
                        self._current_webelement = webelements[0]
                        continue  # если получили элемент, то идем дальше
                    else:  # если не получили, то вычисляем всю цепочку сначала
                        break
                except WebDriverException:
                    break  # если было исключение, то идем сначала
            else:
                break

            time.sleep(0.05)
            if time.time() > end_time:
                print("Не удалось дождаться появления элемента " + self.name_output())
                break
        return webelements if return_list else webelements[0]

    def name_output(self):
        """Метод вычисляет название элементов"""

        log_message = 'c локатором "%s"' % self.locator
        return log_message

    @property
    def is_displayed(self):
        """Воозвращает True, если webelement отображается для пользователя"""

        result = self._wait_property(lambda: self.webelement().is_displayed())
        return result

    def is_enabled(self):
        """Возвращает True, если webelement доступен, False - нет"""

        result = self._wait_property(lambda: self.webelement().is_enabled())
        return result

    @property
    def text(self):
        """Возвращает текст, который содержит webelement"""

        result = self._wait_property(lambda: self.webelement().text)
        if not result:
            result = ''
        return result

    @property
    def coordinates(self):
        """Возвращаем координаты webelement"""

        result = self._wait_property(lambda: self.webelement().location)
        if not result:
            result = {'x': 0, 'y': 0}
        return result

    @property
    def size(self):
        """Возвращаем высоту и ширину объекта"""

        result = self._wait_property(lambda: self.webelement().size)
        if not result:
            result = {'width': 0, 'height': 0}
        return result

    def count_elements(self):
        """Количество элементов на странице"""

        result = self._wait_property(lambda: len(self.webelement(return_list=True)))
        if not result:
            result = 0
        return result

    @property
    def css_class(self):
        """Возвращает строку с css классами элемента"""

        return self.get_attribute('class')

    def inner_html(self):
        """Метод получает html код лежащий внутри webelement"""

        return self.get_attribute('innerHTML')

    def hash(self):
        """md5"""

        return hashlib.md5(self.inner_html().encode()).hexdigest()

    @before_after
    def click(self):
        """Производим клик по элементу

        Если клик не удался, то пытается сделать его self._wait_max секунд
        """

        result = wait(lambda: self.webelement().click())
        return self._check_result_action(result)

    @before_after
    def js_click(self):
        """Клик через JS с игнорированием всех проверок"""

        result = wait(lambda: self.driver.execute_script("arguments[0].click()", self.webelement()))
        return self._check_result_action(result)

    @before_after
    def clear(self):
        """Метод для очистки поля"""

        result = wait(lambda: self.webelement().clear())
        return self._check_result_action(result)

    @before_after
    def type_in(self, tmp_str):
        """Вводит текст в webelement, поле не очищается перед вводом

        :param tmp_str: тест для ввода
        """

        result = wait(lambda: self.webelement().send_keys(tmp_str))
        return self._check_result_action(result)

    def get_attribute(self, attribute):
        """Возвращает значение указанного аттрибута

        :param attribute: атрибут элемента
        """
        result = wait(lambda: self.webelement().get_attribute(attribute))
        if self._check_result_action(result):
            return result
        else:
            return ""

    @staticmethod
    def _check_result_action(result):
        """Метод проверяет результаты выполнения action

        :param result: результат выполнения action
        """
        if isinstance(result, Exception):
            if config.debug:
                print(result)
            return False
        else:
            return True


class Item(Element):

    def __init__(self, how, locator, webelements_func, driver, item_number):
        super().__init__(driver, locator, how)
        copy_webelements_func = webelements_func.copy()
        self._custom_list = copy_webelements_func[-1]
        self.driver = driver
        self.item_number = item_number
        self._webelements = copy_webelements_func[:-1] + [self._get_search_strategy()]

    def _get_search_strategy(self):
        """Возвращает WebElement указанного элемента списка"""

        def method(webelement):
            return self.__get_item_by_number(self.item_number, self._custom_list, self.driver, webelement)
        return method

    def __get_item_by_number(self, item_number, custom_list, driver, webelement):
        """Возвращает WebElement элемента списка с
        заданным порядковым номером
        :param item_number: номер item
        :param custom_list: функция для нахождения списка элементов
        :param driver: драйвер
        :param webelement: webelement в котором ищем
        """

        def func(): return custom_list(webelement=webelement)
        result = wait(lambda: len(func()) >= item_number)
        if result is True:
            return [func()[item_number], ]  # для совместимости

    @property
    def position(self):
        """Позиция элемента в списке"""

        self.webelement()  # надо для того чтобы вычислить номер
        return self.item_number


class ElementsList(Element):
    """Класс для работы с разнообразными списками"""

    def item(self, item_number):
        """Возвращает экземпляр класса Item"""

        return Item(
            how=self.how, locator=self.locator, driver=self.driver,
            webelements_func=self._webelements, item_number=item_number
        )

    @property
    def size(self):
        """Возвращает размер списка"""

        return self.count_elements
