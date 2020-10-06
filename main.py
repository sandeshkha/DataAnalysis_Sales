import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

#combining multiple csv files into one file
os.chdir('/Sales_Data')

extension = 'csv'
all_filenames = [i for i in glob.glob(('*.{}'.format(extension)))]

combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])

combined_csv.to_csv("totalsales_csv.csv", index=False, encoding='utf-8-sig')


# read the updated dataframe
all_data = pd.read_csv('totalsales_csv.csv')

#Clean up data
nan_df = all_data[all_data.isna().any(axis=1)]

all_data = all_data.dropna(how='all')

all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']

#Augment data with additional columns
##Month column added
all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')

#Add column total sales Quantity * Price Each
all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])

all_data['Total Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']

results = all_data.groupby('Month').sum()

#What city had the most sales
def get_city(address):
    return address.split(',')[1]

all_data['City'] = all_data['Purchase Address'].apply(lambda x: get_city(x))

print(all_data.sort_values('Order ID'))

#print(all_data.head())