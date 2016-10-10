


# NOTES:
  # need a means of breaking down and parsing the user's date input 
  # will be determined by the format specified (1,2,3)
  
  # allow for the user to enter month in int of str format (1/'Jan'/'January') 
  

# LOGIC LAYOUT
    # Greet the user and introduce what the program can do 
    # Ask the user what date format they would like to use
    # Receive the user's input and parse it to properly ID it as a datetime
    # Let the user know how long until their specified time 
        # Print out every x seconds 
        # Check if current_time > userTime 
    # Print out ALERT when time == userTime 
    # Ask the user if they would like to enter another time to countdown 
        # ask the user if they would ike to change the date format 




import time 
import datetime 


def _main_():
    
    current_time = time.time()
    print('Welcome to the Countdown Clock 9000. It is currently {0}'.format(
    current_time))
    
    units = _dateFormatChoice()
    dateFormat = _dateFormatter(units) 
    
    #~# lets create a new function to parse the user input and convert it to a 
    #~# true date value (i.e. 12:10 or 12:10:55, etc.) 
    #~if units == 1:
        #~dateFormat = 'hh:mm:ss'
    #~elif units == 2:
        #~dateFormat = 'hh:mm'
    #~elif units == 3:
        #~dateFormat = 'mm:ss'
    
    
    using = True 
    change_dateFormat = False 
    
    # add in logic for handling the restart UI logic 
    while using != False:
        _countdown(units,dateFormat) 
        using = _restartUI() 
        if using != False:
            change_dateFormat = _change_dateFormat()
            if change_dateFormat == True:
                units = _dateFormatChoice()
                dateFormat = _dateFormatter(units) 
                
                
                
    print('Thank you for allowing me to help today!')
    print('\n\nShutting Down..')
    
    # completely and totally unnecessary, but cool all the same 
    i = 0 
    while i < 10:
        i = i + 1 
        time.sleep(0.1)
        print('\t' + '.' * i)
    j = 10 
    while j > 0:
        j = j - 1 
        time.sleep(0.1)
        print('\t' + '.' * j)
    exit 
                 
        
# basic function return status of countdown (if time here --> True; else False)         
def _timerCheck(userTime):
    if userTime < time.time():
        return False
    else:
        return True 
        
def _restartUI():
    print('It looks like your selected time has passed.')
    response = input('Would you like to use my countdown capabilities again? '
    '(y/n)\t>   ')
    response = response.strip().lower()
    if response != 'y' and response != 'n':
        print('That was not a valid response. Please try again.')
        _restartUI()
    elif response == 'y':
        return True
    elif response == 'n':
        return False 

# function to handle the countdown towards the user's time
# use as function and place inside master WHILE loop 
def _countdown(units,dateFormat):
    userTime = input('Please enter your desired date using the format you ' 
    'specified ({0})\t'.format(dateFormat))

    userTime = int(userTime)
    
    status = True 
    # need both conditions so that it will not print a negative time amount 
    while status != False and userTime > time.time():
        print('{0} seconds remain until your specified time of {1}.'.format(str
        (format(userTime - time.time(),'.2f')), userTime))
        
        # run the function to check if the time has passed 
        status = _timerCheck(userTime)
        time.sleep(1) 
        
    print('ALERT! Your time of {0} has arrived!'.format(userTime))
    time.sleep(1.5)
    
# allows the user to specify how they would like to enter the time to countdown
def _dateFormatChoice():
    print("\t1.)hh:mm:ss\n\t2.)hh:mm\n\t3.)mm:ss\n")
    user_choice = input('Which of the following date formats would you like to'
    ' use?\t>\t')
    try:
        if int(user_choice) in (1,2,3):
            user_choice = int(user_choice)
            return user_choice
        else:
            print('Please enter a valid response.')
            _dateFormatChoice()
    except ValueError:
        print('Please enter a valid response.')
        _dateFormatChoice()
        
def  _change_dateFormat():
    response = input('Would you like to change the date format? (y/n)\t')
    response = response.strip().lower()
    if response != 'y' and response != 'n':
        print('Please enter a valid response - y for yes or n for no.')
        _change_dateFormat()
    elif response == 'y':
        return True
    elif response == 'n':
        return False 
        
def _dateFormatter(units):
    if units == 1:
        dateFormat = 'hh:mm:ss'
    elif units == 2:
        dateFormat = 'hh:mm'
    elif units == 3:
        dateFormat = 'mm:ss'
        
    return dateFormat 


_main_()
