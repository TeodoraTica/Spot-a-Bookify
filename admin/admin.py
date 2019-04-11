import mysql.connector
import collections

Book = collections.namedtuple("Book", ["id", "title", "author", "genre", "read_count"])
User = collections.namedtuple("User", ["id", "username", "password", "first_name", "last_name", "email"])

config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'SpotABookify'
}


def user_to_string(user):
    return "ID: " + str(user.id) + "\nUsername: " + user.username + "\nFirst name: " + user.first_name + "\nLast name: " \
           + user.last_name + "\nEmail: " + user.email + "\n\n"


def book_to_string(book):
    return "\"" + book.title + "\" by  " + str(book.author) + " - " + str(book.genre) + "\n"


def get_registration_requests():
    requests = []

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM registrationRequests')
    for (registration_id, username, password, first_name, last_name, email) in cursor:
        requests.append(User(registration_id, username, password, first_name, last_name, email))

    cursor.close()
    connection.close()

    return requests


def get_book_recommendations():
    recommendations = []

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM bookRecommendations')
    for (recommendation_id, title, author, genre) in cursor:
        recommendations.append(Book(recommendation_id, title, author, genre, 0))

    cursor.close()
    connection.close()

    return recommendations


def get_table_size(table_name):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute(f'SELECT * FROM {table_name}')
    cursor.fetchall()
    count = cursor.rowcount

    cursor.close()
    connection.close()

    return count


def get_users_count():
    return get_table_size('users')


def get_book_count():
    return get_table_size('books')


def add_user(new_id, registration):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute(f'INSERT INTO users VALUES ({new_id}, \'{registration.username}\', \'{registration.password}\', '
                   f'\'{registration.first_name}\', \'{registration.last_name}\', \'{registration.email}\')')
    connection.commit()

    cursor.execute(f'DELETE FROM registrationRequests WHERE id = \'{registration.id}\'')
    connection.commit()

    cursor.close()
    connection.close()


def add_book(new_id, book):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    row_count = cursor.execute(f'SELECT * FROM books WHERE title = \'{book.title}\' and author = \'{book.author}\';')
    if row_count == 0:
        cursor.execute(f'INSERT INTO books VALUES ({new_id}, \'{book.title}\', \'{book.author}\',\'{book.genre}\', '
                       f'\'{book.read_count}\')')
        connection.commit()

    cursor.execute(f'DELETE FROM bookRecommendations WHERE id = \'{book.id}\'')
    connection.commit()

    cursor.close()
    connection.close()


if __name__ == '__main__':
    command_manual = 'Please choose one of the following commands: \n' \
                     '0 - Exit\n' \
                     '1 - See registration requests\n' \
                     '2 - Accept registration request\n' \
                     '3 - See books suggested by users\n' \
                     '4 - Accept suggested books\n'

    while True:
        command = int(input(command_manual))

        if command == 0:
            break

        elif command == 1:
            requests = get_registration_requests()
            for request in requests:
                print(user_to_string(request))

        elif command == 2:
            user_count = get_users_count()
            requests = get_registration_requests()
            for request in requests:
                answer = input('Do you want to add the following user? [Y/N]\n' + user_to_string(request))
                if answer.lower() == 'y':
                    add_user(user_count + 1, request)
                    user_count += 1

        elif command == 3:
            recommendations = get_book_recommendations()
            for recommendation in recommendations:
                print(book_to_string(recommendation))

        elif command == 4:
            print("TODO: Accept book suggestions")

        else:
            print("Incorrect command, please try again.\n")
