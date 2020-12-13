
# Build out a means of storing this data into a DB and preserving it for archival and analysis 

client_id = "crmdatagettest"
client_secret = "I88RXVb9y1Am0AXauUSdOr8Pux9zAwNHDRSLX0UKmI6SbtTI0u4inxGa8i6cwVqi"
username = "camjcollins@gmail.com"
password = "Padthai123*"
 
from pypodio2 import api
import pygsheets 
import json 
import pandas as pd 
from sqlalchemy import create_engine


c = api.OAuthClient(
    client_id,
    client_secret,
    username,
    password,    
)


def _get_podio_data(my_list, field):
    output_list = []
    for record in my_list:
        for part in record:
            if part == field:
                output_list.append(record[part])
    return(output_list)


apps_dict = {}
# APPEND LIST WITH ADDITIONAL APP NAME AND IDs
apps_to_grab = [ ["sales_leads", 25523237], 
                 ["offers", 25523238], 
                 ["whiteboard", 25523241], 
                 ["appointments", 25523247] 
               ]

for item in apps_to_grab:
    apps_dict[item[0]] = c.Application.get_items(item[1])['items']


# CREATING EMPTY DICTS TO BE APPENDED 
''' 
    NOTES: CREATED BY IS A MORE DEEPLY NESTED LIST IN THE OBJECT
    WILL NEED TO WRITE ADDITIONAL FOR LOOPS TO GO AND GRAB VALUE
'''
app_item_id_dict = {}
item_created_on_dict = {} 
item_last_event_on_dict = {} 
item_fields_dict = {} 

for key, value in apps_dict.items():
    app_item_id_dict[key] = _get_podio_data(value, "app_item_id")
    item_created_on_dict[key] = _get_podio_data(value, "created_on")
    item_last_event_on_dict[key] = _get_podio_data(value, "last_event_on")
    item_fields_dict[key] = _get_podio_data(value, "fields")

# print(item_fields_dict['appointments'])
# quit() 

def _podio_get_field_data_simple(list_to_search, field_id):
    return_list = [] 
    for record in list_to_search: # record == item in this case (1 sales lead, 1 offer, 1 appt, etc.)
        search_str = ["'field_id': "  + str(field_id) + ", 'label'"]
        if any(word in str(record) for word in search_str): # if the record has data for the specified field..
            for field in record: # field == a field (or attribute) of the item 
                if field['field_id'] == field_id:
                    try:
                        return_list.append(field['values'][0]['value'])
                    except KeyError:
                        return_list.append(field['values'][0]['start'])
        else:
            return_list.append("")
    return(return_list)

def _get_nested_podio_data(list_to_dig, key):
    return_list = []
    for record in list_to_dig:
        try:
            return_list.append(record[key])
        except TypeError:
            return_list.append('')
    return(return_list)


fields_simple = {'sales_leads' : [  ["seller_name" , 217204616], 
                                    ["property_address" , 217204617 ], 
                                    ["seller_phone" , 217204621], 
                                    ["seller_email" , 217204622], 
                                    ["max_allowed_offer" , 217204656], 
                                    ["pp_sqft_arv" , 217204648], 
                                    ["arv" , 217204653], 
                                    ["repair_est" , 217204654], 
                                    ["assignment_fee_wanted" , 217204655], 
                                    ["comp_pp_sqft" , 217204647], 
                                    ["comp_address" , 217251047], 
                                    ["house_sqft" , 217204644], 
                                    ["call_attempts" , 217204626], 
                                    ["seller_asking_price" , 217204639], 
                                    ["offer_amount" , 217204658], 
                                    ["appointment_date" , 217204633], 
                                    ["parcel" , 217204620], 
                                    ["offer_range" , 217204657]
                                 ],           
                 'offers' : [       ["offer_address", 217204663], 
                                    ["offer_dilligence_period_in_days",  217204685], 
                                    ["offer_closing_period_in_days", 217204687], 
                                    ["offer_emd", 217204684], 
                                    ["offer_price", 217204683], 
                                    ["offer_due_dilligence_end", 217204686], 
                                    ["offer_closing_by_date", 217204688],                         
                            ],  
                 'whiteboard' : [   ["whiteboard_tax_id", 217204712], 
                                    ["whiteboard_marketing_price",217204726], 
                                    ["whiteboard_showing_date", 217204728], 
                                    ["whiteboard_closing_date", 217204740], 
                                    ["whiteboard_assignee_name", 217204732], 
                                    ["whiteboard_buyer_emd", 217204735], 
                                    ["whiteboard_closing_location", 217204742]                          
                                ], 
                 'appointments' : [ ["appointment_property_address", 217204797], 
                                    ["appointment_date", 217204798], 
                                    ["appointment_seller_phone", 217204801], 
                                    ["appointment_notes", 217204803]
                            ] }


fields_nested = { 'sales_leads' :  [ ["house_beds" , 217204642, 'text'], 
                                     ["house_baths" , 217204643, 'text'], 
                                     ["motivation" , 217204632, 'text'], 
                                     ["status" , 217204631, 'text'], 
                                     ["source" , 217204630, 'text'], 
                                     ["deal_type" , 217204623, 'text'], 
                                     ["acquisitions_manager" , 217204624, 'name'], 
                                     ["campaign" , 217204659, 'title'], 
                                     ["rehab" , 217204652, 'text'], 
                                   ], 
                  'offers':        [ ["offer_sales_lead_item_id", 217204662, 'app_item_id']], 
                  'whiteboard' :   [ ["whiteboard_sales_lead_item_id", 217204715, 'app_item_id'], 
                                     ["whiteboard_offer_item_id", 217204716, 'app_item_id'], 
                                     ["whiteboard_status", 217204721, 'text'], 
                                     ["whiteboard_transaction_status", 217204723, 'text'], 
                                     ["whiteboard_marketing_stage", 217204725, 'text'], 
                                     ["whiteboard_assignment_stage", 217204730, 'text'], 
                                     ["whiteboard_assignee_id", 217204731, 'app_item_id'], 
                                     ["whiteboard_title_company_id", 217204741, 'app_item_id'], 
                                     ["whiteboard_agreement_sent_to_title", 217204744, 'text']
                                   ], 
                  'appointments' : [ ["appointment_seller_name", 217204796, 'app_item_id'], 
                                     ["appointment_agent", 217204799, 'text'], 
                                     ["appointment_result", 217204804, 'text'], 
                                     ["appointment_is_attending", 217204800, 'name']
                                   ]
                }

''' START BACK HERE (AND TURN IT INTO A FUNCTION) ''' 

sales_lead_items_dict = {} 
for field in fields_simple['sales_leads']:
    sales_lead_items_dict[field[0]] = _podio_get_field_data_simple(item_fields_dict['sales_leads'], field[1])    

for field in fields_nested['sales_leads']:
    sales_lead_items_dict[field[0]] = _get_nested_podio_data(_podio_get_field_data_simple(item_fields_dict['sales_leads'], field[1]), field[2])


print(sales_lead_items_dict)
quit() 
     
sales_leads_fields_simple = [ ["seller_name" , 217204616], 
                              ["property_address" , 217204617 ], 
                              ["seller_phone" , 217204621], 
                              ["seller_email" , 217204622], 
                              ["max_allowed_offer" , 217204656], 
                              ["pp_sqft_arv" , 217204648], 
                              ["arv" , 217204653], 
                              ["repair_est" , 217204654], 
                              ["assignment_fee_wanted" , 217204655], 
                              ["comp_pp_sqft" , 217204647], 
                              ["comp_address" , 217251047], 
                              ["house_sqft" , 217204644], 
                              ["call_attempts" , 217204626], 
                              ["seller_asking_price" , 217204639], 
                              ["offer_amount" , 217204658], 
                              ["appointment_date" , 217204633], 
                              ["parcel" , 217204620], 
                              ["offer_range" , 217204657]
                            ]
# CERTAIN FIELD TYPES REQUIRE ADDITIONAL UN-NESTING: category, app, contact, etc. 
sales_leads_fields_nested = [ ["house_beds" , 217204642, 'text'], 
                              ["house_baths" , 217204643, 'text'], 
                              ["motivation" , 217204632, 'text'], 
                              ["status" , 217204631, 'text'], 
                              ["source" , 217204630, 'text'], 
                              ["deal_type" , 217204623, 'text'], 
                              ["acquisitions_manager" , 217204624, 'name'], 
                              ["campaign" , 217204659, 'title'], 
                              ["rehab" , 217204652, 'text'], 
                            ]


sales_lead_items_dict = {} 
for field in sales_leads_fields_simple:
    sales_lead_items_dict[field[0]] = _podio_get_field_data_simple(item_fields_dict['sales_leads'], field[1])    

for field in sales_leads_fields_nested:
    sales_lead_items_dict[field[0]] = _get_nested_podio_data(_podio_get_field_data_simple(item_fields_dict['sales_leads'], field[1]), field[2])

sales_lead_df = pd.DataFrame.from_dict(sales_lead_items_dict).assign(sales_lead_item_id = app_item_id_dict['sales_leads'], 
                                                                     sales_lead_created_on = item_created_on_dict['sales_leads'], 
                                                                     sales_lead_last_event_on = item_last_event_on_dict['sales_leads'] )
print("Your sales lead dataframe looks like >>> " + '\n')
print(sales_lead_df)
print('\n\n')

offers_fields_simple = [ ["offer_address", 217204663], 
                         ["offer_dilligence_period_in_days",  217204685], 
                         ["offer_closing_period_in_days", 217204687], 
                         ["offer_emd", 217204684], 
                         ["offer_price", 217204683], 
                         ["offer_due_dilligence_end", 217204686], 
                         ["offer_closing_by_date", 217204688],                         
                       ]

offers_fields_nested = [ ["offer_sales_lead_item_id", 217204662, 'app_item_id']]


offer_items_dict = {} 
for field in offers_fields_simple:
    offer_items_dict[field[0]] = _podio_get_field_data_simple(item_fields_dict['offers'], field[1]) 

for field in offers_fields_nested:
       offer_items_dict[field[0]] = _get_nested_podio_data(_podio_get_field_data_simple(item_fields_dict['offers'], field[1]), field[2])

offers_df = pd.DataFrame.from_dict(offer_items_dict).assign(offer_item_id = app_item_id_dict['offers'], 
                                                            offer_created_on = item_created_on_dict['offers'], 
                                                            offer_last_event_on = item_last_event_on_dict['offers'] )

print("Your offers dataframe looks like >>> " + '\n')
print(offers_df)
print('\n\n')



whiteboard_fields_simple = [ ["whiteboard_tax_id", 217204712], 
                             ["whiteboard_marketing_price",217204726], 
                             ["whiteboard_showing_date", 217204728], 
                             ["whiteboard_closing_date", 217204740], 
                             ["whiteboard_assignee_name", 217204732], 
                             ["whiteboard_buyer_emd", 217204735], 
                             ["whiteboard_closing_location", 217204742]                          
                           ]

whiteboard_fields_nested = [ ["whiteboard_sales_lead_item_id", 217204715, 'app_item_id'], 
                             ["whiteboard_offer_item_id", 217204716, 'app_item_id'], 
                             ["whiteboard_status", 217204721, 'text'], 
                             ["whiteboard_transaction_status", 217204723, 'text'], 
                             ["whiteboard_marketing_stage", 217204725, 'text'], 
                             ["whiteboard_assignment_stage", 217204730, 'text'], 
                             ["whiteboard_assignee_id", 217204731, 'app_item_id'], 
                             ["whiteboard_title_company_id", 217204741, 'app_item_id'], 
                             ["whiteboard_agreement_sent_to_title", 217204744, 'text']

                           ]

whiteboard_items_dict = {} 
for field in whiteboard_fields_simple:
    whiteboard_items_dict[field[0]] = _podio_get_field_data_simple(item_fields_dict['whiteboard'], field[1]) 

for field in whiteboard_fields_nested:
       whiteboard_items_dict[field[0]] = _get_nested_podio_data(_podio_get_field_data_simple(item_fields_dict['whiteboard'], field[1]), field[2])

whiteboard_df = pd.DataFrame.from_dict(whiteboard_items_dict).assign(whiteboard_item_id = app_item_id_dict['whiteboard'], 
                                                                     whiteboard_created_on = item_created_on_dict['whiteboard'], 
                                                                     whiteboard_last_event_on = item_last_event_on_dict['whiteboard'] )

print("Your whiteboard dataframe looks like >>> " + '\n')
print(whiteboard_df)
print('\n\n')


appointment_fields_simple = [ ["appointment_property_address", 217204797], 
                              ["appointment_date", 217204798], 
                              ["appointment_seller_phone", 217204801], 
                              ["appointment_notes", 217204803]
                            ]

appointment_fields_nested = [ ["appointment_seller_name", 217204796, 'app_item_id'], 
                              ["appointment_agent", 217204799, 'text'], 
                              ["appointment_result", 217204804, 'text'], 
                              ["appointment_is_attending", 217204800, 'name']
                            ]

appointment_items_dict = {} 
for field in appointment_fields_simple:
    appointment_items_dict[field[0]] = _podio_get_field_data_simple(item_fields_dict['appointments'], field[1]) 

for field in appointment_fields_nested:
       appointment_items_dict[field[0]] = _get_nested_podio_data(_podio_get_field_data_simple(item_fields_dict['appointments'], field[1]), field[2])

appointment_df = pd.DataFrame.from_dict(appointment_items_dict).assign(appointment_item_id = app_item_id_dict['appointments'], 
                                                                       appointment_created_on = item_created_on_dict['appointments'],
                                                                       appointment_last_event_on = item_last_event_on_dict['appointments'] )

print("Your appointments dataframe looks like >>> " + '\n')
print(appointment_df)
print('\n\n')

# TEMP HOLDER CODE TO LOAD DATA TO POSTGRES SQL DB 
engine = create_engine('postgresql://postgres:B*oker123@localhost:5432/podio_test')

sales_lead_df.to_sql("sales_leads_fact", engine, if_exists='replace')
offers_df.to_sql("offers_fact", engine, if_exists='replace')
whiteboard_df.to_sql("whiteboard_fact", engine, if_exists='replace')
appointment_df.to_sql("appointments_fact", engine, if_exists='replace')
quit() 



quit() 

# def _get_podio_data_a(field_id, list_to_search):
#   return_list = [] # Start with an empty to list to be return once appended 
#   for record in list_to_search: # Now iterate thru the list 
#       if any(word in str(record) for word in list("'field_id': "  + str(field_id))): # if the field id is in the record...
#           for component in record:
#               if component['field_id'] == field_id:
#                   return_list.append(component['values'][0]['value'])
#       else: # if the field id is not in the record..
#           return_list.append("") # append the return_list with an empty string 
#   return(return_list) # the function will return the newly appended list 

# def _extract_podio_data(list_to_dig, key):
#     return_list = []
#     for record in list_to_dig:
#         try:
#             return_list.append(record[key])
#         except TypeError:
#             return_list.append('')
#     return(return_list)
    

# def _date_grabber(field_str, field_id, list_to_search):
#     return_list = [] # Start with an empty to list to be return once appended 
#     for record in list_to_search: # Now iterate thru the list 
#         if any(word in str(record) for word in field_str): # if the field id is in the record...
#             for component in record:
#                 if component['field_id'] == field_id:
#                     return_list.append(component['values'][0]['start'])
#         else: # if the field id is not in the record..
#             return_list.append("") # append the return_list with an empty string 
#     return(return_list) # the function will return the newly appended list 



# SNIPPET OF CODE BELOW WILL GRAB DATA FROM SALES LEAD APP 
# seller_name = _get_podio_data_a(["'field_id': 217204616, sales"],217204616, sales_lead_items)                           # SELLER NAME 
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
# call_attempts = _get_podio_data_a(["'field_id': 217204626"],217204626,sales_lead_items)                         # CALL ATTEMPTS 
# seller_asking_price = _get_podio_data_a(["'field_id': 217204639"],217204639,sales_lead_items)                   # SELLER ASKING PRICE 
# offer_amount = _get_podio_data_a(["'field_id': 217204658"],217204658,sales_lead_items)                          # OFFER AMOUNT 
# notes = _get_podio_data_a(["field_id': 217204638"],217204638,sales_lead_items)                                  # NOTES
# parcel = _get_podio_data_a(["'field_id': 217204620"],217204620,sales_lead_items)                                # PARCEL  
# offer_range = _get_podio_data_a(["'field_id': 217204657"],217204657,sales_lead_items)                         # OFFER RANGE

# house_bed = _extract_podio_data(_get_podio_data_a(["'field_id': 217204642"],217204642,sales_lead_items), 'text')               # HOUSE BEDS
# house_bath = _extract_podio_data(_get_podio_data_a(["'field_id': 217204643"],217204643,sales_lead_items), 'text')              # HOUSE BATHS 
# motivation = _extract_podio_data(_get_podio_data_a(["'field_id': 217204632"],217204632,sales_lead_items), 'text')              # MOTIVATION 
# status = _extract_podio_data(_get_podio_data_a(["'field_id': 217204631"],217204631,sales_lead_items), 'text')                  # STATUS  
# source = _extract_podio_data(_get_podio_data_a(["'field_id': 217204630"],217204630,sales_lead_items), 'text')                  # SOURCE  
# deal_type = _extract_podio_data(_get_podio_data_a(["'field_id': 217204623"],217204623,sales_lead_items),'text')               # DEAL TYPE   
# acqusitions_manager = _extract_podio_data(_get_podio_data_a(["'field_id': 217204624"],217204624,sales_lead_items), 'name') # ACQUSITIONS MANAGER    
# campaign = _extract_podio_data(_get_podio_data_a(["'field_id': 217204659"],217204659,sales_lead_items), 'title')               # CAMPAIGN   
# rehab = _extract_podio_data(_get_podio_data_a(["'field_id': 217204652"],217204652,sales_lead_items), 'text')                   # REHAB   

# appointment_date = _date_grabber(["field_id': 217204633"],217204633,sales_lead_items)                          # APPOINTMENT DATE 




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

# print(sales_leads_df)
# quit() 


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

# # print(offers_df)


# whiteboard_sales_lead_item_id = _extract_podio_data(_get_podio_data_a(["'field_id': 217204715"],217204715, whiteboard_lead_items),'app_item_id')
# whiteboard_offer_item_id = _extract_podio_data(_get_podio_data_a(["'field_id': 217204716"],217204716, whiteboard_lead_items),'app_item_id')
# whiteboard_tax_id = _get_podio_data_a(["'field_id': 217204712"],217204712, whiteboard_lead_items)
# whiteboard_status = _extract_podio_data(_get_podio_data_a(["'field_id': 217204721"],217204721,whiteboard_lead_items), 'text')  
# whiteboard_transaction_status = _extract_podio_data(_get_podio_data_a(["'field_id': 217204723"],217204723,whiteboard_lead_items), 'text')  
# whiteboard_marketing_stage = _extract_podio_data(_get_podio_data_a(["'field_id': 217204725"],217204725,whiteboard_lead_items), 'text')  
# whiteboard_marketing_price = _get_podio_data_a(["'field_id': 217204726"],217204726, whiteboard_lead_items)
# # STILL TO WORK ON UN-NESTING THE WEB LINK LIST 
# # whiteboard_web_link = _extract_podio_data(_get_podio_data_a(["'field_id': 217204727"],217204727, whiteboard_lead_items),'resolved_url')
# whiteboard_showing_date  = _date_grabber(["field_id': 217204728"],217204728,whiteboard_lead_items)   
# whiteboard_closing_date  = _date_grabber(["field_id': 217204740"],217204740,whiteboard_lead_items)   
# whiteboard_assignment_stage = _extract_podio_data(_get_podio_data_a(["'field_id': 217204730"],217204730,whiteboard_lead_items), 'text')  
# whiteboard_assignee_name = _get_podio_data_a(["'field_id': 217204732"],217204732, whiteboard_lead_items)
# # these IDs are from multiple apps currently -- should I pull app_ID with it? 
# whiteboard_assignee_id = _extract_podio_data(_get_podio_data_a(["'field_id': 217204731"],217204731, whiteboard_lead_items),'app_item_id')
# whiteboard_buyer_emd = _get_podio_data_a(["'field_id': 217204735"],217204735, whiteboard_lead_items)
# whiteboard_closing_location = _get_podio_data_a(["'field_id': 217204742"],217204742, whiteboard_lead_items)
# # these IDs are from multiple apps currently -- should I pull app_ID with it? 
# whiteboard_title_company_id = _extract_podio_data(_get_podio_data_a(["'field_id': 217204741"],217204741, whiteboard_lead_items),'app_item_id')
# whiteboard_agreement_sent_to_title = _extract_podio_data(_get_podio_data_a(["'field_id': 217204744"],217204744, whiteboard_lead_items),'text')


# whiteboard_df = pd.DataFrame({
#                             'whiteboard_sales_lead_item_id': whiteboard_sales_lead_item_id, 
#                             'whiteboard_offer_item_id': whiteboard_offer_item_id, 
#                             'whiteboard_tax_id': whiteboard_tax_id, 
#                             'whiteboard_status': whiteboard_status, 
#                             'whiteboard_transaction_status': whiteboard_transaction_status, 
#                             'whiteboard_marketing_stage' : whiteboard_marketing_stage, 
#                             'whiteboard_marketing_price' : whiteboard_marketing_price, 
#                             'whiteboard_showing_date': whiteboard_showing_date, 
#                             'whiteboard_closing_date': whiteboard_closing_date, 
#                             'whiteboard_assignment_stage': whiteboard_assignment_stage, 
#                             'whiteboard_assignee_name': whiteboard_assignee_name, 
#                             'whiteboard_assignee_id': whiteboard_assignee_id, 
#                             'whiteboard_buyer_emd' : whiteboard_buyer_emd, 
#                             'whiteboard_closing_location': whiteboard_closing_location, 
#                             'whiteboard_title_company_id': whiteboard_title_company_id, 
#                             'whiteboard_agreement_sent_to_title' : whiteboard_agreement_sent_to_title
#                             })

# print(whiteboard_df) 


# TEMP HOLDER CODE TO LOAD DATA TO POSTGRES SQL DB 
# engine = create_engine('postgresql://postgres:B*oker123@localhost:5432/podio_test')
# sales_leads_df.to_sql("sales_leads_fact", engine)
# offers_df.to_sql("offers_fact", engine)
# quit() 


file_destination_path = 'C:\\Users\\Cameron\Documents\\Python'

# file_source_path = 'C:\\Users\\kacollins\\Downloads'
# file_destination_path = 'C:\\Users\\kacollins\Downloads'

# sales_leads_df.to_csv(file_destination_path + '\podio_sales_leads.csv', index = False)
# offers_df.to_csv(file_destination_path + '\podio_offers.csv', index = False)
# whiteboard_df.to_csv(file_destination_path + '\podio_whiteboard.csv', index = False)


spreadsheet = {
    'properties': {
        'title': title
    }
}
spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                    fields='spreadsheetId').execute()
print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))


# ## UPDATING CODE TO WRITE DFs to GOOGLE SHEETS AUTOMATICALLY 
# gc = pygsheets.authorize(service_file= file_destination_path + '\\cred.json')
# sh = gc.open("Test Podio Sheet")
# wks = sh[0]

# wks.set_dataframe(sales_leads_df,(1,1))



quit() 




# sales_lead_df = pd.DataFrame({ 'sales_lead_item_id' : app_item_id_dict['sales_leads'], 
#                                'sales_lead_create_dt' : item_created_on_dict['sales_leads'], 
#                                'sales_lead_last_event_dt': item_last_event_on_dict['sales_leads'], 
#                             })

# offers_df = pd.DataFrame({ 'offer_item_id' : app_item_id_dict['offers'], 
#                            'offer_create_dt' : item_created_on_dict['offers'], 
#                            'offer_last_event_dt': item_last_event_on_dict['offers'], 
#                             })

# whiteboard_df = pd.DataFrame({ 'whiteboard_item_id' : app_item_id_dict['whiteboard'], 
#                                'whiteboard_create_dt' : item_created_on_dict['whiteboard'], 
#                                'whiteboard_last_event_dt': item_last_event_on_dict['whiteboard'], 
#                                })      

# appointments_df = pd.DataFrame({ 'appointment_item_id' : app_item_id_dict['appointments'], 
#                                  'appointment_create_dt' : item_created_on_dict['appointments'], 
#                                  'appointment_last_event_dt': item_last_event_on_dict['appointments'], 
#                                })      

# print(appointments_df)         
