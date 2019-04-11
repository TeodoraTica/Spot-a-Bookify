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


def book_to_string(book):
    return "\"" + book.title + "\" by  " + book.author + " - " + book.genre + "\n"


def get_books() -> List[Book]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'SpotABookify'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM books')
    books = []
    for (id, title, author, genre, readCount) in cursor:
        book = Book(id, title, author, genre, readCount)
        books.append(book)
    cursor.close()
    connection.close()

    return books

@app.route('/login')
def get_optimal_route() -> str:
    source = request.args.get('username', type=str, default="")
    destination = request.args.get('password', type=str, default="")


@app.route('/')
def index() -> str:
    return json.dumps({'books': get_books()})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
