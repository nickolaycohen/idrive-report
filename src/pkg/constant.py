import json
from enum import Enum

COOKIE = "JSESSIONID=2C9BDBE1435780113780DD4389D5EF24.tomcat8; EVSID=O57IZRCZO07PTZ5FWLAUHA97U92XB50YN8GROYSVX79XCISO6A5PKXKJBQHX; _ga=GA1.1.1750433084.1730231512; __utmc=195969140; _hjSessionUser_5195831=eyJpZCI6IjJmMmMzOTMzLWMyYjYtNWZjZS05NWFlLWNmM2MwMWMxYTY3OSIsImNyZWF0ZWQiOjE3MzE4ODkzNTg4NTAsImV4aXN0aW5nIjp0cnVlfQ==; _clck=fqbcs2%7C2%7Cft3%7C0%7C1763; __utma=195969140.1750433084.1730231512.1738517733.1738527417.5; __utmz=195969140.1738527417.5.3.utmcsr=chatgpt.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _uetvid=e4fd1e30b3de11eeba56f5244243f47a; cto_bundle=yD0oZF9VaFIxS3kxNlRYWHAlMkZOTVBnVlpxZUlDNUFVbThRc0tqTTlQejAwRDBrR1ZHYzE5andMRnE4c1RpcnI5bTZHU0xsc2J1TUlNblJPQm4ybmd5VGhPV1Rrc1pxT0F5TFc2YnJhS2huUkE3bEVoN0dFJTJCMm9td2JvJTJGMyUyQmNxJTJGWVJnRm12NE9FVElaNE04NGg2dmdqWmtCJTJCdDdwZWJYcHhkajRraUklMkJOU3NkUld0NW82UnE0ZmJQd0E0d1QySkdOS3lvWU5leHJuT1k0SWtWNFEwMCUyQnZTOFQ1ckdqTE1hVW16aDZweUtvUzM5eFZjaFglMkZLalQwQTlkb0FuMnBCeWRVeXNadEgwazVWRkNrUDFlTjNqcXVlRUhqeEhqYzhZMjFZJTJGSUh5TFhPaU4lMkZ5eWlBTFYlMkJkMnRUOFl1bEI4RXBtNFZKWA; _ga_WMXM22QXPN=GS1.1.1738547010.8.1.1738547014.56.0.0; WOPI_SESSION=vJbB4Iz2gzMN"

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
