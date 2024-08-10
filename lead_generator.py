import numpy as np
import pandas as pd
np.random.seed(42)
numbers = []
for i in range(50):
    j=np.random.choice([0,1,2,3,4,5,6,7,8,9],10)
    numbers.append(j)
    phonenumbers=[''.join(np.random.choice(list('0123456789'), 10)) for _ in range(50)]
print(phonenumbers)
alphas=list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
names=[''.join(np.random.choice(alphas,10))for _ in range(50)]
print(names)
df=pd.DataFrame({
    'names':names,
    'phonenumbers':phonenumbers
})
print(df)
df.to_csv('support_leads.csv',index=False)