import time 

"""
BASIC GOAL 
	Imagine that your friend is a cashier, but has a hard time counting back change to customers. 
	Create a program that allows him to input a certain amount of change, and then print how how many quarters, 
	dimes, nickels, and pennies are needed to make up the amount needed.For example, if he inputs 1.47, the 
	program will tell that he needs 5 quarters, 2 dimes, 0 nickels, and 2 pennies.
SUBGOALS
	So your friend doesn't have to calculate how much change is needed, allow him to type in the amount 
	of money given to him and the price of the item. The program should then tell him the amount of each 
	coin he needs like usual. To make the program even easier to use, loop the program back to the top 
	so your friend can continue to use the program without having to close and open it every time he needs
	to count change.
"""


def _main_():

	print ("Hell0_Fr1end. Let's ring up some customers!")

	# our coins; possible change items
	quarter = 25
	dime = 10
	nickel = 5
	penny = 1
	
	
	response = ""
	i = 0 
	while response != "exit":
		i = i + 1 
		if i == 1:
			item_price = int(float(input("Enter the item's price:	")) * 100)
			customers_order = []
			customers_order.append(item_price) 
		elif i > 1:
			response = input("Enter the items's price (enter 'exit' to total and complete order)	:")
			if response == "exit":
					break
			else:
				item_price = int(float(response)*100)
				customers_order.append(item_price) 
		
	
	order_total = float(sum(customers_order) * 1.07)							
	print ("Customer's order total is: $" + str(format(order_total/100,'.2f')))
	
		
	# allow the user to enter the price; force them to be ints for ease sake 	
	money_in = float(input("Amount of money recieved from customer:	")) * 100	
	change = money_in - order_total 
	
	# would like to add the functionality to ensure money received is > money owed 
	# need help in figuring out the logic for reiterating when we have an error 

	# Determing coin makeup for our change 
	nbr_q = int(change // quarter)  			# number of quarters to return (thx floor division!)
	remaining_q = change - nbr_q*quarter 		# compute non-quarter change remaining 
	nbr_d = int(remaining_q // dime)			# floor division on remaining change to determine dime count 
	remaining_d = remaining_q - nbr_d*dime 		# change remaining once dimes are used 
	nbr_n = int(remaining_d // nickel) 			# floor division to determine nickel count 
	remaining_n = remaining_d - nbr_n*nickel 	# change remaining (pennies)
	nbr_p = int(remaining_n // penny)			# number of pennies needed 

	# Print the results out to the user 
	print ("Looks like you owe the customer $%s. Easiest change would be: %s quarters,  %s dimes, %s nickels, and %s pennies." % (format(float(change)/100,'.2f'),nbr_q,nbr_d,nbr_n,nbr_p))

	# Call on the _Again_() function; allow the user to loop and start a new order or quit 
	_Again_()


def _Again_():
	decision = input("Would you like to begin another order (y/n):  ")
	decision = decision.strip()
	if decision == "y":
		_main_()
	elif decision == "n":
		print ("Thanks for allowing me to help you today")
		time.sleep(2.5)
	else:
		print ("Please enter a valid response - y for yes or n for no:")
		_Again_()
		exit 
	
 

_main_()
