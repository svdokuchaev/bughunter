import platform
# general
site = 'https://fix-online.sbis.ru'
login = 'Демо_тензор'
password = 'Демо123'
# bot elements action
wait_element = 3
highlight_action = True
debug = False

if platform.system() == "Linux":
    server_url = "http://10.76.178.67:5556"
    grid_server = "http://test-selenium16:4444/wd/hub"
else:
    server_url = "http://localhost:5556"
    grid_server = ""