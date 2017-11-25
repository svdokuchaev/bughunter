# -*- coding: utf-8 -*-
import platform
# general
site = 'https://fix-online.sbis.ru'
login = 'Демо_тензор'
password = 'Демо123'
# bot elements action
wait_element = 3
highlight_action = True
debug = False
os_p = platform.system()
if os_p == "Linux":
    server_url = "http://10.76.178.67:5556"
    grid_server = "http://test-selenium65:4444/wd/hub"
elif os_p == "Darwin":
    server_url = "http://10.76.178.67:5556"
    grid_server = ""
else:
    grid_server = ""
    server_url = "http://localhost:5556"



