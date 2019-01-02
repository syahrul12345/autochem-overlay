
#plot graph handles the data for the plots
import Data
import tkinter as tk
from tkinter import *
import matplotlib as mpl
import numpy as np
import sys
import matplotlib
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
matplotlib.rcParams["toolbar"] = "toolmanager"
from matplotlib.backend_tools import ToolBase


def plot(data,currentSampleId,tree,children):
	fig = plt.gcf()
	if len(children) == 0:
		createNoFilePopup('No cycles are selected')
	else:
		for child in children:
			columnData = tree.item(child)['values']
			#lets check if current sample:
			addToGraphOverlay(fig,columnData,data.sample2,'raw temperature')
	
	
	
	class TempBtn(ToolBase):
		def trigger(self, *args, **kwargs):
			fig.clear()
			print('cleared')
			sampleInfoDict = data.sample2
			for child in children:
				columnData = tree.item(child)['values']
				try:
					addToGraphOverlay(fig,columnData,data.sample2,'raw temperature')
				except KeyError:
					print('There is no temperature data for')
	class TimeBtn(ToolBase):
		def trigger(self, *args, **kwargs):
			fig.clear()
			print('cleared')
			sampleInfoDict = data.sample2
			for child in children:
				columnData = tree.item(child)['values']
				addToGraphOverlay(fig,columnData,data.sample2,'raw time')
	tm = fig.canvas.manager.toolmanager
	tm.add_tool("Temperature", TempBtn)
	fig.canvas.manager.toolbar.add_tool(tm.get_tool("Temperature"), "toolgroup")
	tm.add_tool("Time", TimeBtn)
	fig.canvas.manager.toolbar.add_tool(tm.get_tool("Time"), "toolgroup")
	plt.show()
	

def addToGraphOverlay(fig,columnData,sampleInfoDict,identifier):
	ax = fig.add_subplot(111)
	currentID = columnData[0]
	cycleToPlot = columnData[2]
	#we create identies for the axises
	xaxisIdentifier = identifier
	yaxisIdentifier = columnData[4]
	#get the values for the cycle
	#the key for sampleInfoDict is the sample ID because ID is usinque
	#get the corresponding sampleInfo from sampleInfoDict
	sampleInfo = sampleInfoDict[currentID]
	cycleData = sampleInfo[2][cycleToPlot]
	xdat = cycleData[xaxisIdentifier]
	ydat = cycleData[yaxisIdentifier]
	ax.plot(xdat,ydat,label=('{}: {} [{}]'.format(currentID,sampleInfo[1],cycleToPlot)))
	ax.set_xlabel(identifier)
	ax.set_ylabel('raw tcd')
	ax.legend()
	fig.canvas.draw()

def createNoFilePopup(fillerText):
	popupwin = tk.Tk()
	popupwin.title('Error !')	
	l = tk.Label(popupwin,justify=tk.LEFT,padx=20,text=fillerText)
	l.grid(row=0)
	popupbutton = tk.Button(popupwin,text="OK",command = popupwin.destroy)
	popupbutton.grid(row=1,column=0)