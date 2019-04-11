CREATE DATABASE SpotABookify;
use SpotABookify;

-- Users evidence
CREATE TABLE users (
id int NOT NULL,
username varchar(25) NOT NULL,
password varchar(32) NOT NULL,
firstName varchar(50) NOT NULL,
lastName varchar(50) NOT NULL,
email varchar(200) NOT NULL
);

ALTER TABLE users ADD PRIMARY KEY (id);


-- Users registration requests
CREATE TABLE registrationRequests (
id int NOT NULL,
username varchar(25) NOT NULL,
password varchar(32) NOT NULL,
firstName varchar(50) NOT NULL,
lastName varchar(50) NOT NULL,
email varchar(200) NOT NULL
);

ALTER TABLE registrationRequests ADD PRIMARY KEY (id);

INSERT INTO registrationRequests (id, username, password, firstName, lastName, email) VALUES
(1, 'cutarica_cutare', 'password1', 'Cutarica', 'Cutarel', 'cutaricaCutarel@gmail.com'),
(2, 'anonX', 'password2', 'Anonimus', 'Xulescu', 'anX@gmail.com');


-- Books evidence
CREATE TABLE books (
id int NOT NULL,
title varchar(250) NOT NULL,
author int NOT NULL,
genre int NOT NULL,
readCount int NOT NULL
);

ALTER TABLE books ADD PRIMARY KEY (id);

INSERT INTO books (id, title, author, genre, readCount) VALUES
(1, 'Harry Potter and the Scorcerer\s Stone', 1, 1, 0),
(2, 'Harry Potter and the Chamber of Secrets', 1, 1, 0),
(3, 'Harry Potter and the Prisoner of Azkaban', 1, 1, 0),
(4, 'Harry Potter and the Goblet of Fire', 1, 1, 0),
(5, 'Harry Potter and the Order of the Phoenix', 1, 1, 0),
(6, 'Harry Potter and the Half-Blood Prince', 1, 1, 0),
(7, 'Harry Potter and the Deadly Hollows', 1, 1, 0),
(8, 'The Three Musketeers', 3, 3, 0),
(9, 'For Whom the Bells Toll', 4, 4, 0),
(10, 'Never Let Me Go', 5, 4, 0),
(11, 'The Chronicles of Narnia', 6, 1, 0),
(12, 'Ender\s Game', 2, 2, 0),
(13, 'Speaker for the Dead', 2, 2, 0),
(14, 'Xenocide', 2, 2, 0),
(15, 'The Hobbit', 7, 1, 0),
(16, 'The Fellowship of the Ring', 7, 1, 0),
(17, 'The Two Towers', 7, 1, 0),
(718, 'The Return of The King', 7, 1, 0);


CREATE TABLE bookRecommendations (
id int NOT NULL,
title varchar(250) NOT NULL,
author int NOT NULL,
genre int NOT NULL
);

INSERT INTO bookRecommendations (id, title, author, genre) VALUES
(1, 'Old Man and the Sea', 4, 4),
(2, 'Ender\s Shadow', 2, 2),
(3, 'Remains of the day', 5, 4),
(4, 'Old Man and the Sea', 4, 4);

-- Authors evidence
CREATE TABLE authors (
id int NOT NULL,
name varchar(50) NOT NULL,
nationality varchar(30) NOT NULL
);

ALTER TABLE authors ADD PRIMARY KEY (id);

INSERT INTO authors (id, name, nationality) VALUES
(1, 'J. K. Rowlling', 'British'),
(2, 'Orson Scott Card', 'American'),
(3, 'Alexandre Dumas', 'French'),
(4, 'Ernest Hemingway', 'American'),
(5, 'Kazuo Ishiguro', 'Japanese'),
(6, 'C. S. Lewis', 'British'),
(7, 'J. R. R. Tolkien', 'British');


-- Genres evidence
CREATE TABLE genres (
id int NOT NULL,
name varchar(50) NOT NULL
);

ALTER TABLE genres ADD PRIMARY KEY(id);

INSERT INTO genres (id, name) VALUES
(1, 'fantasy'),
(2, 'SF'),
(3, 'Adventure'),
(4, 'Drama'),
(5, 'Romance');


-- Reads evidence
CREATE TABLE readsEvidence (
idReader int NOT NULL,
idBook int NOT NULL
);
