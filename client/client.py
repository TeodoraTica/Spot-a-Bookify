import requests
import getpass

un = ""
logged_in = False


def parse_response(response):
    tokens = response.split("-")

    if len(tokens) != 2:
        return -1, "[Internal error] Wrong response format"

    return int(tokens[0], 10), tokens[1]


def register(username, password, first_name, last_name, email):
    url = 'http://app:5000/register?username=' + username + \
          '&password=' + password + \
          '&firstName=' + first_name + \
          '&lastName=' + last_name + \
          '&email=' + email
    request = requests.get(url)
    code, message = parse_response(request.text)
    print(message)

    if code != 4:
        return False

    return True


def login(username, password):
    url = 'http://app:5000/login?username=' + username + \
          '&password=' + password
    request = requests.get(url)
    code, message = parse_response(request.text)
    print(message)

    if code != 2 and code != 1:
        return False

    return True


def request_suggestion(option1, option2):
    url = 'http://app:5000/get_suggestion?option1=' + str(option1) +'&option2=' + option2
    request = requests.get(url)
    code, message = parse_response(request.text)

    print(message)


def add_book(title, author, genre, nationality):
    url = 'http://app:5000/add_book?title=' + title \
          + '&author=' + author \
          + '&genre=' + genre \
          + '&nationality=' + nationality \
          + '&username=' + un
    request = requests.get(url)
    code, message = parse_response(request.text)

    print(message)


def get_reads():
    url = 'http://app:5000/get_reads?username=' + un
    request = requests.get(url)
    code, message = parse_response(request.text)

    print(message)


def logout(username):
    url = 'http://app:5000/logout?username=' + username
    request = requests.get(url)
    code, message = parse_response(request.text)
    print(message)


def main():
    global logged_in
    global un

    command_manual = 'Please choose one of the following commands: \n' \
                     '0 - Exit\n' \
                     '1 - Register\n' \
                     '2 - Login\n'
    home_command_manual = 'Please choose one of the following commands: \n' \
                          '0 - Logout\n' \
                          '1 - Add a book\n' \
                          '2 - Get suggestion\n' \
                          '3 - See your previous reads\n'

    command = int(input(command_manual))
    while True:
        if command == 0:
            break

        elif command == 1:
            first_name = input("First name: ")
            last_name = input("Last name: ")
            email = input("Email: ")
            username = input("Username:")
            password = getpass.getpass("Password: ")

            success = register(username, password, first_name, last_name, email)

            if success is False:
                print("Please try again!")

        elif command == 2:
            username = input("Username:")
            password = getpass.getpass("Password:")

            success = login(username, password)

            if success is True:
                logged_in = True
                un = username
                break
            else:
                print("Please try again!")

        else:
            print("Incorrect command, please try again.\n")

        command = int(input(command_manual))

    if command == 0:
        return 0

    while True:
        command = int(input(home_command_manual))

        if command == 0:
            if logged_in is True:
                logout(un)
                logged_in = False
            break
        elif command == 1:
            title = input("Title: ")
            author = input("Author: ")
            genre = input("Genre: ")
            nationality = input("Nationality of the author: ")

            add_book(title, author, genre, nationality)

        elif command == 2:
            options = 'Would you like to select a criteria?\n' \
                      '0 - None\n' \
                      '1 - Popularity\n' \
                      '2 - Author\n' \
                      '3 - Genre\n' \
                      '4 - Nationality of the author\n'
            option1= int(input(options))
            option2 = ""

            if option1 == 2:
                option2 = input("Please specify the author: ")
            elif option1 == 3:
                option2 = input("Please specify the genre: ")
            elif option1 == 4:
                option2 = input("Please specify the nationality of the author: ")

            request_suggestion(option1, option2)

        elif command == 3:
            get_reads()

        else:
            print("Incorrect command, please try again.\n")


if __name__ == '__main__':
    main()
