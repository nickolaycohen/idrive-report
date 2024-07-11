import xml.etree.ElementTree as ET

# Utils
def getRootElement(string):
    # create element tree object
    return ET.fromstring(string)  

def splitPath(path: str):
    # count forward slash
    # last element in the array is "name"
    # all but the last are "parentPath"
    pathArray = path.split('/')
    arraySize = len(pathArray)
    name = pathArray[arraySize-1]
    pathArray.remove(name)
    parentPath = ('/' if arraySize == 3 else '') + '/'.join(pathArray)

    return parentPath, name 
