# ******************NOTE******************
# this file is the submission for the week 4 assignment: updated ATM with
# basic authentication.

from datetime import datetime
import time
import random

# variable definitions

database = {
    1000000000 : ['Test', 'User', 'test@bankosaurus.com', 'password', 1000]
    }

currentUser = None
currentUserName = None
currentUserEmail = None
currentUserPassword = None
accountBalance = 0

# function definitions

def printWelcome():

    print('\nThank you for choosing Bankosaurus ATM.\n')

def printGreeting():

    now = datetime.now()
    date = now.strftime("%A, %B %d, %Y")
    time = now.strftime("%H:%M")

    print('\nWelcome, %s! The date is %s, and the current time is %s.\n'
        % (currentUserName, date, time))

def generateAccountNumber():

    print('We are generating your account number now.\n')
    time.sleep(0.75)
    print('.\n')
    time.sleep(0.75)
    print('..\n')
    time.sleep(0.75)
    print('...\n')
    time.sleep(0.75)
    print('Thank you for your patience.'\
        ' Your account number has been generated.\n')

    return random.randrange(1000000000, 9999999999)

def register():

    print('Please answer these questions to register for a new account.\n')

    firstName = input('What is your first name?\n')
    lastName = input('What is your last name?\n')
    email = input('What is you email address?\n')
    password = input('Please enter a password for your account.\n')
    accountNumber = generateAccountNumber()

    database[accountNumber] = [firstName, lastName, email, password, 0]

    print('This is your account number: %d.\n\n'\
        'Keep it secret. Keep it safe.\n' % accountNumber)
    print('Congratulations! Your account has been created.\n')

    login()

def login():
    global currentUser, currentUserName, currentUserEmail, currentUserPassword
    global accountBalance

    print('Please log in to continue.\n')

    userAccountNumber = int(input('Account number:\n'))
    userPassword = input('Password:\n')

    # I made modifications to this section:
    #
    # 1. I changed the for loop from the video because I wanted to be able to
    # print error statements relevant to the part of the login that was failing.
    # With the way the for loop was written in on of this week's videos, this
    # was not possible so I adjusted it a little bit.
    #
    # 2. I also added the ability to save the authenticated database entry to a
    # set of variables that were specific to the current user so they could be
    # easily referenced.

    for account,userInformation in database.items():
        if(account == userAccountNumber):
            if(userInformation[3] == userPassword):
                authenticatePass = True
                currentUser = userAccountNumber
                currentUserName = userInformation[0] + ' ' + userInformation[1]
                currentUserEmail = userInformation[2]
                currentUserPassword = userPassword
                accountBalance = userInformation[4]
                printGreeting()
                break
            else:
                authenticatePass = False
                errorMessage = 'bad password'
        else:
            authenticatePass = False
            errorMessage = 'bad account number'

    if authenticatePass:
        bankOperation()
    else:
        if(errorMessage == 'bad account number'):
            print('Your acccount number could not be found'\
                ', please try again.\n')
            login()
        elif(errorMessage == 'bad password'):
            print('Your password is incorrect, please try again.\n')
            login()

def clearData():
    global currentUser, currentUserName, currentUserEmail, currentUserPassword

    currentUser = None
    currentUserName = None
    currentUserEmail = None
    currentUserPassword = None
    accountBalance = 0

def printMainMenuOptions():

    print('These are the available options:\n')
    print('1. View Account Balance')
    print('2. Withdrawal')
    print('3. Deposit')
    print('4. Complaint')
    print('5. View Information')
    print('6. Log Out\n')

def optionSelector():

    selectedOption = int(input('Please select an option: \n'))

    if(selectedOption == 1):
        print('You selected option 1.\n')
        printCurrentBalance()
        performAnotherAction()
    elif(selectedOption == 2):
        optionTwo()
    elif(selectedOption == 3):
        optionThree()
    elif(selectedOption == 4):
        optionFour()
    elif(selectedOption == 5):
        optionFive()
    elif(selectedOption == 6):
        logout()
    else:
        print('Invalid option selected, please try again.\n')
        optionSelector()

def printCurrentBalance():
    print('Your current account balance is $%d.\n' % accountBalance)

def optionTwo():
    global accountBalance, database

    print('You selected option 2.\n')

    printCurrentBalance()

    withdrawal = int(input("Enter the amount you'd like to withdraw,"\
        " or enter '0' to return to the main menu.\n"))

    if(withdrawal == 0):
        returnToMenu()
    elif(withdrawal < 0):
        print('You cannot withdraw a negative amount.\n')
        print('You will now be returned to the main menu to try again.\n')
        bankOperation()
    else:
        if(withdrawal > accountBalance):
            print('You cannot withdraw more than your current balance of $%d.\n'
                % accountBalance)
            print('You will now be returned to the main menu to try again.\n')
            bankOperation()
        else:
            newAccountBalance = accountBalance - withdrawal
            accountBalance = newAccountBalance
            database[currentUser][4] = newAccountBalance
            print("You new balance is $%d. Please take your cash.\n"
                % accountBalance)
            performAnotherAction()

def optionThree():
    global accountBalance, database

    print('You selected option 3.\n')

    printCurrentBalance()

    deposit = int(input("Enter the amount you'd like to deposit,"\
        " or enter '0' to return to the main menu.\n"))

    if(deposit == 0):
        returnToMenu()
    elif(deposit < 0):
        print('You cannot deposit a negative amount.\n')
        print('You will now be returned to the main menu to try again.\n')
        bankOperation()
    else:
        newAccountBalance = accountBalance + deposit
        accountBalance = newAccountBalance
        database[currentUser][4] = newAccountBalance
        print("You new balance is $%d.\n" % accountBalance)
        performAnotherAction()

def optionFour():

    print('You selected option 4.\n')

    continueWithComplaint = str.lower(input("If you'd like to submit a"\
        "complaint to our Member Services department, please enter 'Y'.\n"\
        "Otherwise, please enter any other text to return to the main menu.\n"))

    if(continueWithComplaint == 'y'):
        complaint = input("What issue would you like to report?\n\n")
        print("\nThank you for contacting us.\n")
        performAnotherAction()
    else:
        returnToMenu()

def optionFive():

    print('You selected option 5.\n')
    print('This Bankosaurus account is registered to %s.\n' % currentUserName)
    print('The email on this account is %s.\n' % currentUserEmail)
    print("If you'd like to change or update any of the above information, or"\
        " if you'd like to view your account number or change your password,"\
        " please contact Member Services.\n")

    performAnotherAction()

def performAnotherAction():
    furtherAction = str.lower(input("Would you like to perform another action?"\
        " Enter 'Y' for yes, or enter any other text to logout.\n"))

    if(furtherAction == 'y'):
        returnToMenu()
    else:
        logout()

def returnToMenu():
    print("You are returning to the main menu.\n")
    bankOperation()

def logout():

    clearData()

    print('Thank you for using this Bankosaurus ATM!\n')
    print('.\n')
    time.sleep(0.75)
    print('..\n')
    time.sleep(0.75)
    print('...\n')
    time.sleep(0.75)
    print("You have been logged out. Have a nice day!\n")

def bankOperation():

    printMainMenuOptions()
    optionSelector()

def initAtm():

    printWelcome()
    validOptionSelected = False

    while not validOptionSelected:

        registeredUser = int(input('Do you have an account?\n'\
            '1. Yes\n2. No\n'))

        if(registeredUser == 1):
            validOptionSelected = True
            login()
        elif(registeredUser == 2):
            validOptionSelected = True
            register()
        else:
            print('You have entered an invalid option, please try again.')

# run atm

initAtm()
