

import time 

def _main_():
    print ('''
    Welcome to the easy-menu genie. I was designed to make your life 
    as easy as possible. Simply enter the number that corresponds to each 
    menu item ordered by the customer and I will handle the rest. 
    
    For example, if a customer orders a salad and a small drink, simply 
    enter 89. 
    
    For your reference, the menu numbers are as follows"
        1: Chicken Strips
        2: French Fries
        3: Hamburger
        4: Hotdog
        5: Large Drink
        6: Medium Drink
        7: Milk Shake
        8: Salad
        9: Small Drink
    ''')

    _CustomerOrder_()
    
def _CustomerOrder_():
    menu_order = {
        1: 'Chicken Strips', 
        2: 'French Fries', 
        3: 'Hamburger', 
        4: 'Hotdog', 
        5: 'Large Drink', 
        6: 'Medium Drink', 
        7: 'Milk Shake', 
        8: 'Salad', 
        9: 'Small Drink'
        } 
        
    menu_prices = {
        'Chicken Strips': 3.50, 
        'French Fries': 2.50, 
        'Hamburger': 4.00, 
        'Hotdog': 3.50, 
        'Large Drink': 1.75, 
        'Medium Drink': 1.50,
        'Milk Shake': 2.75, 
        'Salad': 3.75, 
        'Small Drink': 1.25
        }
        
    customer_order = input("Enter the customer's order  >  ")
    
    try:
        int(customer_order)
    except ValueError:
        print ("Are you sure you entered a valid order number? Please " + 
            "enter the order number(s) again") 
        _RedoOrder_()
        
    order_prices = []
    order_items = []
    
    for x in customer_order:
        order_prices.append(menu_prices[menu_order[int(x)]])
        order_items.append(menu_order[int(x)])
        
    for x in menu_prices:
        item_count = order_items.count(x)
        if item_count > 0:
            print ('Item: %s | Quantity: %s | Price: %s | Extended Price: %s'
            % (x,str(item_count), str(menu_prices[x]), str(menu_prices[x] * item_count)))
        
    order_status = False
    while order_status != True:
        order_status = _SanityCheck_()
    
    pretax_total = sum(order_prices)
    tax_amount = sum(order_prices) * 0.07 
    order_total = pretax_total + tax_amount 
    
    print (" Order Subtotal: $%s \n Sales Tax: $%s \n Order Total: $%s"
    % (pretax_total, tax_amount, order_total))
        
    _Again_()
        
        
def _SanityCheck_():
    response = input("Does the order above match your customer's " +
    "request? (y/n) >  ")
    response = response.lower().strip()
    if response != 'y' and response != 'n':
        print ("Please enter a valid response - y for yes or n for no")
        _SanityCheck_()
    elif response == 'y':
        return True
    elif response == 'n':
        new_order = _RedoOrder_()
        return new_order 
    
def _RedoOrder_():
    customer_order = input("Please re-enter the customer's order number(s)  >  ")
    try:
        int(customer_order)
    except ValueError:
        print ("Are you sure you entered a valid order number?")
        _RedoOrder_()
    return customer_order 
        
def _Again_():
    response = input("Would you like to begin another order (y/n)   >  ")
    response = response.lower().strip()
    if response != 'y' and response != 'n':
        print ("Please enter a valid response - y for yes or n for no")
        _Again_()
    elif response == 'y':
        _CustomerOrder_()
    elif response == 'n':
        print ("Thanks for letting me help you today.")
        print ("Shutting Down...") 
        time.sleep(0.15)
        exit 
    


_main_()
