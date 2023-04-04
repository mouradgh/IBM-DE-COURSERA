# This code will help you get Data using an API call to exchangeratesapi.io

import requests
import pandas as pd

# Get the APILayer key
api_key = 'xxxxxx'

# Construct the url
url = 'https://api.apilayer.com/exchangerates_data/latest?base=EUR&apikey=' + api_key

# Call the ExchangeRate API
data = requests.get(url)
json_data = data.json()

# Load the  exchange rates into a pandas DataFrame
df = pd.DataFrame.from_dict(json_data)
df.index.name = 'Currency'
df=df.drop(['base', 'success', 'timestamp', 'date'], axis=1)
print(df)

df.to_csv('exchange_rate.csv')




