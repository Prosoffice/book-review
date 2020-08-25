A book review website. Users are able to register and then log in using their username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. I used a third-party API by Goodreads, another book review website, to pull in ratings from a broader audience. Finally, users will be able to query for book details and book reviews programmatically via Goodreads website’s API.

Users also have API access such that If users make a GET request to the website’s /api/<isbn> route, where <isbn> is an ISBN number, the website should return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score. The resulting JSON should follows the format:

{
    "title": "Memory",
    "author": "Doug Lloyd",
    "year": 2015,
    "isbn": "1632168146",
    "review_count": 28,
    "average_score": 5.0
}

