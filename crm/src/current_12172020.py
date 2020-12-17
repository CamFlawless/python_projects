
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
import psycopg2


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


app_items = {}
# APPEND LIST WITH ADDITIONAL APP NAME AND IDs
apps_to_grab = [ ["sales_leads", 25523237], 
                 ["offers", 25523238], 
                 ["whiteboard", 25523241], 
                 ["appointments", 25523247], 
                 ["campaigns", 25523249 ], 
                 ["contacts", 25523245]
               ]

# for item in apps_to_grab:
#    apps_dict[item[0]] = c.Application.get_items(item[1])['items']

## ADJUSTED CODE TO ALLOW UP TO 500 ITEMS TO BE RETURNED IN A SINGLE REQUEST 
for app in apps_to_grab:
    app_items[app[0]] = c.Item.filter(app_id = app[1], attributes = {"limit":500})['items']
    print(str(c.Item.filter(app_id = app[1], attributes = {"limit":500})['total']) + " items in " + str(app[0]) + " application")

# items = c.Item.filter(app_id=25523237, attributes={"limit": 100})
   
# print(app_items['campaigns'])
# quit() 


# CREATING EMPTY DICTS TO BE APPENDED 
''' 
    NOTES: CREATED BY IS A MORE DEEPLY NESTED LIST IN THE OBJECT
    WILL NEED TO WRITE ADDITIONAL FOR LOOPS TO GO AND GRAB VALUE
'''
app_item_id_dict = {}
item_created_on_dict = {} 
item_last_event_on_dict = {} 
item_fields_dict = {} 

for key, value in app_items.items():
    app_item_id_dict[key] = _get_podio_data(value, "app_item_id")
    item_created_on_dict[key] = _get_podio_data(value, "created_on")
    item_last_event_on_dict[key] = _get_podio_data(value, "last_event_on")
    item_fields_dict[key] = _get_podio_data(value, "fields")

# print(app_item_id_dict['sales_leads'])
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
                                  ], 
                 'campaigns'    : [ ["campaign_title", 217204815], 
                                    ["campaign_start", 217204816], 
                                    ["tracking_number", 217204817], 
                                    ["total_leads", 217204819], 
                                    ["cost_per_lead", 217204820]
                                  ], 
                 'contacts'     : [ ["contact_name", 217204777], 
                                    ["contact_phone", 217204778], 
                                    ["conact_address", 217204782], 
                                    ["contact_email", 217204779], 
                                    ["contact_hourly_rate", 217204780]
                                  ]
                }


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
                  'offers':        [ ["offer_sales_lead_item_id", 217204662, 'app_item_id'],
                                     ["offer_title_company_id", 217204690, 'app_item_id']
                                   ], 
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
                                   ], 
                  'campaigns'    :   [], 
                  'contacts'     : [ ["contact_type", 217204783, 'text'], 
                                     ["contact_status", 217204784, 'text']
                                   ]
                                   
                }



def _make_podio_app_data_dict(simple_dict, key_to_use, nested_dict):
    return_dict = {}
    for field in simple_dict[key_to_use]:
        return_dict[field[0]] = _podio_get_field_data_simple(item_fields_dict[key_to_use], field[1])    
    for field in nested_dict[key_to_use]: 
        return_dict[field[0]] =  _get_nested_podio_data(_podio_get_field_data_simple(item_fields_dict[key_to_use], field[1]), field[2])
    return(return_dict)    


app_fields_data = {} 
for app in apps_to_grab:
    app_fields_data[app[0]] = _make_podio_app_data_dict(fields_simple, app[0], fields_nested)


sales_lead_df = pd.DataFrame.from_dict(app_fields_data['sales_leads']).assign(sales_lead_item_id = app_item_id_dict['sales_leads'], 
                                                                              sales_lead_created_on = item_created_on_dict['sales_leads'], 
                                                                              sales_lead_last_event_on = item_last_event_on_dict['sales_leads'] )

offers_df = pd.DataFrame.from_dict(app_fields_data['offers']).assign(offer_item_id = app_item_id_dict['offers'], 
                                                                     offer_created_on = item_created_on_dict['offers'], 
                                                                     offer_last_event_on = item_last_event_on_dict['offers'] )
 
whiteboard_df = pd.DataFrame.from_dict(app_fields_data['whiteboard']).assign(whiteboard_item_id = app_item_id_dict['whiteboard'], 
                                                                             whiteboard_created_on = item_created_on_dict['whiteboard'], 
                                                                             whiteboard_last_event_on = item_last_event_on_dict['whiteboard'] )
 
appointment_df = pd.DataFrame.from_dict(app_fields_data['appointments']).assign(appointment_item_id = app_item_id_dict['appointments'], 
                                                                                appointment_created_on = item_created_on_dict['appointments'],
                                                                                appointment_last_event_on = item_last_event_on_dict['appointments'] )

campaign_df = pd.DataFrame.from_dict(app_fields_data['campaigns']).assign(campaign_item_id = app_item_id_dict['campaigns'], 
                                                                          campaign_created_on = item_created_on_dict['campaigns'],
                                                                          campaign_last_event_on = item_last_event_on_dict['campaigns'] )

contact_df = pd.DataFrame.from_dict(app_fields_data['contacts']).assign(contact_item_id = app_item_id_dict['contacts'], 
                                                                        contact_created_on = item_created_on_dict['contacts'],
                                                                        contact_last_event_on = item_last_event_on_dict['contacts'] )

# print(contact_df)
# quit() 


file_source_path = 'C:\\Users\\Cameron\\Documents\\Python'
file_destination_path = 'C:\\Users\\Cameron\\Documents\\Python'

''' UNCOMMENT TO WRITE DFs to CSVs '''
# sales_lead_df.to_csv(file_destination_path + '\podio_sales_leads.csv', index = False)
# offers_df.to_csv(file_destination_path + '\podio_offers.csv', index = False)
# whiteboard_df.to_csv(file_destination_path + '\podio_whiteboard.csv', index = False)
# appointment_df.to_csv(file_destination_path + '\podio_appointments.csv', index = False)
# campaign_df.to_csv(file_destination_path + '\podio_campaigns.csv', index = False)

 
print(sales_lead_df)
print(offers_df)
print(whiteboard_df)
print(appointment_df)
quit() 



# TEMP HOLDER CODE TO LOAD DATA TO POSTGRES SQL DB 
engine = create_engine('postgresql://postgres:B*oker123@localhost:5432/podio_test')

aws_engine = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="Padthai123",
    host="myfirstpostgresdb.cphlebz1grwu.us-east-2.rds.amazonaws.com",
    port='5432'
)

sales_lead_df.to_sql("sales_leads_fact", engine, if_exists='replace')
offers_df.to_sql("offers_fact", engine, if_exists='replace')
whiteboard_df.to_sql("whiteboard_fact", engine, if_exists='replace')
appointment_df.to_sql("appointments_fact", engine, if_exists='replace')
campaign_df.to_sql("campaigns_fact", engine, if_exists='replace')
contact_df.to_sql("contact_fact", engine, if_exists='replace')

quit() 


