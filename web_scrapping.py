# This code will help you scrap web pages using the BeautifulSoup library

from bs4 import BeautifulSoup
import requests
import pandas as pd
from tabulate import tabulate

# This wikipedia webpage provides information about the largest banks in the world by various parameters
url = 'https://web.archive.org/web/20200318083015/https://en.wikipedia.org/wiki/List_of_largest_banks'

# We scrape the Web Page using requests
html_data = requests.get(url).text

# Using beautifulsoup load the data from the By market capitalization table into a pandas dataframe
soup = BeautifulSoup(html_data, 'html.parser')
data = pd.DataFrame(columns=["Name", "Market Cap (US$ Billion)"])

for row in soup.find_all('tbody')[2].find_all('tr'):
    col = row.find_all("td")
    # print(col)
    # Make sure there is no empty tr
    if len(col) == 3:
        Bank_Name = col[1].text.strip()
        Market_Cap = col[2].text.strip()
        # Append the data of each row to the table
        data = data.append({"Name": Bank_Name, "Market Cap (US$ Billion)": Market_Cap}, ignore_index=True)

print(tabulate(data, headers='keys'))
# print(data.describe())

# Save the results to a Json file
data.to_json('bank_market_cap.json', orient='records', indent=5)
