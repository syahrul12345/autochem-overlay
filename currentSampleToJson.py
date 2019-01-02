#The current sample data will be processed in this currentSample.py script
#By default, all samples will now automatically create and save an XLSX file for future processing. This is
#done by the saveToExcel() function.
import numpy as numpy
import traceback
import json
import glob
import ntpath

#we try to get their axis for each experiment, since each cycle has their own x-data
datas = ['raw temperature','raw time','raw tcd']
dataBaseJsonPath = 'C:/Program Files/Micromeritics/MicroActive for Autochem II 2920/data/json/database.json'
excelPath = 'C:/Program Files/Micromeritics/MicroActive for Autochem II 2920/data/excel/'
info = {}
def getLatestFile(path):
	list_of_files = glob.glob(path+'*XLS') # * means all if need specific format then *.csv
	latestFilePath = max(list_of_files, key=os.path.getctime)
	seperator = '.XLS'
	return ntpath.basename(latestFilePath).split(seperator,1)[0]

def writeToJSONFile(fileName, data):
	filePathNameWExt = 'C:/Program Files/Micromeritics/MicroActive for Autochem II 2920/data/json/'+fileName + '.json'
	with open(filePathNameWExt, 'w') as fp:
		json.dump(data, fp)

def readJSONFile(jsonLocation):
	with open(jsonLocation) as f:
		dataBaseInJson = json.load(f)
	return dataBaseInJson

def getCurrentSampleData():
	# file location is the location of th database
	fileLocation = 'C:/Program Files/Micromeritics/MicroActive for Autochem II 2920/data/json/CeZr5842 180711-2 1100_5.json'
	sample_id = '000-007'
	sample_name = 'CeZr5842 180711-2 1100/5'
	exp_datas = readJSONFile(fileLocation)
	return (sample_id,sample_name,exp_datas)

