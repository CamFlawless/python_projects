
# Build out a means of storing this data into a DB and preserving it for archival and analysis 

client_id = "insert client id"
client_secret = "insert client secret"
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
x = 0 
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

