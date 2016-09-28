

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

### Modifications and/or Extensions 
  # Enforce strict type on user submitted guesses
  # Change initial dialogue on user selected replay 
    # -- Included 9/27/2016
  # Add smack talk based on previous game result 
	# Perhaps store them in an array and select an element at random
	# Something like: smack_talk = smack_talk_array[randint(0,len(smack_talk_array))]
  # Add difficulty selection to first prompt (# of guesses given)
    # - Add in the ability for the user to change difficulty between games 
  # Keep a historical record of win/loss (think on how to store this data)
  # Add in high score functionality - is this the fastest time during this session?

  
# bring in other modules 
import random	# for randint function
import time 	# for sleep function 

def _main_():
	start_time = time.time()
	difficulty = _LevelSelection_() 
	i = 0 
	status = True
	
	while status != False:
		i = i + 1 
		if i == 1:
			print ( ''' 
			
			Welcome to the Higher/Lower Game!
			The game is simple: I will guess a random number between the value of 
			1 and 100. Your job is to figure out my guess. Each time you make a 
			guess, I will let you know if you should guess higher or lower (unless
			you're a genius and happen to guess the same!). 
			Good luck, fr1end. 
			
			''' )
			
		higher_lower(i,difficulty)
		status = _Again_()

	# Exit interface; remind the player how many games they played and 
	# for how long. Would be nice to add the sessions W/L history here 	
	end_time = time.time()
	time_played = str(format(end_time - start_time, '.2f'))
	print ("You played %s game of Higher/Lower for a total of %s seconds" % (i,time_played))
	print ("Pleasure playing with you, fr1end.")
	time.sleep(0.25)
	print ("Shutting Down...")
	time.sleep(0.3)		
	exit 

def higher_lower(i,difficulty):
	if i == 1:
		print ("Let's see if it's true what they say about beginner's luck.")
		game_mode(difficulty)
	elif i > 1:
		print ("Let's try this again")
		game_mode(difficulty)

def game_mode(difficulty):
	
	turn_count = 0 
	
	turn_count_list = [0,20,10,5]
	turn_count = turn_count_list[difficulty]
		
	cpu_guess = random.randint(1,100)
	user_guess = 0
	i = 0
	start_time = time.time()
	
	while i < turn_count + 1 or user_guess != cpu_guess:
		i = i + 1
		if i <= turn_count:
			user_guess = int(input("What is your guess, friend?	>	"))
			guess_diff = user_guess - cpu_guess
			if guess_diff > 0:
				print ("Your guess is a bit high. Try something lower")
			elif guess_diff < 0:
				print ("Your guess is a bit low. Try something higher")
			else:
				break 
		else:
			break 

	end_time = time.time()
	time_played = str(format(end_time - start_time,'.2f')) # will this work?
	if user_guess == cpu_guess:
		print ("Congrats! It took you %s seconds to guess the right number of %s in only %s guesses" % (time_played,cpu_guess,i))
		time.sleep(0.3) 
	else:
		print ("You are not match against me, fr1end.")
		time.sleep(0.3)
		
def _Again_():
	user_status = ""
	response = input("Would you like to play again?	(y/n)	>	")
	response = response.strip()
	if response != "y" and response != "n":
		print ("Please enter a valid reponse: y for yes or n for no")
		_Again_()
	elif response == "y":
		user_status = True
	elif response == "n":
		print ("Hope you had fun, friend!")
		user_status = False

	return user_status
	exit
	
def _LevelSelection_():	
	choice = input("Please enter a difficulty value: 1 for easy, 2 for normal, or 3 for challenge mode   >  ")
	try:
		if int(choice) in (1,2,3):
			return int(choice)
	except ValueError:
		print ("Oops! I didn't get that, please enter a valid selection")
		_LevelSelection_()
	
_main_()
