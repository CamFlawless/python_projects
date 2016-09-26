


# 8-Ball Attempt two

import random 
import time 
import sys


def _main_():

	raw_input("Enter your question:	")

	print """Let me check....>

	"""
	time.sleep(0.5)


	e_ball = [
		"Oh, yeah!", 
		"Sorry, kid", 
		"Better believe it", 
		"Not in this lifetime", 
		"I'm afraid not", 
		"Not today", 
		"For sure!"
	]
	response = random.choice(e_ball)
	print response
	time.sleep(0.5)

	decide()
	


def decide():
	ans = raw_input("Would you like to ask another question?  ad>	")
	ans_l = ans.lower()

	if ans_l == "yes" or ans_l =="y":
		_main_()
	elif ans_l == "no" or ans_l == "n":
		print "Shutting Down..."
		time.sleep(2)
		print "Goodbye!"
		time.sleep(0.75)
		exit 
		quit()
	else:
		print "Please enter a valid response - Yes(Y) / No(N)	"
		decide()


	
_main_()
print(sys.version)









