
'''
   #~When some people receive change after shopping, they put it into a 
   #~container and let it add up over time. Once they fill up the 
   #~container, they'll roll them up in coin wrappers which can then be 
   #~traded in at a bank for what they are worth. While most banks will 
   #~give away coin wrappers for free, it's convenient to have an idea of 
   #~how many you will need. Instead of counting how many coins you have, 
   #~it's easier to separate all of your coins, weigh them, and then 
   #~estimate how many of each type you have and then how many wrappers 
   #~you'll need.
   
   #~For example, if you weigh all of your dimes and see that you have 
   #~1276.9g of them, you can estimate that you have about 563 dimes 
   #~(since each one is 2.268g) and you would be able to fill 11 dime 
   #~wrappers.
   
#~Goal 
   #~Create a program that allows the user to input the total weight of 
   #~each type of coin they have (pennies, nickels, dimes, and quarters), 
   #~and then print out how many of each type of wrapper they would need,
   #~how many coins they have, and the estimated total value of all of 
   #~their money.
#~Subgoals
   #~Round all numbers printed out to the nearest whole number.
   #~Allow the user to select whether they want to submit the weight in 
   #~either grams or pounds.
   
#~Notes  
   #~Penny: weight = 2.500, count/wrapper = 50, value = 0.01
   #~Nickel: weight = 5.000, count/wrapper = 40, value = 0.05
   #~Dime: weight = 2.268, count/wrapper = 50, value = 0.10 
   #~Quarter: weight = 5.670, count/wrapper = 50, value = 0.25
   
   #~Since we are consistently dealing with 4 derivatives of coin, 
   #~it would be easier to store everything in lists and/or dicts 
   #~and call/print them from there; rather than assigning to own vars
   
   #~Determine how to handle the event when the user inputs an incorrect value 
   #~ for their coin weight(s) 
   
   
''' 

def _main_():
    user_units = _unit_choice()
    _user_input(user_units) 

def _user_input(units):
    unit_sys = ''
    if units == 1:
        unit_sys = "grams"
    elif units == 2:
        unit_sys = "pounds" 
        
    coins = {
        'weights': {
            'pennies': 2.500, 
            'nickels': 5.000, 
            'dimes': 2.268, 
            'quarters': 5.670
            }, 
        'wrappers': {
            'pennies': 50,
            'nickels': 40,
            'dimes': 50, 
            'quarters': 50  
            }, 
        'values': {
            'pennies': 0.01, 
            'nickels': 0.05, 
            'dimes': 0.10, 
            'quarters': 0.25
            }
            }

    for i in coins:
        for x in coins[i]:
            print (coins[i][x])
            
    user_coin_weights = {}
    for i in coins['values']:
        try:
            user_coin_weights[i] = float(input("Please enter the weight "
            "of your {0} in {1} > ".format(i,unit_sys)))
        except ValueError:
            print ("Uh-Oh")
            
    # convert user input pounds to grams if imperial chosen as units        
    if units == 2:
        for i in user_coin_weights:
            user_coin_weights[i] = user_coin_weights[i] * 453.592
            
    user_coin_counts = {}
    for i in coins['weights']:
        user_coin_counts[i] = user_coin_weights[i] // coins['weights'][i]
        
    user_wrapper_counts = {}
    for i in coins['wrappers']:
        user_wrapper_counts[i] = user_coin_counts[i] // coins['wrappers'][i]
    
    user_coin_value = {}
    for i in user_coin_counts:
        user_coin_value[i] = user_coin_counts[i] * coins['values'][i]
        
    total_value = 0 
    for i in user_coin_value:
        total_value = total_value + user_coin_value[i]
      
    # now that everything is computed, lets output the results to the user      
    print ('\n \n')     
    print ("It looks like you have a total of {0} coins, made up of: \n".format
    (str(int(sum(user_coin_counts.values())))))
    
    for i in user_coin_counts:
        print ('    '+ str(int(user_coin_counts[i])) + ' ' + i)
    print ('\n') 
    
    print ("To make your life easier, you should need:  \n")
    for i in user_wrapper_counts:
        print ('    '+ str(int(user_wrapper_counts[i])) + ' ' + i + ' wrappers.')
        
# need function to handle when user does not input a int as the weight 
def _redo_input():
    coins = ['pennies', 'nickels', 'dimes', 'quarters']
    
def _unit_choice():
    print ("What units of weight would you like to use?")
    unit_pref = input("Enter 1 for grams. Enter 2 for pounds  > ")
    try:
        unit_pref = int(unit_pref) 
        if unit_pref in (1,2):
            return unit_pref
        else:
            print ("Please enter a valid repsonse - 1 for grams or 2 for "
            "pounds.") 
            _unit_choice() 
    except ValueError:
        print ("That was not a valid response. Please try again")
        _unit_choice()

_main_()
