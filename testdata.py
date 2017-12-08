#Test data to be used in databse
#Open in idle with exec(open('testdata.py').read())

from app import db, models
from decimal import Decimal

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
