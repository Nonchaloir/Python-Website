from sqlite3 import *

db = connect('DataBase.db')
c = db.cursor()


# Creating Consumer table
c.execute('''CREATE TABLE Consumer (\
Consumer_ID INTEGER NOT NULL, email TEXT, password TEXT NOT NULL,\
name TEXT NOT NULL, username TEXT NOT NULL, login TEXT, balance INTEGER,\
PRIMARY KEY(Consumer_ID));''')

#Creating Artist table
c.execute('''CREATE TABLE Artist (\
Artist_ID INTEGER NOT NULL, email TEXT, password TEXT NOT NULL,\
name TEXT NOT NULL, username TEXT NOT NULL, login TEXT, balance INTEGER,\
PRIMARY KEY(Artist_ID));''')

#Creating Song table
c.execute('''CREATE TABLE Songs (\
Song_ID INTEGER NOT NULL, artist_id TEXT NOT NULL, name_of_song TEXT NOT NULL,\
picture TEXT, youtube_link TEXT,audio TEXT,\
PRIMARY KEY(Song_ID),\
FOREIGN KEY(artist_id) REFERENCES Artist(Artist_ID));''')

#Creating Donation table
c.execute('''CREATE TABLE Donation (\
Donation_ID INTEGER NOT NULL, UserID INTEGER NOT NULL, SongID INTEGER NOT NULL,\
Price INTEGER NOT NULL, Comment TEXT, collected TEXT,\
PRIMARY KEY(Donation_ID), \
FOREIGN KEY(UserID) REFERENCES Consumer(Consumer_ID),\
FOREIGN KEY(SongID) REFERENCES Song(Song_ID));''')





db.commit()
db.close()
