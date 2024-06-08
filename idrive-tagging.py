from datetime import datetime
import os
import constant
import requests
import xml.etree.ElementTree as ET
import json 
import sqlite3

# Service calls
def getDevices():
    headers = constant.HEADERS
    devices = list()

    print(constant.statusMsg.CALLING_LIST_DEVICES+'')
    devicesList = requests.post('https://evsweb2652.idrive.com/evs/listDevices', headers=headers)
 
    xml = ET.fromstring(devicesList.content)
    
    # need to filter iDrive Photos bucket before saving
    for item in xml:
        if item.get('device_id') in constant.DRIVE_ID_EXCLUDED:
            #xml.remove(item)
            print(constant.DRIVE_ID_EXCLUDED)
        else:
            devices.append({"device_id": item.get('device_id'),
                            "nick_name": item.get('nick_name')}) 
    return devices

def getFolderProperties(device, p):
    device_id = device[0]
    nick_name = device[1]
    print(constant.statusMsg.CALLING_FOLDER_STATS + nick_name + ' | ' + p)
    getPropertiesData = {"device_id": device_id, "p": p}
    folderProperties = requests.post('https://evsweb2652.idrive.com/evs/getProperties', headers=constant.HEADERS, data=getPropertiesData) 
    root = ET.fromstring(folderProperties.content)
    return {'device_id': device_id, 
            'path': root.get('path'), 
            'size': int(root.get('size')), 
            'filecount': int(root.get('filecount'))}

def setDevicesRootPaths():
    devices = getDevicesFromDB()
    for device in devices:
        device_id = device[0]
        nick_name = device[1]
        browseFolderData = { "device_id": device_id, "p": "/"}
        print(constant.statusMsg.CALLING_BROWSE_FOLDERS + device_id, '-', nick_name)
        folders = requests.post('https://evsweb2652.idrive.com/evs/browseFolder', headers=constant.HEADERS, data=browseFolderData)
        folderRoot = getRootElement(folders.content)
        paths = folderRoot.findall('item')
        for path in paths:
            resname = path.get('resname')
            type = path.get('restype')
            lmd = path.get('lmd')
            print(datetime.strptime(lmd, "%Y/%m/%d %H:%M:%S"))
            # get lmd for the path from DB
            # if path with older lmd exists in DB - call folderProperties
            lmdDB = setPath({"device_id": device_id, "name": resname, "type": type, "lmd": lmd})
            if ( lmdDB):
                print('lmdDB:', lmdDB)
            print('lmd:', lmd)
            print('service date older then the DB - need to update size and filecount:',  
                  not(lmdDB and datetime.strptime(lmd, "%Y/%m/%d %H:%M:%S") == datetime.strptime(lmdDB, "%Y-%m-%d %H:%M:%S")))
            if (not(lmdDB and datetime.strptime(lmd, "%Y/%m/%d %H:%M:%S") == datetime.strptime(lmdDB, "%Y-%m-%d %H:%M:%S"))):
                p = "//" + resname
                restype = path.get('restype')
                if restype == constant.resType.DIRECTORY:
                    folderProperties = getFolderProperties(device, p)    
                    setPathProperties(folderProperties)
    return 

# DB Calls
def setPath(path):
    device_id = path.get('device_id')
    name = path.get('name')
    type = path.get('type')
    conn = sqlite3.connect('assets.db')
    c = conn.cursor()
    c.execute("SELECT datetime(replace(lmd, '/', '-')) as 'lmd' from paths where deviceId=:device_id and name=:name", {'device_id': device_id, 'name':name})
    res = c.fetchall()
    if len(res) == 0:
        c.execute("INSERT INTO paths VALUES (null, :deviceId, :name, :type, :parentPath, :lmd, :size, :filecount)", {'deviceId': device_id, 'name': name, 'type': type, 'lmd': path.get('lmd'), 'parentPath': '', 'size': 0, 'filecount': 0})
    conn.commit()
    conn.close()        
    if len(res) == 0:
        return None
    else:
        return res[0][0]

def setPathProperties(path):
    device_id = path.get('device_id')
    name = path.get('path')[2:]
    size = path.get('size')
    filecount = path.get('filecount')
    conn = sqlite3.connect('assets.db')
    c = conn.cursor()
    c.execute("SELECT datetime(replace(lmd, '/', '-')) as 'lmd' from paths where deviceId=:device_id and name=:name", {'device_id': device_id, 'name':name})
    res = c.fetchall()
    if len(res) == 1:
        c.execute("UPDATE paths SET size = :size, filecount = :filecount WHERE deviceId=:device_id and name=:name", {'device_id': device_id, 'name':name, 'size': size, 'filecount': filecount})
    else:
        raise Exception("DB Update error")
    conn.commit()
    conn.close()        
    if len(res) == 0:
        return None
    else:
        return res[0][0]

def setDevices(devices):
    conn = sqlite3.connect('assets.db')
    c = conn.cursor()

    for device in devices:
        # insert device if not exists
        device_id = device.get('device_id')

        c.execute("SELECT count() from devices where deviceId=:device_id", {'device_id': device_id})
        res = c.fetchall()
        if (res[0][0]) == 0:
            c.execute("INSERT INTO devices VALUES (:deviceId, :nickName)", {'deviceId': device_id, 'nickName': device.get('nick_name')})
    conn.commit()
    conn.close()        
    return

def getDevicesFromDB():
    conn = sqlite3.connect('assets.db')
    c = conn.cursor()

    c.execute("SELECT * from devices ")
    res = c.fetchall()
    conn.commit()
    conn.close() 
    return res       

def initDB():
    dbPath = './assets.db'
    if not os.path.exists(dbPath):
        conn = sqlite3.connect(dbPath)
        c = conn.cursor()

        c.execute("""CREATE TABLE devices (
                deviceId text,
                nickName text)
                """)
        c.execute("""CREATE TABLE paths (
                id integer primary key,
                deviceId text,  
                name text,
                type integer,
                parentPath text,
                lmd text,
                size integer,
                fileCount integer)
                """)
        # c.execute("""CREATE TABLE devicePaths (
        #         deviceId text,  
        #         pathId integer)
        #         """)
        conn.commit()
        conn.close()

def getRootElement(string):
    # create element tree object
    return ET.fromstring(string)  




def main(): 
    # idrive-cleaner

    # init DB
    initDB()

    # get DeviceList from Service
    devices = getDevices()

    # update DeviceList in DB
    setDevices(devices)

    # compare the deviceLists and 
    # generate two lists for the tagged and untagged items
    ## print('Will generate two asset lists')

    setDevicesRootPaths()    

if __name__ == "__main__": 
  
    # calling main function 
    main() 

