from flask import render_template, session, redirect, url_for, flash, request
from sqlalchemy import func
import datetime
from decimal import Decimal
from app import app, db, models, forms

# create tables for author query if tables do not exist
db.create_all()
if models.UserType.query.filter_by(name='student').first() is None:
    role_student = models.UserType(name='student', borrow_length=datetime.timedelta(seconds=14), fine=Decimal('0.5'))
    db.session.add(role_student)
if models.UserType.query.filter_by(name='teacher').first() is None:
    role_teacher = models.UserType(name='teacher', borrow_length=datetime.timedelta(seconds=28), fine=Decimal('0.2'))
    db.session.add(role_teacher)
db.session.commit()


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
    #Given id, queries it from the database and passes the correct author object to page
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())

    author = models.Author.query.filter_by(id=id).first()
    return render_template('authorinfo.html', author=author, login=login)


@app.route('/book/<id>', methods=['GET', 'POST'])
def book(id):
    #Given book (not copy) id, queries it and passes book data to page to display
    #Book info page, from here can borrow a book
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())

    book = models.Book.query.filter_by(id=id).first()

    #Checks if user has borrowed a book, passes id of borrowed copy (0 if not borrowed)
    borrowed_id = 0
    for copy in book.copies:
        if 'userid' in session and session['userid'] == copy.borrower_id:
            borrowed_id = copy.id
    return render_template('bookinfo.html', book=book, login=login, borrowed_id=borrowed_id)


@app.route('/edit/user/<id>', methods=['GET', 'POST'])
def edituser(id):
    #Page to edit user data like name
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())

    user = models.User.query.filter_by(id=id).first()
    form = forms.EditUser(name=user.name)
    form_title = "Edit user " + user.name
    if form.validate_on_submit():
        flash("Changed user " + user.name + " to " + form.name.data)
        user.name = form.name.data
        db.session.commit()
        #If edited user is logged in, change log in data too
        if 'userid' in session and session['userid'] == user.id:
            session['username'] = user.name
        return redirect(url_for('user', id=user.id))
    return render_template('basicform.html', form_title=form_title, form=form, login=login)


@app.route('/edit/author/<id>', methods=['GET', 'POST'])
def editauthor(id):
    #Page to edit author data like name
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())

    author = models.Author.query.filter_by(id=id).first()
    form = forms.EditUser(name=author.name)
    form_title = "Edit author " + author.name
    if form.validate_on_submit():
        flash("Changed author " + author.name + " to " + form.name.data)
        author.name = form.name.data
        db.session.commit()
        return redirect(url_for("author", id=author.id))
    return render_template('basicform.html', form_title=form_title, form=form, login=login)


@app.route('/edit/book/<id>', methods=['GET', 'POST'])
def editbook(id):
    #Page to edit book data like title and author
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())

    book = models.Book.query.filter_by(id=id).first()
    form = forms.EditBook(title=book.title, author=str(book.author_id))
    choices = []
    authors = models.Author.query.all()
    for author in authors:
        choices.append((str(author.id), author.name))
    form.author.choices = choices
    form_title = "Edit book " + book.title
    if form.validate_on_submit():
        flash("Changed book " + book.title)
        book.title = form.title.data
        book.author = models.Author.query.filter_by(id=int(form.author.data)).first()
        db.session.commit()
        return redirect(url_for("book", id=book.id))
    return render_template('basicform.html', form_title=form_title, form=form, login=login)


@app.route('/borrow/<id>', methods=['GET'])
def borrow(id):
    #Page to borrow a book, accessed by redirect from book page
    #Does not display page, instead redirects to previous page
    #ID is book ID, not copy ID
    book = models.Book.query.filter_by(id=id).first()
    for copy in book.copies:
        if copy.borrower is None:
            #If user is logged in, user borrows first available copy of book
            if 'userid' in session:
                user = models.User.query.filter_by(id=session['userid']).first()
                copy.borrower = user
                time = datetime.datetime.now()
                copy.borrow_time = time.replace(microsecond=0)
                copy.return_time = copy.borrow_time + user.type.borrow_length
                db.session.commit()
                flash(session['username'] + " borrowed " + book.title)
                return redirect(redirect_url())
            else:
                flash("Please login to borrow a book")
                return redirect(redirect_url())
    flash("This book is not available")
    return redirect(redirect_url())


@app.route('/returnbook/<id>', methods=['GET'])
def returnbook(id):
    #URL to return the copy of a book. Id is copy ID, not book ID
    copy = models.Copy.query.filter_by(id=id).first()
    if 'userid' in session and copy.borrower_id == session['userid']:
        #calculate fines
        delta = datetime.datetime.now() - copy.return_time
        if delta > datetime.timedelta(0):
            fine = delta.days * (copy.borrower.type.fine + 1)
            flash("Fine of " + str(fine))
        else:
            flash("No fines")
        #reset borrow variables
        copy.borrower = None
        copy.borrow_time = None
        copy.return_time = None
        db.session.commit()
        flash("User " + session['username'] + " returned " + copy.book.title)
    else:
        flash('Error, wrong user id for returning book')
    return redirect(redirect_url())


@app.route('/data', methods=['GET', 'POST'])
def data():
    #Currently displays data from db. Delete later
    #Can delete all data from here
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
        for copy in models.Copy.query.all():
            db.session.delete(copy)
        db.session.commit()
        flash("Deleted all data")
        return redirect(redirect_url())
    return render_template('data.html',
                            users=models.User.query.all(),
                            authors=models.Author.query.all(),
                            books=models.Book.query.all(),
                            copies=models.Copy.query.all(),
                            form=form,
                            login=login)

@app.route('/catalog', methods=['GET','POST'])
def catalog():
    #Catalog of all books
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
        role_student = models.UserType.query.filter_by(name='student').first()
        role_teacher = models.UserType.query.filter_by(name='teacher').first()
        if datatype == 'student':
            newdata = models.User(name=name)
            newdata.type = role_student
        elif datatype == 'teacher':
            newdata = models.User(name=name)
            newdata.type = role_teacher
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
        copies = form.copies.data
        form.title.data = ''
        form.author.data = ''
        form.copies.data = 0
        if copies <= 0:
            flash("Must create at least one copy")
            return redirect(redirect_url())
        author = models.Author.query.filter_by(id=authorid).first()
        book = models.Book(title=title, author=author)
        db.session.add(book)
        for i in range(0, copies):
            copy = models.Copy(book=book)
            db.session.add(copy)
        db.session.commit()
        flash("Added new " + str(copies) + " book(s) with title " + title + " with book ID " + str(book.id))
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
    #Returns previous url
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)
