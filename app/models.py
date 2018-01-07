from app import db
import datetime
from sqlalchemy.ext.hybrid import hybrid_property #, hybrid_method

class UserType(db.Model):
    __tablename__ = 'usertypes'
    id = db.Column(db.Integer, primary_key=True)
    #Add back unique=True later
    name = db.Column(db.String(16), index=True, unique=True)
    borrow_length = db.Column(db.Interval())
    fine = db.Column(db.Integer())
    book_limit = db.Column(db.Integer())
    users = db.relationship('User', backref='usertype')

    def dec_fine(self):
        return self.fine / 100

    def __repr__self(self):
        return '<UserType %r' % (self.name)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    total_fines = db.Column(db.Integer())
    # Need to recalculate overdue_fines with overdue_fines() every time you access it
    overdue_fines = db.Column(db.Integer())
    books = db.relationship('Copy', backref='borrower')
    type_name = db.Column(db.String, db.ForeignKey('usertypes.name'))

    def dec_total_fines(self):
        return self.total_fines / 100

    def overdue_num(self):
        num = 0
        for copy in self.books:
            if datetime.datetime.utcnow() > copy.return_time:
                num += 1
        return num

    def calc_overdue_fines(self):
        fine = 0
        for copy in self.books:
            fine += copy.calc_fine(self.usertype.fine)
        return fine
    
    def __repr__(self):
        return '<User %r>' % (self.name)


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    books = db.relationship('Book', backref='author')

    def __repr__(self):
        return '<Author %r>' % (self.name)


class Book(db.Model):
    #Books are represented here, but they can have multiple unique copies
    #Get number of copies with len(copies)
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    copies = db.relationship('Copy', backref='book')

    def available(self):
        available = 0
        for copy in self.copies:
            if copy.borrower is None:
                available += 1
        return available

    def __repr__(self):
        return '<Book %r, id:%r>' % (self.title, self.id)


class Copy(db.Model):
    #Copy of a book, each has unique id different from the book id
    __tablename__ = 'copies'
    id = db.Column(db.Integer, primary_key=True)
    borrower_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    borrow_time = db.Column(db.DateTime)
    return_time = db.Column(db.DateTime)
    #title = db.Column(db.String, db.ForeignKey('books.title'))

    def is_overdue(self):
        return datetime.datetime.utcnow() > self.return_time

    def time_left(self, absolute=False):
        #Creates timedelta. Note that the function converts the result to positive
        time_left = self.return_time - datetime.datetime.utcnow()
        if absolute:
            return (str(abs(time_left.days)) + " days, " + str(int(time_left.seconds/3600)) 
                    + " hours")
        if time_left.days < 0:
            return "Overdue"
        return (str(time_left.days) + " days, " + str(int(time_left.seconds/3600)) 
                + " hours")


    def calc_fine(self, fine):
        # Given fine in cents per day, calculates fine on book
        if self.return_time is None:
            return 0
        delta = datetime.datetime.utcnow() - self.return_time
        if delta > datetime.timedelta(0):
            return (delta.days + 1) * fine
        return 0

    def __repr__(self):
        return '<Book-Copy %r, id:%r>' % (self.book.title, self.id)
