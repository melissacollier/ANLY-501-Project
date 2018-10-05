#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 09:22:21 2018


"""

import pandas as pd
import json
import urllib

url = "https://ephtracking.cdc.gov:443/apigateway/api/v1/getCoreHolder/441/102/ALL/ALL/2016/0/0?PMDisplayId=1,2"

# Reading the json as a dict
with urllib.request.urlopen(url) as json_data:
    data = json.load(json_data)

# load from_dict
data = pd.DataFrame.from_dict(data['pmTableResultWithCWS'])   
