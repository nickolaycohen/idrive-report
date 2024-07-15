# DB Calls
import os
import sqlite3

from util import splitPath


def setPath(path):
    device_id = path.get('device_id')
    name = path.get('name')
    type = path.get('type')
    rootpath = path.get('rootpath')
    conn = sqlite3.connect('assets.db')
    c = conn.cursor()
    c.execute("SELECT datetime(replace(lmd, '/', '-')) as 'lmd' from paths where deviceId=:device_id and name=:name and parentPath=:parentPath", {'device_id': device_id, 'name':name, 'parentPath': rootpath})
    res = c.fetchall()
    if len(res) == 0:
        c.execute("INSERT INTO paths VALUES (null, :deviceId, :name, :type, :parentPath, :lmd, :size, :filecount, :drilledDown, :tag)", 
                  {'deviceId': device_id, 'name': name, 'type': type, 'lmd': path.get('lmd'), 'parentPath': rootpath, 'size': 0, 'filecount': 0, 'drilledDown': False, 'tag': ''})
    conn.commit()
    conn.close()        
    if len(res) == 0:
        return None
    else:
        return res[0][0]

def setPathProperties(path):
    device_id = path.get('device_id')
    # need to split the path and parse the parentPath and name and add condition for the DB call
    # name = path.get('path')[2:]
    # parentPath = path. 
    parentPath, name = splitPath(path['path'])
    size = path.get('size')
    filecount = path.get('filecount')
    conn = sqlite3.connect('assets.db')
    c = conn.cursor()
    c.execute("SELECT datetime(replace(lmd, '/', '-')) as 'lmd' from paths where deviceId=:device_id and name=:name and parentPath=:parentPath", {'device_id': device_id, 'name': name, 'parentPath': parentPath})
    res = c.fetchall()
    if len(res) == 1:
        c.execute("UPDATE paths SET size = :size, filecount = :filecount WHERE deviceId=:device_id and name=:name and parentPath=:parentPath", {'device_id': device_id, 'name': name, 'parentPath': parentPath, 'size': size, 'filecount': filecount})
    else:
        raise Exception("DB Update error")
    conn.commit()
    conn.close()        
    if len(res) == 0:
        return None
    else:
        return res[0][0]

def setTag(arg: list):

    device_id = arg[1]
    parentPath, name = splitPath(arg[2])
    tag = arg[3]
    conn = sqlite3.connect('assets.db')
    c = conn.cursor()
    c.execute("SELECT tag as 'tag' from paths where deviceId=:device_id and name=:name and parentPath=:parentPath", {'device_id': device_id, 'name': name, 'parentPath': parentPath})
    res = c.fetchall()
    if len(res) == 1:
        c.execute("UPDATE paths SET tag = :tag WHERE deviceId=:device_id and name=:name and parentPath=:parentPath", {'tag': tag, 'device_id': device_id, 'name': name, 'parentPath': parentPath})
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

def getDBDevices():
    conn = sqlite3.connect('assets.db')
    c = conn.cursor()

    c.execute("SELECT * from devices ")
    res = c.fetchall()
    conn.commit()
    conn.close() 
    return res       

def getParentPath(path):
    device_id = path.get('device_id')
    name = path.get('name')

    conn = sqlite3.connect('assets.db')
    c = conn.cursor()

    c.execute("SELECT parentPath as 'parentPath' from paths where deviceId=:device_id and name=:name and parentPath=:parentPath", {'device_id': device_id, 'name': name, 'parentPath': path.get('parentPath')})
    res = c.fetchall()
    conn.commit()
    conn.close() 
    if len(res) == 0:
        return None
    else:
        return res[0][0]
    
def getDrilledDown(path, device_id):
    conn = sqlite3.connect('assets.db')
    c = conn.cursor()
    c.execute("SELECT drilledDown as 'drilledDown' from paths where deviceId=:device_id and replace(parentPath || '/' || name,'///','//')=:name", {'device_id': device_id, 'name':path})
    res = c.fetchall()
    conn.commit()
    conn.close()        
    if len(res) == 0:
        return None
    else:
        return res[0][0]
    
def setDrilledDown(path, device_id):
    conn = sqlite3.connect('assets.db')
    c = conn.cursor()
    c.execute("SELECT drilledDown as 'drilledDown' from paths where deviceId=:device_id and replace(parentPath || '/' || name,'///','//')=:name", {'device_id': device_id, 'name': path})
    res = c.fetchall()
    if len(res) == 1:
        c.execute("UPDATE paths SET drilledDown = true WHERE deviceId=:device_id and replace(parentPath || '/' || name,'///','//')=:name", {'device_id': device_id, 'name': path})
    else:
        raise Exception("DB Update error")
    conn.commit()
    conn.close()        
    if len(res) == 0:
        return None
    else:
        return res[0][0]

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
                fileCount integer,
                drilledDown boolean,
                tag text)
                """)
        conn.commit()
        conn.close()
# END DB Calls
