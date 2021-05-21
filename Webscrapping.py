# -*- coding: utf-8 -*-
"""
Created on Friday 16-08-2020 20:29:03

@author: Nishanth T (Junior Software Developer)

"""

import os
import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import timedelta # A timedelta object represents a duration, the difference between two dates or times.
import pandas as pd
import json
####################### Create a folder ############################

now = datetime.datetime.now()
yesterday = now - timedelta(days = 1)
date_time = yesterday.strftime("%d-%b-%Y")
print(date_time)
#try:
date_time=input('Please enter the Date in dd-Mon-yyyy Format: ')
#datetime.datetime.strptime(date_time,'%d-%b-%Y')

filepath=r'D:/Users/Save_files/'+date_time
if not os.path.exists(filepath):
    os.makedirs(filepath)
    
####################### To get Logs details  ############################

Main_Page='Add Your website name' # The website which i have used is a copyrighted Website so i cannot mention the website name. 
html_page = urlopen(Main_Page)
#print(Content.read())
soup = BeautifulSoup(html_page, "lxml")
link_1 = soup.findAll('a', href=True, text=True)[10] # Extract the Logs link. 
#print(link)
link=link_1['href']

Logs_page = urlopen(Main_Page+link)
#print(Logs_page.read())
soup1 = BeautifulSoup(Logs_page, "lxml")

Log_info=urlopen(Main_Page+link+date_time)
#print(Log_info.read())
soup2 = BeautifulSoup(Log_info, "lxml")
for j in soup2.find_all('a', href=True, text=True)[5::]: # "a" is a anchor tag Hypertext ref [href] is the attribute of anchor tag. 
    get_link=j['href']
    print(get_link)   
    Logdata=urlopen(Main_Page+link+date_time+'/'+get_link)
    S=Logdata.read().decode("utf-8").split('\n')
    list1=[]
    for x in S:
        list1.append(x.split('\t'))
    if list1[1]==[""]:
        del list1[1]   

    try:
        for f in range(1,len(list1)):
            if list1[f][6]==' NaN':
                print('Input parsing Failed','for the ID',list1[f][1])
            if list1[f][9]==' NaN':         
                print('Server status Failed','for the ID',list1[f][1])
            if list1[f][9]==' 0': 
                print('Server status Failed','for the ID',list1[f][1])
            if list1[f][8]==' NaN ':
                print('Json status Failed','for the ID',list1[f][1])
            if list1[f][8]==' 0 ':    
                print('Json status Failed','for the ID',list1[f][1])
    except Exception as e:
        print('Error in displayig Logs',e)       
            
    df=pd.DataFrame(list1[1::],columns=['IT','ID','TIME','ECG API TIME','TOTAL TIME','CPU','ECG API EC','FINAL EC','JSON STATUS','SERVER STATUS'])               
    try:
        df.to_csv(filepath+'/'+'Logs_'+date_time+'_'+get_link+'.csv',index=False,header=True)
        print('Created csv sheet of Logs')
    except Exception as e:
        print(e)

####################### To Get Error Records details ############################

error_name = soup.findAll('a')[8].get_text()
try:
    error_records=urlopen(Main_Page+error_name+date_time+'/')
    soup_error = BeautifulSoup(error_records, "lxml")
    for k in soup_error.find_all('a', href=True, text=True)[5::]:
        link_error=k['href']
        S=link_error.split('.')
        if S[1]=='txt':
            print(link_error)
            errordata=urlopen(Main_Page+error_name+date_time+'/'+link_error)
            ER_data=errordata.read().decode("utf-8").split('\n')
            list2=[]
            for i in ER_data:
                list2.append(i.split('\t'))
            if list2[1]==[""]:
                del list2[1] 
            
            #with open(filepath+'/'+S[0]+'.txt','a') as f:
             #   f.write(str(list2[1::]))
            print('The error count is:',len(list2)-1)
            df1=pd.DataFrame(list2)            
            df1.to_csv(filepath+'/'+'ErrorRecords'+'_'+date_time+'_'+S[0]+'.csv',index=False,header=False)
            print('Error_Report as been generated') 
            try:
                for f in range(1,len(list2)):
                    w=list2[f][2].split('/') 
                    print('The Error Record',list2[f][1],w[0])
            except Exception as e:
                print("Error in displaying the failure error records :",date_time+" "+str(e))   
                                                    
except Exception as e:
    print("Error records are not found on this date :",date_time+" "+str(e))                

####################### To get "Output" Record Details ############################
                
Output_name = soup.findAll('a')[11].get_text()
Output_records=urlopen(Main_Page+Output_name+date_time+'/')
soup_output = BeautifulSoup(Output_records, "lxml")
B=[]
for i in soup_output.find_all('a', href=True, text=True)[5::]:
    link_text=i['href']
    Output_Records=urlopen(Main_Page+Output_name+date_time+'/'+link_text)
    #print(Output_Records.read().decode('utf-8'))
    records=Output_Records.read().decode('utf-8')

# using json.loads() convert dictionary string to dictionary 
    d=link_text.split('-')
    data = json.loads(records)
    
    Record_name=link_text.split('.')

    DiagnosisInfo=data['Record']['Interpretation']
    #print(DiagnosisInfo)

    VTR=data['Record']['VTR']
    ATR=data['Record']['ATR']
    PR=data['Record']['PR']
    RR=data['Record']['RR']
    PD=data['Record']['PD']
    QRSD=data['Record']['QRSD']
    QT=data['Record']['QT']
    QTc=data['Record']['QTc']
    QRSaxis=data['Record']['QRSaxis_final']
    Paxis=data['Record']['Paxis_final']
    Taxis=data['Record']['Taxis_final']

    SQ=data['Record']['SQ']
    error_code=data['ErrorCode']
    server_Push_Status=data['serverPushStatus']
    A={'Record Name':Record_name[0],'VTR':VTR,'ATR':ATR,'PR':PR,'QRSD':QRSD,'QT':QT,'QTc':QTc,'RR':RR,'PD':PD,'QRSaxis':QRSaxis,'Paxis':Paxis,'Taxis':Taxis,'Interpretation':DiagnosisInfo,'SQ':SQ,'ErrorCode':error_code,'ServerStatus':server_Push_Status}
    B.append(A)
    
df2=pd.DataFrame(B)
try:   
    df2.to_csv(filepath+'/'+'Record_Output'+'_'+date_time+'_'+'.csv',index=False,header=True)
    print('Details of all the Records are saved successfully')
except Exception as e:
    print(e)
        
#except Exception as e:
 #   print('Incorrect Date format',e)       





