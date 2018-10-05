import pandas as pd


data2017 = pd.read_csv('https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2017.zip')
data2016 = pd.read_csv('https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2016.zip')
data2015 = pd.read_csv('https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2015.zip')
data2014 = pd.read_csv('https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2014.zip')
data2013 = pd.read_csv('https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2013.zip')
data2012 = pd.read_csv('https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2012.zip')
data2011 = pd.read_csv('https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2011.zip')
countyReference = pd.read_excel("https://www.schooldata.com/pdfs/US_FIPS_Codes.xls")

##fixing the header for CountyReference
new_header = countyReference.iloc[0]
countyReference = countyReference[1:]
countyReference.columns = new_header

##creating a single dataframe for air quality data and exporting to a csv file
allPollutionData = pd.concat([data2017, data2016, data2015, data2014, data2013, data2012, data2011])
allPollutionData.to_csv('All_Pollution_Data.csv')


##There is no null rows
nullCount = allPollutionData.isnull().values.ravel().sum()
print("\nThe total number of rows with null values is: \n")
print(nullCount)


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



