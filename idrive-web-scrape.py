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

def getRoot(filename):
    # create element tree object 
    tree = ET.parse(filename) 

    # get root element 
    treeRoot = tree.getroot() 

    return treeRoot

def saveDevicesList():
    payload = constant.PAYLOAD

    print('Will call iDrive for devices attached to the account ... ')
    devicesList = requests.post('https://evsweb2652.idrive.com/evs/listDevices', headers=payload)
 
    xml = ET.fromstring(devicesList.content)
    
    # need to filter iDrive Photos bucket before saving
    for item in xml:
        if item.get('device_id') in constant.DRIVE_ID_EXCLUDED:
            xml.remove(item)
    
    b_xml = ET.tostring(xml)

    # saving the xml file
    print('Generating device List ... ')

    # need to create the out folder if not exist
    os.makedirs(constant.OUTPUT_DIR, exist_ok=True)
    with open(constant.OUTPUT_DIR + constant.DEVICE_LIST, 'wb') as f: 
        f.write(b_xml) 

def saveFoldersList():
    # TODO
    # this is working only for top level folder
    # maybe we need a parameter to be sent with the directoery level
    payload = constant.PAYLOAD

    devicesRoot = getRoot(constant.OUTPUT_DIR+constant.DEVICE_LIST)

    for item in devicesRoot.findall('item'):
        device_id = item.get('device_id')
        nick_name = item.get('nick_name')
        print('device_id:', device_id, '-', nick_name) 
        foldersData = {
            "device_id": device_id,
            "p": "/"
        }

        # get folders for this directory level
        print('Will call iDrive for folders in this directore level ... ')
        foldersList = requests.post('https://evsweb2652.idrive.com/evs/browseFolder', headers=payload, data=foldersData)

        # saving the xml file 
        print('Generating folder List/s/ ... ')

        filename = constant.OUTPUT_DIR + constant.FOLDER_LIST + '-' + device_id + '.xml'
        with open(filename, 'wb') as f: 
            f.write(foldersList.content) 

def getProperties():
    payload = constant.PAYLOAD
    devicesRoot = getRoot(constant.OUTPUT_DIR+constant.DEVICE_LIST)
    for item in devicesRoot.findall('item'):
        device_id = item.get('device_id')
        nick_name = item.get('nick_name')

        filename = constant.OUTPUT_DIR+ constant.FOLDER_LIST + '-' + device_id + '.xml'
        foldersRoot = getRoot(filename)
        paths = list()
        for res in foldersRoot.findall('item'):
            resname = res.get('resname')
            restype = res.get('restype')

            foldersList = {
                "device_id": device_id,
                "p": "//" + resname
            }

            print('Will call iDrive for folder stats ... ')
            folderProperties = requests.post('https://evsweb2652.idrive.com/evs/getProperties', headers=payload, data=foldersList)
            
            folderRoot = ET.fromstring(folderProperties.content)
            path = folderRoot.get('path')
            size = folderRoot.get('size')
            filecount = folderRoot.get('filecount')
            if restype == '0':
                paths.append({'path': path, 'size': int(size), 'filecount': int(filecount)})
        paths = sorted(paths, key=itemgetter('size'),reverse=True)
        print(*paths, sep = ", ") 

        # field names
        fields = ['path', 'size', 'filecount']

        # name of csv file
        filename = constant.OUTPUT_DIR + constant.FOLDER_PROPS + '-' + nick_name + '.csv'
        
        # writing to csv file
        with open(filename, 'w') as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames=fields)
        
            # writing headers (field names)
            writer.writeheader()
        
            # writing data rows
            writer.writerows(paths) 
    return

def main(): 
    # save DevicesList to an xml file 
    saveDevicesList() 

    # browse Folders for each device
    saveFoldersList()

    # browse Folders for each device
    getProperties()

if __name__ == "__main__": 
  
    # calling main function 
    main() 

