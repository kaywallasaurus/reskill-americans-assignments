from datetime import datetime

name = input('What is your name?\n')
allowedUsers = ['Seyi', 'Mike', 'Love']
allowedPassword = ['passwordSeyi', 'passwordMike', 'passwordLove']
accountBalances = [1000, 500, 300]
selectedOption = None

def printCurrentBalance():
    print('Your current account balance is $%d.\n' % accountBalances[userId])

def endSession():
    print("Thank you for using this ATM.\n"\
    "You have been logged out. Have a nice day.")

def printGreeting():
    now = datetime.now()
    date = now.strftime("%A, %B %d, %Y")
    time = now.strftime("%H:%M")

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

def performAnotherAction():
    furtherAction = input("Would you like to perform another action?"\
        " Enter 'Y' for yes, or enter any other text for no.\n")

    if(furtherAction == 'Y'):
        returnToMenu()
    else:
        endSession()

def optionOne():
    global accountBalances
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
        if(withdrawal > accountBalances[userId]):
            print('You cannot withdraw more than your current balance of $%d.\n'
                % accountBalances[userId])
            print('You will now be returned to the main menu to try again.\n')
            useAtm()
        else:
            newAccountBalance = accountBalances[userId] - withdrawal
            accountBalances[userId] = newAccountBalance
            print("You new balance is $%d. Please take your cash.\n"
                % accountBalances[userId])
            performAnotherAction()

def optionTwo():
    global accountBalances
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
        newAccountBalance = accountBalances[userId] + deposit
        accountBalances[userId] = newAccountBalance
        print("You new balance is $%d.\n"
            % accountBalances[userId])
        performAnotherAction()

def optionThree():
    continueWithComplaint = input("If you'd like to submit a complaint to our"\
        " Member's Services department, please enter 'Y' to continue."\
        " Otherwise, please enter any other text to return to the main menu.\n")

    if(continueWithComplaint == 'Y'):
        complaint = input("What issue would you like to report?\n")
        print("Thank you for contacting us.\n")
        performAnotherAction()
    else:
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
