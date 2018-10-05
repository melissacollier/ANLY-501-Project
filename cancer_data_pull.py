# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 23:51:55 2018

@author: Arshia
"""

import pandas as pd
import io
import requests

url = 'https://www.statecancerprofiles.cancer.gov/incidencerates/index.php?stateFIPS=99&cancer=001&race=00&sex=0&age=001&type=incd&sortVariableName=rate&sortOrder=desc&output=1'
s = requests.get(url).content
ds = pd.read_csv(io.StringIO(s.decode('windows-1252')), skiprows=8, skipfooter=27, engine='python')
print(ds.describe())

#split county, state, SEER, NPCR into separate columns
ds['County'], ds['State'] = ds['County'].str.split(', ', 1).str
ds['State'], ds['SEER'] = ds['State'].str.split('(', 1).str
ds['SEER'], ds['NPCR'] = ds['SEER'].str.split(',', 1).str
ds['NPCR'] = ds['NPCR'].str.replace(")","")
