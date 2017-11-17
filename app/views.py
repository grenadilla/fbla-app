from flask import render_template, session, redirect, url_for, flash
from sqlalchemy import func
from app import app, db, models, forms

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    #add below login stuff to all pages
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(url_for('index'))
    return render_template('index.html', login=login)

@app.route('/user/<id>', methods=['GET','POST'])
def user(id):
    #Given an id, queries it from db and passes user object to page
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(url_for('user', id=str(id)))

    user = models.User.query.filter_by(id=id).first()
    return render_template('userinfo.html', user=user, login=login)

@app.route('/book/<id>', methods=['GET','POST'])
def book(id):
    #Book info page, from here can borrow a book
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(url_for('book', id=str(id)))

    book = models.Book.query.filter_by(id=id).first()
    return render_template('bookinfo.html', book=book, login=login)
   

@app.route('/data', methods=['GET','POST'])
def data():
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(url_for('data'))

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
        return redirect(url_for('data'))
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
        return redirect(url_for('catalog'))
    return render_template('catalog.html',
                            books=models.Book.query.all(),
                            login=login)

@app.route('/adduser', methods=['GET','POST'])
def adduser():
    #Add a new user or author
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(url_for('adduser'))

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
        return redirect(url_for('adduser'))
    return render_template('basicform.html', form=form, login=login)


@app.route('/addbook', methods=['GET','POST'])
def addbook():
    #Add a new book
    login = forms.Login()
    if login.validate_on_submit():
        signin(login.login_data.data)
        return redirect(url_for('addbook'))

    title = None
    form = forms.NewBook()
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
        return redirect(url_for('addbook'))
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

