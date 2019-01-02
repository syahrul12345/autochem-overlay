#This data.py file contains the data class which contains all teh variables required to overlay the sample
#within the mic module, all other modules will call to this data class and store it within the same data class.
#As of this current release, this data class can store data sets from ONLY 2 samples.

class Data:
	def __init__(self):
		self.fileLocation = ''	
		#sample 1 is defined as current and sample2 is the sample to be overlayed(selected) by the scientists
		self.sample1= {}
		self.sample2 = {}

def data():
	data = Data()
	return data
