

# GOAL: parse the DocLegalDescription to extract the physical address of the associated property
# CHALLENGES: 
    # 1.) inconsistent format of text in the field
    # 2.) not all entries have a physical address listed..
    # Last Name Conventions: ETAL, LLC, LLC ETAL, MORTGAGE COMPANY, DECEASED, ESTATE 


# COMPLETED:
    # For those cells that conform to the PHYSICAL STREET ADDRESS xxx PLAT BOOK format 


import pandas as pd 
import usaddress
# import numpy as np 

file_source_path = 'C:\\Users\\Cameron\\Downloads'
file_destination_path = 'C:\\Users\\Cameron\Documents\\Python'

# file_source_path = 'C:\\Users\\kacollins\\Downloads'
# file_destination_path = 'C:\\Users\\kacollins\Downloads'

# creating the df with the lp data from SearchResults.csv export 
df = pd.read_csv(file_source_path + '\SearchResults.csv')

# splitting the IndirectName field into a first and last -- simple at this time, split by first space 
df[['Last Name', 'First Name']] = df['IndirectName'].str.split(' ', 1, expand=True)

# creating two new cols -- one for the starting index and one for the ending index 
start_bound = "PHYSICAL STREET ADDRESS "
end_bound = "PLAT BOOK"
df['start_index'] = df['DocLegalDescription'].str.find("PHYSICAL STREET ADDRESS") 
df['end_index'] = df['DocLegalDescription'].str.find("PLAT BOOK")
# to minimize errors, we only look at rows with the index(es)
df = df[df['start_index'] > 0].reset_index()
df = df[df['end_index'] > df['start_index']].reset_index()

list_of_titles = ['ETAL', 'LLC', 'COMPANY', 'DECEASED', 'ESTATE']

# Line below is from Wes on how to apply the change to the df as a whole 
df['Full Address'] = df.apply(lambda x: x['DocLegalDescription'][int(x['start_index']) + len(start_bound) :int(x['end_index'])].strip(),axis=1) 
df['Title'] = df.apply(lambda x: x['First Name'].rsplit(' ', 1)[-1],axis=1) 
df['Title_A'] = df['Title'].isin(list_of_titles)
df['Title'] = df.apply(lambda x: ' ' if x['Title_A']==False else x['Title'], axis=1)
df['First Name'] = df.apply(lambda x: x['First Name'].replace(x['Title'], '')if x['Title'] in x['First Name'] else x['First Name'], axis=1 )
df['Address Tag'] = df.apply(lambda x: usaddress.tag(x['Full Address']), axis=1)

addr_tag = df['Address Tag'].tolist() 
full_address = df['Full Address'].tolist() 
first_name = df['First Name'].tolist()
last_name = df['Last Name'].tolist()
title = df['Title'].to_list()

def _get_addy_part(address,part):
    result = []
    for addy in address:
        if str(addy[0]).find(part) == -1:
            result.append('')
        else:
            result.append(str(addy[0])[str(addy[0]).find(part) + len(part): str(addy[0]).find("')", str(addy[0]).find(part))].strip())
    
    return(result) 

house_num = _get_addy_part(addr_tag,"'AddressNumber', '")
street = _get_addy_part(addr_tag,"'StreetName', '")
street_post_type = _get_addy_part(addr_tag,"'StreetNamePostType', '")
street_full = [l + ' ' + m + ' ' + str(n) for l,m,n in zip(house_num,street,street_post_type)]
city = _get_addy_part(addr_tag,"'PlaceName', '")
zips = _get_addy_part(addr_tag,"'ZipCode', '")


df2 = pd.DataFrame({'First Name': first_name, 
                    'Last Name': last_name, 
                    # 'Title': title, 
                    'Address': full_address, 
                    'Street': street_full, 
                    'City': city, 
                    'Zip': zips }) 
print(df2.head)
df2.to_csv(file_destination_path + '\clean_lp_list.csv', index = False)
quit() 
