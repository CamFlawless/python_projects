
# Determine how to parse the doc
# How are the elements labeled within the HTML? 
# Once determined, write functions to go and retrieve each data point 
# Write out to CSV (will surely have to do more clean up here) 

# END OUTPUTS:
# - Meal Parts
# - Entries -- items eaten/consumer 
# - Macros -- Carbs, Fat, Protein 
# - Other Nutrients -- Calories, Sodium, Sugar 


from bs4 import BeautifulSoup 
import urllib.request 
import itertools 
from time import * 
import sys 
import datetime 
import csv 

date = strftime('%Y-%m-%d', localtime())

# the URL we want to scrape 
my_url = 'http://www.myfitnesspal.com/food/diary/camflawless?date=' + date
print('Data retrieved from ' + my_url)

s = urllib.request.urlopen(my_url)

soup = BeautifulSoup(s,'html.parser')

# Results set to be used; scraped HTML tags with relevant information 
tables = soup.findAll('table')
entries = soup.findAll('td', {'class' : 'first alt'})
nutrients = soup.findAll('td', {'class' : 'alt nutrient-column'})
macroValues = soup.findAll('span', {'class' : 'macro-value'})
macroPercent = soup.findAll('span', {'class' : 'macro-percentage'})
other_nuts = soup.findAll('td')


other_nutrients = []
for element in other_nuts:
    try:
	    other_nutrients.append(int(element.string))
    except TypeError:
	    pass 
    except ValueError:
	    pass

other_nutrients_list = [tuple(other_nutrients[i:i+3]) for i in 
					 range(0,len(other_nutrients),3)]

# include both the meal_part headers and food entries 
diary_entries = []
for element in entries:
    if 'href' not in str(element):
	    diary_entries.append(element.string.strip())
		
# includes only the meal part headers 
meal_parts = [] 
for element in entries:
    if 'href' not in str(element) and len(element.string.split()) == 1:
        meal_parts.append(element.string)

counter = 0 
food = []    
for element in entries:
    if 'href' not in str(element) and len(element.string.strip()) > 1:
        counter = counter + 1 
        food.append(str(counter))
        food.append(element.string.strip())
 
for i in range(0,len(food)):
    food[i] = str(food[i]).replace(',','')
    
food = [tuple(food[i:i+2]) for i in range(0,len(food),2)]
    
# includes the macro values in a single list 		
macro_values = []
for element in macroValues:
    try:
	    macro_values.append(int(element.string.strip()))
    except ValueError:
	    macro_values.append(0)
	
macro_percentages = []
for element in macroPercent:
    try:
	    macro_percentages.append(int(element.string.strip()))
    except ValueError:
	    macro_percentages.append(0)

# creating a list of tuples for the macro values/percents 
# since we know they are always reported in the same order: C, F, P
# can then extract each tuple and connect it to the correspnding entry 		
macro_value_list = [tuple(macro_values[i:i+3]) for i in range(0,len(macro_values),3)]
macro_percent_list = [tuple(macro_percentages[i:i+3]) for i in 
					  range(0,len(macro_percentages),3)]

macros = ['Carbs', 'Fat', 'Protein']		
macros_remaining = macro_values[len(macro_values)- 3:len(macro_values)]	
for i in range(0, len(macros_remaining)):
    macros_remaining[i] = macros[i] + ' - ' + str(macros_remaining[i]) + 'g'

del macro_value_list[len(macro_value_list)-1]

print(other_nutrients_list)
for element in other_nutrients_list:
    print( str([''.join(str(s)) for s in element]))
	

    # SOURCE: 
# http://stackoverflow.com/questions/15266593/how-to-group-list-items-into-tuple
# Converting the macro data into a list of tuples, where each tuple provides 
# the values for (Cabrs, Fat, Protein) 

count = 0 
macro_file_write = 'macros_' + date + '.csv'
with open(macro_file_write,'w') as file:
    for element in macro_value_list:
        count = count + 1 
        if count == 1:
            file.write(str(count-1) + ',Carbs, Fat, Protein  \n')
        else:
            file.write(str(count-1) + ',' + ''.join(str(s) + ',' for s in element) + '\n')

count = 0 
food_entries_write = 'food_entries_' + date + '.csv'
with open(food_entries_write,'w') as file:
    for element in food:
        count = count + 1
        if count == 1:
            file.write('Item ID,Item Name \n')
        else:
            file.write(''.join(str(s) + ',' for s in element) + '\n')
            
count = 0 
other_nutrients_write = 'other_nuts_' + date + '.csv'
with open(other_nutrients_write,'w') as file:
    for element in other_nutrients_list:
        count = count + 1
        if count == 1:
            file.write('Counter, Calories,Sodium,Sugar \n')
        else:
            file.write(str(count) + ',' +''.join(str(s) + ',' for s in element)  + '\n')
            
