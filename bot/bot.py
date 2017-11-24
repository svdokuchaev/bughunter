"""
# TODO
1) Число запросов при переходе к состоянию
2) Добавить ID бота
3) Действия: ввод, наведение мышки
"""
from collections import defaultdict
import time
import requests
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from elements import Element, ElementsList, wait
import config
import random
import hashlib
import server_api


class States:

    def __init__(self):
        self.__count = 0
        self.current_state = None

    def add_state(self, url, title, hash_screen, screen, errors):

        r = server_api.send_state(url=url, title=title, hash_screen=hash_screen, screenshot=screen)
        if r:
            server_api.send_transaction(self.current_state, r)
            self.__count += 1
            print("=" * 50)
            print("Count States", self.__count)
            print("=" * 50)
            self.current_state = r
            return True
        else:
            return False


class Elements:

    def __init__(self, driver):
        self.top_item = ElementsList(driver, 'a.nav-menu-item__level-1')
        self.sub_item = ElementsList(driver, '.navigation-nav__subMenuOverLink')
        self.head_title_item = Element(driver, '.navigation-nav__HeadTitle')
        self.tabs = ElementsList(driver, '[data-component="SBIS3.CONTROLS.TabButtons"] .controls-TabButton')
        self.controls = ElementsList(driver, '[data-component^="SBIS3.CONTROLS"]')


class Bot(object):

    def __init__(self, registry):
        capabilities = webdriver.DesiredCapabilities.CHROME
        capabilities['loggingPrefs'] = {'browser': "SEVERE", 'performance': 'ALL'}
        self.driver = webdriver.Chrome(desired_capabilities = capabilities)
        self.driver.maximize_window()
        self.start_url = None
        self.items = defaultdict(list)
        self.elements = Elements(self.driver)
        self.states = States()
        self.registry = registry

    def setup(self):
        # открываем первую страницу
        self.open(config.site)
        self.auth(config.login, config.password)
        self.open(config.site)
        time.sleep(2)
        self.start_url = self.driver.current_url

    def open(self, url):
        self.driver.get(url)

    def get_errors(self):
        """"""
        errors = self.driver.get_log('browser')
        return [e for e in errors if "favicon.ico" not in e["message"]]

    def get_network(self):
        """получение траффика"""

        self.driver.get_log('performance')

    def add_state(self):
        """"""
        url = self.driver.current_url
        title = self.driver.title
        screen = self.driver.get_screenshot_as_base64()
        hash_screen = hashlib.md5(screen.encode()).hexdigest()
        errors = self.get_errors()
        requests_count = self.get_network()
        self.states.add_state(url, title, hash_screen, screen, errors)

    def auth(self, login, password):
        auth = {"jsonrpc": "2.0", "protocol": 4, "method": "САП.Authenticate", "id": 1,
                "params": {"data": {
                    "s": [{"t": "Строка", "n": "login"},
                          {"t": "Строка", "n": "password"}],
                    "d": [login, password],
                    "_type": "record"}}}
        headers = {'Content-type': 'application/json; charset=UTF-8', 'User-Agent': 'BugHunter/0.1'}
        r = requests.post('%s/auth/service/sbis-rpc-service300.dll' % config.site,
                          headers=headers, json=auth)
        sid = r.cookies.get("sid")
        cps = r.cookies.get("CpsUserId")
        self.driver.add_cookie({'name': 'sid', 'value': sid, 'path': '/', 'secure': False})
        self.driver.add_cookie({'name': 'CpsUserId', 'value': cps, 'path': '/', 'secure': False})

    def kill(self):
        self.driver.quit()

    def move(self):
        sub_index = 0

        while True:
            time.sleep(3)
            # пройтись по списку, открыть страницы
            item = self.elements.top_item.item(self.registry)
            text = item.text.split('\n')[0]
            print('Head ', text)

            # открыть пункт
            if not item.click():
                raise Exception("Бот не смог открыть головной раздел")

            # проверяем, а не ушли ли мы с нажатия на top пункт сразу же в раздел
            # если нет подразделов
            sub_items = self.items[text]
            current_url = self.driver.current_url
            if current_url != self.start_url:
                sub_items.append((current_url,))
                time.sleep(5)
                self.walk_on_tabs()
                break

            # часто и 1 пункт кликабельный
            if not sub_items:  # если это в первый раз
                self.elements.head_title_item.click()
                time.sleep(1)

            # проверяем, а не произошел ли переход по нажатию на head
            sub_items = self.items[text]
            current_url = self.driver.current_url
            if current_url != self.start_url:
                sub_items.append((current_url, ))
                self.walk_on_tabs()
                self.driver.get(self.start_url)
                continue

            # получаем список элементов
            count_sub_elements = self.elements.sub_item.count_elements

            sub_element = self.elements.sub_item.item(sub_index)
            if sub_element and sub_element.text:
                sub_text = sub_element.text.split('\n')[0]
                print("Sub ", sub_text)
                sub_element.click()
                time.sleep(2)
                current_url = self.driver.current_url
                if current_url != self.start_url:
                    sub_items.append((current_url,))
                    print("Url ", current_url)
                    self.items[text].append((sub_text, current_url))
                    self.walk_on_tabs()

            self.driver.get(self.start_url)
            sub_index += 1
            if sub_index == count_sub_elements:
                break

    def walk_on_tabs(self):
        tabs = self.elements.tabs
        res = wait(lambda: self.elements.tabs.is_displayed is True, 10)
        if res:
            time.sleep(5)
            su = self.driver.current_url
            for index in range(tabs.count_elements()):
                negative = 0
                while negative < 10:
                    tab = tabs.item(index)
                    if tab.is_displayed and 'controls-Checked__checked' not in tab.css_class:
                        print(tab.text)
                        if not tab.click():
                            negative += 1
                            continue
                        time.sleep(3)
                        res = self.walk_in_registry()
                        if res:
                            negative = 0
                        else:
                            negative += 1
                        time.sleep(5)
                        self.open(su)
                        if self.close_windows_and_alert():
                            self.open(su)
                    else:
                        break

                self.driver.get(su)
                wait(lambda: self.elements.tabs.is_displayed is True, 10)
        else:
            negative = 0
            time.sleep(5)
            su = self.driver.current_url
            while negative < 10:
                time.sleep(3)
                res = self.walk_in_registry()
                if res:
                    negative = 0
                else:
                    negative += 1
                time.sleep(5)
                self.open(su)
                if self.close_windows_and_alert():
                    self.open(su)

    def close_windows_and_alert(self):
        """Закрывает все открытые окна, кроме 1.
        Закрывает окно с alert
        Переключается на 1 окно
        """
        res = False
        self.close_alert()
        windows = self.driver.window_handles
        if len(windows) > 1:
            for window in windows[1:]:
                self.driver.switch_to.window(window)
                res1 = self.close_alert()
                self.driver.refresh()
                res2 = self.close_alert()
                if not res:
                    res = res1 or res2
        self.driver.switch_to.window(self.driver.window_handles[0])
        return res

    def close_alert(self):
        """Закрывает alert"""
        time.sleep(0.5)
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
            return True
        except NoAlertPresentException:
            return False

    def walk_in_registry(self):
        counter = 0
        negative = 0
        set_elements = set()
        findNewState = False
        while negative < 25:
            count = self.elements.controls.count_elements()
            index = random.randint(0, count)
            item = self.elements.controls.item(index)
            hash_elm = item.hash()
            if hash_elm not in set_elements and item.get_attribute('name') != "UserNameLinkButton":
                set_elements.add(hash_elm)
                size = item.size
                if size['height'] * size['width'] > 255:
                    if item.click():
                        # TODO новые окна!!!
                        counter += 1
                        negative = 0
                        time.sleep(1)
                        if self.add_state():
                            findNewState = True
                        if counter > 10:
                            return findNewState
                        else:
                            continue
            negative += 1
        return False


def run_bot(registry):
    bot = Bot(registry)
    try:
        bot.setup()
        bot.move()
    except Exception as error:
        print(error)
    finally:
        bot.kill()

if __name__ == '__main__':
    run_bot(1)