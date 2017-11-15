#Test data to be used in databse
#Open in idle with exec(open('testdata.py').read())

from app import db, models

def addData():
    u = models.User(name='jeff')
    a = models.Author(name='arthur')
    b = models.Book(title='Testy Book', borrower = u, author = a)
    db.session.add(u)
    db.session.add(a)
    db.session.add(b)

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
