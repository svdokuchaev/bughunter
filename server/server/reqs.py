auth = {
    "jsonrpc": "2.0",
    "protocol": 4,
    "method": "САП.Authenticate",
    "params": {
        "data": {
            "s": [{
                      "t": "Строка",
                      "n": "login"
                  },
                  {
                      "t": "Строка",
                      "n": "password"
                  },
                  {
                      "t": "Строка",
                      "n": "machine_name"
                  },
                  {
                      "t": "Строка",
                      "n": "machine_id"
                  },
                  {
                      "t": "Строка",
                      "n": "plugin_id"
                  }],
            "d": [None,
                  "1q2w3e4r5t",
                  "TSD-DOKUCHAEVSV",
                  "608949b8-404f-f13b-9045-6ab82d12b1b9",
                  "21bb5389-1c2b-4534-bd02-263ccef5b820"],
            "_type": "record"
        }
    },
    "id": 1
}

headers = {
    'Content-type': 'application/json; charset=UTF-8',
    'User-Agent': 'Webinar Loader',
}