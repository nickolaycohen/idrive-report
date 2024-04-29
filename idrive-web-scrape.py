import xml.etree.ElementTree as ET 
import constant, os
import requests
import csv
from operator import itemgetter

def filterXML(root, filter):
    for item in root.findall('item'):
        if item.get('device_id') == filter:
            root.remove(item)
    return root 

def getRootElementFromFile(filename):
    # create element tree object 
    tree = ET.parse(filename) 
    return tree.getroot() 

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

def saveFoldersProperties(level, devices, lowerLevelPaths):
    headers = constant.HEADERS

    for device in devices:
        higherLevelPaths = list()
        lowerLevelPathsToRemove = list()
        device_id = device.get('device_id')
        nick_name = device.get('nick_name')

        if level == 1:
            lowerLevelPaths = list()
            foldersData = { "device_id": device_id, "p": "/"}
            print(constant.statusMsg.CALLING_BROWSE_FOLDERS + device_id, '-', nick_name)
            foldersList = requests.post('https://evsweb2652.idrive.com/evs/browseFolder', headers=headers, data=foldersData)
            folderRoot = getRootElement(foldersList.content)
            allItems = folderRoot.findall('item')
            for rootFolder in allItems:
                p = "//" + rootFolder.get('resname')
                restype = rootFolder.get('restype')
                if restype == constant.resType.DIRECTORY:
                    folderPropertiesData = {"device_id": device_id, "p": p}
                    getFolderProperties(headers, lowerLevelPaths, device, p, folderPropertiesData)
            print('*** paths:', lowerLevelPaths) 
        else:
            print('*** else - paths is passed - level is more than 1')
        for path in lowerLevelPaths:
            resname = path.get('path')

            if not lowerLevelPaths:
                p = "/"
            else: 
                p = "//" + resname

            foldersData = {"device_id": device_id, "p": p}

            # get folders for this directory level
            foldersList = requests.post('https://evsweb2652.idrive.com/evs/browseFolder', headers=headers, data=foldersData)
            folderlevelRoot = ET.fromstring(foldersList.content)
            for folderItem in folderlevelRoot.findall('item'):
                folderItemResName = folderItem.get('resname')
                restype = folderItem.get('restype')
                if restype == constant.resType.DIRECTORY:
                    p = resname + '/' + folderItemResName
                    folderPropertiesData = {"device_id": device_id, "p": p}
                    getFolderProperties(headers, higherLevelPaths, device, p, folderPropertiesData)
            lowerLevelPathsToRemove.append(path)

        # add lowerLevelPaths if not in higher level paths list
        for pathToRemove in lowerLevelPathsToRemove:
            lowerLevelPaths.remove(pathToRemove)
        for lowerLevelPath in lowerLevelPaths:
            higherLevelPaths.append(lowerLevelPath)

        # sort combined list
        higherLevelPaths = sorted(higherLevelPaths, key=itemgetter('size'),reverse=True)
        higherLevelPaths =  higherLevelPaths[:constant.MAX_DIRECTORY_COUNT_TO_RETURN_FOR_NEXT_LEVEL]

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
            writer.writerows(higherLevelPaths) 
        # TODO - fix the return 
        return higherLevelPaths

def getFolderProperties(headers, paths, device, p, folderPropertiesData):
    device_id = device.get('device_id')
    nick_name = device.get('nick_name')
    print(constant.statusMsg.CALLING_FOLDER_STATS + nick_name + ' | ' + p)
    folderProperties = requests.post('https://evsweb2652.idrive.com/evs/getProperties', headers=headers, data=folderPropertiesData) 
    folderPropertiesRoot = ET.fromstring(folderProperties.content)
    folderPropertiesRootpath = folderPropertiesRoot.get('path')
    folderPropertiesRootsize = folderPropertiesRoot.get('size')
    filecount = folderPropertiesRoot.get('filecount')
    paths.append({'device_id': device_id, 'path': folderPropertiesRootpath, 'size': int(folderPropertiesRootsize), 'filecount': int(filecount)})

def main(): 
    # directory level
    currentLevel = 1

    # get DevicesList xml 
    devices = getDevicesList() 

    paths = list()
    while currentLevel < constant.MAX_DIRECTORY_LEVEL_TO_SCAN:
        # save Folder Properties for each device
        paths = saveFoldersProperties(currentLevel, devices, paths)
        print('*** paths: ', paths)
        currentLevel += 1

if __name__ == "__main__": 
  
    # calling main function 
    main() 

