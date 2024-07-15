from datetime import datetime
import constant
import requests
import xml.etree.ElementTree as ET
from db import getDBDevices, getDrilledDown, getParentPath, setDrilledDown, setPath, setPathProperties
from util import getRootElement

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
    headers = constant.HEADERS
    devices = list()

    print(constant.statusMsg.CALLING_LIST_DEVICES+'')
    session = retry_session(retries=5)
    devicesList = session.post(url='https://evsweb2652.idrive.com/evs/listDevices', headers=headers)
 
    xml = ET.fromstring(devicesList.content)
    
    # need to filter iDrive Photos bucket before saving
    for item in xml:
        if not item.get('device_id') in constant.DRIVE_ID_EXCLUDED:
            devices.append({"device_id": item.get('device_id'),
                            "nick_name": item.get('nick_name')}) 
    return devices

def getFolderProperties(device, p):
    device_id = device['device_id']
    nick_name = device['nick_name']
    print(constant.statusMsg.CALLING_FOLDER_STATS + nick_name + ' | ' + p)
    getPropertiesData = {"device_id": device_id, "p": p}
    session = retry_session(retries=5)
    folderProperties = session.post(url='https://evsweb2652.idrive.com/evs/getProperties', data=getPropertiesData, headers=constant.HEADERS)

    root = ET.fromstring(folderProperties.content)
    return {'device_id': device_id, 
            'path': root.get('path'), 
            'size': int(root.get('size')), 
            'filecount': int(root.get('filecount'))}

def setDevicesRootPaths(rootpath):
    devices = getDBDevices()
    for device in devices:
        setDevicePaths(rootpath, {'device_id': device[0], 'nick_name': device[1]})
    return 

def setDevicePaths(rootpath, device):
    device_id = device['device_id']
    nick_name = device['nick_name']
    browseFolderData = { "device_id": device_id, "p": rootpath}
    print(constant.statusMsg.CALLING_BROWSE_FOLDERS + device_id, '-', nick_name)
    session = retry_session(retries=5)
    folders = session.post(url='https://evsweb2652.idrive.com/evs/browseFolder', data=browseFolderData, headers=constant.HEADERS)

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
            if restype == constant.resType.DIRECTORY:
                folderProperties = getFolderProperties(device, p)    
                setPathProperties(folderProperties)
