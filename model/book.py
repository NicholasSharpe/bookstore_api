import datetime as dt
import uuid

from marshmallow import Schema, fields
from marshmallow.decorators import post_load

class Book():
    def __init__(self, title: str, author: str, tags: list[str], releaseDate: dt.date):
        self.id = uuid.uuid4().int
        self.title = title
        self.author = author
        self.tags = tags
        self.releaseDate = releaseDate

    def __repr__(self):
        return '<Book(name={self.title!r})>'.format(self=self)

class BookSchema(Schema):
    id = fields.Int()
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    tags = fields.List(fields.String, attribute="tags")
    releaseDate = fields.Date(required=True)

    @post_load
    def make_book(self, data, **kwargs):
        return Book(**data)
        