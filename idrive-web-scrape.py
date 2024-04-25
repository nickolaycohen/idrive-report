import xml.etree.ElementTree as ET 
import constant
import requests
import csv
from operator import itemgetter, attrgetter

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

    devicesList = requests.post('https://evsweb2652.idrive.com/evs/listDevices', headers=payload)
 
     # saving the xml file 
    with open('deviceList.xml', 'wb') as f: 
        f.write(devicesList.content) 

    devicesRoot = getRoot('deviceList.xml')

    xml = ET.fromstring(devicesList.content)
    
    # # need to filter iDrive Photos bucket before saving
    for item in xml:
        if item.get('device_id') == 'R01663474652000128789':
            xml.remove(item)
    
    b_xml = ET.tostring(xml)

    # saving the xml file
    with open('deviceList.xml', 'wb') as f: 
        f.write(b_xml) 

    devicesRoot = getRoot('deviceList.xml')

    for item in devicesRoot.findall('item'):
        print('device_id-nick_name:', item.get('device_id'), '-', item.get('nick_name')) 

def saveFoldersList():
    payload = constant.PAYLOAD

    devicesRoot = getRoot('deviceList.xml')

    for item in devicesRoot.findall('item'):
        device_id = item.get('device_id')
        nick_name = item.get('nick_name')
        print('device_id:', device_id, '-', nick_name) 
        foldersData = {
            "device_id": device_id,
            "p": "/"
        }

        foldersList = requests.post('https://evsweb2652.idrive.com/evs/browseFolder', headers=payload, data=foldersData)

        # saving the xml file 
        filename = 'foldersList-' + device_id + '.xml'
        with open(filename, 'wb') as f: 
            f.write(foldersList.content) 


def getProperties():
    payload = constant.PAYLOAD
    devicesRoot = getRoot('deviceList.xml')
    for item in devicesRoot.findall('item'):
        device_id = item.get('device_id')
        nick_name = item.get('nick_name')

        filename = 'foldersList-' + device_id + '.xml'
        foldersRoot = getRoot(filename)
        paths = list()
        for res in foldersRoot.findall('item'):
            resname = res.get('resname')
            restype = res.get('restype')

            foldersList = {
                "device_id": device_id,
                "p": "//" + resname
            }

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
        filename = 'folderProps-' + nick_name + '.csv'
        
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

