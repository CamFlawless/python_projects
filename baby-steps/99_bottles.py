


#~ GOAL
#~   Create a program that prints out every line to the song "99 bottles 
#~ of beer on the wall." This should be a pretty simple program, so to 
#~ make it a bit harder, here are some rules to follow.
#~ RULES
#~  ** If you are going to use a list for all of the numbers, do not 
#~ manually type them all in. Instead, use a built in function.
#~  ** Besides the phrase "take one down," you may not type in any 
#~ numbers/names of numbers directly into your song lyrics.
#~  ** Remember, when you reach 1 bottle left, the word "bottles" becomes 
#~ singular.
#~  ** Put a blank line between each verse of the song.



'''
99 bottles of beer on the wall, 99 bottles of beer.
Take one down and pass it around, 98 bottles of beer on the wall.
'''

x = 100

lyrics_a = 'bottles of beer on the wall,'
lyrics_b = 'bottles of beer.'
lyrics_c = 'Take one down and pass it around,'
lyrics_d = 'bottles of beer on the wall.\n'

while x >= 0:
	x = x - 1
	if x > 2:
		print ("%s %s %s %s"  % (str(x), lyrics_a, str(x), lyrics_b))
		print ("%s %s %s" % (lyrics_c, str(x-1), lyrics_d))
		print (x)
	if x == 2:
		print ("%s %s %s %s" % (str(x), lyrics_a.replace('bottles',
		'bottle'), str(x), lyrics_b))
		print ("%s %s %s \n" % (lyrics_c, str(x-1), lyrics_d.replace(
		'bottles','bottle')))
	if x == 1:
		print ("%s %s %s %s" % (str(x), lyrics_a.replace('bottles', 
		'bottle'), str(x), lyrics_b.replace('bottles','bottle')))
		print ("%s %s %s \n" % (lyrics_c, 'no more', lyrics_d))
	if x == 0:
		print ("No more bottles of beer on the wall, no more bottles " 
		"of beer")
		print ("Go to the store and buy some more, 99 bottles of beer "
		"on the wall \n \n") 
		
