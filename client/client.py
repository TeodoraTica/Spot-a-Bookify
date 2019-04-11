import requests

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
            print("TODO: register\n")

        elif command == 2:
            print("TODO: login\n")

        else:
            print("Incorrect command, please try again.\n")

