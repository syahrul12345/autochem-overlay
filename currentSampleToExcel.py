#The current sample data will be processed in this currentSample.py script
#By default, all samples will now automatically create and save an XLSX file for future processing. This is
#done by the saveToExcel() function.
# import mic
import numpy as numpy
import traceback
import sys
sys.path.append('C:/MicroActive/scripts/Autochem-Master/xlsxwriter')
import xlsxwriter
import os
import mic
path = os.path.dirname(mic.__file__)
#we try to get their axis for each experiment, since each cycle has their own x-data
datas = ['raw temperature','raw time','raw tcd']
def getDataFromAutochem():
	#sample name
	sample_name = mic.sample_information('sample description')
	
    

#lets get all the experiments within this sample:
	exp_all = mic.dyn_chem_experiment_all()
	exp_numbers = []
	exp_descriptions = []
	exp_datas = {}
	for i, expdict in exp_all.items():
		for j, exp in expdict.items():
			#exp is the current cycle such as h2-tpr(cycle 1) etc
			exp_data = {}
			exp_numbers.append( i if j == 0 else "Mass spec %d-%d:" % (i, j))
			exp_descriptions.append(exp["id"] if j == 0 else exp["id"].split(": ", 1)[1])
			
			for data in datas:
				exp_data[data] = exp[data]
			exp_datas[exp["id"]] = exp_data

    #Create XLSX file to save into excel
	wb = xlsxwriter.Workbook('C:/MicroActive/Excel/%s.xlsx' %sample_name)
	ws = wb.add_worksheet()
	ws.write(0,0,sample_name)
	global column
	column = 0
	global dataColumns
	dataColumns = 0
	for key,result in exp_datas.items():
		#key is th name of the current experiment such as 'h2-tpr(cycle1)'
		#results is the dictionary of data values such as temp,time,tcd
		#amount of data available if 
		noOfData = len(result.keys())
		ws.merge_range(1,column,1,column+noOfData-1,key)
		column += noOfData
		# we merge the headers appropriately
		for dataName,dataResults in result.items():
			ws.write(2,dataColumns,dataName)
			ws.write_column(3,dataColumns,dataResults)
			dataColumns += 1

	wb.close()
	
	# our data of interest for version 1 is RAW TCD aginst time for experiment 1(cycle1) 
	# and 3(cylc2)
	# first we obtain the experiments 1 
	#exp1 = mic.dyn_chem_experiment(exp_num = 1)
	#exp2 = mic.dyn_chem_experiment(exp_num = 3)
	#experimentType = ''
	
	# get th name of the experiment
	# name = exp1['id']
	# # for each experiment, we want the raw TCD information
	# experimentType = 'raw tcd'
	# data1 = np.array(exp1[experimentType])
	# data2 = np.array(exp2[experimentType])

	# # get the raw temp for the experiment
	# rawTemp1 = np.array(exp1['raw temperature'])
	# rawTemp2 = np.array(exp2['raw temperature'])
	# absolute1 = data1[0]
	# absolute2 = data2[0]
	# data1 = absolute1 - data1
	# data2 = absolute2 - data2
	# # we get the time range
	# time1 = np.array(exp1['raw time'])
	# time2 = np.array(exp2['raw time'])
	# lengthTime = len(time1)
	# # we plot the graph in micromeritics
	# mic.graph(name,xlabel='temperature (Celcius)',ylabel= experimentType)
	# mic.graph.add(exp1['id'],rawTemp1,data1,marker='o',graphtype='points')
	# mic.graph.add(exp2['id'],rawTemp2,data2,marker='^',graphtype='points')

	# first lets get all the experments
	# sample_name = mic.sample_information('sample description')
	
	# exp_all = mic.dyn_chem_experiment_all()

	# experiment 1,2,3 etc
	
	# experiment descripton such as 'H2 tpr cycle one'
	# for i, expdict in exp_all.items():
 #    	for j, exp in expdict.items():
 #        	exp_number.append(i if j == 0)
 #        	exp_description.append(exp["id"] if j == 0 else exp["id"].split(": ", 1)[1])
	
def saveDataToExcel():
	return null

getDataFromAutochem()
