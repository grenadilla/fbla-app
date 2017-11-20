from flask import render_template, session, redirect, url_for, flash, request
from sqlalchemy import func
from app import app, db, models, forms

# create tables for author query if tables do not exist
db.create_all()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    #add below login stuff to all pages
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(url_for('index'))
    return render_template('index.html', login=login)


@app.route('/user/<id>', methods=['GET', 'POST'])
def user(id):
    #Given an id, queries it from db and passes user object to page
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())

    user = models.User.query.filter_by(id=id).first()
    return render_template('userinfo.html', user=user, login=login)

@app.route('/author/<id>', methods=['GET','POST'])
def author(id):
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())

    author = models.Author.query.filter_by(id=id).first()
    return render_template('authorinfo.html', author=author, login=login)


@app.route('/book/<id>', methods=['GET', 'POST'])
def book(id):
    #Book info page, from here can borrow a book
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())

    book = models.Book.query.filter_by(id=id).first()
    return render_template('bookinfo.html', book=book, login=login)


@app.route('/borrow/<id>', methods=['GET'])
def borrow(id):
    book = models.Book.query.filter_by(id=id).first()
    if book.borrower is None:
        if 'userid' in session:
            user = models.User.query.filter_by(id=session['userid']).first()
            book.borrower = user
            db.session.commit()
            flash(session['username'] + " borrowed " + book.title)
        else:
            flash("Please login to borrow a book")
    else:
        flash("This book is not available")
    return redirect(redirect_url())


@app.route('/returnbook/<id>', methods=['GET'])
def returnbook(id):
    book = models.Book.query.filter_by(id=id).first()
    if book.borrower_id == session['userid']:
        book.borrower = None
        db.session.commit()
        flash("User " + session['username'] + " returned " + book.title)
    else:
        flash('Error, wrong user id for return')
    return redirect(redirect_url())


@app.route('/data', methods=['GET', 'POST'])
def data():
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())

    form = forms.DeleteData()
    if form.validate_on_submit():
        for user in models.User.query.all():
            db.session.delete(user)
        for author in models.Author.query.all():
            db.session.delete(author)
        for book in models.Book.query.all():
            db.session.delete(book)
        db.session.commit()
        flash("Deleted all data")
        return redirect(redirect_url())
    return render_template('data.html',
                            users=models.User.query.all(),
                            authors=models.Author.query.all(),
                            books=models.Book.query.all(),
                            form=form,
                            login=login)

@app.route('/catalog', methods=['GET','POST'])
def catalog():
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())
    return render_template('catalog.html',
                            books=models.Book.query.all(),
                            login=login)

@app.route('/adduser', methods=['GET','POST'])
def adduser():
    #Add a new user or author
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())

    name = None
    form = forms.NewData()
    if form.validate_on_submit():
        name = form.name.data
        datatype = form.type.data
        form.name.data = ''
        form.type.data = ''
        if datatype == 'user':
            newdata = models.User(name=name)
        elif datatype == 'author':
            newdata = models.Author(name=name)
        db.session.add(newdata)
        db.session.commit()
        flash("Added new " + datatype + " with name " + newdata.name + " with ID " + str(newdata.id))
        return redirect(redirect_url())
    return render_template('basicform.html', form=form, login=login)


@app.route('/addbook', methods=['GET','POST'])
def addbook():
    #Add a new book
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())

    title = None
    form = forms.NewBook()

    choices = []
    authors = models.Author.query.all()
    for author in authors:
        choices.append((str(author.id), author.name))
    form.author.choices = choices

    if form.validate_on_submit():
        title = form.title.data
        authorid = form.author.data
        form.title.data = ''
        form.author.data = ''
        author = models.Author.query.filter_by(id=authorid).first()
        book = models.Book(title=title, author=author)
        db.session.add(book)
        db.session.commit()
        flash("Added new book with title " + title + " with ID " + str(book.id))
        return redirect(redirect_url())
    return render_template('basicform.html', form=form, login=login)

def signin(data):
    #given login data checks database and signs in
    data.strip()
    if data.isdigit():
        user = models.User.query.filter_by(id=data).first()
        if user is not None:
            session['userid'] = user.id
            session['username'] = user.name
            flash("Logged in " + user.name)
        else:
            flash("No user found with id " + str(data))
    else:
        user = models.User.query.filter(func.lower(models.User.name) == func.lower(data)).first()
        if user is not None:
            session['userid'] = user.id
            session['username'] = user.name
            flash("Logged in " + user.name)
        else:
            flash("No user found with name " + data)


def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)