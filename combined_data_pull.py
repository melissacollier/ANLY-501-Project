# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 11:15:30 2018

@author: Lin
@dataset is very large, please wait for a few mins to load it.
"""

import urllib
import urllib.request
import pandas as pd
import json
import io
import requests

### cleaning data function
def checkType(data):
    ### Checking datatypes before cleaning
    print (data.info())

# get unique value for each variable
def get_Univalue(dataset):
    names = list(dataset) # list of header name
    
    for i in range(0,len(names)-1):
        var = names[i]
        unique_values = dataset[var].unique()
        file1 = open('unique_values.txt','a')
        file1.write('The unique values for ' + ' " '+ str(var) + '"' + ' are ' + str(unique_values) + '.\n\n')
        file1.close()

# detect missing values
def missingValue(dataset):
    print(dataset.isnull().sum())
    
 def main():
    ### Water Data
    url='https://ephtracking.cdc.gov:443/apigateway/api/v1/getCoreHolder/441/2/ALL/ALL/2016/0/0'
    waterResp = urllib.request.urlopen(url)
    waterRawdata = json.loads(waterResp.read().decode())
    # read json into dataframe, "dict" format, cannot read dict directly
    waterDF=pd.DataFrame.from_dict(waterRawdata['pmTableResultWithCWS'])    
    #### output into .csv file, optional
    waterDF.to_csv('waterQuality.csv', sep='\t', encoding='utf-8')
    ### use cleaning data function
    waterResult = waterClean(waterDF)

    ### Cancer Data
    url = 'https://www.statecancerprofiles.cancer.gov/incidencerates/index.php?stateFIPS=99&cancer=001&race=00&sex=0&age=001&type=incd&sortVariableName=rate&sortOrder=desc&output=1'
    s = requests.get(url).content
    ds = pd.read_csv(io.StringIO(s.decode('windows-1252')), skiprows=8, skipfooter=27, engine='python')   


###SPECIFIC TO WATER NEEDS TO BE PULLED OUT
### cleaning data function
def waterClean(data):
    ### Datatype of dataValue is object, change it into numericals
    data['dataValue'] = pd.to_numeric(data['dataValue'], errors='coerce')
       
    ### Checking missing values/typos/outliers in datasets   
    print(pd.isna(data).sum())
    print (data.describe().transpose())
    print (data['display'].value_counts())
    print (data['dataValue'].value_counts())
    print (data['title'].value_counts())
    displayOUT = data['display'].unique()
    dataValueOUT = data['dataValue'].unique()
    titleOUT = data['title'].unique()
    
    ### Cleaning data
    ### 1. remove non detect value of water quality 
    data = data[(data['display'] != 'Non Detect')]
    ### Datatype of dataValue is object, change it into numericals
    data['dataValue'] = pd.to_numeric(data['dataValue'], errors='coerce')
    ### 2. get the means of all values for each county using "groupby" method
    result = data.groupby(['title'])['dataValue'].mean()
    ### change "series" into "dataframe" datatype
    result = result.to_frame().reset_index()
    result.columns = ['Location','Value']
    ### split the location column into two column("county","state"), expand=True to add these two column into dataframe
    result[['county','state']] =result['Location'].str.split(',', n=1, expand=True)
    ### remove the location column
    del result['Location']
    print (result.describe())
    ### the max value is 31.837500, which is lower than 50

    ### According to documents in its original website:
    ### level < 1 means non-dect arsenic
    ### level in (1-10) means less than MCL == "no harm"
    ### level in (10-50) means "harmful"
    ### binning the mean into three categories
    bins = [0,1,10,50]
    labels=['Non Detect','Less than or equal MCL','More than MCL' ]
    result['Quality']=pd.cut(result['Value'],bins,labels=labels)
    return result
    
main()
