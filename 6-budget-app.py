# ******************NOTE******************
# this file is the submission for the week 6 assignment: budget app

# dependencies

from getpass import getpass
from datetime import datetime
import time
import random
import validation  # type: ignore
import budgetdb  # type: ignore


def loading():
    time.sleep(0.5)
    print('...\n')
    time.sleep(0.5)
    print('..\n')
    time.sleep(0.5)
    print('.\n')
    time.sleep(0.5)


# budget class Information


class Budget:

    def __init__(self, name, amount, used=0):
        self.name = name
        self.amount = amount
        self.used = used
        self.remaining = int(self.amount - self.used)

    # methods

    def update_remaining(self):
        self.remaining = int(self.amount - self.used)

    def check_balance(self):
        loading()
        print('Here is the information for your %s budget:\n' % self.name)
        time.sleep(0.75)
        print('- Your budget for %s is $%d.\n' % (self.name, self.amount))
        time.sleep(0.75)
        print('- You have used $%d from this budget.\n' % self.used)
        time.sleep(0.75)
        self.update_remaining()
        print('- You have $%d remaining.\n' % self.remaining)

    def deposit(self):
        loading()
        print('Your budget amount is $%d.\n' % self.amount)

        deposit = int(input("Enter the amount you'd like to change the budget"
                            " by, or enter '0' to return to the menu.\n"))

        if deposit == 0:
            loading()
            category_operation(self.name, self.amount)
        elif deposit < 0:
            if deposit < (-1 * self.amount):
                print('You cannot subtract more than is currently available.'
                      ' Please try again.\n')
                category_operation(self.name, self.amount)
            else:
                new_budget = self.amount + deposit
                self.amount = new_budget

                budgetdb.update_cat(current_account, self.name, self.amount,
                                    self.used)

                loading()
                print('The budget for %s is now $%d.\n' % (self.name,
                      self.amount))
                perform_another_action(self.name, self.amount)
        else:
            new_budget = self.amount + deposit
            self.amount = new_budget

            budgetdb.update_cat(current_account, self.name, self.amount,
                                self.used)

            loading()
            print('The budget for %s is now $%d.\n' % (self.name, self.amount))
            perform_another_action(self.name, self.amount)

    def withdraw(self):
        loading()
        print('Your available amount is $%d.\n' % self.remaining)

        withdrawal = int(input("Enter the amount you used from your %s budget,"
                               " or enter '0' to return to the menu.\n"
                               % self.name))

        if withdrawal == 0:
            loading()
            category_operation(self.name, self.amount)
        elif withdrawal < 0:
            loading()
            print('You cannot log a negative amount. Please try again.\n')
            category_operation(self.name, self.amount)
        elif withdrawal > self.remaining:
            loading()
            print('Sorry, you do not have enough budget for this purchase.\n')
            category_operation(self.name, self.amount)
        else:
            new_used = self.used + withdrawal
            self.used = new_used
            self.update_remaining()

            budgetdb.update_cat(current_account, self.name, self.amount,
                                self.used)

            loading()
            print('You have $%d remaining in your %s budget.\n' %
                  (self.remaining, self.name))
            perform_another_action(self.name, self.amount)

    def transfer(self):
        loading()
        print('Your available amount is $%d.\n' % self.remaining)

        transfer = int(input("Enter the amount you would like to transfer"
                             " from your %s budget, or enter '0' to return"
                             " to the menu.\n" % self.name))

        if transfer == 0:
            loading()
            category_operation(self.name, self.amount)
        elif transfer < 0:
            loading()
            print('You cannot transfer a negative amount. Please try again.\n')
            category_operation(self.name, self.amount)
        elif transfer > self.remaining:
            loading()
            print('You cannot transfer more than the available amount for %s.'
                  ' Please try again.\n' % self.name)
        else:

            loading()

            budgetdb.list_categories(current_account)

            opt = int(input("\nPlease choose the number of the category"
                            " you would like to transfer to:\n"))

            is_option_valid = validation.selection(current_account, opt)

            if is_option_valid:
                txr_to = opt - 1
                cat_raw_data = budgetdb.read_cat_index(current_account,
                                                       txr_to)
                cat_data = cat_raw_data.split(',')

                if cat_data[0] == self.name:
                    loading()
                    print('You cannot transfer to the same category you'
                          ' are transferring from. Please go back'
                          ' and try again.\n')
                    category_operation(self.name, self.amount)
                else:
                    name = cat_data[0]
                    budget = int(cat_data[1])
                    used = int(cat_data[2])
                    txr_cat = Budget(name, budget, used)
                    new_amount = txr_cat.amount + transfer
                    txr_cat.amount = new_amount
                    old_budget_amt = self.amount - transfer
                    self.amount = old_budget_amt

                    loading()
                    print("This change will transfer $%d from your %s"
                          " budget to your %s budget.\n" % (transfer,
                                                            self.name,
                                                            txr_cat.name))
                    confirm = input("To continue with this change,"
                                    " please enter 'Y'. To return to the"
                                    " menu, press any other key.\n")

                    if confirm.lower() == 'y':
                        budgetdb.update_cat(current_account, self.name,
                                            self.amount, self.used)
                        budgetdb.update_cat(current_account, txr_cat.name,
                                            txr_cat.amount, txr_cat.used)
                        loading()
                        print('Your transfer is complete!\n')
                        perform_another_action(self.name, self.amount)
                    else:
                        loading()
                        category_operation(self.name, self.amount)
            else:
                loading()
                print('Invalid option selected. Please try again.\n')
                category_operation(self.name, self.amount)

    def clear(self):
        loading()
        print('Your available amount is $%d.\n' % self.remaining)

        print('You can reset your available %s budget to $%d.\n' %
              (self.name, self.amount))

        confirm = input("\nTo reset your %s budget, please enter 'Y'. To go"
                        " back to the %s options, enter 'N'.\n"
                        % (self.name, self.name))

        if confirm.lower() == 'y':
            self.used = 0
            self.update_remaining()

            budgetdb.update_cat(current_account, self.name, self.amount,
                                self.used)

            loading()
            print('Your available %s budget has been reset to $%d.\n'
                  % (self.name, self.remaining))
            perform_another_action(self.name, self.amount)
        elif confirm.lower() == 'n':
            loading()
            category_operation(self.name, self.amount)
        else:
            print('Invalid option selected. Please try again.')
            category_operation(self.name, self.amount)

# global variables


current_account = None
current_user_first = 'Unknown'
current_user_last = 'Unknown'
current_user_full = 'Unknown'
current_user_email = 'Unknown'
current_user_password = None

current_user = 'Unknown'

current_cat = Budget('current', 0)

# function definitions


def print_welcome():

    print('\nThank you for downloading The Bankosaurus Budget Manager!\n')


def print_greeting():

    now = datetime.now()
    date = now.strftime("%A, %B %d, %Y")
    time = now.strftime("%H:%M")

    print('\nWelcome, %s! The date is %s, and the current time is %s.\n'
          % (current_user_full, date, time))


def generate_account_number():

    print('We are generating your account number now.\n')
    time.sleep(0.75)
    print('\n.\n')
    time.sleep(0.75)
    print('..\n')
    time.sleep(0.75)
    print('...\n')
    time.sleep(0.75)
    print('Thank you for your patience.'
          ' Your account number has been generated.\n')

    return random.randrange(1000000001, 9999999999)


def register():

    print('Please answer these questions to register for an account.\n')

    first_name = input('What is your first name?\n')
    last_name = input('What is your last name?\n')
    email = input('What is your email address?\n')
    password = getpass('Please enter a password for your account.\n')
    account_number = generate_account_number()

    print('This is your account number: %d.\n\n'
          'Keep it secret. Keep it safe.\n' % account_number)

    if budgetdb.create(account_number, first_name, last_name, email, password):
        print('Congratulations! Your account has been created.\n')
        login()
    else:
        print('***Your account could not be created. Please try again.***')
        init_budget()


def login():

    print("\nPlease log in to continue or type 'Exit' to go back.\n")

    user_account_number = input('Account number:\n')
    is_account_valid = validation.validate_account_number(user_account_number)

    if is_account_valid:

        if is_account_valid == 'exit':

            init_budget()

        else:

            raw_user = budgetdb.read_acct(user_account_number)

            if raw_user:

                user_password = getpass('Password:\n')
                authentication = budgetdb.login_auth(raw_user, user_password)

                if authentication:
                    update_current_user(user_account_number)
                    print_greeting()
                    budget_operation()
                else:
                    login()

            else:
                print('Your acccount could not be found. Please try again.\n')
                login()

    else:
        login()


def update_user_info(raw_user):
    global current_account, current_user_first, current_user_last
    global current_user_full, current_user_email, current_user_password

    user_data = str.split(raw_user, ',')

    current_account = int(user_data[0])
    current_user_first = user_data[1]
    current_user_last = user_data[2]
    current_user_full = current_user_first + ' ' + current_user_last
    current_user_email = user_data[3]
    current_user_password = user_data[4]


def update_current_user(user_account_number):
    global current_user

    raw_user = budgetdb.read_acct(user_account_number)
    update_user_info(raw_user)

    current_user = str(current_account) + ',' + current_user_first + ',' +\
        current_user_last + ',' + current_user_email + ',' +\
        str(current_user_password)


def clear_cat():
    global current_cat

    current_cat = Budget('current', 0)


def clear_data():
    global current_user, current_account, current_user_first, current_user_last
    global current_user_full, current_user_email, current_user_password
    global current_cat

    current_account = None
    current_user_first = 'Unknown'
    current_user_last = 'Unknown'
    current_user_full = 'Unknown'
    current_user_email = 'Unknown'
    current_user_password = None

    current_user = 'Unknown'

    current_cat = Budget('current', 0)


def print_main_menu_options():

    print('These are the available options:\n')
    print('Need help?')
    print("Enter '0' to see more details on the available options.\n")
    print('1. View Budget Categories')
    print('2. Add a Category')
    print('3. Log Out\n')


def main_menu_option_selector():

    selected_option = int(input('Please select an option: \n'))

    if selected_option == 0:
        main_menu_help()
    elif selected_option == 1:
        view_categories()
    elif selected_option == 2:
        add_category()
    elif selected_option == 3:
        logout()
    else:
        print('Invalid option selected. Please try again.\n')
        main_menu_option_selector()


def main_menu_help():
    print("\nHere's a more detailed explanation of the available options:\n")
    time.sleep(0.75)
    print("1. View existing budget categories and perform further actions\n")
    time.sleep(0.75)
    print("2. Add a new budget category and set a budget amount\n")
    time.sleep(0.75)
    print("3. Log out of The Bankosaurus Budget Manager\n")
    time.sleep(1)
    main_menu_option_selector()


def print_category_menu():

    print('These are the available options for %s:\n' % current_cat.name)
    print('Need help?')
    print("Enter '0' to see more details on the available options.\n")
    print('1. Check Available Balance')
    print('2. Update Available Balance')
    print('3. Use Balance')
    print('4. Transfer Balance')
    print('5. Reset Balance')
    print('6. Return to Main Menu\n')


def category_option_selector(name, amt):

    selected_option = int(input('Please select an option: \n'))

    if selected_option == 0:
        category_menu_help(name, amt)
    elif selected_option == 1:
        option_one(name, amt)
    elif selected_option == 2:
        option_two(name, amt)
    elif selected_option == 3:
        option_three(name, amt)
    elif selected_option == 4:
        option_four(name, amt)
    elif selected_option == 5:
        option_five(name, amt)
    elif selected_option == 6:
        budget_operation()
    else:
        print('Invalid option selected. Please try again.\n')
        category_option_selector(name, amt)


def category_menu_help(name, amt):
    print("\nHere's a more detailed explanation of the available options:\n")
    time.sleep(0.75)
    print("1. Check the available balance for %s\n" % name)
    time.sleep(0.75)
    print("2. Change the available balance for %s\n" % name)
    time.sleep(0.75)
    print("3. Subtract balance to reflect recent spending\n")
    time.sleep(0.75)
    print("4. Move available balance from %s to a different category\n" % name)
    time.sleep(0.75)
    print("5. Reset your available balance to %d\n" % amt)
    time.sleep(0.75)
    print("6. Go back to the main menu\n")
    time.sleep(1)
    category_option_selector(name, amt)


def view_categories():
    global current_cat

    print('\nHere are the categories you currently have set.\n')
    print('To see additional options, please select a category.\n')

    budgetdb.list_categories(current_account)

    selected_option = int(input('Please enter the number for the category'
                                " you want to use, or enter '0' to go"
                                ' back to the main menu.\n'))

    is_option_valid = validation.selection(current_account, selected_option)

    if is_option_valid:
        print('One moment while we fetch your category data.\n')
        index = selected_option - 1
        cat_raw_data = budgetdb.read_cat_index(current_account, index)
        cat_data = cat_raw_data.split(',')
        name = cat_data[0]
        budget = int(cat_data[1])
        used = int(cat_data[2])
        current_cat = Budget(name, budget, used)
        loading()
        category_operation(current_cat.name, current_cat.amount)
    else:
        print('Invalid option selected. Please try again.\n')
        view_categories()


def add_category():

    print('\n**** Category Creation ****\n')

    name = input('What would you like to name this category?\n')

    is_amt_valid = False

    while is_amt_valid is False:

        amt = int(input('\nPlease enter your budget for this category as a'
                        ' whole number.\n'))

        is_amt_valid = validation.validate_budget(amt)

        if is_amt_valid:
            continue
        else:
            print('Your budget amount needs to be a number. Please try again.')

    name_up = budgetdb.to_sentence_case(name)

    loading()

    print('Your new category for %s has a budget of $%d.\n' % (name_up, amt))

    confirm = input("\nTo confirm your new category, please enter 'Y'. To try"
                    " again, enter 'N'. Enter any other key to go back to"
                    " the main menu.\n")

    if confirm.lower() == 'y':
        category = Budget(name_up, amt)
        budgetdb.create_cat(current_account, category)
        print('%s has been added to your categories.\n\n' % name_up)
        time.sleep(1)
        budget_operation()
    elif confirm.lower() == 'n':
        add_category()
    else:
        budget_operation()


def option_one(name, budget):

    print('\nYou selected option 1.\n')

    current_cat.check_balance()

    perform_another_action(name, budget)


def option_two(name, budget):
    print('\nYou selected option 2.\n')
    print('**** Update Available Balance ****\n')

    current_cat.deposit()

    perform_another_action(name, budget)


def option_three(name, budget):

    print('\nYou selected option 3.\n')
    print('**** Use Your Balance ****\n')

    current_cat.withdraw()

    perform_another_action(name, budget)


def option_four(name, budget):

    print('\nYou selected option 4.\n')
    print('**** Transfer to Another Category ****\n')

    current_cat.transfer()


def option_five(name, budget):

    print('\nYou selected option 5.\n')
    print('**** Reset Available Balance ****\n')

    current_cat.clear()

    perform_another_action(name, budget)


def budget_operation():

    print_main_menu_options()
    main_menu_option_selector()


def category_operation(name, budget):

    print_category_menu()
    category_option_selector(name, budget)


def perform_another_action(name, budget):

    further_action = str.lower(input("To perform another action within this"
                                     " category, press 'Y'. To return to the"
                                     " main menu, press any other key.\n"))

    if further_action == 'y':
        category_operation(name, budget)
    else:
        clear_cat()
        budget_operation()


def exit():
    print('Have a nice day!\n')


def logout():

    clear_data()

    print('\nThank you for using The Bankosaurus Budget Manager!\n')
    loading()
    print("You have been logged out. Have a nice day!\n")


def init_budget():

    print_welcome()

    valid_option_selected = False

    while not valid_option_selected:

        try:
            registered_user = int(input('Do you have an account?\n'
                                        '\n1. Yes\n2. No\n3. Exit\n'))
        except ValueError:
            print('You have entered an invalid option. Please try again.')
            init_budget()
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

# run budget app


init_budget()
