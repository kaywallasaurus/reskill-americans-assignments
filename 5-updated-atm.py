# ******************NOTE******************
# this file is the submission for the week 5 assignment: updated ATM with
# modules for verification and file system database.

from datetime import datetime
import time
import random
import validation  # type: ignore
import database  # type: ignore

# variable definitions

current_account = None
current_user_first = 'Unknown'
current_user_last = 'Unknown'
current_user_full_name = 'Unknown'
current_user_email = 'Unknown'
current_user_password = None
account_balance = 0

current_user = 'Unknown'

# function definitions


def print_welcome():

    print('\nThank you for choosing Bankosaurus ATM.\n')


def print_greeting():

    now = datetime.now()
    date = now.strftime("%A, %B %d, %Y")
    time = now.strftime("%H:%M")

    print('\nWelcome, %s! The date is %s, and the current time is %s.\n'
          % (current_user_full_name, date, time))


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

    return random.randrange(1000000001, 9999999999)


def register():

    print('Please answer these questions to register for a new account.\n')

    first_name = input('What is your first name?\n')
    last_name = input('What is your last name?\n')
    email = input('What is you email address?\n')
    password = input('Please enter a password for your account.\n')
    account_number = generate_account_number()

    print('This is your account number: %d.\n\n'
          'Keep it secret. Keep it safe.\n' % account_number)

    if database.create(account_number, first_name, last_name, email, password):
        print('Congratulations! Your account has been created.\n')
        login()
    else:
        print('***Your account was not be created.***')
        init_atm()


def login():

    print("\nPlease log in to continue or type 'Exit' to go back.\n")

    user_account_number = input('Account number:\n')
    is_account_valid = validation.validate_account_number(user_account_number)

    if is_account_valid:

        if is_account_valid == 'exit':

            init_atm()

        else:

            raw_user = database.read(user_account_number)

            if raw_user:

                user_password = input('Password:\n')
                authentication = database.login_auth(raw_user, user_password)

                if authentication:
                    database.create_auth_session(raw_user)
                    update_user_info(raw_user)
                    print_greeting()
                    bank_operation()
                else:
                    login()

            else:
                print('Your acccount could not be found. Please try again.\n')
                login()

    else:
        login()


def update_user_info(raw_user):
    global current_account, current_user_first, current_user_last
    global current_user_full_name, current_user_email, current_user_password
    global account_balance

    user_data = str.split(raw_user, ',')

    current_account = int(user_data[0])
    current_user_first = user_data[1]
    current_user_last = user_data[2]
    current_user_full_name = current_user_first + ' ' + current_user_last
    current_user_email = user_data[3]
    current_user_password = user_data[4]
    account_balance = int(user_data[5])


def update_current_user():
    global current_user

    current_user = str(current_account) + ',' + current_user_first + ',' +\
        current_user_last + ',' + current_user_email + ',' +\
        str(current_user_password) + ',' + str(account_balance)


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
    global current_account, current_user_first, current_user_last
    global current_user_full_name, current_user_email, current_user_password
    global account_balance, current_user

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
            new_account_balance = account_balance - withdrawal
            account_balance = new_account_balance

            update_current_user()
            database.update_both(current_user, current_account)

            print("Your new balance is $%d. Please take your cash.\n"
                  % account_balance)
            perform_another_action()


def option_three():
    global current_account, current_user_first, current_user_last
    global current_user_full_name, current_user_email, current_user_password
    global account_balance, current_user

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
        new_account_balance = account_balance + deposit
        account_balance = new_account_balance

        update_current_user()
        database.update_both(current_user, current_account)

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
          % current_user_full_name)
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

    database.delete_auth_session()

    print('Thank you for using this Bankosaurus ATM!\n')
    print('.\n')
    time.sleep(0.75)
    print('..\n')
    time.sleep(0.75)
    print('...\n')
    time.sleep(0.75)
    print("You have been logged out. Have a nice day!\n")


def exit():
    print('Have a nice day!\n')


def bank_operation():

    print_main_menu_options()
    option_selector()


def init_atm():

    print_welcome()

    valid_option_selected = False

    while not valid_option_selected:

        try:
            registered_user = int(input('Do you have an account?\n'
                                        '\n1. Yes\n2. No\n3. Exit\n'))
        except ValueError:
            print('You have entered an invalid option. Please try again.')
            init_atm()
        else:
            if registered_user == 1:
                valid_option_selected = True
                login()
            elif registered_user == 2:
                valid_option_selected = True
                register()
            elif registered_user == 3:
                valid_option_selected = True
                exit()
            else:
                print('You have entered an invalid option. Please try again.')


# run atm


init_atm()
