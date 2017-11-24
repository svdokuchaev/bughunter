import requests
import config
import random


def send_state(url, title, hash_screen, screenshot, has_bug=None):
    body = {"url": url, "title": title, "state_hash": hash_screen, "screenshot": screenshot}
    if has_bug:
        body["has_bug"] = has_bug
    response = requests.post(config.server_url + "/state", json=body)
    return random.choice([False, 1,2,3,4,5,6])


def send_transaction(id_old, id_new):
    body = {}
    response = requests.post(config.server_url, json=body)
    return True