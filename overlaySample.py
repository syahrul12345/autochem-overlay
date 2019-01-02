import os
import json
import re
def getDataFromJson(fileLocation):
        try:
                #Scientist will chose the sample file as an ovrlay, aka 000-151 etc etc
                jsonDir = 'C:/Program Files/Micromeritics/MicroActive for Autochem II 2920/data/json/'
                #first lets get the sample id from fileLocation
                sample_id = os.path.split(os.path.splitext(fileLocation)[0])[1]
                #lets remove the .smp suffix
                #using this sample id, we can find the sample name
                with open(jsonDir+sample_id+'.json') as d:
                        sample_json = json.load(d)
                        sample_name = sample_json['sample name']
                        exp_datas = sample_json['Data']
                        
                return (sample_id,sample_name,exp_datas)
        except:
                raise