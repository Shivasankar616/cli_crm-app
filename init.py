import pandas as pd
import numpy as np

df2=pd.read_csv('C:\crm panel\lead_generator.csv')
print('Data loaded successfully')
print('shape:',df2.shape)
print('preprocessing..........')
df2['status'] = 0
df2['result'] = 'unhandled'
print('.........')
df2.to_csv('data.csv',index=False)
print('Data_csv created successfully')