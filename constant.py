import json
from enum import Enum

COOKIE = "JSESSIONID=0AB0BC40D0CE80F67F9F5B66F70D88EE.tomcat8; EVSID=YIRWAJ407DJV925NJBXL7IRMR77D58O2QO0X5TH5OUX97NEWX8IVFIQ6MDOA; _ga=GA1.1.1595886500.1711031752; __utmc=195969140; __utmz=195969140.1711031752.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _clck=1t2vn9r%7C2%7Cfk9%7C0%7C1541; _ga_6M4NL51X43=GS1.1.1713807257.1.1.1713807537.0.0.0; __utma=195969140.1595886500.1711031752.1713964438.1714132021.5; _uetvid=6fff8c60a20e11ee839f9f2e92805aaf; cto_bundle=XQoQi19aRFhMJTJGREgwNVg3RmNhUFE1N1lCbmw0UXFFb0hwcCUyRmZYRm9Mamt0cEZ3RThRSGdGNGZWeHJ6bVpmNDlYMG1ta1czSk0lMkZTMDJiOEsxR09wampyb0g2SWhLQzlCUTB5Y0hSOThEd3RnejZsTEFSQlZWeDZZcW4lMkZ0b1l3QnczSzE2WkF3U2NQMzJuSDhFN0Z5aFV4dXBpNkJxRXBJeVJEN2t3a2g2b0o0elR6d1dzY3dNbW8lMkJrTiUyQkNocnJ4R2tIWCUyRmhwY1VMcUNBZ2RCVlFIc05VOG1ENnBiMyUyRktPb29aVDM2ck9NZzNEb0pFQ1MxdGo4VVkxUGZZSnFpM3VEZVVSQg; _ga_WMXM22QXPN=GS1.1.1714132020.5.1.1714132035.0.0.0"

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
    CALLING_LIST_DEVICES = '*** CALLING *** iDrive for devices attached to the account ... '
    CALLING_BROWSE_FOLDERS = '*** CALLING *** iDrive for folders in this directore level for:'
    CALLING_FOLDER_STATS = '*** CALLING *** iDrive for folder stats for:'
    GENERATING_DEVICE_LIST = '*** GENERATING *** device List ... '
    GENERATING_FOLDER_LIST = '*** GENERATING *** folder List/s/ for '
    SAVING_FOLDER_STATS = '*** SAVING *** folder stats for '

MAX_DIRECTORY_LEVEL_TO_SCAN = 4

MAX_DIRECTORY_COUNT_TO_RETURN_FOR_NEXT_LEVEL = 3
