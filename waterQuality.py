# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 11:15:30 2018

@author: Lin
@dataset is very large, please wait for a few mins to load it.
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
    
#    #### output into .csv file, optional
    waterDF.to_csv('waterQuality.csv', sep='\t', encoding='utf-8')

    ### use cleaning data function
    waterResult = waterClean(waterDF)


### Data features
def waterClean(data):
    ### Checking datatypes before cleaning
    print (data.info())
    ### Datatype of dataValue is object, change it into numericals
    data['dataValue'] = pd.to_numeric(data['dataValue'], errors='coerce')
    ### Checking missing values/typos/outliers in datasets  
    with open ('waterCheck.txt','w') as wc:
#        wc.write("\nHave a general understanding of the dataset:\n")
#        wc.write(data.info().to_string())
        wc.write("Check if there is missing value for each column:\n")
        wc.write(pd.isna(data).sum().to_string())
        wc.write("\nOverall review of dataset:\n")
        wc.write(data.describe().transpose().to_string())
        wc.write("\nvalue_counts() function: check is there any error value in 'display' colomn\n")
        wc.write(data['display'].value_counts().to_string())
        wc.write("\nvalue_counts() function:check is there any error value in 'dataValue' colomn\n")
        wc.write(data['dataValue'].value_counts().to_string())
        wc.write("\nvalue_counts() function:check is there any error value in 'title' colomn \n")
        wc.write(data['title'].value_counts().to_string()) 
    ### Second method to check missing values/typos/outliers in datasets   
    displayOUT = data['display'].unique()
    dataValueOUT = data['dataValue'].unique()
    titleOUT = data['title'].unique()
    
    ### Cleaning data

    ### Datatype of dataValue is object, change it into numericals
    data['dataValue'] = pd.to_numeric(data['dataValue'], errors='coerce')
    ### 1. get the means of all values for each county using "groupby" method
    result = data.groupby(['title'])['dataValue'].mean()
    ### change "series" into "dataframe" datatype
    with open ('waterCheck.txt','a') as wc:
        wc.write("\nThe mean value of arsenic concerntration for each county\n")
        wc.write(result.to_string())
        
    ### change "series" into "dataframe" datatype    
    result = result.to_frame().reset_index()
    result.columns = ['Location','Value']
    
    ### 2. split the location column into two column("county","state"), expand=True to add these two column into dataframe
    result[['county','state']] =result['Location'].str.split(',', n=1, expand=True)
    ### remove the location column
    del result['Location']
    print (result.describe())
    ### the max value is 31.837500, which is lower than 50
    
    
    ### 3. binning the mean into three categories
    ### According to documents in its original website:
    ### level < 1 means non-dect arsenic
    ### level in (1-10) means less than MCL == "no harm"
    ### level in (10-50) means "harmful"
    bins = [-1,1,10,50]
    labels=['Non Detect','Less than or equal 10','More than 10' ]
    ### 4. remove non detect value of water quality 
    result = result[(result['Quality'] != 'Non Detect')]
    result['Quality']=pd.cut(result['Value'],bins,labels=labels)
    with open ('waterCheck.txt','a') as wc:
        wc.write("\nThe cleaned dataset and new dataset features\n")
        wc.write(result.to_string())
    
    return result
    
main()
