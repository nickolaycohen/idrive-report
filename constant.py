import json
from enum import Enum

COOKIE = "JSESSIONID=B14AB090C0D4EE2D9BA9C55011BCAB1E.tomcat8; EVSID=DDS9MWGU61NWSOHSGQZUE6RZ1Y4TOFTQ94HC9J7JDT0HI26BUEQ9XRE5FCU3; _ga=GA1.1.1274378669.1692572772; __utmc=195969140; __utmz=195969140.1692572772.1.1.utmgclid=Cj0KCQjw84anBhCtARIsAISI-xcLuCJVgLLLxrpy6nUZV8a78mZtOvhJl4DXwLMeeknauV6GbSd1HtcaAjrjEALw_wcB|utmccn=(not%20set)|utmcmd=(not%20set)|utmctr=(not%20provided); __utma=195969140.1274378669.1692572772.1713297019.1720745449.16; _uetvid=e4fd1e30b3de11eeba56f5244243f47a; _clck=s1onni%7C2%7Cfne%7C0%7C1475; cto_bundle=7Mh8mV9VaFIxS3kxNlRYWHAlMkZOTVBnVlpxZUpvMG5udFNCZ2EyQlI5VHgzU0VIRmJBQlhMYjUzZG1NUTh3dHQwRFJCY0l3T2xDeGNtMkdrMXlRWU1XQVNBSk4xQzZjdlIlMkI0JTJCejlQNTVLbFpjbkVGcCUyRjM5WlYlMkZYaXF2Q1VBcWIyVmIwWGhBJTJGUSUyRjNYYzlCMnhnem8lMkIzSEdhRmY2MFZrYzJmYkJ3dUdEeEhkNVFMalVTb21RNnI2dVU5c2MxZEczTWlsTDBZME9VS09UQWN3c3hmWFg2YlNtZEpTa2swR0QyVUdyUFQ0c3VGR3JGQSUyQm9yT1Z1Q1FYWDIxcFY0aDR6dG5DUEYy; _ga_WMXM22QXPN=GS1.1.1720745448.16.0.1720745450.58.0.0"

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
