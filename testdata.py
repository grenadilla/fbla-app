#Test data to be used in databse
#Open in idle with exec(open('testdata.py').read())

from app import db, models
from decimal import Decimal
from sqlalchemy.exc import IntegrityError
import random
import forgery_py
import string

table = str.maketrans({key: None for key in string.punctuation})
random.seed()

def addData():
    ut = models.UserType.query.filter_by(name='student').first()
    u = models.User(name='Jeffrey', type=ut, total_fines=0)
    a = models.Author(name='John Smith')
    b = models.Book(title='Biography', author=a)
    c = models.Copy(book=b)
    db.session.add(u)
    db.session.add(a)
    db.session.add(b)
    db.session.add(c)

def add_author(num=1):
    for i in range(num):
        author = models.Author(name=forgery_py.name.full_name())
        db.session.add(author)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

def add_book(num=1):
    authors = models.Author.query.all()
    for i in range(num):
        book = models.Book(title=forgery_py.lorem_ipsum.title().translate(table), author=authors[random.randint(0,len(authors)-1)])
        for c in range(random.randint(1,5)):
            copy = models.Copy(book=book)
            db.session.add(copy)
        db.session.add(book)
    db.session.commit()


def deleteData():
    users = models.User.query.all()
    authors = models.Author.query.all()
    books = models.Book.query.all()
    for u in users:
        db.session.delete(u)
    for a in authors:
        db.session.delete(a)
    for b in books:
        db.session.delete(b)
