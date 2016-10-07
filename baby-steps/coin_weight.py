
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
   
   #~Think of how I could add all of the user's coin data into a single nested 
   #~similar to what I have done with the coins dict(s) 
'''


def _main_():
    user_units = _unit_choice()
    _user_input(user_units) 
  

def _user_input(units):
    
    # handling the unit preference chosen by the user 
    unit_sys = ''
    if units == 1:
        unit_sys = "grams"
    elif units == 2:
        unit_sys = "pounds" 
    
    # Nested dicts for our coin information     
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

    user_coins = {}
    user_coins['weights'] = {}
    user_coins['counts'] = {} 
    user_coins['wrappers'] = {}
    user_coins['values'] = {} 
        
    for i in coins['weights']:
        while True:
            try:
                user_coins['weights'][i] = float(input('Please enter the '
                'weight of your {0} in {1}  > '.format(i, unit_sys)))
                break 
            except ValueError or NameError:
                print("That doesn't look like a valid number. Please retry.")
                pass
                
    if units == 2:
        for i in user_coins['weights']:
            user_coins['weights'][i] = user_coins['weights'][i] * 453.592
    
    for i in coins['weights']:
        user_coins['counts'][i] = user_coins['weights'][i] // coins['weights'][i]
    
    for i in coins['wrappers']:
        user_coins['wrappers'][i] = user_coins['counts'][i] // coins['wrappers'][i] 
    
    for i in coins['values']:
        user_coins['values'][i] = user_coins['counts'][i] * coins['values'][i]
            
    total_coin_count = sum(user_coins['counts'].values())
    total_coin_value = sum(user_coins['values'].values())
    total_wrapper_count = sum(user_coins['wrappers'].values())
    
    print('\nIt looks like you have a total of {0} coins, made up of: '.format(
    str(int(total_coin_count))))
    
    for i in user_coins['counts']:
        print('\t' + str(int(user_coins['counts'][i])) + ' ' + i + ' totaling $'
        + str(round(user_coins['values'][i],2)))
    print('\t' + str(int(total_coin_count)) + ' coins in all totaling $' + 
    str(round(float(total_coin_value),2)))
    print('\n')
    
    print('To make your life easier, you should need {0} wrappers in total '
    'made up of:    '.format(str(int(total_wrapper_count))))
    
    for i in user_coins['wrappers']:
        print('\t' + str(int(user_coins['wrappers'][i])) + ' ' + i + ' wrappers.')
    print('\n\n')
    

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
