# Goal
    # I'm sure you've used a magic 8 ball at one point in your life. You ask it a 
	# question, turn it right side up and it gives an answer by way of a floating 
	# die with responses written on it. You can create one in python. You must:
	# Allow the user to enter their question
	# Display an in progress message( i.e. "thinking")
	# Create 20 responses, and show a random response
	# Allow the user to ask another question or quit
# Bonus 
    # Using whatever module you like, add a gui. Your gui must have:
		# A box for users to enter the question
		# At least 4 buttons: Ask , clear(the text box), play again and 
		# quit(this must close the window)



import time 
import random 

e_ball = [
	"Yes", 
	"No", 
	"Hard to say", 
	"Not in this lifetime", 
	"Definitely", 
	"Not likely, kid",
	"I'd bet not"
	] 
	


def _main_():
	user_q = input("Please enter your quesiton, fr1end	>  ")
	print ("Thinking...")
	time.sleep(2.0) 
	
	print (e_ball[random.randint(0,len(e_ball))])
	time.sleep(2.5)
	restart()
	
def restart():
	response = input("Would you like to ask another question? (y/n)	")
	response = response.lower().strip()
	
	if response == "y":
		_main_()
	elif response == "n":
		print ("Sorry to see you go. Shutting Down...")
		time.sleep(0.7)
		print ("Goodbye!")
		time.sleep(1.0)
		exit 
	else:
		print ("Please enter a valid repsonse - y for yes or n for no")
		restart()
		
		
_main_() 
