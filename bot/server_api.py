import requests
import config


def send_state(url, title, hash_screen, screenshot, has_bug=None):
    try:
        body = {"url": url, "title": title, "state_hash": hash_screen, "screenshot": screenshot}
        if has_bug:
            body["has_bug"] = has_bug
        response = requests.post(config.server_url + "/state", json=body)
        _id = response.json()
        return int(_id)
    except Exception as error:
        print(error)


def send_transaction(source, target, action_type):
    try:
        body = dict(source=source, target=target, action=action_type)
        response = requests.post(config.server_url + "/transition", json=body)
        if response.status_code != 200:
            print("Сервер ответил не 200")
    except Exception as error:
        print(error)