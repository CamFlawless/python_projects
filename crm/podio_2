
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


c = api.OAuthClient(client_id, client_secret, username, password)



def _get_podio_data(my_list, field):
    output_list = []
    for record in my_list:
        for part in record:
            if part == field:
                output_list.append(record[part])
    return(output_list)


apps_dict = {}
# APPEND LIST WITH ADDITIONAL APP NAME AND IDs
my_apps =      [ ["sales_leads", 25523237], 
                 ["offers", 25523238], 
                 ["whiteboard", 25523241], 
                 ["appointments", 25523247] 
               ]

for app in my_apps:
    apps_dict[app[0]] = c.Application.get_items(app[1])['items']

# print(apps_dict)
# quit() 
# CREATING EMPTY DICTS TO BE APPENDED 
''' 
    NOTES: CREATED BY IS A MORE DEEPLY NESTED LIST IN THE OBJECT
    WILL NEED TO WRITE ADDITIONAL FOR LOOPS TO GO AND GRAB VALUE
'''



app_item_id_dict = {}
item_created_on_dict = {} 
item_created_by_dict = {}
item_last_event_on_dict = {} 
item_fields_dict = {} 

for key, value in apps_dict.items():
    app_item_id_dict[key] = _get_podio_data(value, "app_item_id")
    item_created_on_dict[key] = _get_podio_data(value, "created_on")
    created_by_list = []
    for item in  _get_podio_data(value, "created_by"):
        created_by_list.append(item['name'])
    item_created_by_dict[key] = created_by_list
    item_last_event_on_dict[key] = _get_podio_data(value, "last_event_on")
    item_fields_dict[key] = _get_podio_data(value, "fields")

# print(item_fields_dict['sales_leads'][0])
# quit() 



''' Lets now programatically go through the app item records and get a list of all the fields 
    We will get the label/name, type, and field_id 
    We will zip them up and include in a nested dict for us to use further down the script
''' 
app_fields = {} 
for app in my_apps:
    field_labels = []
    field_types = [] 
    field_ids = [] 
    for record in item_fields_dict[app[0]]:
        for field in record:
            field_labels.append(field['label'])
            field_types.append(field['type'])
            field_ids.append(field['field_id'])
    # WE USE THE SET TO REMOVE DUPLICATES ENTRIES; ZIP TO COMBINE THE THREE INTO A TUPLED LIST 
    app_fields[app[0]] = list(set(zip(field_labels, field_types, field_ids)))

# print(app_fields)
# quit() 


dict1 = {} 
for field in app_fields['sales_leads']:
    dict1[field] = {} 
    search_str = ["'field_id': "  + str(field[2]) + ", 'label'"]
    record_values = [] 
    for record in item_fields_dict['sales_leads']:
        if any(word in str(record) for word in search_str):
            # print(record)
            for entry in record:
                # print(entry)
                # print(field[2])
                # quit() 
                if entry['field_id'] == field[2] and entry['type'] == "app":
                    # print(entry)
                    # quit()
                    ''' what do we want to do if the field we are on is the field we are searching for?
                        ** we would want to extract the corresponding value from the object ''' 
                    if entry['type'] == "date": # what to grab when we see a date
                        print(entry['values'][0]['start'])
                    if entry['type'] == "contact":
                        print(entry['values'][0]['value']['name'])
                    if entry['type'] == "category":
                        print(entry['values'][0]['value']['text'])
                    if entry['type'] == "app":
                        print(entry['values'][0]['value']['app_item_id'])
                        quit() 
                else:
                    pass



                #     if entry['type'] == "category":
                #         print(entry['values'][0]['value']['text'])
                #     elif entry['type'] == "text": 
                #         print(entry['values'][0]['value'])
                #     elif entry['type'] == "money": 
                #         print(entry['values'][0]['value'])
                #     elif entry['type'] == "contact": 
                #         print(entry['values'][0]['name'])
                #     elif entry['type'] == "app": 
                #         print(entry['values'][0]['app_item_id'])
                #     quit() 
                # else:
                #     pass
                # quit() 
                
print(record_values)
quit() 
        




''' 
WE HAVE ALL THE APPS --> my_apps[0]
SO NOW WE HAVE ALL RECORDS RETURNED --> item_field_dict[my_apps[0]]
WE HAVE ALL THE AVAILABLE FIELDS --> app_fields[my_apps[0]]

How can we loop through each field for each record in each app? 

my_data = {} 
for app in my_app:
    for record in app:
        for field in app_fields[app]:
            if str("'field_id': " + str(field[2]) + ", 'label'") in records:
                print(record)
                my_data[app][field[1]] = 
            find the field value (if it exist) --> append to list within dict if so, append empty string to dict if not
            if field[1] == "date" then:
                do this...
            if field[1] == "name" then:
                do this...
            if field[1] == "category" then:
                do this...
            if field[1] == "text then:
                do this...



## DICT OF ALL ITEMS RETURNED BY ALL APPS == apps_dict
print(apps_dict)
print('\n\n')
## LIST OF APPS == my_apps
print(my_apps)
print('\n\n')
## LIST OF RECORDS == item_fields_dict[my_apps[0]] (this is a dict keyed by app_name)
print(item_fields_dict['sales_leads'])
print('\n\n')
## LIST OF FIELDS == app_fields[my_apps[0]] (this is a dict keyed by app_name)
print(app_fields['sales_leads'])
print('\n\n')
'''
# quit() 



for app in my_apps:
    for item in item_fields_dict[app[0]]:
        print(type(item))
        print(item)
        quit()
    for item in item_fields_dict[app[0]][[1][0]]:
        print(item)
        quit() 
        # for field in app_fields[app[0]]:





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

app_data = {}
for app in my_apps: # app name == app[0] [sales_offer, offers, etc.]
    print(app[0])
    for item in item_fields_dict[app[0]]: # this is the record's fields detail 
        print(item) #$$ CONFIDENT THIS IS THE RECORD (i.e. RECORD)
        quit() 
        field_values = [] 
        for field in app_fields[app[0]]: # this is the field to query for 
            # print(field[2]) # CONFIDENT THIS IS THE FIELD_ID INT 
            # for record in item:
            quit() 

quit() 




# for app in my_apps:
#     for field in app_fields[app[0]]:
#         print(item_fields_dict['offers'])
#         print(field[2])
#         print(_podio_get_field_data_simple(item_fields_dict['offers'], field[2]))
#         quit() 
    

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


podio_data_master = {}
for app in my_apps:
    field_data = {}
    for field in app_fields[app[0]]:
        field_data[field[0]] = field[1]
        print(field)
        print(field_data)
        quit()


# if field type in (app, category, date, contact)

# print(app_fields)
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



def _make_podio_app_data_dict(simple_dict, key_to_use, nested_dict):
    return_dict = {}
    for field in simple_dict[key_to_use]:
        return_dict[field[0]] = _podio_get_field_data_simple(item_fields_dict[key_to_use], field[1])    
    for field in nested_dict[key_to_use]: 
        return_dict[field[0]] =  _get_nested_podio_data(_podio_get_field_data_simple(item_fields_dict[key_to_use], field[1]), field[2])
    return(return_dict)    


app_fields_data = {} 
for app in my_apps:
    app_fields_data[app[0]] = _make_podio_app_data_dict(fields_simple, app[0], fields_nested)



sales_lead_df = pd.DataFrame.from_dict(app_fields_data['sales_leads']).assign(sales_lead_item_id = app_item_id_dict['sales_leads'], 
                                                                              sales_lead_created_on = item_created_on_dict['sales_leads'], 
                                                                              sales_lead_last_event_on = item_last_event_on_dict['sales_leads'], 
                                                                              sales_lead_created_by = item_created_by_dict['sales_leads'] )

offers_df = pd.DataFrame.from_dict(app_fields_data['offers']).assign(offer_item_id = app_item_id_dict['offers'], 
                                                                     offer_created_on = item_created_on_dict['offers'], 
                                                                     offer_last_event_on = item_last_event_on_dict['offers'],
                                                                     offer_created_by = item_created_by_dict['offers'] )
 
whiteboard_df = pd.DataFrame.from_dict(app_fields_data['whiteboard']).assign(whiteboard_item_id = app_item_id_dict['whiteboard'], 
                                                                             whiteboard_created_on = item_created_on_dict['whiteboard'], 
                                                                             whiteboard_last_event_on = item_last_event_on_dict['whiteboard'], 
                                                                             whiteboard_created_by = item_created_by_dict['whiteboard'] )
 
appointment_df = pd.DataFrame.from_dict(app_fields_data['appointments']).assign(appointment_item_id = app_item_id_dict['appointments'], 
                                                                                appointment_created_on = item_created_on_dict['appointments'],
                                                                                appointment_last_event_on = item_last_event_on_dict['appointments'], 
                                                                                appointment_created_by = item_created_by_dict['appointments'] )
 
 
print(sales_lead_df)
print(offers_df)
print(whiteboard_df)
print(appointment_df)
quit() 



# TEMP HOLDER CODE TO LOAD DATA TO POSTGRES SQL DB 
engine = create_engine('postgresql://postgres:B*oker123@localhost:5432/podio_test')

sales_lead_df.to_sql("sales_leads_fact", engine, if_exists='replace')
offers_df.to_sql("offers_fact", engine, if_exists='replace')
whiteboard_df.to_sql("whiteboard_fact", engine, if_exists='replace')
appointment_df.to_sql("appointments_fact", engine, if_exists='replace')
quit() 



quit() 
