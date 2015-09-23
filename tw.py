#!/usr/bin/env python

import pandas
# From SF/Dataloader export a CSV in this format:
# "Account ID","First Name","Last Name","Consumer Email","Alternate Email","Alternate EMail 2","Alternate EMail 3","Personal Email","Corporate Email","Preferred Email"
contacts = pandas.read_csv('contacts.csv', usecols=['Account ID', 'Consumer Email'])
contacts = contacts.drop_duplicates(subset='Consumer Email')
contacts.rename(columns={'Consumer Email': 'Email'}, inplace=True)
contacts['Email'] = contacts['Email'].str.lower()
# the tw.csv comes from MailChimp in this format:
# "Email Address","First Name","Last Name",user__pk,"subscription starts","subscription ends","Texas Weekly",EMAIL_TYPE,MEMBER_RATING,OPTIN_TIME,OPTIN_IP,CONFIRM_TIME,CONFIRM_IP,LATITUDE,LONGITUDE,GMTOFF,DSTOFF,TIMEZONE,CC,REGION,LAST_CHANGED,LEID,EUID,NOTES

tw = pandas.read_csv('tw.csv', usecols=['Email Address', 'First Name', 'Last Name', 'EUID'])
tw.rename(columns={'Email Address': 'Email', 'EUID': 'Legacy ID'}, inplace=True)
tw['Email'] = tw['Email'].str.lower()

result = pandas.merge(tw, contacts, on='Email', how='left')
result = result[['Account ID', 'Legacy ID']]
result['Primary Campaign Source'] = '70116000000wQkZ'
result['Description'] = 'imported from Tinypass'
result['Amount'] = '0.00'
result['Stage'] = 'Closed Won'
result['Name'] = 'TW Subscription'
result['Record Type'] = '01216000001IhQNAA0'
result['Close Date'] = '06/04/2015'
# handle missing separately
#missing = result[result['Account ID'].isnull()]
#missing.to_csv('missing.csv', index=False)
result.to_csv('result.csv', index=False)

#import ipdb; ipdb.set_trace()
