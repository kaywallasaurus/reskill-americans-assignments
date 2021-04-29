# ******************NOTE******************
# this file is the submission for the week 4 assignment: updated ATM with
# basic authentication.

from datetime import datetime
import time
import random
import validation  # type: ignore

# variable definitions

database = {
    1000000000: ['Test', 'User', 'test@bankosaurus.com', 'password', 1000]
    }

current_user = None
current_user_name = None
current_user_email = None
current_user_password = None
account_balance = 0

# function definitions


def print_welcome():

    print('\nThank you for choosing Bankosaurus ATM.\n')


def print_greeting():

    now = datetime.now()
    date = now.strftime("%A, %B %d, %Y")
    time = now.strftime("%H:%M")

    print('\nWelcome, %s! The date is %s, and the current time is %s.\n'
          % (current_user_name, date, time))


def generate_account_number():

    print('We are generating your account number now.\n')
    time.sleep(0.75)
    print('.\n')
    time.sleep(0.75)
    print('..\n')
    time.sleep(0.75)
    print('...\n')
    time.sleep(0.75)
    print('Thank you for your patience.'
          ' Your account number has been generated.\n')

    return random.randrange(1000000000, 9999999999)


def register():

    print('Please answer these questions to register for a new account.\n')

    first_name = input('What is your first name?\n')
    last_name = input('What is your last name?\n')
    email = input('What is you email address?\n')
    password = input('Please enter a password for your account.\n')
    account_number = generate_account_number()

    database[account_number] = [first_name, last_name, email, password, 0]

    print('This is your account number: %d.\n\n'
          'Keep it secret. Keep it safe.\n' % account_number)
    print('Congratulations! Your account has been created.\n')

    login()


def login():
    global current_user, current_user_name, current_user_email
    global current_user_password, account_balance

    print('Please log in to continue.\n')

    user_account_number = int(input('Account number:\n'))
    validation.validate_account_number(user_account_number)
    user_password = input('Password:\n')

    # I made modifications to this section:
    #
    # 1. I changed the for loop from the video because I wanted to be able to
    # print error statements relevant to the login variable that was failing.
    # With the way the for loop was written in on of this week's videos, this
    # was not possible so I adjusted it a little bit.
    #
    # 2. I also added the ability to save the authenticated database entry to a
    # set of variables that were specific to the current user so they could be
    # easily referenced.

    for account, user_information in database.items():
        if account == user_account_number:
            if user_information[3] == user_password:
                authenticate_pass = True
                current_user = user_account_number
                current_user_name = user_information[0] + ' ' +\
                    user_information[1]
                current_user_email = user_information[2]
                current_user_password = user_password
                account_balance = user_information[4]
                print_greeting()
                break
            else:
                authenticate_pass = False
                error_message = 'bad password'
        else:
            authenticate_pass = False
            error_message = 'bad account number'

    if authenticate_pass:
        bank_operation()
    else:
        if error_message == 'bad account number':
            print('Your acccount number could not be found'
                  '. Please try again.\n')
            login()
        elif error_message == 'bad password':
            print('Your password is incorrect. Please try again.\n')
            login()


def clear_data():
    global current_user, current_user_name, current_user_email
    global current_user_password, account_balance

    current_user = None
    current_user_name = None
    current_user_email = None
    current_user_password = None
    account_balance = 0


def print_main_menu_options():

    print('These are the available options:\n')
    print('1. View Account Balance')
    print('2. Withdrawal')
    print('3. Deposit')
    print('4. Complaint')
    print('5. View Information')
    print('6. Log Out\n')


def option_selector():

    selected_option = int(input('Please select an option: \n'))

    if selected_option == 1:
        print('You selected option 1.\n')
        print_current_balance()
        perform_another_action()
    elif selected_option == 2:
        option_two()
    elif selected_option == 3:
        option_three()
    elif selected_option == 4:
        option_four()
    elif selected_option == 5:
        option_five()
    elif selected_option == 6:
        logout()
    else:
        print('Invalid option selected. Please try again.\n')
        option_selector()


def print_current_balance():
    print('Your current account balance is $%d.\n' % account_balance)


def option_two():
    global account_balance, database

    print('You selected option 2.\n')

    print_current_balance()

    withdrawal = int(input("Enter the amount you'd like to withdraw,"
                           " or enter '0' to return to the main menu.\n"))

    if withdrawal == 0:
        return_to_menu()
    elif withdrawal < 0:
        print('You cannot withdraw a negative amount.\n')
        print('You will now be returned to the main menu to try again.\n')
        bank_operation()
    else:
        if withdrawal > account_balance:
            print('You cannot withdraw more than the current balance of $%d.\n'
                  % account_balance)
            print('You will now be returned to the main menu to try again.\n')
            bank_operation()
        else:
            newaccount_balance = account_balance - withdrawal
            account_balance = newaccount_balance
            database[current_user][4] = newaccount_balance
            print("Your new balance is $%d. Please take your cash.\n"
                  % account_balance)
            perform_another_action()


def option_three():
    global account_balance, database

    print('You selected option 3.\n')

    print_current_balance()

    deposit = int(input("Enter the amount you'd like to deposit,"
                        " or enter '0' to return to the main menu.\n"))

    if deposit == 0:
        return_to_menu()
    elif deposit < 0:
        print('You cannot deposit a negative amount.\n')
        print('You will now be returned to the main menu to try again.\n')
        bank_operation()
    else:
        newaccount_balance = account_balance + deposit
        account_balance = newaccount_balance
        database[current_user][4] = newaccount_balance
        print("Your new balance is $%d.\n" % account_balance)
        perform_another_action()


def option_four():

    print('You selected option 4.\n')

    continue_with_complaint = str.lower(input("If you'd like to submit a"
                                              " complaint to our Member"
                                              " Services department, please"
                                              " enter 'Y'.\nOtherwise, please"
                                              " enter any other text to return"
                                              " to the main menu.\n"))

    if continue_with_complaint == 'y':
        complaint = input("What issue would you like to report?\n\n")
        print("\nThank you for contacting us.\n")
        perform_another_action()
    else:
        return_to_menu()


def option_five():

    print('You selected option 5.\n')
    print('This Bankosaurus account is registered to %s.\n'
          % current_user_name)
    print('The email on this account is %s.\n' % current_user_email)
    print("If you'd like to change or update any of the above information, or"
          " if you'd like to view your account number or change your password,"
          " please contact Member Services.\n")

    perform_another_action()


def perform_another_action():
    further_action = str.lower(input("Would you like to perform another action"
                                     "? Enter 'Y' for yes, or enter any other"
                                     " text to logout.\n"))

    if further_action == 'y':
        return_to_menu()
    else:
        logout()


def return_to_menu():
    print("You are returning to the main menu.\n")
    bank_operation()


def logout():

    clear_data()

    print('Thank you for using this Bankosaurus ATM!\n')
    print('.\n')
    time.sleep(0.75)
    print('..\n')
    time.sleep(0.75)
    print('...\n')
    time.sleep(0.75)
    print("You have been logged out. Have a nice day!\n")


def bank_operation():

    print_main_menu_options()
    option_selector()


def init_atm():

    print_welcome()
    valid_option_selected = False

    while not valid_option_selected:

        registered_user = int(input('Do you have an account?\n'
                                    '1. Yes\n2. No\n'))

        if registered_user == 1:
            valid_option_selected = True
            login()
        elif registered_user == 2:
            valid_option_selected = True
            register()
        else:
            print('You have entered an invalid option. Please try again.')

# run atm


init_atm()
