#!/usr/bin/python
import json
import requests
import hashlib
import sys
import argparse
import time
import datetime

print('Script started at: ' + datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S'))

apiUrl = 'http://localhost:7043'


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output')
args = parser.parse_args()

if not args.output:
    print('curseParser.py -o <outputPath>')
    sys.exit(2)
else:
    outputpath = args.output
    print('Setting output dir:' + str(outputpath))

start_time = time.time()
modsFound = []
jsonProjects = []
newJson = {}

jsonFileName = outputpath + '/curseProjects.json'
hashFileName = jsonFileName + '.md5'

print('Requesting addon JSON')
j = requests.get(apiUrl + '/api/addon')
j_obj = j.json()

print('Started parsing addon JSON for projects')

newJson['timestamp'] = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
for project in j_obj:
    if (project['PackageType'].lower() == 'mod') and (project['GameId'] == 432):
        tempJson = requests.get(apiUrl + '/api/addon/' + str(project['Id']) + '/files')
        tempJson = tempJson.json()
        for projectFile in tempJson:
            try:
                if str(projectFile['Id']) not in modsFound:
                    modsFound.append(str(projectFile['Id']))
                    tmpMod = {
                        'projectID': project['Id'],
                        'projectFileID': projectFile['Id'],
                        'fileName': projectFile['FileNameOnDisk'],
                        'gameVersion': projectFile['GameVersion']
                    }
                    jsonProjects.append(tmpMod)
            except TypeError:
                print('Error on: ' + str(project['Id']))
                pass

newJson['data'] = jsonProjects
newJson = json.dumps(newJson)
jsonFile = open(jsonFileName, 'w')
jsonFile.write(newJson)
jsonFile.close()

fileHash = hashlib.md5()
fileHash.update(open(jsonFileName).read().encode('utf-8'))

hashFile = open(hashFileName, 'w')
hashFile.write(str(fileHash.hexdigest()))
hashFile.close()
print("--- %s seconds ---" % str(datetime.timedelta(seconds=(time.time() - start_time))))
