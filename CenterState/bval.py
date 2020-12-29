


import pandas as pd 
import csv 


field_list = [] 

with open('C:\\Users\\Cameron\\Documents\Python\CenterState\\bval.txt', "r") as f:
    copy = False
    for line in f:
        if line.strip() == 'START-OF-FIELDS':
            copy = True
            continue 
        if line.strip() == 'END-OF-FIELDS':
            copy = False 
            continue 
        elif copy == True:
            field_list.append(line)



rows_list = [] 

with open('C:\\Users\\Cameron\\Documents\Python\CenterState\\bval.txt', "r") as f:
    copy = False
    for line in f:
        if line.strip() == 'START-OF-DATA':
            copy = True
            continue 
        if line.strip() == 'END-OF-DATA':
            copy = False 
            continue 
        elif copy == True:
            rows_list.append(line)


df = pd.DataFrame(rows_list)

df = df[0].str.split('|', expand = True)
df = df.drop(columns = [1,2,3,33])
df.columns = field_list 

print(df)
