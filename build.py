#avoid running this in MicroActive as this python3.2 does not support this script. Run from CMD
import sys
sys.path.append('C/users/administrator/appdata/local/programs/python/python37-32/lib/site-packages')
import json
import os, os.path
import xlrd
import glob
import ntpath
import re
import Sample
#contain a key:value pair where key is the sample no , and value is the sample name:
# example : database = {'0-151' : 'SMO12345 J1998G Age 1000/10/5'}
database = {}
dataBaseJsonPath = 'C:/Program Files/Micromeritics/MicroActive for Autochem II 2920/data/json/database.json'
excelPath = 'C:/Program Files/Micromeritics/MicroActive for Autochem II 2920/data/excel/'

def readJSONFile(jsonLocation):
        with open(jsonLocation) as f:
                dataBaseInJson = json.load(f)
        return dataBaseInJson

def writeToJSONFile(fileName, data):
        filePathNameWExt = 'C:/Program Files/Micromeritics/MicroActive for Autochem II 2920/data/json/'+fileName + '.json'
        with open(filePathNameWExt, 'w') as fp:
                json.dump(data, fp)
def buildDatabase():
        database = readJSONFile(dataBaseJsonPath)
        print("Searching for added files")
        for file in os.listdir(excelPath):
                if file.endswith(".XLS"):
                        length = len(str(file))-4
                        fileNumber = file[0:length]
                        #lets check it exists in the database:
                        if fileNumber not in database.keys():
                                #does not exist in datbase
                                print(file + ' not in databas, analyzing')
                                wb = xlrd.open_workbook(excelPath+str(file))
                                ws = wb.sheet_by_index(0)
                                try:
                                        overallDict = parse(ws,'Signal')
                                        overallDict2 = parse(ws,'Temperature')
                                        #copy the top line to add in more information eg 
                                        #overallDict3 = parse(ws,'concentration') <--- for example
                                        print('Temperature Report Found')
                                        dataDict = overallDict2['Data']
                                        for key in overallDict['Data']:
                                                overallDict['Data'][key]['raw temperature'] =overallDict2['Data'][key]['raw temperature']
                                                #add in new data type by coping line above
                                                #overallDict['Data'][key]['raw temperature'] =overallDict3['Data'][key]['raw temperature'] <--- for example
                                except IndexError:
                                        print('No temperature report found')
                                        print(' ')
                                except TypeError:
                                        print('Chemisorption data found')
                                database[fileNumber] = overallDict['sample name']
                                writeToJSONFile('%s'%fileNumber,overallDict)
                                writeToJSONFile('database',database)
def parse(ws,dataType):
        sample = Sample.sample()
        #we create the json file
        #first lets get the type of experiment
        #lets see where the sample report starts
        column = 0
        row = 0
        completeFind = True
        name = ws.cell_value(rowx=5,colx=1)
        while completeFind == True:
                complete = ws.cell_value(rowx=row,colx=column)
                if 'Completed:' not in complete:
                        row +=1
                else:
                        row +=8
                        completeFind == False
                        break
        crawl = True
        while crawl == True:
                check = ws.cell_value(rowx=row,colx=column)
                if column > 20:
                        flag = True
                if dataType not in check:
                        column += 1
                else:
                        crawl = False
                        break
        #column is where the signal report starts
        #we parse starting from that column, since the first header is from 3 cells below
        row +=3
        flag = False
        iterRow = row
        global iterCol
        iterCol = column
        while flag == False:
                #no more experiments
                try:    
                        expName = ws.cell_value(rowx=iterRow,colx=iterCol)
                        if expName == '':
                                break;
                        else:
                                try:
                                        expNameNew = expName.split("- ",1)[1]
                                        sample.sampleDict[expNameNew] = {}
                                        sameExperiment = True
                                except AttributeError:
                                        #chmisorption present
                                        print('Chemisorption Detected')
                                        # for Expvalue in sampleDict.values():
                                        #         #current experiment
                                        #         for key,value in Expvalue.items():
                                        #                 # the key is type of data eg raw tcd
                                        #                 value = list(filter(None,value))
                                        #                 print('The length of ' + key + 'is' + int(len(value)))
                                        #                 sampleDict[Expvalue][key] = value
                                        chemsorptionName = ws.cell_value(rowx=0,colx=column)
                                        sample.sampleDict[chemsorptionName] = {}
                                        sample.sampleDict[chemsorptionName]['raw time'] = ws.col_values(iterCol,0)
                                        sample.sampleDict[chemsorptionName]['raw tcd'] = ws.col_values(iterCol+1,0)
                                        sampeExperiment = False
                                        flag = True
                                        break;

                                while sameExperiment == True:                                                           
                                        #get the correct headers
                                        headerLong = ws.cell_value(rowx=iterRow+1,colx=iterCol)
                                        header = extract(headerLong)
                                        #lets get the value for this header
                                        #current row value is set to the header row
                                        if header == 'Time':
                                                sample.sampleDict[expNameNew]['raw time'] = list(filter(killWhite,ws.col_values(iterCol,iterRow+2)))
                                        if header == 'Signal':
                                                sample.sampleDict[expNameNew]['raw tcd'] = list(filter(killWhite,ws.col_values(iterCol,iterRow+2)))
                                        if header == 'Temperature':
                                                sample.sampleDict[expNameNew]['raw temperature'] = list(filter(killWhite,ws.col_values(iterCol,iterRow+2)))
                                        iterCol += 1

                                        try:
                                                expName1 = ws.cell_value(rowx=iterRow,colx=iterCol)
                                                if expName1 == '':
                                                        #if empty value means same sample
                                                        continue
                                                elif expName1 == '|':
                                                        #end of report with dash
                                                        #lets find the concentration 
                                                        concentrationFlag = False
                                                        iterCol += 1
                                                        while concentrationFlag == False:
                                                                expNameConc = ws.cell_value(rowx=iterRow,colx=iterCol)
                                                                # expNameConc is equals to Concentration - H2TPR(First Cycle)
                                                                if 'Concentration' in expNameConc:
                                                                        while True:
                                                                                concExp = expNameConc.split("- ",1)[1]
                                                                                header = extract(ws.cell_value(rowx=iterRow+1,colx=iterCol))
                                                                                if header == 'Concentratio':
                                                                                        sample.sampleDict[concExp]['raw concentration'] = list(filter(killWhite,ws.col_values(iterCol,iterRow+2)))
                                                                                        break
                                                                                else:
                                                                                        iterCol +=1
                                                                else:
                                                                        try:
                                                                                iterCol +=1
                                                                        except IndexError:
                                                                                print('Attmptd to find Concentration and attempt end')
                                                                                break

                                                else:
                                                        expNameTemp = expName1.split("- ",1)[1]
                                                        if expNameTemp == expNameNew:
                                                                continue
                                                        else:
                                                                break

                                        except (IndexError,AttributeError):
                                                #index error means end of data
                                                break

                except IndexError:
                        print('End of Report')
                        flag = True
        overallDict = {}
        overallDict['sample name'] = name
        overallDict['Data'] = sample.sampleDict
        return overallDict
        
def killWhite(dataPoint):
        if dataPoint == '':
                return False
        else:
                return True

def extract(headerLong):
        spaceIndex = headerLong.find(' ')
        header = headerLong[0:spaceIndex]
        return header
def getLatestFile(path):
        list_of_files = glob.glob(path+'*XLS') # * means all if need specific format then *.csv
        latestFilePath = max(list_of_files, key=os.path.getctime)
        seperator = '.XLS'
        return ntpath.basename(latestFilePath).split(seperator,1)[0]

if __name__ == "__main__":
        buildDatabase()
        