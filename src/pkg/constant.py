import json
from enum import Enum

COOKIE = "JSESSIONID=2C9BDBE1435780113780DD4389D5EF24.tomcat8; EVSID=GJ1NXRORT19BG4C3G2DG43086O6E34JM5329MH0TJNF2S2I1L9EIIY5KG9TZ; _ga=GA1.1.1750433084.1730231512; __utma=195969140.1750433084.1730231512.1730231512.1730231512.1; __utmc=195969140; __utmz=195969140.1730231512.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _uetvid=e4fd1e30b3de11eeba56f5244243f47a; _clck=fqbcs2%7C2%7Cfqf%7C0%7C1763; cto_bundle=rWMl719VaFIxS3kxNlRYWHAlMkZOTVBnVlpxZU1DekYzeDJ6QlVGWjBGJTJGN3RUUHNiWEtTWEM5ajUwTlRjNHpiJTJCJTJGcWc3Nm0wZEo0RTlxQWZVUXVFb1F4ZVBBc2tkTTMzUiUyQiUyRkRJN2R2NmFiQUtVRyUyQkVoOG0yVEZqOHN0UWo2SGUlMkZZbjAxTU5LNENYN0VvNkNLTFV3NmxyNHE1WjBFS0h3YmtLVlpiJTJCSTMlMkJGdHMlMkZTc1NxYmpvYU0zaDN0YXVNRmIyQWR1cEZ5R0llWmd6Qng3SjVUWFBxVDU1U0glMkJOS0RFc0lIRDZ0MTgyYjMzJTJCY1dYaUZvemglMkJ4NmdFNjV4dE5UMkI3UFJ4Vw; _ga_WMXM22QXPN=GS1.1.1730231512.1.0.1730231520.52.0.0; _hjSessionUser_5195831=eyJpZCI6IjJmMmMzOTMzLWMyYjYtNWZjZS05NWFlLWNmM2MwMWMxYTY3OSIsImNyZWF0ZWQiOjE3MzE4ODkzNTg4NTAsImV4aXN0aW5nIjp0cnVlfQ=="

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
