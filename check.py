import sys
sys.path.append('C/users/administrator/appdata/local/programs/python/python37-32/lib/site-packages')
import json
import os, os.path
import xlrd
import glob
import ntpath
import re
import pandas
jsonPath = 'C:/Program Files/Micromeritics/MicroActive for Autochem II 2920/data/json/test/'
excelPath = 'C:/Program Files/Micromeritics/MicroActive for Autochem II 2920/data/excel/'

def readJSONFile(jsonLocation):
        with open(jsonLocation) as f:
                dataBaseInJson = json.load(f)
        return dataBaseInJson

for file in os.listdir(jsonPath):
	answer = readJSONFile(jsonPath + file)
	for key in answer['Data'].keys():
		for dataDictKey in answer['Data'][key].keys():
			print('the length of the experiment: ' + key + 'of data type ' + dataDictKey + 'is ' + str(len(answer['Data'][key][dataDictKey])))
			print(type(''))

