from datetime import datetime
import sys
import xml.etree.ElementTree as ET
import json

from pkg.db import initDB, setDevices, setTag
from pkg.idrive import getDevices, setDevicesRootPaths, getTop10Folders, setDevicePaths

def main(): 
    # idrive-cleaner

    # init DB
    initDB()

    # get DeviceList from Service
    devices = getDevices()

    # update DeviceList in DB
    setDevices(devices)
    
    # process arguments
    # need to add handling of multiple API call types
    argCount = len(sys.argv)
    arg = sys.argv
    if (argCount > 1):
        device = [x for x in devices if (x['device_id'] == sys.argv[1])][0]
        print('*** MAIN *** - NFO: passed device:', device)
        rootPath = sys.argv[2] if argCount == 3 else None
        tag = sys.argv[3] if argCount == 4 else None
        if tag:
            setTag(sys.argv)
        # print('*** MAIN *** - NFO: device id {0} passed'.format(device['device_id']))
        else:
            setDevicePaths(rootPath,device)

    # # compare the deviceLists and 
    # generate two lists for the tagged and untagged items
    ## print('Will generate two asset lists')
    # else:
    #     setDevicesRootPaths("//")    

    # return top 10 entries
    # print('Will call getTop10Folders')
    # top10folders = getTop10Folders()
    # print('top10folders:')
    # print(top10folders)
    # print('json of top10folders:')
    # print(json.dumps(top10folders))
    # return top10folders
    return

if __name__ == "__main__": 
  
    # calling main function 
    main() 
