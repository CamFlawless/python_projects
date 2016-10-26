
# Determine how to parse the doc
# How are the elements labeled within the HTML? 
# Once determined, write functions to go and retrieve each data point 
# Write out to CSV (will surely have to do more clean up here) 


'''

Table is initiated with the <table class="table0 "> tags
Table contents are within the <tbody> and </tbody> tags 
Meal-parts are within <tr class="meal_header">
Item entries are within <td class="first alt"> 


'''


from bs4 import BeautifulSoup 
import urllib.request 
from time import * 
import sys 
import datetime 

date = strftime('%Y-%m-%d', localtime())

# the URL we want to scrape 
my_url = 'http://www.myfitnesspal.com/food/diary/camflawless?date=' + date
print('Data retrieved from ' + my_url)

s = urllib.request.urlopen(my_url)

soup = BeautifulSoup(s,'html.parser')

tables = soup.findAll('table')
entries = soup.findAll('td', {'class' : 'first alt'})
nutrients = soup.findAll('td', {'class' : 'alt nutrient-column'})
macroValues = soup.findAll('span', {'class' : 'macro-value'})
macroPercent = soup.findAll('span', {'class' : 'macro-percentage'})

# empty dict to store each meal_part in (bfast, lunch, dinner, snack)
diary_entries = []
for element in entries:
    if 'href' not in str(element):
	    diary_entries.append(element.string.strip())

meal_parts = [] 
for element in entries:
    if 'href' not in str(element) and len(element.string.split()) == 1:
        meal_parts.append(element.string)

food = [] 
counter= 0 
for element in entries:
    if 'href' not in str(element) and len(element.string.split()) > 1:
	    counter = counter + 1 
	    food.append(element.string.strip() + ' - ' +str(counter))

# for x in range(0,len(diary_entries)):
    # print(diary_entries[x])
	
macro_values = []
for element in macroValues:
    macro_values.append(int(element.string.strip()))
	
macro_percentages = []
for element in macroPercent:
    macro_percentages.append(int(element.string.strip()))

# PRINT DEBUGGING 	
# print(macro_values)
# print(macro_percentages)
# print(food)

''' NOTES:
	We know macro values and percentages are in sets of 3 (carbs,fat,protein)
	Use it to our advantage and leverage that logic 
'''

carbs = []
fat = []
protein = []

# determine how to have the list send each of its items to their category 
i = 0 
for x in range(0,len(macro_values)):
