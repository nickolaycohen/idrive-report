import json
from enum import Enum

COOKIE = "JSESSIONID=0AB0BC40D0CE80F67F9F5B66F70D88EE.tomcat8; EVSID=DV23GDKLEJJ92EMIYPNTXXIUDH3YBOLP2EN61FVOMFI0KWPRE8JOWRSDTFHX; _ga=GA1.1.1595886500.1711031752; __utmc=195969140; __utmz=195969140.1711031752.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _clck=1t2vn9r%7C2%7Cfk9%7C0%7C1541; _ga_6M4NL51X43=GS1.1.1713807257.1.1.1713807537.0.0.0; __utma=195969140.1595886500.1711031752.1716428127.1716500580.11; _uetvid=6fff8c60a20e11ee839f9f2e92805aaf; cto_bundle=t6NhL19aRFhMJTJGREgwNVg3RmNhUFE1N1lCbmpCUHVzRzhKejE1dmFuZFRaMXElMkJIb3MwbEwlMkZaZzFicGlhaWZqSDFJS0tMS1M3JTJCMVpXRWFrNmcxemcwenhRSVg3VUYydmxJJTJGZGNYMFg5dFZuRFhJMkVMYXpQelJZcyUyRmI5TUYxWWdRZXJlRlh5ekRRRDU3ek4lMkJ5STY4RUFuT0VuaGUlMkJqVTRCbkR6eE1Wc3JTa01iRzlIZzJwUEFTJTJCSWpBaWluRUhzZGYzeGo2aWQ0UGQ0MmRuejBiZGIzY01YMmZJek1wTVo1U0RodGpycmg0JTJCaDdZeEVHbGx3SlFkcW9tNHZaam9mUk0xZVhFcHNIckFGaEV6NW15VDVLVnhKWEZkYXZEQjEzdDlKTFk5NndBdGwwQUxVejc5OVlVSGdoOFElMkZYbFA4JTJGcEglMkJ5; _ga_WMXM22QXPN=GS1.1.1716500568.11.1.1716500582.0.0.0"

HEADERS = {
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"', 
        'Accept': '*/*', 
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 
        "sec-ch-ua-mobile": "?0", 
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36", 
        "sec-ch-ua-platform": 'macOS', 
        "sec-gpc": "1", 
        "host": "evsweb2652.idrive.com", 
        "Cookie": COOKIE
    }

OUTPUT_DIR = './out/'
DEVICE_LIST_FILENAME = 'deviceList.xml'
FOLDER_LIST_FILENAME = 'folderList'
FOLDER_PROPS_FILENAME = 'folderProps'

class resType(str, Enum):
    DIRECTORY = '0'
    FILE = '1'

DRIVE_ID_EXCLUDED = ('R01663474652000128789')

class statusMsg(str, Enum):
    CALLING_LIST_DEVICES = '*** API - SERVICE *** iDrive -  List Devices '
    CALLING_BROWSE_FOLDERS = '*** API - SERVICE *** iDrive - Browse Folders: '
    CALLING_FOLDER_STATS = '*** API - SERVICE *** iDrive - Folder Stats: '

MAX_DIRECTORY_LEVEL_TO_SCAN = 4

MAX_DIRECTORY_COUNT_TO_RETURN_FOR_NEXT_LEVEL = 3
