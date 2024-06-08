import json
import sys
import xml.etree.ElementTree as ET 
import constant, os
import requests
import csv
from operator import itemgetter

def getRootElement(string):
    # create element tree object
    return ET.fromstring(string)  

def getDevicesList():
    headers = constant.HEADERS
    devices = list()

    print(constant.statusMsg.CALLING_LIST_DEVICES+'')
    devicesList = requests.post('https://evsweb2652.idrive.com/evs/listDevices', headers=headers)
 
    xml = ET.fromstring(devicesList.content)
    
    # need to filter iDrive Photos bucket before saving
    for item in xml:
        if item.get('device_id') in constant.DRIVE_ID_EXCLUDED:
            xml.remove(item)
        else:
            devices.append({"device_id": item.get('device_id'),
                            "nick_name": item.get('nick_name')}) 
    return devices

def saveFoldersProperties(level, device, paths):
    #headers = constant.HEADERS

    rootPaths = list()
    lowerLevelPathsToRemove = list()
    device_id = device.get('device_id')
    nick_name = device.get('nick_name')

    if level == 1:
        paths = list()
        browseFolderData = { "device_id": device_id, "p": "/"}
        print(constant.statusMsg.CALLING_BROWSE_FOLDERS + device_id, '-', nick_name)
        foldersList = requests.post('https://evsweb2652.idrive.com/evs/browseFolder', headers=constant.HEADERS, data=browseFolderData)
        folderRoot = getRootElement(foldersList.content)
        allItems = folderRoot.findall('item')
        for rootFolder in allItems:
            p = "//" + rootFolder.get('resname')
            restype = rootFolder.get('restype')
            if restype == constant.resType.DIRECTORY:
                folderPropertiesData = {"device_id": device_id, "p": p}
                setFolderProperties(paths, device, p, folderPropertiesData)
            paths = sorted(paths, key=itemgetter('size'),reverse=True)
            paths = paths[:constant.MAX_DIRECTORY_COUNT_TO_RETURN_FOR_NEXT_LEVEL]
        print('*** paths:', json.dumps(paths)) 
    else:
        print('*** else - paths is passed - level is bigger than 1')
    for path in paths:
        resname = path.get('path')
        p = "/" if not paths else "//" + resname

        browseFolderData = {"device_id": device_id, "p": p}
        # get folders for this directory level
        foldersList = requests.post('https://evsweb2652.idrive.com/evs/browseFolder', headers=headers, data=browseFolderData)
        folderlevelRoot = ET.fromstring(foldersList.content)
        for folderItem in folderlevelRoot.findall('item'):
            folderItemResName = folderItem.get('resname')
            restype = folderItem.get('restype')
            if restype == constant.resType.DIRECTORY:
                p = resname + '/' + folderItemResName
                folderPropertiesData = {"device_id": device_id, "p": p}
                setFolderProperties(rootPaths, device, p, folderPropertiesData)
        lowerLevelPathsToRemove.append(path)

    # add lowerLevelPaths if not in higher level paths list
    for pathToRemove in lowerLevelPathsToRemove:
        paths.remove(pathToRemove)
    for lowerLevelPath in paths:
        rootPaths.append(lowerLevelPath)

    # sort combined list
    rootPaths = sorted(rootPaths, key=itemgetter('size'),reverse=True)
    rootPaths = rootPaths[:constant.MAX_DIRECTORY_COUNT_TO_RETURN_FOR_NEXT_LEVEL]

    # field names
    fields = ['device_id', 'path', 'size', 'filecount']

    # name of csv file
    filename = constant.OUTPUT_DIR + constant.FOLDER_PROPS_FILENAME + '-' + nick_name + '-level' + str(level+1) + '.csv'
    
    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv dict writer object
        print(constant.statusMsg.SAVING_FOLDER_STATS + nick_name)
        writer = csv.DictWriter(csvfile, fieldnames=fields)
    
        # writing headers (field names)
        writer.writeheader()
    
        # writing data rows
        writer.writerows(rootPaths) 
    # TODO - fix the return 
    return rootPaths

def setFolderProperties(paths, device, p, getPropertiesData):
    device_id = device.get('device_id')
    nick_name = device.get('nick_name')
    print(constant.statusMsg.CALLING_FOLDER_STATS + nick_name + ' | ' + p)
    folderProperties = requests.post('https://evsweb2652.idrive.com/evs/getProperties', headers=constant.HEADERS, data=getPropertiesData) 
    root = ET.fromstring(folderProperties.content)
    rootPath = root.get('path')
    rootsize = root.get('size')
    filecount = root.get('filecount')
    paths.append({'device_id': device_id, 'path': rootPath, 'size': int(rootsize), 'filecount': int(filecount)})

def main(): 
    # get DevicesList  
    devices = getDevicesList() 
    device = devices[int(sys.argv[1])] if sys.argv[1] else devices[0]

    paths = list()
    currentLevel = 1
    while currentLevel < constant.MAX_DIRECTORY_LEVEL_TO_SCAN:
        # save Folder Properties for passed device index
        paths = saveFoldersProperties(currentLevel, device, paths)
        currentLevel += 1

if __name__ == "__main__": 
  
    # calling main function 
    main() 

