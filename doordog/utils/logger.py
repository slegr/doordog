""""""
from datetime import datetime
from doordog.utils.configs import get_global_config
from colorama import Fore, Back, Style
import requests
from datetime import datetime

configs = get_global_config()
# Define the endpoint here
logs_endpoint = configs['endpoints']['post-logs']
# Styles
padding = 8
type_colors = {
    'Info': Fore.BLUE,
    'Warning': Fore.YELLOW,
    'Error': Fore.RED,
    'Critical': Fore.YELLOW + Back.RED
}
# Accumulated logs
logs = []

def get_time():
    return datetime.now().strftime("%m/%d/%Y %H:%M:%S")

def log(type, message):
    cur_time = get_time()
    logs.append({'type': type, 'message': message, 'datetime': cur_time})
    # print(type_colors[type] + cur_time + "::",type.ljust(padding), ":", message, Style.RESET_ALL)
    print(type_colors[type] + cur_time + ":", message, Style.RESET_ALL)

def info(message):
    log('Info', message)

def warning(message):
    log('Warning', message)

def error(message):
    log('Error', message)

def critical(message):
    log('Critical', message)

def send_logs():
    if len(logs) > 0:
        response = requests.post(logs_endpoint, data={logs: logs}, timeout=3)
        if response.status_code == 200 or response.status_code == 201:
            logs.clear()
