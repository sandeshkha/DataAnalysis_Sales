import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

#combining multiple csv files into one file
# os.chdir('/Sales_Data')
#
# extension = 'csv'
# all_filenames = [i for i in glob.glob(('*.{}'.format(extension)))]
#
# combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
#
# combined_csv.to_csv("totalsales_csv.csv", index=False, encoding='utf-8-sig')


# read the updated dataframe
all_data = pd.read_csv('/Users/sandeshkhanal/Documents/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/totalsales_csv.csv')

#Clean up data
#find data with NaN
nan_df = all_data[all_data.isna().any(axis=1)]

#Drop all NaN from data
all_data = all_data.dropna(how='all')

#Get the month and put it in a new column
all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']

#Augment data with additional columns
##Month column added
all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')

#Add column total sales Quantity * Price Each
all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])

all_data['Total Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']

#What month had the higest sales
results = all_data.groupby('Month').sum()

#What city had the most sales
def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(' ')[1]

# Get city and state in a seprate coulumn
all_data['City'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")

results = all_data.groupby('City').sum()
print(results)
