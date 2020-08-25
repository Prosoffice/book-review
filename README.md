# This simple web app was developed for the CS50 Web Programming with Python and Javascript course. This is a simple web application for book reviewing.

Users are able to register and then log in using their username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. I used a third-party API by Goodreads, another book review website, to pull in ratings from a broader audience. Finally, users will be able to query for book details and book reviews programmatically via Goodreads website’s API.

Users also have API access such that If a user make a GET request to the website’s ```/api/<isbn> route``` where ```<isbn>``` is an ISBN number, the website returns a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score. The resulting JSON should follows the format:
```
{
    "title": "Memory",
    "author": "Doug Lloyd",
    "year": 2015,
    "isbn": "1632168146",
    "review_count": 28,
    "average_score": 5.0
}
```
## Objectives
- Getting Comfy with Flask Web development
- Practice with SQL and POSTGRESQL
- Get started with API requests and development

## Getting started
To use this project, first git clone this repository and install the requirements by using:
```
pip3 install -r requirements.txt
```
This will install Flask and other dependencies.

You need to tell Flask which file will run the application. If you are using Linux:
```
export FLASK_APP=application.py
```
I've used a PostgreSQL database hosted locally on my machine for this project, but you can host the database on your own computer if you want. Just remember to create a .env file containing the link to this database and, if you want to use integration with Goodreads API, also an API key, as the following:
```
DATABASE_URL=your_database_url
GOODREADS_KEY=your_goodreads_key
```
Remember not to leave a space before and after the equality sign as shown above

I've created a simple Python script called import.py for uploading the .csv data to the database. This script performance is not optimal and there are about 5000 rows in the csv file, so it may take some time uploading all rows.

After the database is set, you can start the web app by running:
```
flask run
or
python application.py
```
The front-end for this web application is very simple and not user friendly at all. My main goal with this project was just learning more about the back-end and getting used with databases and Flask web development.

I may come back in the future and upload some new designs, and also add new features ;).





