import time
import random

# variable definitions

accountNumber = None
database = {
    0000000000 : [ 'Test', 'User', 'test-user@bankosaurus.com', 'password' ]
    }

# function definitions

def printWelcome():
    print('Welcome to the Bankosaurus ATM.\n')

def register():
    global accountNumber
    print('Please answer these questions to register for a new account.\n')

    firstName = input('What is your first name?\n')
    lastName = input('What is your last name?\n')
    email = input('What is you email address?\n')
    password = input('Please enter a password for your account.\n')
    accountNumber = generateAccountNumber()

    print(type(accountNumber))

    database[accountNumber] = [firstName, lastName, email, password]

    print('This is your account number: %d.\n\n'\
        'Keep it secret. Keep it safe.\n' % accountNumber)

    print('Your account has been created.\n')
    login()

def generateAccountNumber():
    print('We are generating your account number now.\n')
    time.sleep(0.5)
    print('.\n')
    time.sleep(1)
    print('..\n')
    time.sleep(1)
    print('...\n')
    time.sleep(1)
    print('Thank you for your patience.'\
        ' Your account number has been generated.')
    return random.randrange(1000000000, 9999999999)

def login():
    global accountNumber
    print('Please login to continue.\n')

    userAccountNumber = int(input('Account number:\n'))
    userPassword = input('Password:\n')

    ###### test statements; I was using these to see if I could figure out why
    ###### the if(accountNumber == userAccountNumber) was failing.

    # accountNumberType = type(accountNumber)
    # userAccountNumberType = type(userAccountNumber)

    # print('\nthe account number is %d' % accountNumber)
    # print('the data type account number is %s' % accountNumberType)
    # print('the account number the user entered is %d' % userAccountNumber)
    # print('the data type of the entered acct number is %s\n' % userAccountNumberType)

    ###### end of test statements

    for accountNumber,userDetails in database.items():
            if(accountNumber == userAccountNumber):
                if(userDetails[3] == userPassword):
                    bankOperation()
                else:
                    print('Invalid password.')
            else:
                print('Invalid account number.')
                login()

#### the below commented code is basically the same for loop as above just with
#### different verbiage on some of the variables, etc.

#    for accountNumber,userInformation in database.items():
#        if(accountNumber == userAccountNumber):
#            if(userInformation[3] == userPassword):
#                bankOperation()
#            else:
#                print('The password you entered is incorrect,'\
#                    ' please try again.')
#                login()
#        else:
#            print('The account number you entered is incorrect,'\
#                ' please try again.')
#            login()

def bankOperation():
    print('Some bank operations here.')

def initAtm():

    printWelcome()
    validOptionSelected = False

    while not validOptionSelected:

        registeredUser = int(input('Please select an option.'\
            ' Do you have an account?\n'\
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
