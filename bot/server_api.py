# -*- coding: utf-8 -*-
import requests
import config


class ServerApi(object):

    def __init__(self):
        self.bot_id = self.send_start()
        self.headers = {"bot_id": self.bot_id}

    def send_transaction(self, source, target, action_type):
        try:
            body = dict(source=source, target=target, action=action_type)
            response = requests.post(config.server_url + "/transition", json=body, headers=self.headers)
            if response.status_code != 200:
                print("Сервер ответил не 200")
        except Exception as error:
            print("send_transaction error")
            print(error)

    @staticmethod
    def send_start():
        response = requests.post(config.server_url + "/bot")
        try:
            return response.content.decode().strip("\n")
        except Exception:
            raise Exception("Ошибка регистрации бота")

    def send_stop(self):
        response = requests.delete(config.server_url + "/bot", headers=self.headers)
        if response.status_code != 200:
            print("delete /bot error")
            print(response.content.decode())

    def send_state(self, url, title, hash_screen, screenshot, request_count, has_bug):
        try:
            body = {
                "url": url,
                "title": title,
                "state_hash": hash_screen,
                "screenshot": screenshot,
                "request_count": request_count
            }
            if has_bug:
                body["has_bug"] = has_bug
            response = requests.post(config.server_url + "/state", json=body, headers=self.headers)
            _id = response.json()
            return int(_id)
        except Exception as error:
            print("sent_state error")
            print(error)