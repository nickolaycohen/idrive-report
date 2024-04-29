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

    # b_xml = ET.tostring(xml)

    # # saving the xml file
    # print()

    # # need to create the out folder if not exists
    # os.makedirs(constant.OUTPUT_DIR, exist_ok=True)
    # with open(constant.OUTPUT_DIR + constant.DEVICE_LIST_FILENAME, 'wb') as f: 
    #     f.write(b_xml) 
    return devices

def saveFoldersProperties(level, devices, paths):
    # TODO
    # this is currently working only for second level folder
    # Need a parameter to be sent with the directory depth
    headers = constant.HEADERS

    for device in devices:
        pathsToReturn = list()
        device_id = device.get('device_id')
        nick_name = device.get('nick_name')

        if level == 1:
            paths = list()
            foldersData = { "device_id": device_id, "p": "/"}
            print(constant.statusMsg.CALLING_BROWSE_FOLDERS + device_id, '-', nick_name)
            foldersList = requests.post('https://evsweb2652.idrive.com/evs/browseFolder', headers=headers, data=foldersData)
            folderRoot = getRootElement(foldersList.content)
            allItems = folderRoot.findall('item')
            for rootFolder in allItems:
                getFoldersProperties2(headers, paths, device_id, nick_name, rootFolder)
            print('*** paths:', paths) 
        else:
            print('*** else - paths is passed - level is more than 1')
        for path in paths:
            resname = path.get('path')

            if not paths:
                p = "/"
            else: 
                p = "//" + resname

            foldersData = {"device_id": device_id, "p": p}

            # get folders for this directory level
            foldersList = requests.post('https://evsweb2652.idrive.com/evs/browseFolder', headers=headers, data=foldersData)
            folderlevelRoot = ET.fromstring(foldersList.content)
            for folderItem in folderlevelRoot.findall('item'):
                folderItemResName = folderItem.get('resname')
                folderItemRestype = folderItem.get('restype')
                if folderItemRestype == constant.resType.DIRECTORY:
                    getFolderProperties(headers, pathsToReturn, device_id, nick_name, resname, folderItemResName)
            # paths.pop(path)
        pathsToReturn = sorted(pathsToReturn, key=itemgetter('size'),reverse=True)

        # field names
        fields = ['device_id', 'path', 'size', 'filecount']

        # name of csv file
        filename = constant.OUTPUT_DIR + constant.FOLDER_PROPS_FILENAME + '-' + nick_name + '-level2.csv'
        
        # writing to csv file
        with open(filename, 'w') as csvfile:
            # creating a csv dict writer object
            print(constant.statusMsg.SAVING_FOLDER_STATS + nick_name)
            writer = csv.DictWriter(csvfile, fieldnames=fields)
        
            # writing headers (field names)
            writer.writeheader()
        
            # writing data rows
            writer.writerows(pathsToReturn) 

def getFoldersProperties2(headers, paths, device_id, nick_name, rootFolder):
    path = rootFolder.get('resname')
    foldersProps = {"device_id": device_id, "p": "//" + path}
    print(constant.statusMsg.CALLING_FOLDER_STATS + nick_name + ' | ' + path)
    folderProperties = requests.post('https://evsweb2652.idrive.com/evs/getProperties', headers=headers, data=foldersProps)
    folderPropertiesRoot = ET.fromstring(folderProperties.content)
    folderPropertiesRootsize = folderPropertiesRoot.get('size')
    filecount = folderPropertiesRoot.get('filecount')
    paths.append({'device_id': device_id,'path': path,'size': folderPropertiesRootsize,'filecount': filecount})

def getFolderProperties(headers, pathsToReturn, device_id, nick_name, resname, folderItemResName):
    foldersProps = {"device_id": device_id, "p": "//" + resname + '/' + folderItemResName}
    print(constant.statusMsg.CALLING_FOLDER_STATS + nick_name + ' | ' + resname + ' | ' + folderItemResName)
    folderProperties = requests.post('https://evsweb2652.idrive.com/evs/getProperties', headers=headers, data=foldersProps) 
    folderPropertiesRoot = ET.fromstring(folderProperties.content)
    folderPropertiesRootpath = folderPropertiesRoot.get('path')
    folderPropertiesRootsize = folderPropertiesRoot.get('size')
    filecount = folderPropertiesRoot.get('filecount')
    pathsToReturn.append({'device_id': device_id, 'path': folderPropertiesRootpath, 'size': int(folderPropertiesRootsize), 'filecount': int(filecount)})

def main(): 
    # directory level
    currentLevel = 1

    # get DevicesList xml 
    devices = getDevicesList() 

    # browse Folders for each device
    # paths = saveFoldersList(devices)

    paths = list()
    while currentLevel < constant.MAX_LEVEL:
        # browse Folders for each device
        paths = saveFoldersProperties(currentLevel, devices, paths)
        currentLevel += 1
    # get stats and save csv for each folder of each device
    # saveFolderProperties()

if __name__ == "__main__": 
  
    # calling main function 
    main() 

