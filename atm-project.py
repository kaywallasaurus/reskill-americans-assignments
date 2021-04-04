from datetime import datetime

name = input('What is your name?\n')
allowedUsers = ['Seyi', 'Mike', 'Love']
allowedPassword = ['passwordSeyi', 'passwordMike', 'passwordLove']
accountBalance = None
selectedOption = None

def resetBalance():
    global accountBalance
    accountBalance = 500

def printCurrentBalance():
    global accountBalance
    print('Your current account balance is $%d.\n' % accountBalance)

def endSession():
    print("You have been logged out. Have a nice day.")

def printGreeting():
    now = datetime.now()
    date = now.strftime("%A, %B %d, %Y")
    time = now.strftime("%H:%M")

    resetBalance()

    print('Welcome, %s! The date is %s, and the current time is %s.\n'
        % (name, date, time))

def printMainMenuOptions():
    print('These are the available options:\n')
    print('1. Withdrawal')
    print('2. Deposit')
    print('3. Complaint')
    print('4. Log Out\n')

def selectAnOption():
    global selectedOption
    selectedOption = int(input('Please select an option: \n'))

def printOption():
    print('You selected option %d.\n' % selectedOption)

def returnToMenu():
    print("You are returning to the main menu.\n")
    useAtm()

def optionOne():
    global accountBalance
    printOption()
    printCurrentBalance()
    withdrawal = int(input("Enter the amount you'd like to withdraw,"\
        " or enter '0' to return to the main menu.\n"))

    if(withdrawal == 0):
        returnToMenu()
    elif(withdrawal < 0):
        print('You cannot withdraw a negative amount.\n')
        print('You will now be returned to the main menu to try again.\n')
        useAtm()
    else:
        if(withdrawal > accountBalance):
            print('You cannot withdraw more than your current balance of $%d.\n'
                % accountBalance)
            print('You will now be returned to the main menu to try again.\n')
            useAtm()
        else:
            newAccountBalance = accountBalance - withdrawal
            accountBalance = newAccountBalance
            print("You new balance is $%d. Please take your cash.\n"
                % accountBalance)
            endSession()

def optionTwo():
    global accountBalance
    printOption()
    printCurrentBalance()
    deposit = int(input("Enter the amount you'd like to deposit,"\
        " or enter '0' to return to the main menu.\n"))

    if(deposit == 0):
        returnToMenu()
    elif(deposit < 0):
        print('You cannot deposit a negative amount.\n')
        print('You will now be returned to the main menu to try again.\n')
        useAtm()
    else:
        newAccountBalance = accountBalance + deposit
        accountBalance = newAccountBalance
        print("You new balance is $%d.\n"
            % accountBalance)
        endSession()

def optionThree():
    continueWithComplaint = int(input("If you'd like to submit a complaint to our Member's Services"\
        " department, please enter '1' to continue. Otherwise, please enter"\
        " '0' to return to the main menu.\n"))

    if(continueWithComplaint == 1):
        complaint = input("What issue would you like to report?\n")
        print("Thank you for contacting us.\n")
        endSession()
    elif(continueWithComplaint == 0):
        returnToMenu()

def optionFour():
    endSession()

def optionSelector():
    selectAnOption()

    if(selectedOption == 1):
        optionOne()
    elif(selectedOption == 2):
        optionTwo()
    elif(selectedOption == 3):
        optionThree()
    elif(selectedOption == 4):
        optionFour()
    else:
        print('Invalid option selected. Your session will now end.\n')
        endSession()

def useAtm():
    printMainMenuOptions()
    optionSelector()

# atm initialization begins here

if(name in allowedUsers):
    password = input('Your passsword?\n')
    userId = allowedUsers.index(name)

    if(password == allowedPassword[userId]):
        printGreeting()
        useAtm()
    else:
        print('Password incorrect, please try again.')

else:
    print('Name not found, please try again.')
