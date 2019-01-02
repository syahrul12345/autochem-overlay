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
import Plot
	
def start(data):
	currentSampleId = '0'
	overlayWindow = tk.Tk()
	overlayWindow.title('Configure Overlay')
	sampleFrame = tk.Frame(overlayWindow)
			
	#create the bottom gui
	#creates an empty table
	tree = ttk.Treeview(overlayWindow)
	tree['show'] = 'headings'
	tree["columns"] = ("zero","one","two","three","four")
	for column in tree["columns"]:
		tree.column(column)
			
	tree.heading("zero",text="Sample ID")
	tree.heading("one", text="Sample Name")
	tree.heading("two", text="Experiment")
	tree.heading("three", text="X-axis")
	tree.heading("four", text="Y-axis")

	#lets create the heading for the current sample 

	#lets create up to Four sample locations
	overlayButtonFrame = tk.Frame()
	widgets = []
	for i in range(1,5):
		title = tk.Label(overlayButtonFrame,name='title{}'.format(i),text="Overlay Sample {}: ".format(i),padx=20,justify=tk.LEFT)
		label = tk.Label(overlayButtonFrame,name='label{}'.format(i),text="",padx=20,justify=tk.LEFT)
		button = tk.Button(overlayButtonFrame,name='button{}'.format(i),text="Location..",justify=tk.CENTER,padx=20,width=25)
		widgets.append([title,label,button])
		title.grid(row = i,column=0)
		label.grid(row = i,column=1)
		button.grid(row=i,column=2)
	buttonFrame = tk.Frame(overlayWindow)
	tk.Button(buttonFrame,text="Plot",command = lambda: plotGraph(data,currentSampleId,tree,tree.get_children())).grid(row=0,column=0)
	tk.Button(buttonFrame,text="Delete",command=lambda: tree.delete(tree.selection()[0])).grid(row=0,column=1)	
	
	def plotGraph(data,currentSampleId,tree,children):
		#plot script handles the plotting
		Plot.plot(data,currentSampleId,tree,children)
		overlayWindow.destroy()
		
	
	overlayButton1 = widgets[0][2]
	overlayLabel1 = widgets[0][1]
	overlayButton1['command'] = lambda:getFileLocation(data,tree,overlayLabel1,overlayButton1,1)
	
	overlayButton2 = widgets[1][2]
	overlayLabel2 = widgets[1][1]
	overlayButton2['command'] = lambda:getFileLocation(data,tree,overlayLabel2,overlayButton2,2)
	
	overlayButton3 = widgets[2][2]
	overlayLabel3 = widgets[2][1]
	overlayButton3['command'] = lambda:getFileLocation(data,tree,overlayLabel3,overlayButton3,3)
	
	overlayButton4 = widgets[3][2]
	overlayLabel4 = widgets[3][1]
	overlayButton4['command'] = lambda:getFileLocation(data,tree,overlayLabel4,overlayButton4,4)
	
	sampleFrame.grid(row=0)
	overlayButtonFrame.grid(row=1)
	tree.grid(row = 2)
	buttonFrame.grid(row=3)
	overlayWindow.mainloop()

def getFileLocation(data,tree,currentLabel,currentButton,number):
	fileLocation = filedialog.askopenfilename(initialdir = "C:/Program Files/Micromeritics/MicroActive for Autochem II 2920/data/NEO",title = "Select file",filetypes=[("Sample files",".smp")])
	data.fileLocation = fileLocation
	try:
		overlaySampleAns = overlaySample.getDataFromJson(data.fileLocation)
		overlaySampleId = overlaySampleAns[0]
		overlaySampleName = overlaySampleAns[1]
		overlaySampleData = overlaySampleAns[2]
		data.sample2[overlaySampleId] = overlaySampleAns
		overlaySampleCycles = list(overlaySampleData.keys())
		currentLabel['text'] = overlaySampleName

		parentFrame = currentLabel.master
		currentButton.grid_forget()
		currentLabel.grid_forget()
		overlayVar = StringVar(parentFrame)
		overlayVar.set(overlaySampleCycles[0])
		overlayDropdown = OptionMenu(parentFrame,overlayVar,*overlaySampleCycles)
		tk.Label(parentFrame,text="Overlay Sample {}".format(number),justify=tk.LEFT).grid(row = number,column=0)
		tk.Label(parentFrame,text=overlaySampleName,justify=tk.LEFT).grid(row = number,column=1)
		overlayDropdown.grid(row = number,column = 2)
		tk.Button(parentFrame,text="ADD",justify=tk.LEFT,command=lambda: tree.insert("",'end',values=(overlaySampleId,overlaySampleName,overlayVar.get(),"raw time","raw tcd"))).grid(row=number,column=3)
		

	except IOError:
		createNoFilePopup('No JSON file for {}'.format(data.fileLocation))

def createNoFilePopup(fillerText):
	popupwin = tk.Tk()
	popupwin.title('Error !')	
	l = tk.Label(popupwin,justify=tk.LEFT,padx=20,text=fillerText)
	l.grid(row=0)
	popupbutton = tk.Button(popupwin,text="OK",command = popupwin.destroy)
	popupbutton.grid(row=1,column=0)
	
	
