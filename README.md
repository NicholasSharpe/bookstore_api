# bookstore_api
This is a simple Flask API where users can view, add, and delete books with HTTP requests.

## GET /books
If no query parameters are supplied this route will return all of the books.

This route has the following optional parameters:

| Parameter |     Type    | Valid Fields | Example | Description |
| --------- | ----------- | ------------ | ------- | ----------- |
| tags      | string      | any          | non-fiction,science,space | Will return books that have all of the listed tags |
| authors   | string      | any          | stephen+hawking,harper+lee | Will return books written by any of the listed authors |
| sortMethod | string     | title, author, releaseDate | title | Will sort the returned books on the given field |
| sortDirection | string | asc, desc | desc | Will determine the sort order of the retuned books(default ascending) |

## POST /books
Will add a new book.

Requires a JSON body with the following fields:

| field     |     Type    | Example |
| --------- | ----------- | ------- |
| title     | string      | "Pride and Prejudice" |
| author    | string      | "Jane Austen" |
| releaseDate | date      | "1813-01-28" |
| tags      | string[]    | ["fiction", "coming-of-age"] |

Example JSON body:
```
{
    "author": "Jane Austen",
    "tags": ["fiction", "coming-of-age"],
    "releaseDate": "1813-01-28",
    "title": "Pride and Prejudice"
}
```

## DELETE /books
Will delete a book.

This route has one required parameter:
| Parameter |     Type    | Valid Fields | Example | Description |
| --------- | ----------- | ------------ | ------- | ----------- |
| id        | int         | any          | 111980837600839165884765723879098819647 | The id of the book to be deleted |
