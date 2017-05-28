import json

def input_data():
    config_file = json.loads(open("config.json", "r").read())
    return config_file['customers_file'], config_file['quantity_file'], config_file['proxy_file'], config_file['interval']

def getLastRow():
    config_file = json.loads(open("config.json", "r").read())
    return config_file['last_row']

def isFirstStart():
    config_file = json.loads(open("config.json", "r").read())
    if (config_file['first_start'] == "True"):
        return True
    else:
        return False
        
def notFirstStart():
    config_file = json.loads(open("config.json", "r").read())
    config_file['first_start'] = "False"
    outfile = json.dump(config_file, open("config.json", "w"))

def change_row(row_number):
    config_file = json.loads(open("config.json", "r").read())
    config_file['last_row'] = row_number
    outfile = json.dump(config_file, open("config.json", "w"))
