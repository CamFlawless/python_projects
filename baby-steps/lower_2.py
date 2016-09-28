




#BASIC GOAL 
	#Create a simple game where the computer randomly selects a number 
	#between 1 and 100 and the user has to guess what the number is. 
	#After every guess, the computer should tell the user if the guess is
	#higher or lower than the answer. When the user guesses the correct 
	#number, print out a congratulatory message.
#SUB GOALS
	#-Add an introduction message that explains to the user how to play 
	#your game.
	#-In addition to the congratulatory message at the end of the game, 
	#also print out how many guesses were taken before the user arrived 
	#at the correct answer.
	#-At the end of the game, allow the user to decide if they want to 
	#play again (without having to restart the program).




### Modifications
	# Change initial dialogue on user selected replay
	# Add smack talk based on previous game result 
	# Add difficulty selection to first prompt (# of guesses given) 
	# Keep a historical record of win/loss (think on how to store this data)

import random 
import time 

def _main_():
	
	i = 0 
	status = True
	
	while status <> False:
		i = i + 1 
		if i == 1:
			print ''' 
			
			Welcome to the Higher/Lower Game!
			
			The game is simple: I will guess a random number between the value of 
			1 and 100. Your job is to figure out my guess. Each time you make a 
			guess, I will let you know if you should guess higher or lower (unless
			you're a genius and happen to guess the same!). 
			
			Good luck, fr1end. '''  
			
		higher_lower(i)
		status = _Again_()
		
	print "Pleasure playing with you, fr1end,"
	time.sleep(0.25)
	print "Shutting Down..."
	time.sleep(0.3)		
	exit 

def higher_lower(i):
	if i == 1:
		print "Let's see if it's true what they say about beginner's luck."
		game_mode()
	elif i > 1:
		print "Let's try this again"
		game_mode()

def game_mode():
	cpu_guess = random.randint(1,1)
	user_guess = 0
	i = 0 

	while user_guess <> cpu_guess:
		user_guess = int(raw_input("What is your guess, friend?	>	"))
		i = i + 1 
		guess_diff = user_guess - cpu_guess 
		if guess_diff > 0:
			print "Your guess is a bit high. Try something lower"
		elif guess_diff < 0:
			print "Your guess is a bit low. Try something higher"
		
	print "Congrats! You guessed the right number of %s in only %s guesses" % (cpu_guess,i)
	
def _Again_():
	response = raw_input("Would you like to play again?	(y/n)	>	")
	response = response.strip()
	if response != "y" and response != "n":
		print "Please enter a valid reponse: y for yes or n for no"
		_Again_()
	elif response == "y":
		status = True
	elif response == "n":
		print "Hope you had fun, friend!"
		status = False

	return status
	exit
	
	
_main_()
