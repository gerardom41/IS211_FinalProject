# IS211_FinalProject
Final Project Book Catalogue
As a base I useded hw12 as the starting point since it already had a login, dashboard, database, html pages
The same /login route was used with the dashboard being renamed and made into a simple list
The database was modified to have only the basic table of books
The basics being title author page and rating
In the api function the use of param helped get the correct url
with a try catch errors due to key, index, type, and requests are catched
the first book matching is put into book_info which is then filtered for info
title authors page count and rating are filtered with rating using get since some dont have 
A regex of 13 digits which is the isbn length is used as basic filter on submit
authors are converted into a string from a list
after the info has been filtered and passed through it gets inserted
The delete route used a dropdown menu in the html for ease of use
The title value is passed into the database to then be deleted
The database set up is mostly copied from hw 12
Connecting to a file with .db, creating tables based of a schema, clearing tables on start
Read data and count items are helper functions that help the database get the correct info and keep the id count to the items in the database 
