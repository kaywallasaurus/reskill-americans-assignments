import os

# variables

data_path = 'atm-data/'
auth_path = data_path + 'auth-session.txt'
all_users = os.listdir(data_path)

# functions


def create(account_number, first_name, last_name, email, password):
    global saved_info

    user_details = str(account_number) + ',' + first_name + ',' + last_name\
        + ',' + email + ',' + password + ',' + str(0)

    if does_account_exist(account_number):
        return False

    if does_email_exist(email):
        return False

    try:
        saved_info = open(data_path + str(account_number) + '.txt', 'x')
    except FileExistsError:
        print('This account already exists. Please try again.')
        return False
    else:
        saved_info.write(user_details)
    finally:
        saved_info.close()
        return True


def does_account_exist(account_number):

    for user in all_users:

        if user == str(account_number) + '.txt':
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
            split_user_data = str.split(read(user), ',')

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


def read(file_name):

    try:
        if str(file_name).endswith('.txt'):
            current_details = open(data_path + file_name)
        else:
            current_details = open(data_path + str(file_name) + '.txt')
    except FileNotFoundError:
        print('We were unable to locate your information. Please try again.')
        return False
    else:
        return current_details.readline()
    finally:
        current_details.close()


def create_auth_session(raw_user):

    auth_session = open(auth_path, 'x')
    auth_session.write(raw_user)
    auth_session.close()


def update_auth(current_user):

    auth_session = open(auth_path, 'w')
    auth_session.write(current_user)
    auth_session.close()


def update_user_data(account_number):

    user_file = open(data_path + str(account_number) + '.txt', 'w')
    session_data = read('auth-session.txt')

    if session_data:
        user_file.write(session_data)
        user_file.close()
    else:
        print('Something went wrong. Please log out and try again.')


def update_both(current_user, account_number):
    update_auth(current_user)
    update_user_data(account_number)


def delete_auth_session():

    os.remove(auth_path)
