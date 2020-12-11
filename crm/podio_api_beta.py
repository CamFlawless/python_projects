
# Build out a means of storing this data into a DB and preserving it for archival and analysis 

client_id = "crmdatagettest"
client_secret = "I88RXVb9y1Am0AXauUSdOr8Pux9zAwNHDRSLX0UKmI6SbtTI0u4inxGa8i6cwVqi"
username = "camjcollins@gmail.com"
password = "Padthai123*"
 
from pypodio2 import api
import json 
import pandas as pd 
from sqlalchemy import create_engine



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
offer_items = c.Application.get_items(25523238)['items']
whiteboard_items = c.Application.get_items(25523241)['items']

# for item in whiteboard_items:
#     print(type(item))
#     print(item) 
#     print('\n\n')
# quit() 

# print(offer_items)
# quit() 

def _get_podio_data(my_list, field):
    output_list = []
    for record in my_list:
        for part in record:
            if part == field:
                output_list.append(record[part])
    return(output_list)
    
# # objects related to sales lead application    
# sales_lead_item_id = _get_podio_data(item_details, "app_item_id")
# sales_lead_created_on = _get_podio_data(item_details, "created_on")
# sales_lead_link = _get_podio_data(item_details, "link")
# sales_lead_created_by = _get_podio_data(item_details, "created_by")[0]['name']
# sales_lead_last_event_on = _get_podio_data(item_details, "last_event_on")
# sales_lead_items = _get_podio_data(item_details, "fields")

# # objects related to offers application    
# offer_item_id =  _get_podio_data(offer_items, "app_item_id")
# offer_lead_created_on = _get_podio_data(offer_items, "created_on")
# offer_lead_link = _get_podio_data(offer_items, "link")
# offer_lead_created_by = _get_podio_data(offer_items, "created_by")[0]['name']
# offer_lead_last_event_on = _get_podio_data(offer_items, "last_event_on")
# offer_lead_items = _get_podio_data(offer_items, "fields")


whiteboard_item_id =  _get_podio_data(whiteboard_items, "app_item_id")
whiteboard_lead_created_on = _get_podio_data(whiteboard_items, "created_on")
whiteboard_lead_link = _get_podio_data(whiteboard_items, "link")
whiteboard_lead_created_by = _get_podio_data(whiteboard_items, "created_by")[0]['name']
whiteboard_lead_last_event_on = _get_podio_data(whiteboard_items, "last_event_on")
whiteboard_lead_items = _get_podio_data(whiteboard_items, "fields")



## TEST PRINT 
# for item in sales_lead_items:
#     print(item)
#     print('\n\n\n')
# for item in offer_items:
#     print(item)
#     print('\n\n\n')
# for item in whiteboard_lead_items:
#     print(item)
#     print('\n\n\n')
# quit() 

# items --> list of list of dicts?
# record --> list of dicts 
# entry --> 

def _get_podio_data_a(field_str, field_id, list_to_search):
    return_list = [] # Start with an empty to list to be return once appended 
    for record in list_to_search: # Now iterate thru the list 
        if any(word in str(record) for word in field_str): # if the field id is in the record...
            for component in record:
                if component['field_id'] == field_id:
                    return_list.append(component['values'][0]['value'])
        else: # if the field id is not in the record..
            return_list.append("") # append the return_list with an empty string 
    return(return_list) # the function will return the newly appended list 

def _extract_podio_data(list_to_dig, key):
    return_list = []
    for record in list_to_dig:
        try:
            return_list.append(record[key])
        except TypeError:
            return_list.append('')
    return(return_list)

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



# # SNIPPET OF CODE BELOW WILL GRAB DATA FROM SALES LEAD APP 
# seller_name = _get_podio_data_a(["'field_id': 217204654"],217204616, sales_lead_items)                           # SELLER NAME 
# property_address = _get_podio_data_a(["'field_id': 217204617"],217204617,sales_lead_items)                      # PROPERTY ADDRESS
# seller_phone = _get_podio_data_a(["'field_id': 217204621"],217204621,sales_lead_items)                          # SELLER PHONE
# seller_email = _get_podio_data_a(["'field_id': 217204622"],217204622,sales_lead_items)                          # SELLER EMAIL
# max_allowed_offer = _get_podio_data_a(["'field_id': 217204656"],217204656,sales_lead_items)                     # MAX ALLOWED OFFER  
# pp_sqft_arv = _get_podio_data_a(["'field_id': 217204648"],217204648,sales_lead_items)                           # PP/SQFT ARV
# arv = _get_podio_data_a(["'field_id': 217204653"],217204653,sales_lead_items)                                   # ARV
# repair_est = _get_podio_data_a(["'field_id': 217204654"],217204654, sales_lead_items)                           # REPAIR PRICE EST 
# assignment_fee_wanted = _get_podio_data_a(["'field_id': 217204655"],217204655,sales_lead_items)                 # ASSIGNMENT FEE WANTED 
# comp_pp_sqft = _get_podio_data_a(["'type': 'money', 'field_id': 217204647"],217204647, sales_lead_items)        # COMPS PP/SQFT 
# comp_address = _get_podio_data_a(["'field_id': 217251047"],217251047,sales_lead_items)                          # COMPS ADDRESS
# house_sqft = _get_podio_data_a(["'type': 'number', 'field_id': 217204644"],217204644,sales_lead_items)          # HOUSE SQFT
# house_bed = _extract_podio_data(_get_podio_data_a(["'field_id': 217204642"],217204642,sales_lead_items), 'text')               # HOUSE BEDS
# house_bath = _extract_podio_data(_get_podio_data_a(["'field_id': 217204643"],217204643,sales_lead_items), 'text')              # HOUSE BATHS 
# call_attempts = _get_podio_data_a(["'field_id': 217204626"],217204626,sales_lead_items)                         # CALL ATTEMPTS 
# seller_asking_price = _get_podio_data_a(["'field_id': 217204639"],217204639,sales_lead_items)                   # SELLER ASKING PRICE 
# offer_amount = _get_podio_data_a(["'field_id': 217204658"],217204658,sales_lead_items)                          # OFFER AMOUNT 
# notes = _get_podio_data_a(["field_id': 217204638"],217204638,sales_lead_items)                                  # NOTES
# appointment_date = _date_grabber(["field_id': 217204633"],217204633,sales_lead_items)                          # APPOINTMENT DATE 
# motivation = _extract_podio_data(_get_podio_data_a(["'field_id': 217204632"],217204632,sales_lead_items), 'text')              # MOTIVATION 
# status = _extract_podio_data(_get_podio_data_a(["'field_id': 217204631"],217204631,sales_lead_items), 'text')                  # STATUS  
# source = _extract_podio_data(_get_podio_data_a(["'field_id': 217204630"],217204630,sales_lead_items), 'text')                  # SOURCE  
# parcel = _get_podio_data_a(["'field_id': 217204620"],217204620,sales_lead_items)                                # PARCEL  
# deal_type = _extract_podio_data(_get_podio_data_a(["'field_id': 217204623"],217204623,sales_lead_items),'text')               # DEAL TYPE   
# acqusitions_manager = _extract_podio_data(_get_podio_data_a(["'field_id': 217204624"],217204624,sales_lead_items), 'name') # ACQUSITIONS MANAGER    
# campaign = _extract_podio_data(_get_podio_data_a(["'field_id': 217204659"],217204659,sales_lead_items), 'title')               # CAMPAIGN   
# rehab = _extract_podio_data(_get_podio_data_a(["'field_id': 217204652"],217204652,sales_lead_items), 'text')                   # REHAB   
# offer_range = _get_podio_data_a(["'field_id': 217204657"],217204657,sales_lead_items)                         # OFFER RANGE


# sales_leads_df = pd.DataFrame({
#                    'sales_lead_item_id': sales_lead_item_id, 
#                    'created_on': sales_lead_created_on, 
#                    # 'sales_lead_link': sales_lead_link, 
#                    'sales_lead_created_by': sales_lead_created_by, 
#                    'seller_name': seller_name, 
#                    'property_address': property_address,
#                    'seller_phone': seller_phone,
#                    'seller_email': seller_email, 
#                    'last_event_on' : sales_lead_last_event_on, 
#                    'max_allowed_offfer' : max_allowed_offer, 
#                    'pp_sqft_arv': pp_sqft_arv, 
#                    'arv': arv, 
#                    'repair_est' : repair_est, 
#                    'assignment_fee_wanted' : assignment_fee_wanted, 
#                    'comp_pp_sqft': comp_pp_sqft, 
#                    'comp_address': comp_address, 
#                    'house_sqft': house_sqft, 
#                    'house_bed': house_bed, 
#                    'house_bath': house_bath, 
#                    'call_attempts': call_attempts, 
#                    'seller_asking_price': seller_asking_price, 
#                    'offer_amount': offer_amount, 
#                    'appointment_date' : appointment_date, 
#                    'motivation' : motivation, 
#                    'status' : status, 
#                    'source' : source, 
#                    'parcel' : parcel, 
#                    'deal_type' : deal_type, 
#                    'acqusitions_manager' : acqusitions_manager, 
#                    'campaign': campaign, 
#                    'rehab' : rehab 
#                    # 'notes': notes
#                     })

# # print(sales_leads_df)


# offer_address = _get_podio_data_a(["'field_id': 217204663"],217204663, offer_lead_items)
# offer_dilligence_period_in_days = _get_podio_data_a(["'field_id': 217204685"],217204685, offer_lead_items)
# offer_closing_period_in_days = _get_podio_data_a(["'field_id': 217204687"],217204687, offer_lead_items)
# offer_emd = _get_podio_data_a(["'field_id': 217204684"],217204684, offer_lead_items)
# offer_price = _get_podio_data_a(["'field_id': 217204683"],217204683, offer_lead_items)
# offer_due_dilligence_end = _date_grabber(["field_id': 217204686"],217204686,offer_lead_items)      
# offer_closing_by_date = _date_grabber(["field_id': 217204688"],217204688,offer_lead_items)   
# offer_sales_lead_item_id = _extract_podio_data(_get_podio_data_a(["'field_id': 217204662"],217204662, offer_lead_items),'app_item_id')


# offers_df = pd.DataFrame({
#                     'offer_id': offer_item_id, 
#                     'offer_sales_lead_item_id': offer_sales_lead_item_id, 
#                     'offer_lead_created_on': offer_lead_created_on, 
#                     'offer_lead_created_by': offer_lead_created_by, 
#                     'offer_lead_last_event_on': offer_lead_last_event_on,
#                     'offer_address': offer_address,
#                     'offer_dilligence_period_in_days': offer_dilligence_period_in_days,
#                     'offer_closing_period_in_days': offer_closing_period_in_days,
#                     'offer_emd' : offer_emd,
#                     'offer_price' : offer_price, 
#                     'offer_due_dilligence_end' : offer_due_dilligence_end, 
#                     'offer_closing_by_date' : offer_closing_by_date
#                     })

# print(offers_df)


whiteboard_sales_lead_item_id = _extract_podio_data(_get_podio_data_a(["'field_id': 217204715"],217204715, whiteboard_lead_items),'app_item_id')
whiteboard_offer_item_id = _extract_podio_data(_get_podio_data_a(["'field_id': 217204716"],217204716, whiteboard_lead_items),'app_item_id')
whiteboard_tax_id = _get_podio_data_a(["'field_id': 217204712"],217204712, whiteboard_lead_items)
whiteboard_status = _extract_podio_data(_get_podio_data_a(["'field_id': 217204721"],217204721,whiteboard_lead_items), 'text')  
whiteboard_transaction_status = _extract_podio_data(_get_podio_data_a(["'field_id': 217204723"],217204723,whiteboard_lead_items), 'text')  
whiteboard_marketing_stage = _extract_podio_data(_get_podio_data_a(["'field_id': 217204725"],217204725,whiteboard_lead_items), 'text')  
whiteboard_marketing_price = _get_podio_data_a(["'field_id': 217204726"],217204726, whiteboard_lead_items)
# STILL TO WORK ON UN-NESTING THE WEB LINK LIST 
# whiteboard_web_link = _extract_podio_data(_get_podio_data_a(["'field_id': 217204727"],217204727, whiteboard_lead_items),'resolved_url')
whiteboard_showing_date  = _date_grabber(["field_id': 217204728"],217204728,whiteboard_lead_items)   
whiteboard_closing_date  = _date_grabber(["field_id': 217204740"],217204740,whiteboard_lead_items)   
whiteboard_assignment_stage = _extract_podio_data(_get_podio_data_a(["'field_id': 217204730"],217204730,whiteboard_lead_items), 'text')  
whiteboard_assignee_name = _get_podio_data_a(["'field_id': 217204732"],217204732, whiteboard_lead_items)
whiteboard_assignee_name = _get_podio_data_a(["'field_id': 217204732"],217204732, whiteboard_lead_items)
# these IDs are from multiple apps currently -- should I pull app_ID with it? 
whiteboard_assignee_id = _extract_podio_data(_get_podio_data_a(["'field_id': 217204731"],217204731, whiteboard_lead_items),'app_item_id')
whiteboard_buyer_emd = _get_podio_data_a(["'field_id': 217204735"],217204735, whiteboard_lead_items)
whiteboard_closing_location = _get_podio_data_a(["'field_id': 217204742"],217204742, whiteboard_lead_items)
# these IDs are from multiple apps currently -- should I pull app_ID with it? 
whiteboard_title_company_id = _extract_podio_data(_get_podio_data_a(["'field_id': 217204741"],217204741, whiteboard_lead_items),'app_item_id')
whiteboard_assignee_id = _extract_podio_data(_get_podio_data_a(["'field_id': 217204744"],217204744, whiteboard_lead_items),'text')


whiteboard_df = pd.DataFrame({
                            'whiteboard_sales_lead_item_id': whiteboard_sales_lead_item_id, 
                            'whiteboard_offer_item_id': whiteboard_offer_item_id, 
                            'whiteboard_tax_id': whiteboard_tax_id, 
                            'whiteboard_status': whiteboard_status, 
                                                      
})


# print(whiteboard_marketing_price); 
# print(whiteboard_marketing_stage)
# print(whiteboard_assignment_stage)
quit() 
# NOW GRABBING DATA FROM OFFERS APP 
# MANY FIELDS ARE DUPLICITOUS SO NO NEED TO BRING THEM ALL 
# JUST ENSURE WE GET THE SALES LEAD ID 


# TEMP HOLDER CODE TO LOAD DATA TO POSTGRES SQL DB 
engine = create_engine('postgresql://postgres:B*oker123@localhost:5432/podio_test')
sales_leads_df.to_sql("sales_leads_fact", engine)
offers_df.to_sql("offers_fact", engine)
quit() 


file_destination_path = 'C:\\Users\\Cameron\Documents\\Python'

sales_leads_df.to_csv(file_destination_path + '\podio_sales_leads.csv', index = False)
offers_df.to_csv(file_destination_path + '\podio_offers.csv', index = False)

quit() 



'''

SECTION BELOW IS UNUSED
    - includes comment and test code for misc. use. 

''' 






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



quit() 

# def _return_data_values(input_list):
#     return_list = []
#     for item in input_list:
#         return_list.append(item[0]['value'])
#     return(return_list)

property_address = _return_data(fields,217204617)


print(_return_data_b(property_address))
quit() 



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
