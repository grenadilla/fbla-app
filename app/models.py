from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index=True, unique=True)
    books = db.relationship('Copy', backref='borrower')

    def __repr__(self):
        return '<User %r>' % (self.name)

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index=True, unique=True)
    books = db.relationship('Title', backref='author')

    def __repr__(self):
        return '<Author %r>' % (self.name)

class Book(db.Model):
    #Books are represented here, but they can have multiple unique copies
    #Get number of copies with len(copies)
    __tablename__='books'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(128), index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    copies = db.relationship('Copy', backref='book')

    def __repr__(self):
        return '<Book %r, id:%r>' % (self.title, self.id)

class Copy(db.Model):
    #Copy of a book, each has unique id different from the book id
    __tablename__ = 'copies'
    id = db.Column(db.Integer, primary_key = True)
    borrower_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    title = db.Column(db.String, db.ForeignKey('books.title')

    def __repr__(self):
        return '<Book-Copy %r, id:%r>' % (self.title_text, self.id)
