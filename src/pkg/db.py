# DB Calls
import os
import sqlite3, psycopg2
import json

from .util import splitPath
from .config import load_config

def connect():
    """ Connect to the PostgreSQL database server """
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.', )
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def setPath(path):
    device_id = path.get('device_id')
    name = path.get('name')
    type = path.get('type')
    lmd = path.get('lmd')
    rootpath = path.get('rootpath')
    select_sql = """SELECT lmd from paths where device_id=%s and name=%s and parent_path=%s"""
    insert_sql = """INSERT INTO paths(device_id,name,type,lmd,parent_path,size,file_count,drilled_down,tag) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                        
    try:
        conn = connect()
        curr = conn.cursor()
        curr.execute(select_sql, (device_id,name,rootpath))
        res = curr.fetchall()
        if len(res) == 0:
            curr.execute(insert_sql, 
                    (device_id, name, type, lmd, rootpath, 0, 0, False, '',))
        conn.commit()
        if len(res) == 0:
            return None
        else:
            return res[0][0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return 

def setPathProperties(path):
    device_id = path.get('device_id')
    # need to split the path and parse the parentPath and name and add condition for the DB call
    # name = path.get('path')[2:]
    # parentPath = path. 
    parentPath, name = splitPath(path['path'])
    size = path.get('size')
    filecount = path.get('filecount')
    conn = connect()
    select_sql = """SELECT lmd from paths 
                where device_id= %s and name = %s and parent_path = %s"""
    update_sql = """UPDATE paths 
                SET size = %s, file_count = %s WHERE device_id=%s and name = %s and parent_path=%s"""

    c = conn.cursor()
    c.execute(select_sql, (device_id, name, parentPath))
    res = c.fetchall()
    if len(res) == 1:
        c.execute(update_sql, (size, filecount, device_id, name, parentPath, ))
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
    
    conn = connect()
    select_sql = "SELECT tag from paths where device_id=%sand name=%s and parent_path=%s"
    update_sql = "UPDATE paths SET tag = %s WHERE device_id=%s and name=%s and parent_path=%s"

    c = conn.cursor()
    c.execute(select_sql, (device_id, name, parentPath))
    res = c.fetchall()
    if len(res) == 1:
        c.execute(update_sql, (tag, device_id, name, parentPath))
    else:
        raise Exception("DB Update error")
    conn.commit()
    conn.close()        
    if len(res) == 0:
        return None
    else:
        return res[0][0]

def setDevices(devices):
    conn = connect()
    c = conn.cursor()

    for device in devices:
        # insert device if not exists
        device_id = device.get('device_id')
        c.execute("""SELECT count(*) from devices where device_id = %s """, [device_id])
        res = c.fetchall()
        if (res[0][0]) == 0:
            print('will insert device_id:', device_id)
            c.execute("""INSERT INTO devices VALUES (%s, %s)""", (device_id, device.get('nick_name')))
    conn.commit()
    conn.close()        
    return

def getDBDevices():
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT * from devices ")
    res = c.fetchall()
    conn.commit()
    conn.close() 
    return res       

def getParentPath(path):
    device_id = path.get('device_id')
    name = path.get('name')
    parent_path = path.get('parentPath')

    sql = """SELECT parent_path as "parentPath" from paths 
            where device_id= %s and name = %s and parent_path = %s"""

    conn = connect()

    c = conn.cursor()

    c.execute(sql, (device_id, name, parent_path))
    res = c.fetchall()
    conn.commit()
    conn.close() 
    if len(res) == 0:
        return '//'
    else:
        return res[0][0]
    
def getDrilledDown(path, device_id):
    conn = connect()
    sql = """SELECT drilled_down as drilledDown from paths where device_id = %s and replace(parent_path || '/' || name,'///','//') = %s """
    c = conn.cursor()
    c.execute(sql, (device_id, path))
    res = c.fetchall()
    conn.commit()
    conn.close()        
    if len(res) == 0:
        return None
    else:
        return res[0][0]
    
def setDrilledDown(path, device_id):
    # conn = sqlite3.connect('assets.db')
    conn = connect()
    select_sql = """SELECT drilled_down from paths where device_id=%s and replace(parent_path || '/' || name,'///','//')=%s"""
    update_sql = """UPDATE paths SET drilled_down = true WHERE device_id=%s and replace(parent_path || '/' || name,'///','//')=%s"""

    c = conn.cursor()
    c.execute(select_sql, (device_id, path))
    res = c.fetchall()
    print()
    if len(res) == 1:
        c.execute(update_sql, (device_id, path))
    else:
        raise Exception("DB Update error")
    conn.commit()
    conn.close()        
    if len(res) == 0:
        return None
    else:
        return res[0][0]

def getTop10Folders():
    # conn = sqlite3.connect('assets.db')
    c = conn.cursor()
    c.execute("select  case when p.size / 1000000000000 > 0 then cast(p.size / 1000000000000 as string) || ' TB' when p.size / 1000000000 > 0 then cast(p.size / 1000000000 as string) || ' GB' when p.size / 1000000 > 0 then cast(p.size / 1000000 as string) || ' MB' when p.size / 1000 > 0 then cast(p.size / 1000 as string) || ' kB' else cast(p.size as string) || ' B' end as sizeB, p.deviceId, d.nickName, p.parentPath, p.name, p.size, p.fileCount from paths p inner join devices d on d.deviceId = p.deviceId where not p.drilledDown order by p.size desc limit 10")
    res = c.fetchall()
    conn.commit()
    conn.close() 
    if len(res) == 0:
        return None
    else:
        return res


def initDB():
    # conn = psycopg2.connect(
    #     host="localhost",
    #     database="assets",
    #     user="nickolaycohen",
    #     password=""
    # )
    # print('in initDB')
    conn = connect()
    # dbPath = './assets.db'
    # if not os.path.exists(dbPath):
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS devices (
            device_id text,
            nick_name text)
            """)
    c.execute("""CREATE TABLE IF NOT EXISTS paths (
            id serial primary key,
            device_id text,  
            name text,
            type integer,
            parent_path text,
            lmd text,
            size int8,
            file_count integer,
            drilled_down boolean,
            tag text)
            """)
    conn.commit()
    conn.close()
# END DB Calls

# if __name__ == '__main__':
    # config = load_config()
    # connect(config)