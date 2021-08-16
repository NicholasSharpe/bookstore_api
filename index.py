from flask import Flask, jsonify, request, make_response
from marshmallow import schema, ValidationError

from model.book import Book, BookSchema
from model.filter_type import FilterType

import json
import datetime as dt

app = Flask(__name__)

SORTING_METHODS = ['author', 'releaseDate', 'title']

SORTING_DIRECTIONS = ['desc', 'asc']

bookList = [
    Book('1984', 'George Orwell', ['dystopian', 'fiction'], dt.date(1949, 6, 8)),
    Book('To Kill a Mocking Bird', 'Harper Lee', ['thriller', 'law', 'fiction'], dt.date(1960, 7, 11)),
    Book('The Great Gatsby', 'F. Scott Fitzgerald', ['tragedy', 'party', 'fiction'], dt.date(1925, 4, 10)),
    Book('The Catcher in the Rye', 'J. D. Salinger', ['coming-of-age', 'life lessons', 'fiction'], dt.date(1951, 7, 16)),
    Book('The Lord of the Rings', 'J. R. R. Tolkien', ['fantasy', 'fiction'], dt.date(1954, 7, 29)),
    Book('Sapiens: A Brief History of Humankind', 'Yuval Noah Harari', ['history', 'non-fiction'], dt.date(2011, 1, 1)),
    Book('Educated', 'Tara Westover', ['biography', 'non-fiction'], dt.date(2018, 2, 18)),
    Book('In Cold Blood', 'Truman Capote', ['true crime', 'non-fiction'], dt.date(1965, 1, 1)),
    Book('Between the World and Me', 'Ta-Nehisi Coates', ['non-fiction', 'biography'], dt.date(2015, 7, 14)),
    Book('A Brief History of Time', 'Stephen Hawking', ['non-fiction'], dt.date(1988, 1, 1))
]

@app.route('/books')
def get_books():

    responseBookList = []
    filters = []
    tags = []
    authors = []
    sortMethod = ""
    sortDirection = ""

    # Get filter arguments
    tagsStr = request.args.get('tags')
    if tagsStr is not None:
        tags = tagsStr.split(",")
        filters.append(FilterType.TAGS)
    authorsStr = request.args.get('authors')
    if authorsStr is not None:
        authors = authorsStr.split(",")
        filters.append(FilterType.AUTHORS)

    # Get sorting arguments
    sortMethod = request.args.get('sortMethod')
    if sortMethod is not None and sortMethod not in SORTING_METHODS:
        return json_response({ "error": "Not a valid sorting method. Try: {}".format(SORTING_METHODS) }, 400)
    sortDirection = request.args.get('sortDirection')
    if sortDirection is not None and sortDirection not in SORTING_DIRECTIONS:
        return json_response({ "error": "Not a valid sorting direction. Try: {}".format(SORTING_DIRECTIONS) }, 400)

    # If there are filters, filter the books
    if len(filters) == 0:
        responseBookList = bookList
    else:
        if FilterType.TAGS in filters:
            responseBookList = list(filter(lambda book: all(tag in book.tags for tag in tags), bookList))       
        if FilterType.AUTHORS in filters:
            responseBookList = list(filter(lambda book: book.author.lower() in map(str.lower, authors), (responseBookList if len(responseBookList) > 0 else bookList)))

    # Sort the list
    sortBool = True if sortDirection == SORTING_DIRECTIONS[0] else False
    if sortMethod is not None:
        if sortMethod == SORTING_METHODS[0]: # Author
            responseBookList.sort(key = lambda x: x.author, reverse=sortBool)
        elif sortMethod == SORTING_METHODS[1]: # Release Date
            responseBookList.sort(key = lambda x: x.releaseDate, reverse=sortBool)
        elif sortMethod == SORTING_METHODS[2]: # Title
            responseBookList.sort(key = lambda x: x.title, reverse=sortBool)
 
    # Send json response with requested books
    schema = BookSchema(many=True)
    response = schema.dump(responseBookList)
    return jsonify(response)

@app.route('/books', methods=['POST'])
def add_book():
    try:
        book = BookSchema().load(request.get_json())
    except ValidationError as err:
        return json_response(err.messages, 400)

    for b in bookList:
        if book.title == b.title:
            return json_response({"error": "Book already exists!"}, 400)

    bookList.append(book)
    return json_response({ "bookAdded": True }, 200)

@app.route('/books', methods=['DELETE'])
def delete_book():

    # Get id
    id = int(request.args.get('id'))

    # Look for book using id
    for book in bookList:
        if book.id == id:
            bookList.remove(book)
            return json_response({ "message": "{} removed".format(book.title)}, 200)
    
    # Return 404 if book is not found
    return json_response({ "error" : "Book not found"}, 404)

def json_response(message: json, code: int):
    response = make_response(jsonify(message), code)
    response.headers["Content-Type"] = "application/json"
    return response 