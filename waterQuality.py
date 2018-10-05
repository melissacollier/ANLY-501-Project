# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 11:15:30 2018

@author: Lin
"""

import urllib
import urllib.request
import re
import requests
import pandas as pd
import json
from urllib.request import urlopen
import matplotlib.pyplot as plt

def main():
    ### URL for arsenic level values in 2016

    url='https://ephtracking.cdc.gov:443/apigateway/api/v1/getCoreHolder/441/2/ALL/ALL/2016/0/0'
    waterResp = urllib.request.urlopen(url)
    waterRawdata = json.loads(waterResp.read().decode())

#    #### output the waterquality jsontxt file, optional
#    waterRawfile = open('water.json', 'w', encoding= 'utf-8')
#    json.dump(waterRawdata,waterRawfile)
#    waterRawfile.close()
    
    #### read json into dataframe, "dict" format, cannot read dict directly
    waterDF=pd.DataFrame.from_dict(waterRawdata['pmTableResultWithCWS']) 
#   print (waterDF)
    waterDF['dataValue'] = pd.to_numeric(waterDF['dataValue'], errors='coerce')
    #### output into .csv file, optional
#    waterDF.to_csv('waterQuality.csv', sep='\t', encoding='utf-8')

    ### select cleaning data function
    waterResult = waterClean(waterDF)


### cleaning data function
def waterClean(data):
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
    bins = [0,1,10,50]
    labels=['Non Detect','Less than or equal MCL','More than MCL' ]
    result['Quality']=pd.cut(result['Value'],bins,labels=labels)
    return result
    
main()
