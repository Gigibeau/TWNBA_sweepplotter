
"""
Created on Wed Nov  6 14:49:22 2019

@author: bgruebel
"""

import numpy as np
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
from tkinter import simpledialog
from tkinter.filedialog import askdirectory

#Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilenames() # show an "Open" dialog box and return the path to the selected file
print(filename)

fileName = askdirectory()
#Eingabe = simpledialog.askstring(title="Speichern",prompt="Spice:                   ")



import os
file=filename[0]
base=os.path.splitext(file)[0]
head,tail=os.path.split(file)
head+=str('/Test.xlsx' )
base=head
print(head)
#base+=str('.xlsx')
print(base)

Dateinamen=[]
Streifenname=[]
Streifen=[]

Fingerbreite=[]
Rho_c=[]
Rho_c_F=[]
Sheet=[]
Sheet_F=[]
Rc=[]
Liste=[]
index=0
index2=0
startdaten=0
titel='Var'
vari=1

for k in range(0,len(filename)):
    f=open(filename[k], "r")
    ohneendung=os.path.splitext(filename[k])[0]
    index=0-index2
    file=ohneendung    
    file+=('.xlsx')
    
    
    if f.mode == 'r':
        contents=f.readlines()
        laengecontent=len(contents)
        x = contents[1].find("Run: ")
        y = len(contents[1])
        numberofsteps=int(contents[1][x+7:y-2])
        Datenset=int((laengecontent-1-numberofsteps)/numberofsteps)
        parameter=contents[0].count('\t')
        
        writer = pd.ExcelWriter(file, engine='xlsxwriter')
        
        for l in range(0,parameter):
            XDaten=[[0 for i in range(numberofsteps+1)] for j in range(Datenset+2)]
            XDaten[0][0]=contents[0].split()[0]
            for i in range(1,numberofsteps+1):    
                XDaten[0][i]=contents[0].split()[l+1]
                XDaten[1][i]=contents[(i-1)*Datenset+i]
                for j in range(2,Datenset+2):
                    XDaten[j][i]=float(contents[j+(i-1)*(Datenset+1)].split()[l+1])
                    XDaten[j][0]=float(contents[j+(i-1)*(Datenset+1)].split()[0])
            
            xdaten=np.array(XDaten)
            df = pd.DataFrame(xdaten)
            fehler1 = contents[0].find("/")
            #fehler2
            if fehler1>=0:
                XDaten[0][1]=XDaten[0][1].replace("/"," DIV ")
            
            df.to_excel(writer, sheet_name=XDaten[0][1],index=False)
        writer.save()


