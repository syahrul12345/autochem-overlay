import sys
sys.path.append('C:/Users/Administrator/AppData/Local/Programs/Python/Python37-32')

import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
if not hasattr(sys, 'argv'):
    sys.argv  = ['']
import overlaySample
import Data
import currentSampleToJson


def getFileLocation(data):
	#should be a SMP file, it will either obtain data from the corresponding XLXS(if it exists) OR
	#create a new XLSX file with the prepackeged mic module by micromeritics(feature still testing, and possibly impossible)
	fileLocation = filedialog.askopenfilename(initialdir = "C:/Program Files/Micromeritics/MicroActive for Autochem II 2920/data",title = "Select file",filetypes=[("Sample files",".smp")])
	data.fileLocation = fileLocation
	
def start(data):
	# check if an overlay file was not slected:
	if data.fileLocation == '':
		createNoFilePopup('No sample overlay file is selected!')
	else:
		# there will be no issue to get the current sample file
		try:
			# lets check if ovrlaySampleExists
			
			#get overlay info
			overlaySampleAns = overlaySample.getDataFromJson(data.fileLocation)
			overlaySampleId = overlaySampleAns[0]
			overlaySampleName = overlaySampleAns[1]
			overlaySampleData = overlaySampleAns[2]
			data.sample2 = overlaySampleAns
			overlaySampleCycles = list(overlaySampleData.keys())
			#get currentsample info
			currentSample = currentSampleToJson.getCurrentSampleData()
			currentSampleId = currentSample[0]
			currentSampleName = currentSample[1]
			currentSampleData = currentSample[2]
			data.sample1 = currentSample
			currentSampleCycles = list(currentSampleData.keys())

			
			#create overlay window
			overlayWindow = tk.Tk()
			overlayWindow.title('Configure Overlay')
			sampleFrame = tk.Frame(overlayWindow)
			
			#create the bottom gui
			#creates an empty table
			tree = ttk.Treeview(overlayWindow)
			tree['show'] = 'headings'
			tree["columns"] = ("zero","one","two","three","four")
			tree.column("zero")
			tree.column("one")
			tree.column("two")
			tree.column("three")
			tree.column("four")

			tree.heading("zero",text="Sample ID")
			tree.heading("one", text="Sample Name")
			tree.heading("two", text="Experiment")
			tree.heading("three", text="X-axis")
			tree.heading("four", text="Y-axis")


			#set overlay info
			overlayVar = StringVar(sampleFrame)
			overlayVar.set(overlaySampleCycles[0])
			overlayDropdown = OptionMenu(sampleFrame,overlayVar,*overlaySampleCycles)
			tk.Label(sampleFrame,text="Overlay Sample {}".format(1),padx=20,justify=tk.LEFT).grid(row = 1,column=0)
			tk.Label(sampleFrame,text=overlaySampleName,padx=5,justify=tk.LEFT).grid(row = 1,column=1)
			overlayDropdown.grid(row = 1,column = 2)
			tk.Button(sampleFrame,text="ADD",padx=5,justify=tk.LEFT,command=lambda: tree.insert("",'end',values=(overlaySampleId,overlaySampleName,overlayVar.get(),"raw time","raw tcd"))).grid(row=1,column=3)

			#set currentsample info
			currentVar = StringVar(sampleFrame)
			currentVar.set(currentSampleCycles[0])
			currentDropdown = OptionMenu(sampleFrame,currentVar,*currentSampleCycles)		
			tk.Label(sampleFrame,text="Current Sample:",padx=20,justify=tk.LEFT).grid(row = 0,column=0)
			tk.Label(sampleFrame,text=currentSampleName,padx=5,justify=tk.LEFT).grid(row = 0,column=1)
			currentDropdown.grid(row = 0, column = 2)
			tk.Button(sampleFrame,text="ADD",padx=5,justify=tk.LEFT,command=lambda: tree.insert("",'end',values=(currentSampleId,currentSampleName,currentVar.get(),"raw time","raw tcd"))).grid(row=0,column=3)
			
			buttonFrame = tk.Frame(overlayWindow)
			tk.Button(buttonFrame,text="Plot",command = lambda: plotGraph(data,currentSampleId,tree,tree.get_children())).grid(row=0,column=0)
			tk.Button(buttonFrame,text="Delete",command=lambda: tree.delete(tree.selection()[0])).grid(row=0,column=1)	
		
			sampleFrame.grid(row=0)
			tree.grid(row = 1)
			buttonFrame.grid(row=2)
			
			overlayWindow.mainloop()
			#triggers the overlay window
			
		except FileNotFoundError:
			createNoFilePopup('No JSON file for {}'.format(data.fileLocation))
		

def plotGraph(data,currentSampleId,tree,children):
	i = 0
	#first lets chck if ther are loops to be selected:
	if len(children) == 0:
		createNoFilePopup('No cycles are selected')
	else:
		currentSampleInfo = data.sample1
		overlaySampleInfo = data.sample2
		#mic.graph('Overlay Graph',xlabel='time(min)',ylabel='TCD')
		for child in children:
			columnData = tree.item(child)['values']
			#lets check if current sample:
			if columnData[0] == currentSampleId:
				#first lets call the corrct cycle
				cycleToPlot = columnData[2]
				#get the values for the cycle
				cycleData = currentSampleInfo[2][cycleToPlot]
				#we create identifier
				xaxisIdentifier = columnData[3]
				xdat = cycleData[xaxisIdentifier]
				#we create identifir
				yaxisIdentifier = columnData[4]
				ydat = cycleData[yaxisIdentifier]
			else:
				cycleToPlot = columnData[2]
				#get the values for the cycle
				cycleData = overlaySampleInfo[2][cycleToPlot]
				#we create identifier
				xaxisIdentifier = columnData[3]
				xdat = cycleData[xaxisIdentifier]
				#we create identifir
				yaxisIdentifier = columnData[4]
				ydat = cycleData[yaxisIdentifier]
				
			
	

def initialize(sampleAndCycles):
	return null
def createNoFilePopup(fillerText):
	popupwin = tk.Tk()
	popupwin.title('Error !')	
	l = tk.Label(popupwin,justify=tk.LEFT,padx=20,text=fillerText)
	l.grid(row=0)
	popupbutton = tk.Button(popupwin,text="OK",command = popupwin.destroy)
	popupbutton.grid(row=1,column=0)
	
def createWindow(data):
	root = tk.Tk()
	root.title('Select Overlay')
	tk.Label(root,text='Select sample file to overlay:',justify=tk.CENTER,padx=20).grid(row=0)
	tk.Button(root,text="Location",justify=tk.CENTER,padx=20,width=25,command=lambda: getFileLocation(data)).grid(row=1)
	frame= tk.Frame(root)
	frame.grid(row=2)
	tk.Button(frame,text="OK" ,command = lambda: start(data)).pack(side=tk.LEFT)
	tk.Button(frame,text="Cancel", command=root.destroy).pack(side=tk.LEFT)
	root.mainloop()

