
# Build out a means of storing this data into a DB and preserving it for archival and analysis 

client_id = "crmdatagettest"
client_secret = "I88RXVb9y1Am0AXauUSdOr8Pux9zAwNHDRSLX0UKmI6SbtTI0u4inxGa8i6cwVqi"
username = "camjcollins@gmail.com"
password = "Padthai123*"
 
from pypodio2 import api
import json 
import pandas as pd 

c = api.OAuthClient(
    client_id,
    client_secret,
    username,
    password,    
)

# print(c.Application.find(25523237))
# app_details = c.Application.find(25523237)

# THIS IS PROVIDING LIST OF ITEMS FROM THE LEADS APP
# APPEARS TO BE A HEAVILY NESTED OBJECT (LIST OF DICTS OF LISTS, ETC.) 
item_details = c.Application.get_items(25523237)['items']



# x = 1 
# for record in item_details:
#     if x == 1 :
#         print(record['fields'])
#         quit() 
#         for part in record:
#             print(['part ' + str(x) + ' is..'])
#             print(part) 
#             print('\n')
#     x = x + 1 
# quit() 



def _get_podio_data(my_list, field):
    output_list = []
    for record in my_list:
        for part in record:
            if part == field:
                output_list.append(record[part])
    return(output_list)
    
item_id = _get_podio_data(item_details, "app_item_id")
# seller_name = _get_podio_data(item_details, "title")
created_on = _get_podio_data(item_details, "created_on")
link = _get_podio_data(item_details, "link")
# created_via = _get_podio_data(item_details, "created_via")
created_by = _get_podio_data(item_details, "created_by")[0]['name']
last_event_on = _get_podio_data(item_details, "last_event_on")
items = _get_podio_data(item_details, "fields")
# print(type(fields)) ---> LIST of DICTS 

# fields_i_want = [217204616, 217204617, 217204620 ,217204621, 217204622, 217204623, 217204624, 217204626, 217204630, 217204631, 217204632,
#                  217204633, 217204639, 217204640, 217204641, 217204642, 217204643, 217204644, 217251047, 217204647, 217204648, 217204652, 
#                  217204653, 217204654, 217204655, 217204656, 217204658, 217204659]


# if for the record, the field id key is found, append list with values 
# if not, append the list with empty string 
# need to do check with IF statement on loop iterating through the records 


# items --> list of list of dicts?
# record --> list of dicts 
# entry --> 




x = 0 
y = 0 

# any(word in str(record) for word in "'field_id': " + str(field_id))

# def _my_fav_function(field_id, list_to_search):
#     return_list = [] # Start with an empty to list to be return once appended 
#     # print("'field_id': " + str(field_id))
#     for record in list_to_search: # Now iterate thru the list 
#         if any(word in str(record) for word in "'field_id': " + str(field_id)): # if the field id is in the record...
#             for component in record:
#                 if component['field_id'] == field_id:
#                     return_list.append(component['values'][0]['value'])
#         else: # if the field id is not in the record..
#             return_list.append("") # append the return_list with an empty string 
#     return(return_list) # the function will return the newly appended list 

# print(_my_fav_function(217204654, items))
# quit() 



field_str = ["'type': 'money', 'field_id': 217204647"]
return_list = [] # Start with an empty to list to be return once appended 

# for record in items: # Now iterate thru the list 
#     print(any(word in str(record) for word in field_str))
# quit() 

# print(len(items))
# for record in items: # Now iterate thru the list 
#     if any(word in str(record) for word in field_str): # if the field id is in the record...
#         # print(str(record))
#         # print('\n\n')
#         for component in record:
#             if component['field_id'] == 217204647:
#                 return_list.append(component['values'][0]['value'])
#     else: # if the field id is not in the record..
#         # print(str(record))
#         # print('\n\n')
#         return_list.append("") # append the return_list with an empty string 
# print(return_list) # the function will return the newly appended list 
# quit() 



def _my_fav_function(field_str, field_id, list_to_search):
    return_list = [] # Start with an empty to list to be return once appended 
    for record in list_to_search: # Now iterate thru the list 
        if any(word in str(record) for word in field_str): # if the field id is in the record...
            for component in record:
                if component['field_id'] == field_id:
                    return_list.append(component['values'][0]['value'])
        else: # if the field id is not in the record..
            return_list.append("") # append the return_list with an empty string 
    return(return_list) # the function will return the newly appended list 

def _date_grabber(field_str, field_id, list_to_search):
    return_list = [] # Start with an empty to list to be return once appended 
    for record in list_to_search: # Now iterate thru the list 
        if any(word in str(record) for word in field_str): # if the field id is in the record...
            for component in record:
                if component['field_id'] == field_id:
                    return_list.append(component['values'][0]['start'])
        else: # if the field id is not in the record..
            return_list.append("") # append the return_list with an empty string 
    return(return_list) # the function will return the newly appended list 

# SEE HOW TO CREATE A SINGLE FUNCTION TO DO WHAT BOTH OF THESE ARE DOING 
def _further_dig(list_to_dig):
    return_list = []
    for record in list_to_dig:
        try:
            return_list.append(record['text'])
        except TypeError:
            return_list.append('')
    return(return_list)

def _further_digging(list_to_dig):
    return_list = []
    for record in list_to_dig:
        try:
            return_list.append(record['name'])
        except TypeError:
            return_list.append('')
    return(return_list)

def _return_title(list_to_dig):
    return_list = []
    for record in list_to_dig:
        try:
            return_list.append(record['title'])
        except TypeError:
            return_list.append('')
    return(return_list)
# print(_further_dig(house_bed))
# quit() 

# print(_my_fav_function(["'type': 'money', 'field_id': 217204647"],217204647, items))
# # # print(_my_fav_function(["'field_id': 21720467"],21720467, items))

# quit() 
        

# search = ["'field_id': 217204654"]
# return_list = []
# for record in items:
#     # print(record)
#     # print(str(record))
#     # quit() 
#     if any(word in str(record) for word in search):        
#         # Now that we know the field has a value for this record
#         # We want to find it and append it to the return_list  
#         for component in record:
#             if component['field_id']  == 217204654:
#                 return_list.append(component['values'][0]['value'])
#     else:
#         return_list.append("")
# print(len(return_list))
# quit() 

'''
STILL OUTSTANDING ATTRIBUTES:

'''

seller_name = _my_fav_function(["'field_id': 217204654"],217204616, items)                           # SELLER NAME 
property_address = _my_fav_function(["'field_id': 217204617"],217204617,items)                      # PROPERTY ADDRESS
seller_phone = _my_fav_function(["'field_id': 217204621"],217204621,items)                          # SELLER PHONE
seller_email = _my_fav_function(["'field_id': 217204622"],217204622,items)                          # SELLER EMAIL
max_allowed_offer = _my_fav_function(["'field_id': 217204656"],217204656,items)                     # MAX ALLOWED OFFER  
pp_sqft_arv = _my_fav_function(["'field_id': 217204648"],217204648,items)                           # PP/SQFT ARV
arv = _my_fav_function(["'field_id': 217204653"],217204653,items)                                   # ARV
repair_est = _my_fav_function(["'field_id': 217204654"],217204654, items)                           # REPAIR PRICE EST 
assignment_fee_wanted = _my_fav_function(["'field_id': 217204655"],217204655,items)                 # ASSIGNMENT FEE WANTED 
comp_pp_sqft = _my_fav_function(["'type': 'money', 'field_id': 217204647"],217204647, items)        # COMPS PP/SQFT 
comp_address = _my_fav_function(["'field_id': 217251047"],217251047,items)                          # COMPS ADDRESS
house_sqft = _my_fav_function(["'type': 'number', 'field_id': 217204644"],217204644,items)          # HOUSE SQFT
house_bed = _further_dig(_my_fav_function(["'field_id': 217204642"],217204642,items))               # HOUSE BEDS
house_bath = _further_dig(_my_fav_function(["'field_id': 217204643"],217204643,items))              # HOUSE BATHS 
call_attempts = _my_fav_function(["'field_id': 217204626"],217204626,items)                         # CALL ATTEMPTS 
seller_asking_price = _my_fav_function(["'field_id': 217204639"],217204639,items)                   # SELLER ASKING PRICE 
offer_amount = _my_fav_function(["'field_id': 217204658"],217204658,items)                          # OFFER AMOUNT 
notes = _my_fav_function(["field_id': 217204638"],217204638,items)                                  # NOTES
appointment_date = _date_grabber(["field_id': 217204633"],217204633,items)                          # APPOINTMENT DATE 
motivation = _further_dig(_my_fav_function(["'field_id': 217204632"],217204632,items))              # MOTIVATION 
status = _further_dig(_my_fav_function(["'field_id': 217204631"],217204631,items))                  # STATUS  
source = _further_dig(_my_fav_function(["'field_id': 217204630"],217204630,items))                  # SOURCE  
parcel = _my_fav_function(["'field_id': 217204620"],217204620,items)                                # PARCEL  
deal_type = _further_dig(_my_fav_function(["'field_id': 217204623"],217204623,items))               # DEAL TYPE   
acqusitions_manager = _further_digging(_my_fav_function(["'field_id': 217204624"],217204624,items)) # ACQUSITIONS MANAGER    
campaign = _return_title(_my_fav_function(["'field_id': 217204659"],217204659,items))               # CAMPAIGN   
rehab = _further_dig(_my_fav_function(["'field_id': 217204652"],217204652,items))                   # REHAB   

offer_range = _my_fav_function(["'field_id': 217204657"],217204657,items)                         # OFFER RANGE





print(offer_range)
quit() 



# my_beds = []
# for record in house_bed:
#     try:
#         my_beds.append(record['text'])
#     except TypeError:
#         my_beds.append('')
# print(my_beds)
# quit()



# print("seller name " + str(len(seller_name)))
# print("address " + str(len(property_address)))
# print("seller_phone " + str(len(seller_phone)))
# print("seller_email " + str(len(seller_email)))
# print("max_allowed_offer " + str(len(max_allowed_offer)))
# print("pp_sqft_arv " + str(len(pp_sqft_arv)))
# print("repair_est " + str(len(repair_est))) # 2 ENTRIES
# print("assignment_fee " + str(len(assignment_fee))) # 2 ENTRIES
# print("comp_pp_sqft " + str(len(comp_pp_sqft))) # 0 ENTRIES 

# print("comp_address " + str(len(comp_address)))
# print("house_sqft " + str(len(house_sqft)))
# print("house_bed " + str(len(house_bed)))
# print("house_bath " + str(len(house_bath)))
# print("call_attempts" + str(len(call_attempts)))
# quit() 

df = pd.DataFrame({
                   'item_id': item_id, 
                   'created_on': created_on, 
                   # 'link': link, 
                   'created_by': created_by, 
                   'seller_name': seller_name, 
                   'property_address': property_address,
                   'seller_phone': seller_phone,
                   'seller_email': seller_email, 
                   'last_event_on' : last_event_on, 
                   'max_allowed_offfer' : max_allowed_offer, 
                   'pp_sqft_arv': pp_sqft_arv, 
                   'arv': arv, 
                   'repair_est' : repair_est, 
                   'assignment_fee_wanted' : assignment_fee_wanted, 
                   'comp_pp_sqft': comp_pp_sqft, 
                   'comp_address': comp_address, 
                   'house_sqft': house_sqft, 
                   'house_bed': house_bed, 
                   'house_bath': house_bath, 
                   'call_attempts': call_attempts, 
                   'seller_asking_price': seller_asking_price, 
                   'offer_amount': offer_amount, 
                   'appointment_date' : appointment_date, 
                   'motivation' : motivation, 
                   'status' : status, 
                   'source' : source, 
                   'parcel' : parcel, 
                   'deal_type' : deal_type, 
                   'acqusitions_manager' : acqusitions_manager, 
                   'campaign': campaign, 
                   'rehab' : rehab 
                   # 'notes': notes
                    })

print(df)


# file_destination_path = 'C:\\Users\\Cameron\Documents\\Python'
# df.to_csv(file_destination_path + '\podio_sales_leads.csv', index = False)

quit() 



# def _return_data(items, field_id):
#     return_list = [] 
#     for record in items:
#         for field in record:
#             if field['field_id']  == field_id:
#                 try:
#                     return_list.append(field['values'][0]['value'])
#                 except KeyError:
#                     return_list.append('') 
#     return(return_list)

## Below are the "simple" fields -- they do NOT require additional un-nesting 
## Will work on additional code for other items
seller_name = _return_data(items,217204616)        # SELLER NAME 
property_address = _return_data(items,217204617)   # PROPERTY ADDRESS
seller_phone = _return_data(items,217204621)       # SELLER PHONE
seller_email = _return_data(items,217204622)       # SELLER EMAIL
max_allowed_offer = _return_data(items,217204656)  # MAX ALLOWED OFFER  
pp_sqft_arv = _return_data(items,217204648)        # PP/SQFT ARV
arv = _return_data(items,217204653)                # ARV
repair_est = _return_data(items,217204654)         # REPAIR PRICE EST 
assignment_fee = _return_data(items,217204655)     # ASSIGNMENT FEE WANTED 
comp_pp_sqft = _return_data(items,21720467)        # COMPS PP/SQFT 
comp_address = _return_data(items,217251047)       # COMPS ADDRESS
house_sqft = _return_data(items,217204644)         # HOUSE SQFT
house_bed = _return_data(items,217204642)          # HOUSE BEDS
house_bath = _return_data(items,217204643)         # HOUSE BATHS 
call_attempts = _return_data(items,217204626)      # CALL ATTEMPTS 

# print(len(seller_name))
# print(len(property_address))
# print(len(seller_phone))
# print(len(seller_email))
# print(len(max_allowed_offer))
# print(len(pp_sqft_arv))
# print(len(repair_est)) # 2 ENTRIES
# print(len(assignment_fee)) # 2 ENTRIES
# print(len(comp_pp_sqft)) # 0 ENTRIES 
# quit() 
# print(len(comp_address))
# print(len(house_sqft))
# print(len(house_bed))
# print(len(house_bath))
# print(len(call_attempts))



quit() 

# def _return_data_values(input_list):
#     return_list = []
#     for item in input_list:
#         return_list.append(item[0]['value'])
#     return(return_list)

property_address = _return_data(fields,217204617)


print(_return_data_b(property_address))
quit() 


addy = []
for entry in property_address:
    addy.append(entry[0]['value'])
print(addy)
quit() 
print(property_address['value'])
print(len(property_address))
quit() 
# seller_phone = _return_data(fields,217204621)

# seller_names = _return_data(fields,217204616)




seller_phone = _return_data(fields,217204621)
phone = []
for item in seller_phone:
    phone.append(item[0]['value'])
print(phone) 
quit() 

# print(seller_name)
# print(property_address)
# print(seller_phone)
# quit() 

print(_return_data(fields,217204616))
print(type(_return_data(fields, 217204616)))
quit() 



for record in fields:
    if y < 3:
        for field in record:
            # if field['field_id'] in fields_i_want:
            #     print(type(field['values']))
            #     print(field['values'])
            #     print('\n\n')

            #     print(str(field['field_id']) + ' -- ' + str(field['label']))
            # for key in field:
            #     test[key] = field[key]
            #     print(field[key])
            #     quit() 

            print(str(y) + ' -- ' + str(type(field)) + '\n\n')
            print(field)
            y = y + 1 
            
    # print(type(item)) ---> LIST 
    # print(str(x) + ' ' +  str(type(record)) + '\n\n')
    # print('\n\n')
    x = x + 1 
quit()     

''' 
fields[0] = seller_name
fields[1] = property address
fields[4] = seller phone
fields[5] = seller email 
fields[6] = deal type 
fields[7] = acquisition manager 
fields[11] = status 
fields[12] = motivation 
fields[20] = max allowed offer 
fields[21] = campaign 
fields[
'''

print(type(fields))
print(fields[0])
quit() 

new_create = []
for item in created_by:
    # print(type(item)) --->> DICT
    x = 1 
    for value in item.items():
        if x == 2:
            new_create.append(value[1])
        x = x + 1 
    #print(item)

print(pd.DataFrame({ 'item_id': item_id, 
                     'created_on': created_on,
                     # 'created_via': created_via,  
                     'created_by': new_create,
                     'seller_name': seller_name, 
                     'last_event_on': last_event_on
                     }))
                    

# lead_contact_name = _get_podio_data(item_details, "title")
# for list in _get_podio_data(item_details, "fields"):
    # for item in list:
        
        

quit() 
            

 

quit()  
print(type(app_details))
# print(app_details['url_label'])
app_dict_keys = list(app_details.keys())

print(app_dict_keys)


quit() 

my_workspace = c.Item.find(1596597192) #Get https://hoist.podio.com/api/item/22481
for item in my_workspace:
    print(item)
    print('\n')
    
# my_app = c.Apps.Find(25523237)
# print(my_app)
print(c.Space.find_by_url("https://podio.com/bhbofferscom/crm-test/apps"))
# print(c.Space.find_by_url("https://remaxtraditions.podio.com/remaxtraditions/")) #Find ID

# items = c.Application.get_items(48294)['items']

quit() 
#To create an item
item = {
	"fields":[
		{"external_id":"org-name", "values":[{"value":"The Items API sucks"}]}
	]
}
#print c.Application.find(179652)
c.Item.create(app_id, item)
			
#Undefined and created at runtime example
#print c.transport.GET.user.status()

# Other methods are:
# c.transport.PUT.#{uri}.#{divided}.{by_slashes}()
# c.transport.DELETE.#{uri}.#{divided}.{by_slashes}()
# c.transport.POST.#{uri}.#{divided}.{by_slashes}(body=paramDict))
# For POST and PUT you can pass "type" as a kwarg and register the type as either
# application/x-www-form-urlencoded or application/json to match what API expects.

#items[0]['fields'][2]['values'][0]['value']['file_id']
