#!/usr/bin/env python3
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

def main():
    ### URL for arsenic level values in 2016
    url = "https://ephtracking.cdc.gov/apigateway/api/v1/getCoreHolder/441/102/ALL/ALL/2016/0/0?PMDisplayId=1,2,3"
    waterResp = urllib.request.urlopen(url)
    waterRawdata = json.loads(waterResp.read().decode())

#    #### output the waterquality jsontxt file, optional
    waterRawfile = open('water.json', 'w', encoding= 'utf-8')
    json.dump(waterRawdata,waterRawfile)
    waterRawfile.close()
    
    #### read json into dataframe, "dict" format, cannot read dict directly
    waterDF=pd.DataFrame.from_dict(waterRawdata['pmTableResultWithCWS']) 
    print (waterDF)
    
    #### output into .csv file
    waterDF.to_csv('waterQuality.csv', sep='\t', encoding='utf-8')
