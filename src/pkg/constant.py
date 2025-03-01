import json
from enum import Enum

COOKIE = "JSESSIONID=10690FB24CD646C6BB09C61BAED01A96.tomcat8; EVSID=EB22DT4GDV9WU7ZSA4QP7FQDCGR0PGZD7EPVUHCE6W2GDWSHAYFN9B7QF3YP; WOPI_SESSION=cy8kPvB6F8vY"

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
