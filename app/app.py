from flask import Flask
from flask import request
from typing import List, Dict
import collections
import mysql.connector
import json
import numpy

app = Flask(__name__)

DATABASE_NAME = "SpotABookify"

Book = collections.namedtuple("Book", ["id", "title", "author", "genre", "readCount"])

sessions = []

config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'SpotABookify'
}

authors_dict = {}
genres_dict = {}


def strip_symbols(s):
    s = ''.join(c for c in s if c.isalpha())
    return s.lower()


def set_up():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM authors")
    for (author_id, name, _) in cursor:
        authors_dict[author_id] = name

    cursor.execute("SELECT * FROM genres")
    for (genre_id, name, ) in cursor:
        genres_dict[genre_id] = name

    cursor.close()
    connection.close()


def get_author_id(author):
    author_id = -1
    for k, v in authors_dict.items():
        if strip_symbols(author) in strip_symbols(v):
            author_id = k
            return author_id

    return author_id


def get_genre_id(genre):
    genre_id = -1
    for k, v in genres_dict.items():
        if strip_symbols(genre) == strip_symbols(v):
            genre_id = k
            return genre_id
    return genre_id


def get_user_id(username):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')

    found = False
    for (user_id, un, _, _, _, _) in cursor:
        if username == un:
            sessions.append(username)
            return user_id

    cursor.close()
    connection.close()


def get_book_id(title, author, genre):
    books = get_books()
    for book in books:
        if strip_symbols(book.title) == strip_symbols(title) \
                and strip_symbols(author) in strip_symbols(book.author) \
                and strip_symbols(book.genre) == strip_symbols(genre):
            return book.id
    return -1


def username_exists(username):
    user_id = get_user_id(username)
    if user_id < 0:
        return False
    return True


def book_to_string(book):
    return "\"" + book.title + "\" by " + authors_dict[book.author] + ", " + genres_dict[book.genre] + "\n"


def get_table_size(table_name):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute(f'SELECT * FROM {table_name}')
    cursor.fetchall()
    count = cursor.rowcount

    cursor.close()
    connection.close()

    return count


def get_registration_requests_count():
    return get_table_size('registrationRequests')


def get_books() -> List[Book]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM books')
    books = []
    for (book_id, title, author, genre, readCount) in cursor:
        book = Book(book_id, title, author, genre, readCount)
        books.append(book)
    cursor.close()
    connection.close()

    return books


def get_distribution_by_popularity(books):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    read_counts = {}
    total_reads = 0

    for book in books:
        read_counts[book.id] = 0

    cursor.execute('SELECT * FROM readsEvidence')
    for (reader_id, book_id) in cursor:
        read_counts[book_id] = read_counts.get(book_id, 0) + 1
        total_reads += 1

    cursor.close()
    connection.close()

    reads = []
    for book in books:
        reads.append(read_counts[book.id])

    if total_reads == 0:
        reads[numpy.random.choice(len(reads))] = 1
        total_reads = 1

    return list(map(lambda r: r / total_reads, reads))


def get_distribution_by_author(books, author):
    author_id = get_author_id(author)
    if author_id < 0:
        author_id = 0

    books_by_author = [book for book in books if book.author == author_id]

    return books_by_author


def get_distribution_by_genre(books, genre):
    genre_id = get_genre_id(genre)
    if genre_id < 0:
        genre_id = 0

    books_by_genre = [book for book in books if book.genre == genre_id]

    return books_by_genre


def get_distribution_by_country(books, nationality):
    authors = []
    books_by_nationality = []

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute(f'SELECT * FROM authors WHERE nationality=\'{nationality}\'')
    for (author_id, _, _) in cursor:
        authors.append(author_id)

    cursor.close()
    connection.close()

    for author_id in authors:
        books_by_nationality += [book for book in books if book.author == author_id]

    return books_by_nationality


def add_registration_request(reg_id, username, password, first_name, last_name, email):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute(
        f'INSERT INTO registrationRequests VALUES '
        f'({reg_id}, \'{username}\', \'{password}\', \'{first_name}\', \'{last_name}\', \'{email}\')')

    connection.commit()

    cursor.close()
    connection.close()


def add_read_evidence(book_id, username):
    user_id = get_user_id(username)
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute(
        f'INSERT INTO readsEvidence VALUES '
        f'({user_id}, {book_id})')

    connection.commit()

    cursor.close()
    connection.close()


def add_book_recommendation(title, author, genre):
    count = get_table_size('bookRecommendations')
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute(
        f'INSERT INTO bookRecommendations VALUES '
        f'({count + 1}, \'{title}\', {author}, {genre})')

    connection.commit()

    cursor.close()
    connection.close()


def add_author_recommendation(author, nationality):
    count = get_table_size('authorRecommendations')
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute(
        f'INSERT INTO authorRecommendations VALUES '
        f'({count + 1}, \'{author}\', \'{nationality}\')')

    connection.commit()

    cursor.close()
    connection.close()


def add_genre_recommendation(genre):
    count = get_table_size('genreRecommendations')
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute(
        f'INSERT INTO genreRecommendations VALUES '
        f'({count + 1}, \'{genre}\')')

    connection.commit()

    cursor.close()
    connection.close()


def pending_registration(username, email):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM registrationRequests')

    found = False
    for (_, un, _, _, _, em) in cursor:
        if username == un and email == em:
            found = True
            break

    cursor.close()
    connection.close()

    return found


def can_login(username, password):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')

    found = False
    for (_, un, pw, _, _, _) in cursor:
        if username == un and password == pw:
            sessions.append(username)
            found = True
            break

    cursor.close()
    connection.close()

    return found


@app.route('/register')
def register():
    username = request.args.get('username', type=str, default="")
    password = request.args.get('password', type=str, default="")
    first_name = request.args.get('firstName', type=str, default="")
    last_name = request.args.get('lastName', type=str, default="")
    email = request.args.get('email', type=str, default="")

    if username_exists(username) is True:
        return "1-Username already reserved. Please choose another one."

    if pending_registration(username, email):
        return "3-There is another pending registration request for this username."

    reg_count = get_registration_requests_count()

    add_registration_request(reg_count + 1, username, password, first_name, last_name, email)

    return "4-Your registration request has been recorded."


@app.route('/login')
def login() -> str:
    username = request.args.get('username', type=str, default="")
    password = request.args.get('password', type=str, default="")

    if username in sessions:
        return "1-You are already logged in."

    if can_login(username, password):
        return "2-Welcome!"

    return "3-Invalid username or password. Please try again or register."


@app.route('/logout')
def logout() -> str:
    username = request.args.get('username', type=str, default="")

    if username in sessions:
        sessions.remove(username)
        return "1-You have successfully logged out."

    return "2-You were not logged in."


@app.route('/get_suggestion')
def get_suggestion() -> str:
    option1 = request.args.get('option1', type=int, default=0)
    option2 = request.args.get('option2', type=str, default="")

    set_up()
    books = get_books()

    if option1 == 0:
        suggestion = books[numpy.random.choice(len(books))]
    elif option1 == 1:
        suggestion = books[numpy.random.choice(len(books), p=get_distribution_by_popularity(books))]
    elif option1 == 2:
        books_by_author = get_distribution_by_author(books, option2)
        suggestion = books_by_author[numpy.random.choice(len(books_by_author))]
    elif option1 == 3:
        books_by_genre = get_distribution_by_genre(books, option2)
        suggestion = books_by_genre[numpy.random.choice(len(books_by_genre))]
    elif option1 == 4:
        books_by_country = get_distribution_by_country(books, option2)
        suggestion = books_by_country[numpy.random.choice(len(books_by_country))]

    return f'0-Based on your previous reads, we recommend:\n{book_to_string(suggestion)}'


@app.route('/add_book')
def add_book() -> str:
    title = request.args.get('title', type=str, default="")
    author = request.args.get('author', type=str, default="")
    genre = request.args.get('genre', type=str, default="")
    nationality = request.args.get('nationality', type=str, default="")
    username = request.args.get('username', type=str, default="")
    set_up()

    author_id = get_author_id(author)
    genre_id = get_genre_id(genre)
    book_id = get_book_id(title, author_id, genre_id)

    if book_id >= 0:
        add_read_evidence(book_id, username)
        return '0-Your book has been successfully added'

    message = ''
    if author_id < 0:
        add_author_recommendation(author, nationality)
        message = '1-Unfortunately your book could not be added because our database lacks ' \
                  'either the author or genre. Please try again later!'

    if genre_id < 0:
        add_genre_recommendation(genre)
        message = '1-Unfortunately your book could not be added because our database lacks ' \
                  'either the author or genre. Please try again later!'

    if len(message) == 0:
        add_book_recommendation(title, author_id, genre_id)
        return '2-Thanks for your suggestions! We did not know about this book yet, but we will ' \
               'add it to our data base'

    return message


@app.route('/get_reads')
def get_reads() -> str:
    username = request.args.get('username', type=str, default="")

    set_up()
    books = get_books()

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    user_id = get_user_id(username)
    message = '0-'

    cursor.execute(f'SELECT * FROM readsEvidence WHERE idReader={user_id}')
    for (_, book_id) in cursor:
        for book in books:
            if book.id == book_id:
                message += book_to_string(book)

    cursor.close()
    connection.close()

    return message


@app.route('/')
def index() -> str:
    return json.dumps({'books': get_table_size('authorRecommendations')})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
