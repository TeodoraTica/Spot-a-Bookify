from copy import deepcopy
from flask import Flask
from flask import request
from typing import List, Dict
import collections
import mysql.connector
import json
import sys
import random
import string

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


def book_to_string(book):
    return "\"" + book.title + "\" by  " + book.author + " - " + book.genre + "\n"


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


@app.route('/register')
def register():
    username = request.args.get('username', type=str, default="")
    password = request.args.get('password', type=str, default="")
    first_name = request.args.get('firstName', type=str, default="")
    last_name = request.args.get('lastName', type=str, default="")
    email = request.args.get('email', type=str, default="")

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')

    found = False
    for (_, un, _, _, _, _) in cursor:
        if username == un:
            sessions.append(username)
            found = True
            break

    if found:
        cursor.close()
        connection.close()
        return "1-Username already reserved. Please choose another one."

    cursor.execute('SELECT * FROM registrationRequests')

    found = False
    for (_, un, pw, _, _, _) in cursor:
        if username == un and password == pw:
            found = True
            break

    if found:
        cursor.close()
        connection.close()
        return "3-There is another pending registration request for this username."

    reg_count = get_registration_requests_count()

    cursor.execute(
        f'INSERT INTO registrationRequests VALUES '
        f'({reg_count + 1}, \'{username}\', \'{password}\', \'{first_name}\', \'{last_name}\', \'{email}\')')

    cursor.commit()

    cursor.close()
    connection.close()

    return "4-Your registration request has been recorded."


@app.route('/login')
def login() -> str:
    username = request.args.get('username', type=str, default="")
    password = request.args.get('password', type=str, default="")

    if username in sessions:
        return "1-You are already logged in."

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')

    found = False
    for (_, un, pw, _, _, _) in cursor:
        if username == un and password == pw:
            sessions.append(username)
            found = True
            break

    if found:
        cursor.close()
        connection.close()
        return "2-Welcome!"

    cursor.execute('SELECT * FROM registrationRequests')

    found = False
    for (_, un, pw, _, _, _) in cursor:
        if username == un and password == pw:
            found = True
            break

    if found:
        cursor.close()
        connection.close()
        return "3-Your registration request is pending approval."

    cursor.close()
    connection.close()

    return "4-Invalid username or password. Please try again or register."


@app.route('/logout')
def logout() -> str:
    username = request.args.get('username', type=str, default="")

    if username in sessions:
        return "You have successfully logged out."

    return "You were not logged in."


@app.route('/')
def index() -> str:
    return json.dumps({'books': get_books()})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
