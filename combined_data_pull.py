# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 11:15:30 2018

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
    
# function to write size/shape results to a .txt
def dataInfo(dataset):
    file1 = open('basic dataframe info.txt','a')
    file1.write('Size of the dataframe is ' + str(dataset.shape) +'.\n\n')
    file1.write('There are ' + str(dataset.size) + ' elements in this dataset.\n\n')
    file1.write('Data types of each columns are\n ' + str(dataset.dtypes) +'\n\n')
    file1.close()

##count of null rows
def nullCount(dataset):
    file1 = open('basic dataframe info.txt','a')
    nulls = dataset.isnull().values.ravel().sum()
    file1.write('\nThe total number of rows with null values is: \n' + str(nulls) +'.\n\n')
    file1.close()

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

    ### Air quality Data
    data2017 = pd.read_csv('https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2017.zip')
    data2016 = pd.read_csv('https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2016.zip')
    data2015 = pd.read_csv('https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2015.zip')
    data2014 = pd.read_csv('https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2014.zip')
    data2013 = pd.read_csv('https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2013.zip')
    data2012 = pd.read_csv('https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2012.zip')
    data2011 = pd.read_csv('https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2011.zip')
    countyReference = pd.read_excel("https://www.schooldata.com/pdfs/US_FIPS_Codes.xls")


#######
### Air Quality Cleaning
#######
    
##fixing the header for CountyReference
new_header = countyReference.iloc[0]
countyReference = countyReference[1:]
countyReference.columns = new_header

##creating a single dataframe for air quality data and exporting to a csv file
allPollutionData = pd.concat([data2017, data2016, data2015, data2014, data2013, data2012, data2011])
allPollutionData.to_csv('All_Pollution_Data.csv')


dataOnlyStateCounty = allPollutionData.loc[:,['State','County']]
referenceStateCounty = countyReference.loc[:,['State','County']]
##groupby('State') is grouping the dataframe by the unique values in the State column.
##The values in Country column are mapped to each unique value from State column.
##Tthen index for County column and turn the values that are mapped to the State column into 
##each distinct list groupings.
##Then turn each unique grouping to a dict
a = dataOnlyStateCounty.groupby('State')['County'].apply(list).to_dict()
b = referenceStateCounty.groupby('State')['County'].apply(list).to_dict()


columns = ['Year','Days with AQI','Good Days','Moderate Days','Max AQI','90th Percentile AQI',
           'Median AQI','Days CO','Days NO2','Days Ozone',
           'Days SO2','Days PM2.5','Days PM10']


##break statement is used to exit out of the nearest for loop
##The purpose of this loop is to determine invalid States and Counties
##The output has repitition because there are multiple state,county entries within some keys.
##These aren't duplicates because the same state,county is used across different years.
def stateCountyChecker(a,b):
    countCounty = 0
    countState = 0
    
    for key in a:
          for value in a[key]:
                try:
                      if value not in b[key]:
                            print("The following state|county is a messy data entry: ", key,'|', value)
                            countCounty += 1
                except KeyError:
                      print(key,"is not a valid State or the entry is messy")
                      countState += 1
                      break
                  
    print('The number of messy States is',countState)
    print('The number of messy Counties is',countCounty)


##Leap years have 366 days.  2012 and 2016 are leap years
##The purpose of this loop is to run through each column and determine the extent of messy data
def numericColumnChecker(allPollutionData,columns):
    for i in columns:
          c = allPollutionData[i].value_counts().sort_index()
          if i == 'Year':
                print("Expecting years to be between 2011 and 2017")
                indexLength = len(c)-1
                
                if c.index[0] < 2011 or c.index[indexLength] > 2017:
                      print("There are invalid entries in years column")
                      invalidEntries = c[(c.index < 2011) | (c.index > 2017)].sum()
                      print("The number of invalid entries is", invalidEntries)
                else:
                      print("No invalid entries for",i)
                      
          elif (i == 'Days with AQI' or i == 'Good Days' or i == 'Moderate Days' or i == 'Days CO'
                or i == 'Days NO2' or i == 'Days Ozone' or i == 'Days SO2' or i == 'Days PM2.5'
                or i == 'Days PM10'):
                print("Expecting entries for",i,"column to between 0 and 366")
                indexLength = len(c)-1
                
                if c.index[0] < 0 or c.index[indexLength] > 366:
                      print("There are invalid intries in",i)
                      invalidEntries = c[(c.index < 0) | (c.index > 366)].sum()
                      print("The number of invalid entries is", invalidEntries)
                else:
                      print("No invalid entries for",i)
                      
          elif (i == 'Max AQI' or i == '90th Percentile AQI' or i == 'Median AQI'):
                print("Expecting entries for",i,"column to be greater than 0")
    
                if c.index[0] < 0:
                      print("There are invalid intries in",i)
                      invalidEntries = c[c.index < 0].sum()
                      print("The number of invalid entries is", invalidEntries)
                else:
                      print("No invalid entries for",i)



##creating a bin for the Days PM2.5 variable.
##0 is when there is zero days with PM2.5 and 1 is when there are days with PM2.5
def hasPM25(airPollutionData):
    binLabels = [0,1]
    binRange = [0,1,367]
    allPollutionData['hasPM2.5'] = pd.cut(allPollutionData['Days PM2.5'],bins = binRange, 
                    right = False, labels = binLabels)
    return airPollutionData


#######
### Water Data features
#######
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
    bins = [0,1,10,50]
    labels=['Non Detect','Less than or equal MCL','More than MCL' ]
    ### 4. remove non detect value of water quality 
    result = result[(result['Quality'] != 'Non Detect')]
    result['Quality']=pd.cut(result['Value'],bins,labels=labels)
    with open ('waterCheck.txt','a') as wc:
        wc.write("\nThe cleaned dataset and new dataset features\n")
        wc.write(result.to_string())
    
    return result


main()
