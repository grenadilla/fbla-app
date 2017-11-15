from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index=True, unique=True)
    books = db.relationship('Book', backref='borrower')

    def __repr__(self):
        return '<User %r>' % (self.name)

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index=True, unique=True)
    books = db.relationship('Book', backref='author')

    def __repr__(self):
        return '<Author %r>' % (self.name)

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(128), index=True)
    borrower_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __repr__(self):
        return '<Book %r, id:%r>' % (self.title, self.id)
