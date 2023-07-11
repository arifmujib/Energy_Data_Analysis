import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import credentials
import requests


url = "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/"

parameters = {
    'api_key':credentials.api_key
}

header = {'X-Params': '{"frequency":"hourly","data":["value"],"facets":{},"start":"2022-01-01T00","end":"2022-01-28T00","sort":[{"column":"period","direction":"desc"}],"offset":0,"length":5}'}


def EIA_API_request(url=url,frequency="hourly",data_value='["value"]',facets='{}',start="2022-01-01T00",end="2022-01-28T00",sort='[{"column":"period","direction":"desc"}]',offset=0,length=5):
    """This function gets the data from EIA API.
    INPUT: Different search Parameters from the EIA API dashboard
    Output: Dataframe with the result"""

    header = {'X-Params': '{"frequency":"%s","data":%s,"facets":%s,"start":"%s","end":"%s","sort":%s,"offset":%d,"length":%d}'%(
        frequency,data_value,facets,start,end,sort,offset,length)}

    #print(header)
    response = requests.get(url, params=parameters,headers=header)
    if response.status_code == 200:
        received = len(response.json()['response']['data'])
        print("Successfully retrieved %d data"%received)
    else:
        print(response.status_code)
        return response.status_code


    json = response.json()
    data = pd.json_normalize(json['response']['data'])
    entries = (data.shape[0]<length)*json['response']['total']
    
    for new_offset in range(offset+received,entries,5000):
        header = {'X-Params':
                  '{"frequency":"%s","data":%s,"facets":%s,"start":"%s","end":"%s","sort":%s,"offset":%d,"length":%d}'%(
        frequency,data_value,facets,start,end,sort,new_offset,length)}
        #print(header)
        response = requests.get(url, params=parameters,headers=header)
        json = response.json()
        new_data = pd.json_normalize(json['response']['data'])
        data = pd.concat([data,new_data], ignore_index=True)

    print("Out of %s, %d entries received"%(json['response']['total'], data.shape[0]))    
    return data