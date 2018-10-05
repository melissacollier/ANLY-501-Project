# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 16:58:16 2018

@author: shera
"""

import pandas as pd
import io
import requests

url = 'https://www.statecancerprofiles.cancer.gov/incidencerates/index.php?stateFIPS=99&cancer=001&race=00&sex=0&age=001&type=incd&sortVariableName=rate&sortOrder=desc&output=1'
s = requests.get(url).content
ds = pd.read_csv(io.StringIO(s.decode('windows-1252')), skiprows=8, skipfooter=27, engine='python')
print(ds.describe())

#split county, state, SEER, NPCR into separate columns
#ds['County'], ds['State'] = ds['County'].str.split(', ', 1).str
#ds['State'], ds['SEER'] = ds['State'].str.split('(', 1).str
#ds['SEER'], ds['NPCR'] = ds['SEER'].str.split(',', 1).str
#ds['NPCR'] = ds['NPCR'].str.replace(")","")

############################################################################################
# export the ds to a .csv
ds.to_csv('uncleaned_cancer.csv', sep=',', encoding='utf-8')

# import the .csv back to investigate the cleanliness
cancer = pd.read_csv('uncleaned_cancer.csv')

# dimension of dataframe
cancer.shape

# #elements in the dataframe
cancer.size

# data type for each variable
cancer.dtypes


# function to write above results to a .txt
def dataInfo(dataset):
    file1 = open('basic dataframe info.txt','a')
    file1.write('Size of the dataframe is ' + str(dataset.shape) +'.\n\n')
    file1.write('There are ' + str(dataset.size) + ' elements in this dataset.\n\n')
    file1.write('Data types of each columns are\n ' + str(dataset.dtypes) +'\n\n')
    file1.close()
    
# test on cancer dataset
dataInfo(cancer)

# detect missing values
def missingValue(dataset):
    print(dataset.isnull().sum())

missingValue(cancer)


### weird, no missing value?
### detect incorrect values using unique()

# get unique value for each variable

def get_Univalue(dataset):
    names = list(dataset) # list of header name
    
    for i in range(0,len(names)-1):
        var = names[i]
        unique_values = dataset[var].unique()
        file1 = open('unique_values.txt','a')
        file1.write('The unique values for ' + ' " '+ str(var) + '"' + ' are ' + str(unique_values) + '.\n\n')
        file1.close()
 
# test on cancer dataset
get_Univalue(cancer)

