import requests
import getpass

un = ""
logged_in = False


def register(username, password, first_name, last_name, email):
    url = 'http://app:5000/register?username=' + username + \
          '&password=' + password + \
          '&firstName=' + first_name + \
          '&lastName=' + last_name + \
          '&email=' + email
    request = requests.get(url)
    print(request.text)


def login(username, password):
    url = 'http://app:5000/login?username=' + username + \
          '&password=' + password
    request = requests.get(url)
    print(request.text)


def logout():
    print("todo")


if __name__ == '__main__':
    command_manual = 'Please choose one of the following commands: \n' \
                     '0 - Exit\n' \
                     '1 - Register\n' \
                     '2 - Login\n'
    home_command_manual = 'Please choose one of the following commands: \n' \
                          '0 - Exit\n' \
                          '1 - Add a book\n' \
                          '2 - Get suggestion\n'

    while True:
        command = int(input(command_manual))

        if command == 0:
            break

        elif command == 1:
            first_name = input("First name:")
            last_name = input("Last name:")
            email = input("Email:")
            username = input("Username:")
            password = getpass.getpass("Password:")

            register(username, password, first_name, last_name, email)

        elif command == 2:
            username = input("Username:")
            password = getpass.getpass("Password:")

            login(username, password)

            if logged_in:
                break

        else:
            print("Incorrect command, please try again.\n")
