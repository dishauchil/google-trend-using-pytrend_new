pip install pytrends
import pandas as pd
import numpy as np
import pytrends
from pytrends.request import TrendReq
pytrend = TrendReq()
import time
import sys
print('Python: '+sys.version)
print('Pandas: '+pd.__version__)

#returning the time in seconds since the point where the time starts
startTime = time.time()

#hl=language and tz=Timezone Offset (in minutes)
pytrend = TrendReq(hl='en-US', tz=360, retries=10, backoff_factor=0.5)

#read keyword csv
df = pd.read_csv(r'D:\*******\keyword_list.csv')
df

#change the dataframe values to list
df2 = df["keywords"].values.tolist()
df2

KEYWORDS_CODES=[pytrend.suggestions(keyword=i) [0] for i in df2]
df_CODES= pd.DataFrame(KEYWORDS_CODES)
df_CODES
df_CODES.to_csv('MIDS.csv')
EXACT_KEYWORDS=df_CODES['mid'].to_list()
Individual_EXACT_KEYWORD = list(zip(*[iter(EXACT_KEYWORDS)]*1))
Individual_EXACT_KEYWORD = [list(x) for x in Individual_EXACT_KEYWORD]
data = {}
i = 1
for keywords in Individual_EXACT_KEYWORD:
    pytrend.build_payload(kw_list=keywords, #kw_list = Keywords to get data for
                          cat=0, #cat=Category to narrow results
                          timeframe = '2020-01-01 2020-12-31', #Start and end dates
                          geo = "US", #geo=geographical area
                          gprop='') #Default grouping
    data[i] = pytrend.interest_over_time()
    i+=1
df_trends = pd.concat(data, axis=1)

#collecting execution time
executionTime = (time.time() - startTime)
print('Execution time in sec.: ' + str(executionTime))

df_trends.columns = df_trends.columns.droplevel(0) #drop outside header
df_trends = df_trends.drop('isPartial', axis = 'columns') #drop "isPartial"
df_trends

df_trends.to_csv('Final Report.csv')

