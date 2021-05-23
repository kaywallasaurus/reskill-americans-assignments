import os


def validate_account_number(account_number):
    if account_number:
        if str.lower(account_number) == 'exit':
            return 'exit'
        elif len(str(account_number)) == 10:
            try:
                int(account_number)
                return True
            except ValueError:
                print('The number you entered is invalid. Please try again.')
                return False
        else:
            print("Account number must be 10 characters. Please try again.")
            return False
    else:
        print('Account number is required to continue. Please try again.')
        return False


def validate_budget(amt):
    if type(amt) == int:
        if amt < 0:
            print('This value cannot be negative. Please try again.')
            return False
        else:
            return True
    else:
        print('Your input is not a number. Please try again.')
        return False


def selection(account_number, selected_option):

    data_path = 'budget-app-data/'

    account_path = data_path + str(account_number) + '/'
    category_path = account_path + 'categories' + '/'

    available_categories = os.listdir(category_path)

    item_count = len(available_categories)

    if validate_budget(selected_option):
        if selected_option > item_count:
            return False
        else:
            return True
    else:
        return False
