from flask import render_template, session, redirect, url_for, flash, request
from sqlalchemy import func
import datetime
from app import app, db, models, forms

# create tables for author query if tables do not exist
db.create_all()
if models.UserType.query.filter_by(name='student').first() is None:
    role_student = models.UserType(name='student',
                                   borrow_length=datetime.timedelta(14),
                                   fine=50,
                                   book_limit=5)
    db.session.add(role_student)
if models.UserType.query.filter_by(name='teacher').first() is None:
    role_teacher = models.UserType(name='teacher',
                                   borrow_length=datetime.timedelta(28),
                                   fine=20,
                                   book_limit=10)
    db.session.add(role_teacher)
db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    # add below login stuff to all pages
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(url_for('index'))
    return render_template('index.html', login=login)


@app.route('/user/<id>', methods=['GET', 'POST'])
def user(id):
    # Given an id, queries it from db and passes user object to page
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())

    user = models.User.query.filter_by(id=id).first()
    return render_template('userinfo.html', user=user, login=login)


@app.route('/author/<id>', methods=['GET', 'POST'])
def author(id):
    # Given id, queries it from the database and passes the correct
    # author object to page
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())

    author = models.Author.query.filter_by(id=id).first()
    return render_template('authorinfo.html', author=author, login=login)


@app.route('/book/<id>', methods=['GET', 'POST'])
def book(id):
    # Given book (not copy) id, queries it and passes book data to page to
    # display book info page, from here can borrow a book
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())

    book = models.Book.query.filter_by(id=id).first()

    # Checks if user has borrowed a book, passes id of borrowed
    # copy (0 if not borrowed)
    borrowed_id = 0
    for copy in book.copies:
        if 'userid' in session and session['userid'] == copy.borrower_id:
            borrowed_id = copy.id
    return render_template('bookinfo.html',
                           book=book,
                           login=login,
                           borrowed_id=borrowed_id)


@app.route('/edit/user/<id>', methods=['GET', 'POST'])
def edituser(id):
    # Page to edit user data like name
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())

    user = models.User.query.filter_by(id=id).first()
    form = forms.EditUser(name=user.name, type=user.type.name)
    form_title = "Edit user " + user.name
    if form.validate_on_submit():
        flash("Changed " + user.type.name + " " + user.name + " to "
              + form.type.data + " " + form.name.data)
        usertype = models.UserType.query.filter_by(name=form.type.data).first()
        user.name = form.name.data
        user.type = usertype
        db.session.commit()
        # If edited user is logged in, change log in data too
        if 'userid' in session and session['userid'] == user.id:
            session['username'] = user.name
        return redirect(url_for('user', id=user.id))
    return render_template('basicform.html',
                           form_title=form_title,
                           form=form,
                           login=login)


@app.route('/edit/author/<id>', methods=['GET', 'POST'])
def editauthor(id):
    # Page to edit author data like name
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
    return render_template('basicform.html',
                           form_title=form_title,
                           form=form,
                           login=login)


@app.route('/edit/book/<id>', methods=['GET', 'POST'])
def editbook(id):
    # Page to edit book data like title and author
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
    return render_template('basicform.html',
                           form_title=form_title,
                           form=form,
                           login=login)


@app.route('/edit/usertypes', methods=['Get', 'POST'])
def editusertypes():
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())

    student = models.UserType.query.filter_by(name='student').first()
    teacher = models.UserType.query.filter_by(name='teacher').first()

    form = forms.EditUserType(student_borrow_length=student.borrow_length.days,
                              student_fine=student.fine,
                              student_book_limit=student.book_limit,
                              teacher_borrow_length=teacher.borrow_length.days,
                              teacher_fine=teacher.fine,
                              teacher_book_limit=teacher.book_limit)

    if form.validate_on_submit():
        student.borrow_length = datetime.timedelta(form.student_borrow_length.data)
        student.fine = form.student_fine.data
        student.book_limit = form.student_book_limit.data
        teacher.borrow_length = datetime.timedelta(form.teacher_borrow_length.data)
        teacher.fine = form.teacher_fine.data
        teacher.book_limit = form.teacher_book_limit.data
        db.session.commit()
        flash("Updated user settings")
    return render_template("basicform.html",
                           form=form,
                           student=student,
                           teacher=teacher,
                           login=login)


@app.route('/delete/user/<id>', methods=['GET', 'POST'])
def deleteuser(id):
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())
    
    user = models.User.query.filter_by(id=id).first()
    if user is not None:
        flash("Deleted user " + user.name + " ID: " + str(user.id))
        if int(session['userid']) == user.id:
            session['userid'] = None
            session['username'] = None
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for('index'))


@app.route('/delete/author/<id>', methods=['GET', 'POST'])
def deleteauthor(id):
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())
    
    author = models.Author.query.filter_by(id=id).first()
    if author is not None:
        flash("Deleted author " + author.name + " ID: " + str(author.id))
        for book in author.books:
            flash("Deleted book " + book.title)
            for copy in book.copies:
                db.session.delete(copy)
            db.session.delete(book)
        db.session.delete(author)
        db.session.commit()

    return redirect(url_for('index'))


@app.route('/delete/book/<id>', methods=['GET', 'POST'])
def deletebook(id):
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())
    
    book = models.Book.query.filter_by(id=id).first()
    if book is not None:
        flash("Deleted book " + book.title + " ID: " + str(book.id))
        for copy in book.copies:
            db.session.delete(copy)
        db.session.delete(book)
        db.session.commit()

    return redirect(url_for('index'))


@app.route('/borrow/<id>', methods=['GET'])
def borrow(id):
    # Page to borrow a book, accessed by redirect from book page
    # Does not display page, instead redirects to previous page
    # ID is book ID, not copy ID
    book = models.Book.query.filter_by(id=id).first()
    for copy in book.copies:
        if copy.borrower is None:
            # If user is logged in, user borrows first available copy of book
            if 'userid' in session:
                user = models.User.query.filter_by(id=session['userid']).first()
                if len(user.books) >= user.type.borrow_limit:
                    flash('You have reached your borrow limit. '
                          'Please return another book to borrow this book')
                else:
                    copy.borrower = user
                    time = datetime.datetime.utcnow()
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
    # URL to return the copy of a book. Id is copy ID, not book ID
    copy = models.Copy.query.filter_by(id=id).first()
    if 'userid' in session and copy.borrower_id == session['userid']:
        # calculate fines
        delta = datetime.datetime.utcnow() - copy.return_time
        if delta > datetime.timedelta(0):
            fine = (delta.days + 1) * copy.borrower.type.fine
            user = models.User.query.filter_by(id=session['userid']).first()
            user.total_fines += fine
            flash("Fine of " + str(fine / 100))
        # reset borrow variables
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
    # Currently displays data from db. Delete later
    # Can delete all data from here
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


@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    # Catalog of all books
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())
    return render_template('catalog.html',
                           books=models.Book.query.all(),
                           login=login)


@app.route('/add/user', methods=['GET', 'POST'])
def adduser():
    # Add a new user or author
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())

    name = None
    form = forms.NewUser()
    if form.validate_on_submit():
        name = form.name.data
        if db.session.query(db.exists().where(models.User.name == name)).scalar():
            flash("A user with name " + name + " already exists. Please choose a different name")
        else:
            datatype = form.type.data
            form.name.data = ''
            form.type.data = ''
            role_student = models.UserType.query.filter_by(name='student').first()
            role_teacher = models.UserType.query.filter_by(name='teacher').first()
            if datatype == 'student':
                newdata = models.User(name=name, total_fines=0)
                newdata.type = role_student
            elif datatype == 'teacher':
                newdata = models.User(name=name, total_fines=0)
                newdata.type = role_teacher
            db.session.add(newdata)
            db.session.commit()
            flash("Added new " + datatype + " with name "
                  + newdata.name + " with ID " + str(newdata.id))
        return redirect(redirect_url())
    return render_template('basicform.html', form=form, login=login)

@app.route('/add/author', methods=['GET', 'POST'])
def addauthor():
    # Add a new author
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())

    form = forms.NewAuthor()
    if form.validate_on_submit():
        name = form.name.data
        if db.session.query(db.exists().where(models.Author.name == name)).scalar():
            flash("A author with name " + name + " already exists. Please choose a different name")
        else:
            author = models.Author(name=name)
            db.session.add(author)
            db.session.commit()
            flash("Added new author with name " + name +  " with ID " + str(author.id))
        return redirect(redirect_url())
    return render_template('basicform.html', form=form, login=login)


@app.route('/add/book', methods=['GET', 'POST'])
def addbook():
    # Add a new book
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
        if copies == 1:
            flash("Added a new book. Title: " + title + ", ID: " + str(book.id))
        else:
            flash("Added a new book. Title: " + title + ", ID: " + str(book.id)
                    + ", Copies: " + str(copies))
        return redirect(redirect_url())
    return render_template('basicform.html',
                           form=form,
                           login=login)


@app.route('/fines', methods=['GET', 'POST'])
def fines():
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())

    users = models.User.query.filter(models.User.total_fines > 0)
    return render_template('fines.html', users=users, login=login)


@app.route('/borrowedbooks', methods=['GET', 'POST'])
def borrowedbooks():
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(redirect_url())

    copies = models.Copy.query.filter(models.Copy.borrower != None).all()
    return render_template('borrowedbooks.html', copies=copies, login=login)


def signin(data):
    # given login data checks database and signs in
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
    # Returns previous url
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)
