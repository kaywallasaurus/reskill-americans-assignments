import os

# variables

data_path = 'budget-app-data/'
all_users = os.listdir(data_path)

# new functions


def to_sentence_case(string):
    return string[0].upper() + string[1:].lower()

# db functions


def create(account_number, first_name, last_name, email, password):

    user_details = str(account_number) + ',' + first_name + ',' + last_name\
        + ',' + email + ',' + password

    if does_account_exist(account_number):
        return False

    if does_email_exist(email):
        return False

    os.makedirs(data_path + str(account_number))

    account_path = data_path + str(account_number) + '/'

    os.makedirs(account_path + 'categories')

    saved_info = open(account_path + 'account_details.txt', 'x')
    saved_info.write(user_details)
    saved_info.close()

    return True


def does_account_exist(account_number):

    for user in all_users:

        if user == str(account_number):
            print('An account already exists with this account number. Please'
                  ' try again.\n')
            return True

    return False


def does_email_exist(email):

    for user in all_users:

        if user == '.DS_Store':
            # would LOVE to know if there's a better way to ignore this file
            continue
        else:
            if read_acct(user):
                split_user_data = str.split(read_acct(user), ',')
            else:
                print('We are unable find your account. Please register or'
                      ' try again.')
                return False

        if email in split_user_data:
            print('The email address you entered is already registered. Please'
                  ' try to log in using your account number instead.\n')
            return True

    return False


def login_auth(raw_user, user_password):

    split_user_data = str.split(raw_user, ',')

    if user_password == split_user_data[4]:
        return True
    else:
        print('Your password is incorrect. Please try again.\n')
        return False


def read_acct(account_number):

    account_path = data_path + str(account_number) + '/'

    try:
        current_details = open(account_path + 'account_details.txt')
    except FileNotFoundError:
        print('We are unable find your account. Please register or try again.')
        return False
    else:
        data = current_details.readline()
        current_details.close()
        return data


def create_cat(account_number, cat):

    account_path = data_path + str(account_number) + '/'
    category_path = account_path + 'categories' + '/'

    try:
        new_cat = open(category_path + cat.name.lower() + '.txt', 'w')
    except FileExistsError():
        print('This category already exists. Please try again.')
        return False
    else:
        data = cat.name + ',' + str(cat.amount) + ',' + str(cat.used)
        new_cat.write(data)


def list_categories(account_number):

    account_path = data_path + str(account_number) + '/'
    category_path = account_path + 'categories' + '/'

    available_categories = os.listdir(category_path)

    i = 0

    for category in available_categories:
        if category == '.DS_Store':
            continue
        else:
            cat_raw_data = read_cat(account_number, category)
            cat_data = cat_raw_data.split(',')
            name = cat_data[0]
            x = i + 1
            print(str(x) + '. ' + name + '\n')
            i += 1


def read_cat(account_number, file_name):

    account_path = data_path + str(account_number) + '/'
    category_path = account_path + 'categories' + '/'

    if file_name.endswith('.txt'):
        category_details = open(category_path + file_name)
    else:
        category_details = open(category_path + file_name + '.txt')

    return category_details.readline()

    category_details.close()


def read_cat_index(account_number, index):

    account_path = data_path + str(account_number) + '/'
    category_path = account_path + 'categories' + '/'

    available_categories = os.listdir(category_path)

    line = available_categories.index('.DS_Store')

    if index >= line:
        adj_index = index + 1
        file_name = available_categories[adj_index]
    else:
        file_name = available_categories[index]

    category_details = open(category_path + file_name)

    return category_details.readline()

    category_details.close()


def update_cat(account_number, name, budget, used):

    account_path = data_path + str(account_number) + '/'
    category_path = account_path + 'categories' + '/'
    file_name = name.lower() + '.txt'

    cat_update = open(category_path + file_name, 'w')

    data = name + ',' + str(budget) + ',' + str(used)
    cat_update.write(data)
    cat_update.close()
