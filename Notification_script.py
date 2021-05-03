# -*- coding: utf-8 -*-
"""
Created on Friday 16-08-2020 20:29:03

@author: Nishanth T (Junior Python Developer)

"""

import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import timedelta # A timedelta object represents a duration, the difference between two dates or times.
import pandas as pd
import tkinter as tk
from tkinter import messagebox as mb

####################### Create a folder ############################
root = tk.Tk()
root.withdraw()

now = datetime.datetime.now()
date_time = now.strftime("%d-%b-%Y")
print(date_time)

####################### Scrap the website details  ############################

Main_Page='Add Your website name' #Add Your website name It is a copyrighted Website so i cannot mention the website name. 
html_page = urlopen(Main_Page)
soup = BeautifulSoup(html_page, "lxml")

error_name = soup.findAll('a')[7].get_text()
try:
    error_records=urlopen(Main_Page+error_name+date_time+'/')
    soup_error = BeautifulSoup(error_records, "lxml")
    for k in soup_error.find_all('a', href=True, text=True)[5::]:
        link_error=k['href']
        S=link_error.split('.')
        if S[1]=='txt':
            #print(link_error)
            errordata=urlopen(Main_Page+error_name+date_time+'/'+link_error)
            ER_data=errordata.read().decode("utf-8").split('\n')
            list2=[]
            for i in ER_data:
                list2.append(i.split('\t'))
            if list2[1]==[""]:
                del list2[1] 
                    
            df1=pd.DataFrame(list2)      
            #mb.showinfo("Error Report",'Error_Report as been generated',parent=root) 
            B=[]
            try:
                for f in range(1,len(list2)):
                    w=list2[f][2].split('/') 
                    B.append(list2[f][1]+w[0])
                
                mb.showinfo(title='Error Report',message=str(B),parent=root)
            except Exception as e:
                mb.showinfo("Error Report","Error in displaying the failure error records " +" " +date_time+" "+str(e),parent=root)   
                                                    
except Exception as e:
    mb.showinfo("Error Report","Error records are not found on this date "+ " "+date_time+" "+str(e),parent=root)                

root.destroy()
root.mainloop()





