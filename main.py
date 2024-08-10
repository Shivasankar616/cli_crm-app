import pandas as pd
import numpy as np
import sqlite3
import uuid
import plotly.express as px 
from datetime import datetime, timedelta

conn = sqlite3.connect('crm.db')
cursor = conn.cursor()
print('==============================================================================')
print('Database connected successfully')

def login():
    while True:
        print('Enter your name:')
        name = input()
        user = cursor.execute('SELECT * FROM bda WHERE name = \'{}\''.format(name)).fetchone()
        if user == None:
            print()
            print('Wrong name, try again')
            print()  
        else:
            print()
            print('user found........')
            print('Welcome',name,'to the CRM panel')
            break
    return None if user == None else user[0]
    
def getData(bda_id):
    return cursor.execute('SELECT * FROM sales WHERE bda_id = \'{}\';'.format(bda_id)).fetchall()
    
def divideleads(data):  
    handled_leads = []
    unhandled_leads = []
    for i in data:
        if i[5]=='0':
            unhandled_leads.append(i)
        else:
            handled_leads.append(i)
    return handled_leads,unhandled_leads                   

def analyze(bda_id):
    data = getData(bda_id)
    df = pd.DataFrame([i[4] for i in data] ,columns=['sales'])
    values = df['sales'].value_counts().to_list()
    names = df['sales'].value_counts().index
    colors = ['gold','mediumturquoise','darkorange','lightgreen','red']
    fig = px.pie(df,values=values,names=names,title='lead Results')
    fig.update_traces(
    textposition='inside', textinfo='percent+label', marker=dict(colors=colors,line=dict(color='#000000', width=1))
 )
    fig.write_html('lead_results.html', auto_open = True)
    print('Analysis is done, opening the results in browser')
def checkout(bda_id):
    today = datetime.now().strftime('%Y-%M-%d')
    results = cursor.execute('SELECT lead_result FROM sales WHERE bda_id=\'{}\' AND lead_status = 1'.format(bda_id)).fetchall()
    rate = 2000
    total_leads = cursor.execute('SELECT COUNT(*) FROM sales WHERE bda_id=\'{}\''.format(bda_id)).fetchone()
    handled = cursor.execute('SELECT COUNT(*) FROM sales WHERE bda_id=\'{}\' AND lead_status = 1'.format(bda_id)).fetchone()
    unhandled= cursor.execute('SELECT COUNT(*) FROM sales WHERE bda_id=\'{}\' AND lead_status = 0'.format(bda_id)).fetchone()
    print('Total leads :', total_leads[0])
    print('Handled leads:',handled[0])
    print('unhandled leads:',unhandled[0])
    print('Rate per conversion:', rate)
    counter = 0 
    for i in results:
        if i[0] == 'interested':
          counter += 1
    print('Total interesetd leads:', counter)      
    payout = counter * rate
    print('----------------------------------------------------------------------------------------------------------')
    print('Payouts:',payout)
    print('----------------------------------------------------------------------------------------------------------')
    cursor.execute('INSERT into bda_payouts VALUES( ?, ?, ?, ?, ?)',(str(uuid.uuid4()), bda_id, today,'Salary paid',payout))
    conn.commit()
    print('Payout done successfully')
    
bda_id = login()

while True:
    data = getData(bda_id)
    results = divideleads(data)
    print('--------------------------------------------------')
    print('Remaining Leads:{}'.format(len(results[1])))
    print('Handled leads:{}'.format(len(results[0])))
    print()
    print('---------------------------------------------------')
    print()
    print('1.Handle next lead')
    print('2.show remaining leads')
    print('3.show handled leads')
    print('4.Analyze')
    print('5.Checkout')
    print('0.Exit')
    print()
    ch = int(input('Enter your choice: '))
    print()
    if ch == 0:
        print('Thank you')
        break
    elif ch == 1:
        current_lead = cursor.execute('SELECT * FROM sales WHERE bda_id=\'{}\' AND lead_status= 0;'.format(bda_id)).fetchone()
        if current_lead == None:
            print('No more leads to handled! Congratulations')
            break
        print()
        print('Name:{} | Phone number: {}'.format(current_lead[1],current_lead[2]))
        print()
        print('Make the call and enter the result from the options')
        print()
        print('1.Interested')
        print('2.not interested')
        print('3.call back later')
        print('4.DNP (Did not pick)')
        print('5.Junk lead/wrong number')
        res = int(input('Enter the result:'))
        match(res):
            case 1:
                print('Lead is interested')
                answer = 'interested'
            case 2:
                print('Lead is not answered')
                answer = 'Not interested'
            case 3:
                print('Lead asked to call back later')
                answer = 'call back later'
            case 4:
                print('Lead did not pick the call')
                answer = 'DNP (Did not pick)'
            case 5:
                print('lead is junk/wrong number')
                answer = 'Junk lead/wrong number'
            case _:        
                print('Invalid option')
                answer = 'N/A'
        cursor.execute('UPDATE sales SET lead_status = 1, lead_result = \'{}\' WHERE id = \'{}\';'.format(answer,current_lead[0])) 
        conn.commit()
        print() 
        print('lead_updated')   
    elif ch == 2:
        print('-------------------------------------------------------------------------------------------------------')
        print('----------------  Remaining leads ------------------       ')
        print(' names  | phonenumbers')
        for i in results[1]:
            print(' {} | {}'.format(i[2],i[3]))
        print('--------------------------------------------------------------------------------')    
    elif ch == 3:
        print('-------------------------------------------------------------------------------------------------------')
        print('----------------  Handled leads ------------------       ')
        print(' names  | phonenumbers')
        for i in results[0]:
            print(' {} | {}'.format(i[2],i[3]))
        print('--------------------------------------------------------------------------------')  
    elif ch == 4:
        analyze(bda_id)
    elif ch == 5:
        checkout(bda_id)
        break
    else:
        print('Wrong option try again')   