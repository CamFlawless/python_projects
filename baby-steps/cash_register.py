

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
    # -- Includeqd as of 9/29/2016 
  # Change initial dialogue on user selected replay 
    # -- Included 9/27/2016
  # Add smack talk based on previous game result 
	# Perhaps store them in an array and select an element at random
	# Something like: smack_talk = smack_talk_array[randint(0,len(smack_talk_array))]
  # Add difficulty selection to first prompt (# of guesses given)
    # - Add in the ability for the user to change difficulty between games 
  # Keep a historical record of win/loss (think on how to store this data)
	# - Add increased functionality to provide w/l ratio (win %)
	# - Can I add in a high streak info (check for repeating 0/1)
  # Add in high score functionality - is this the fastest time during this session?

  
# bring in other modules 
import random	# for randint function
import time 	# for sleep function as well as time manipulations 

def _main_():
	print ( ''' 
	Welcome to the Higher/Lower Game!
	The game is simple: I will guess a random number between the value of 
	1 and 100. Your job is to figure out my guess. Each time you make a 
	guess, I will let you know if you should guess higher or lower (unless
	you're a genius and happen to guess the same!). 
	Good luck, fr1end. 
	''' )
	
	start_time = time.time()
	difficulty = _LevelSelection_() 

	# this is an empty array/list where I will host the game history 
	# retun a 0 if the user lost; 1 if the user wins
	game_history = []
	i = 0 
	status = True
	change_diff = False 
	
	while status != False:
		i = i + 1 
		higher_lower(i,difficulty)
		game_history.append(game_mode(difficulty))
		print (SmackTalk(game_history[len(game_history) - 1]))
		status = _Again_()
		if status != False:
			change_diff = _ChangeLevel_()
			if change_diff == True:
				difficulty = _LevelSelection_()
		
		
	# Exit interface; remind the player how many games they played and 
	# for how long. Would be nice to add the sessions W/L history here 	
	win_count = sum(game_history)
	end_time = time.time()
	time_played = str(format(end_time - start_time, '.2f'))
	print ("You played %s games of Higher/Lower in %s seconds and won %s of them" % (i,time_played,win_count))
	print ("Pleasure playing with you, fr1end.")
	time.sleep(0.25)
	print ("Shutting Down...")
	time.sleep(0.3)		
	exit 

def _LevelSelection_():	
	print ("Before we get started, please enter a difficulty value..")
	choice = input("Please enter 1 for easy, 2 for normal, or 3 for challenge mode   >  ")
	try:
		if int(choice) in (1,2,3):
			return int(choice)
	except ValueError:
		print ("Oops! I didn't get that, please enter a valid selection")
		_LevelSelection_()
	
def higher_lower(i,difficulty):
	if i == 1 and difficulty == 3:
		print ("It looks like someone is confident, let's see about that.")
		print ("Let's see if it's true what they say about beginner's luck.")
	elif i == 1 and difficulty != 3:
		print ("Let's see if it's true what they say about beginner's luck.")
	elif i > 1:
		print ("Let's try this again")

def game_mode(difficulty):
	
	# Add in remaining turn count to be printed with each user guess
	# A way to have a message on the user's last available turn?
	# Is there a way to re-do the turn on invalid number entry rather 
	# than restarting the entire game? 
	
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
			user_guess = input("What is your guess, friend?	>	")
			try:
				int(user_guess)
			except ValueError:
				print ("Oops! That's not a number - restarting the game.")
				user_guess = input("What is your guess, friend?  >	") 	
			user_guess = int(user_guess)
			guess_diff = user_guess - cpu_guess
			if user_guess > 100 or user_guess < 1:
				print  ("You wasted a guess; remember my guess is between 1 and 100")
			elif guess_diff < 0:
				print ("Your guess is a bit low. Try something higher")
			elif user_guess > 0:
				print ("Your guess is a bit high. Try something lower")
			else:
				break 
		else:
			break 

	end_time = time.time()
	time_played = str(format(end_time - start_time,'.2f')) # will this work?
	if user_guess == cpu_guess:
		print ("Congrats! It took you %s seconds to guess the right number of %s in only %s guesses" % (time_played,cpu_guess,i))
		time.sleep(0.3) 
		return 1 
	else:
		print ("You are not match against me, fr1end.")
		print ("The correct answer was....%s" % (cpu_guess))
		time.sleep(0.3)
		return 0 
		
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
	
def _ChangeLevel_():
	response = input("Would you like to change the difficulty? (y/n)	>   ")
	response = response.strip()
	if response != "y" and response != "n":
		print ("Please enter a valid reponse: y for yes or n for no")
	elif response == "y":
		return True
	elif response == "n":
		return False 

def SmackTalk(result):
	smack_w = [
		"Better luck next time, scrub",
		"2 EZ. GG n00b",
		"Don't quit your day job, kid"
		]
	smack_l = [
		"You got lucky is all...",
		"I'll get you next time, my man",
		"I will not let this bring me down"
		]
	if result == 0:
		return (random.choice(smack_w))
	elif result == 1:
		return (random.choice(smack_l))
	
_main_()
