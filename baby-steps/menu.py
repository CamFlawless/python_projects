
# GOAL
  # Imagine you have started up a small restaurant and are trying to make it 
  # easier to take and calculate orders. Since your restaurant only sells 9 
  # different items, you assign each one to a number, as shown below.
	# Chicken Strips - $3.50
	# French Fries - $2.50
	# Hamburger - $4.00
	# Hotdog - $3.50
	# Large Drink - $1.75
	# Medium Drink - $1.50
	# Milk Shake - $2.25
	# Salad - $3.75
	# Small Drink - $1.25
  # To quickly take orders, your program should allow the user to type in a string 
  # of numbers and then it should calculate the cost of the order. For example, if 
  # one large drink, two small drinks, two hamburgers, one hotdog, and a salad are ordered,
  # the user should type in 5993348, and the program should say that it costs $19.50. Also, 
  # make sure that the program loops so the user can take multiple orders without having to 
  # restart the program each time.
# SUBGOALS
  # If you decide to, print out the items and prices every time before the user types in 
  # an order. Once the user has entered an order, print out how many of each item have been 
  # ordered, as well as the total price. If an item was not ordered at all, then it should not show up.
  
 


 
import time   


def _main_():
	print ('''
			Welcome to the easy-menu genie. I was designed to make your life
			as a waiter as easy as can be. Simply enter the numbers of the items
			ordered by the customer and I will do the rest. 
			
			For exmaple, if the customer orders a Salad and a Small Drink, simply 
			enter 89. 
			
			In case you're having trouble remembering the menu numbers, they are:
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

	# Let's make use of Python's built in dictionary data type 
	# I have to imagine that there is a way to combine these into a single var 
	# Learn how to do it and make it work!  
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
		'Chicken Strips' : 3.50,  
		'French Fries' : 2.50,  
		'Hamburger' : 4.00, 
		'Hotdog' : 3.50, 
		'Large Drink' : 1.75,
		'Medium Drink' : 1.50, 
		'Milk Shake' : 2.75,  
		'Salad' : 3.75, 
		'Small Drink' : 1.25
		}

	customer_order = input("Enter the customer's order number(s)	> ")
	try:
		int(customer_order)
	except ValueError:
		print ("Are you sure you entered numbers? Let's try that again!")
		_CustomerOrder_()
		
	order_prices =  []
	order_items = []
	for x in customer_order:
		order_prices.append(menu_prices[menu_order[int(x)]])
		order_items.append(menu_order[int(x)])
		
	for x in menu_prices:
		item_count = order_items.count(x)
		if item_count > 0:
			print ('Item: %s | Quantity: %s | Item Price: %s | Extended Price: %s' % (x,str(item_count), str(menu_prices[x]), str(menu_prices[x] * item_count)))
	
	# Should I create a new function to handle this logic?
	# Want to avoid iterating endlessly 
	# Would also help to add better conditional commentary/print statements 
	response = input(("Does the list above match the customer's order?	(y/n)	>  	"))
	if response != "n" and response  != "y":
		print ("Please enter a valid response - y for yes or n for no")
		response = input(("Does the list above match the customer's order?	(y/n)	>  	"))
	elif response == "n":
		_CustomerOrder_()	
	
	item_counts = []
	for x in order_items:
		item_counts.append(order_items.count(x))
			
	order_total = sum(order_prices)	
	print ("The customer's order total is $%s" % (order_total))
	
	_Again_() 
	
def _Again_():
	response = input("Would you like to begin another order? (y/n)	>	")
	if response != "y" and response != "n":
		print ("Please enter a valid response - y for yes or n for no")
		_Again_()
	if response == "y":
		_CustomerOrder_()
	elif response == "n":
		print ("I hope I was of value to you today")
		print ("Shutting Down...")
		time.sleep(0.5)
		exit 
				


		
_main_()