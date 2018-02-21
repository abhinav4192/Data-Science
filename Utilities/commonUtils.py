import os
from os.path import isfile, join

def getAllFiles(folderNames,folderPath):
    filePaths = []
    for folderName in sorted(folderNames):
        folderName = join(folderPath,folderName)
        for fileName in sorted(os.listdir(folderName)):
            fileName = join(folderName,fileName)
            if fileName.endswith('.txt') and isfile(fileName):
                filePaths.append(fileName)
    return filePaths