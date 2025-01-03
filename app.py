#!/usr/bin/env python
# coding: utf-8

# In[37]:


import csv
from faker import Faker
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# ## Using Faker to Augment Data

# In[2]:


#Initialize Faker
fake=Faker()

# In[3]:


#Input and Output Files
input_file='Expense Data.csv' #Original file with 5 entries
output_file='augmented_expense.csv' #Output file with augmented data

# In[4]:


#Load existing data
with open(input_file, 'r') as file:
    reader=csv.reader(file)
    rows=list(reader)

# In[5]:


#Extract header and data rows
header=rows[0]
base_data=rows[1:]

# In[6]:


#Generate new data using faker
new_data=[]
for _ in range(1000):     #Generate 1000 new rows
    base_row=random.choice(base_data)    #Randomly pick an existing row as a abse   
    
    #Generate a fake data around the existing one
    original_date=datetime.strptime(base_row[0], '%Y-%m-%d')
    random_days=random.randint(-30,30)  #+/- 30 days
    new_date=original_date + timedelta(days=random_days)
    
    #Generate fake amount around the base amount
    base_amount=float(base_row[1])
    amount_variation=round(random.uniform(-10,10), 2) #Vary by +/- $10
    new_amount=max(1.0, base_amount + amount_variation)     #Ensure positive
    
    
    #Use the same category and payment method
    category=base_row[2]
    payment_method=base_row[3]
    
    #Generate a fake description
    new_description=fake.sentence(nb_words=5) if random.random() > 0.5 else base_row[4]
    
    #Add the new row to the dataset
    new_data.append([new_date.strftime('%Y-%m-%d'),f"{new_amount:.2f}",category,payment_method,new_description])

# In[7]:


#Write the augmented data to a new csv file
with open (output_file, 'w', newline="") as file:
    writer=csv.writer(file)
    writer.writerow(header)       #Write the header
    writer.writerows(new_data)    #Write the generated data

print(f"Augmented dataset created as '{output_file}'.")

# In[8]:


df=pd.read_csv("augmented_expense.csv")
df.head()

# ## Setup the Database

# In[10]:


#Connect SQLite 
connection = sqlite3.connect('expense.db')

#Create a cursor to execute sql commands
cursor = connection.cursor()

# In[16]:


#Define the table structure
cursor.execute('''
CREATE TABLE IF NOT EXISTS expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    payment_method TEXT NOT NULL,
    description TEXT
)
''')

#Commit changes and close the connection
connection.commit()
connection.close()

print('Database and table created successfully!')

# ## Load the CSV Data into Database

# In[17]:


#File paths
csv_file='augmented_expense.csv'
database_file='expense.db'

# In[18]:


#Connect to the sqlite database
connection=sqlite3.connect(database_file)
cursor=connection.cursor()

# In[20]:


#Open csv file and load data
with open (csv_file, 'r') as file:
    reader=csv.DictReader(file)      #Read CSV as dictionary
    for row in reader:                #Insert each row into the table
        cursor.execute('''
        INSERT INTO expense (date,amount,category,payment_method,description)
        VALUES (?,?,?,?,?)
        ''', (row['Data'], row['Amount'], row['Category'], row['Payment Method'], row['Description']))

#Commit changes and close the connection
connection.commit()
connection.close()

print('Data loaded into the database successfully!')    

# ## Test Database

# In[24]:


#Connect to the database
connection=sqlite3.connect('expense.db')
cursor=connection.cursor()

#Query the first 5 rows
cursor.execute('SELECT * FROM expense LIMIT 5')
rows=cursor.fetchall()

#Print the results
for row in rows:
    print(row)
    
#Close the connection
#connection.close()

# # Perform SQL Queries on Database

# ## Basic Queries
#   ### 1. View All Data

# In[25]:


cursor.execute("SELECT * FROM expense")
rows=cursor.fetchall()

for row in rows:
    print(row)

# ### 2. Filter by Category

# In[26]:


category='Groceries'
cursor.execute("SELECT * FROM expense WHERE category=?",(category,))
rows=cursor.fetchall()

for row in rows:
    print(row)

# ### 3. Sum of Expenses by Category

# In[27]:


cursor.execute("SELECT category, SUM(amount) AS total FROM expense GROUP BY category")
rows=cursor.fetchall()

for row in rows:
    print(row)

# ## Advanced Queries
#   ### 4. Find Top Spending Categories

# In[28]:


cursor.execute("SELECT category, SUM(amount) AS total FROM expense GROUP BY category ORDER BY total DESC LIMIT 5")
rows=cursor.fetchall()

for row in rows:
    print(row)

# ### 5. Monthly Expense Breakdown

# In[31]:


cursor.execute("""
SELECT strftime ('%Y-%m', date) AS month, SUM(amount) AS total
FROM expense
GROUP BY month
ORDER BY month
""")
rows=cursor.fetchall()

for row in rows:
    print(row)

# # Analyze Data with Python

# In[33]:


#Query data into pandas dataframe
df=pd.read_sql_query("SELECT * FROM expense", connection)

#Close the connection
connection.close()

#Display first 5 rows
df.head()

# ## Perform Analysis
# ### 1. Total Expenses by Category

# In[35]:


category_totals=df.groupby('category')['amount'].sum()
print(category_totals)

# ### 2. Monthy Trends

# In[36]:


df['month']=pd.to_datetime(df['date']).dt.to_period('M')
monthly_totals=df.groupby('month')['amount'].sum()
print(monthly_totals)

# # Visualize the Data

# ### 1. Bar Chart of Total Expenses by Category

# In[39]:


category_totals.plot(kind='bar', title='Total Expenses by Category', ylabel='Amount')
plt.show()

# ### 2. Line Chart for Monthy Trends

# In[40]:


monthly_totals.plot(kind='line', title='Monthly Expense Trend', ylabel='Amount', xlabel='Month')
plt.xticks(rotation=45)
plt.show()

# ### 3. Pie Chart of Category Distribution

# In[44]:


category_totals.plot(kind='pie', title='Expense Distribution by Category', autopct='%1.1f%%')
plt.ylabel('')    #Hides the default y-axis label
plt.show()

# In[ ]:



