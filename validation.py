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
