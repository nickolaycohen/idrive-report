from datetime import datetime
from pkg.constant import HEADERS, statusMsg, DRIVE_ID_EXCLUDED, resType
import requests
import xml.etree.ElementTree as ET
from pkg.db import getDBDevices, getDrilledDown, getParentPath, setDrilledDown, setPath, setPathProperties, getTop10Folders
from pkg.util import getRootElement

# Do API retry
# https://stackoverflow.com/questions/23267409/how-to-implement-retry-mechanism-into-python-requests-library

# https://stackoverflow.com/questions/49121365/implementing-retry-for-requests-in-python?rq=3
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

def retry_session(retries, session=None, backoff_factor=0.3):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# Service calls
def getDevices():
    headers = HEADERS
    devices = list()

    print(statusMsg.CALLING_LIST_DEVICES+'')
    session = retry_session(retries=5)
    listDevicesResponse = session.post(url='https://evsweb2652.idrive.com/evs/listDevices', headers=headers)

    if listDevicesResponse and listDevicesResponse.status_code == 200: 
        xml = ET.fromstring(listDevicesResponse.content)
        
        # need to filter iDrive Photos bucket before saving
        for item in xml:
            if not item.get('device_id') in DRIVE_ID_EXCLUDED:
                devices.append({"device_id": item.get('device_id'),
                                "nick_name": item.get('nick_name')}) 
        return devices
    else:
        raise SystemExit('ERROR: Response code:', listDevicesResponse.status_code, listDevicesResponse.text)

def getFolderProperties(device, p):
    device_id = device['device_id']
    nick_name = device['nick_name']
    print(statusMsg.CALLING_FOLDER_STATS + nick_name + ' | ' + p)
    getPropertiesData = {"device_id": device_id, "p": p}
    session = retry_session(retries=5)
    getPropertiesResponse = session.post(url='https://evsweb2652.idrive.com/evs/getProperties', data=getPropertiesData, headers=HEADERS)

    if getPropertiesResponse and getPropertiesResponse.status_code == 200: 
        root = ET.fromstring(getPropertiesResponse.content)
        return {'device_id': device_id, 
                'path': root.get('path'), 
                'size': int(root.get('size')), 
                'filecount': int(root.get('filecount'))}
    else:
        raise SystemExit('ERROR: Response code:', getPropertiesResponse.status_code, getPropertiesResponse.text)


def setDevicesRootPaths(rootpath):
    devices = getDBDevices()
    for device in devices:
        setDevicePaths(rootpath, {'device_id': device[0], 'nick_name': device[1]})
    return 

def setDevicePaths(rootpath, device):
    device_id = device['device_id']
    nick_name = device['nick_name']
    browseFolderData = { "device_id": device_id, "p": rootpath}
    print(statusMsg.CALLING_BROWSE_FOLDERS + device_id, '-', nick_name)
    session = retry_session(retries=5)
    folders = session.post(url='https://evsweb2652.idrive.com/evs/browseFolder', data=browseFolderData, headers=HEADERS)

    folderRoot = getRootElement(folders.content)
    paths = folderRoot.findall('item')

    drilledDown = getDrilledDown(rootpath, device_id)
    # print('drilledDown:', drilledDown)
    if drilledDown == 0:
        print('*** DB *** set path', rootpath, 'of drive: ', device_id, ' | ', nick_name, ' as drilledDown')
        setDrilledDown(rootpath, device_id)

    for path in paths:
        resname = path.get('resname')
        type = path.get('restype')
        lmd = path.get('lmd')
        lmdDB = setPath({"device_id": device_id, "name": resname, "type": type, "lmd": lmd, "rootpath": rootpath})
                  
        needToUpdateSizeFilecount = not(lmdDB and datetime.strptime(lmd, "%Y/%m/%d %H:%M:%S") == datetime.strptime(lmdDB, "%Y-%m-%d %H:%M:%S"))
        if (needToUpdateSizeFilecount):
            parentPath = getParentPath({"device_id": device_id, "name": resname, "parentPath": rootpath})
            p = (parentPath if parentPath == '//' else parentPath + '/') + resname 
            restype = path.get('restype')
            if restype == resType.DIRECTORY:
                folderProperties = getFolderProperties(device, p)    
                setPathProperties(folderProperties)
