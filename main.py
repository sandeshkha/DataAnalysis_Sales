import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter

#combining multiple csv files into one file
os.chdir('/Sales_Data')

extension = 'csv'
all_filenames = [i for i in glob.glob(('*.{}'.format(extension)))]

combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])

combined_csv.to_csv("totalsales_csv.csv", index=False, encoding='utf-8-sig')


# read the updated dataframe
all_data = pd.read_csv('totalsales_csv.csv')

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

# Plot City Sales Data
cities = [city for city, df in all_data.groupby('City')]
City = all_data['City'].unique()
plt.bar(cities, results['Sales'])
plt.xticks('cities', rotation ='vertical', size = 8)
plt.ylabel('US Cities')
plt.xlabel('Sales in USD')
plt.show()

#Time to display advertisments

#Covert Order date to datetime function
all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])

all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute'] = all_data['Order Date'].dt.minute

#Graph the sales by the time
hours = [hour for hour, df in all_data.groupby('Hour')]

plt.plot(hours, all_data.groupby(['Hours']).count())
plt.xticks(hours)
plt.grid()
plt.xlabel('Hour')
plt.ylabel('Number of orders')

#Create a new dataframe to group all ordered items together
df = all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df = df[['Order ID', 'Grouped']].drop_duplicates()

count = Counter()

# The two most grouped product in sale
for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))

for key, value in count.most_common(10):
    print(key,value)

#
product_data = all_data.groupby['Product']
quantity_ordered = product_data.sum()['Quantity Ordered']

products = [product for product, df in product_data]

#Graph Products and the quantity ordered
plt.bar(products, quantity_ordered)
plt.xticks(products, rotation ='vertical', size = 8)
plt.ylabel('Quantity Ordered')
plt.xlabel('Product')
plt.show()

#Comparing two graphs with quantiy and price of the products
prices = all_data.groupby('Product').mean()['Price Each']

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered, 'g-')
ax2.bar(products, prices, 'b-')

ax1.set_xlabel("Product Name")
ax1.set_xlabel("Quantity Ordered", color='g')
ax2.set_ylabel("Price ($)", color='b')
ax1.set_xticklabels(products, rotaion='vertical', size=8)
