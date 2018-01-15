# VLib <a name="vlib"></a>
Vlib is a database program written in the Python programming language using the micro web framework Flask and a SQLite database. VLib stores data on books, book copies, borrowers (both students and teachers), and authors. Various data, such as books borrowed by students, are connected in the relational SQL database. Various parts of the program are implemented as webpages, with numerous links between pages to aid in navigation.

The full code for VLib can be found on [Github](https://github.com/grenadilla/fbla-app)

## Contents
1. [Summary](#vlib)
1. [How To Use](#how-to-use)
1. [Tools Used](#tools-used)
1. [File Structure](#file-structure)
1. [How It Works](#how-it-works)

## How To Use <a name="how-to-use"></a>
### Opening
VLib comes in two forms whose only difference is their distribution method. VLib can either used from a windows executable or at this [website](grenadilla.pythonanywhere.com).


To use the windows executable, first run vlibextractor.exe, a self extracting archive that will extract the full contents of VLib into a folder in a directory of your choosing. Next, open the resulting VLib folder, and scroll down and run VLib.exe.

After cx\_freeze converts the application to a windows executable, some of the code is not packaged, and the the remaining files can be hard to find. Much of the code can still be found in the app folder under Vlib/app, but it is suggested to view the code either from Github or from the included vlibcode folder.

### Navigation
![The Home Page](https://i.imgur.com/goPv2M2.png)

+ **Home**
    + The page you are on right now.
+ **User**
    + The name of the logged in user. Clicking on this name will bring you to the user page for this user, where fines can be payed and books can be borrowed. 
+ **Catalog**
    + The catalog of all books in the system. Here you can search for books and authors by ID, name, and title.
+ **Users**
    + Choose here to view either a list of all students or a list of all teachers in the system
+ **Add**
    + This is where new users, authors, and books are added into the system.
+ **Fines**
    + A list of users with unpaid fines. Includes fines in both returned and unreturned books. The list can be sorted.
+ **Borrowed Books**
    + A list of all borrowed books. Select 'overdue' to view only overdue books. The list can be sorted.
+ **User Settings**
    + Change settings for students and teachers such as how long they can borrow a book, their daily fines, and how many books they can borrow at a time.
+ **Login**
    + Change the currently logged in user by inputting a student or teacher's name or ID number. A logged in user can pay off fines and borrow books. 

### Adding Data
![Books can be added on this page](https://i.imgur.com/Pc54KkO.png)

Users (students and teachers), authors, and books can be added into the system by clicking on the 'Add' dropdown and choosing an option. Books require valid authors to be added before they can be added. Pictured above is the page where you can add data for a new book.

### The User Page
![The User Page](https://i.imgur.com/DMNVqS1.png)

The user page has information on the user, including their ID number, whether they are a student or teacher, their unpaid fines, and a list of their books. From the user page librarians can input the ID number of books to keep track of the books students and teachers have borrowed. From the user page librarians can also keep track of fine payments by users by inputting them in the system here. Clicking on the name of the author of a book will take you to the information page for that author. Clicking on any other information on a book will take you to that book's information page, where the book can be returned. Click on the edit page to change the user's name and whether they are a student or teacher.

### The Book Page
![The Book Page](https://i.imgur.com/BEOMnOn.png)

The book page has information on the book, including its ID number, author, and each of its copies. Clicking on the author's name will take you to the author's page. Clicking on the name of any student or teacher borrowing a copy will take you to the information page for that user. The table of copies displays information on who is borrowing the copy and the time of borrowing and due data, if any. Click on the edit button to change the book's title and its author, and to add additional copies. Clicking on the red 'X' next to the ID number of a copy will allow you to delete that copy. Finally, book copies can be borrowed or returned here, but only if a user is logged in.

### The Author Page
![The Author Page](https://i.imgur.com/UC7wOsW.png)

The author page has information on the author, including ID number and name. It lists all the books the author has written and the number of available copies for each. Clicking on any of the books will take you to the page for that book.

### The Catalog
![The Catalog](https://i.imgur.com/5VrA19a.png)

The catalog allows you to search for books and author by ID number, title, and name. Clicking on a book's title will take you to its page, and clicking on the name of an author will take you to the author's page. Below the search bar is a list of all books in the system.

## Tools Used <a name="tools-used"></a>
VLib was written mainly using Python 3, using the following modules and their dependencies (a full list can be found in [requirements.txt](https://raw.githubusercontent.com/grenadilla/fbla-app/master/requirements.txt)):

* [Flask](http://flask.pocoo.org/):
Flask is a python web microframework
    * [Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/):
VLib uses the [Bootstrap](https://getbootstrap.com/) web framework through Flask-Bootstrap.
    * [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/):
[WTForms](https://wtforms.readthedocs.io/en/latest/) is used to create the input forms used to create new students, teachers, authors, books, and more.
    * [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/):
[SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM used to communicate with the SQLite database
* [pywebview](https://github.com/r0x0r/pywebview):
Pywebview is a webview wrapper used in VLib for offline use to load VLib in its own window.
* [cx\_freeze](https://anthony-tuininga.github.io/cx_Freeze/):
cx\_freeze is a tool used to freeze VLib into an executable that can be run on windows without the need for the user to download any extra dependencies such as Python. The frozen version of VLib has all dependencies packaged with it for an easy download.

## File Structure <a name="file-structure"></a>
The basic structure of the application is as follows:

    VLib/
      run.py
      runwindow.py
      config.py
      app.db
      setup.py
      app/
        __init__.py
        models.py
        forms.py
        views.py
        static/
          js/
            scripts.js
            select2.min.js
          css/
            style.css
            select2.min.css
          images/
            home.png
            ...
            etc.
        templates/
          base.html
          index.html
          ...
          etc.

### run.py and runwindow.py
run.py first imports the app created in the app package. Note that 'app' the variable and 'app' the package are different things, which is why `from app import app` is used. Then the app is run, starting the server.

runwindow.py calls the run function defined in run.py, but opens it in a webview window, allowing it to look and act like a stand-alone application without needing to open a web browser.

### config.py
config.py holds all the configuration options.

### app.db
app.db is the SQLite database that holds all the data.

### setup.py
setup.py was a script autobuilt using cxfreeze-quickstart to generate a cx\_freeze distutils script, which was modified for VLib. setup.py allows the application to be frozen, meaning it bundles all the code and dependencies so VLib can run as a stand alone executable. setup.py freezes runwindow.py, which is the script which runs VLib in windowed mode.

### app and \_\_init\_\_.py
\_\_init\_\_.py declares the app folder to be a package folder. \_\_init\_\_.py initializes the app with `app = Flask(__name__)` and also imports various variables at the package level for easier access in the rest of the code. The `app` variable created here is the variable used in run.py to start the server

### models.py and Data Classes
models.py creates all the data classes to be used by SQLAlchemy and the tables to be used by the SQLite database. There are 5 data classes: 

+ **UserType**:
    + There are always exactly two instances of UserType: student and teacher. UserType holds information for each usertype, defining the amount of books that can be borrwed, the length of time that they can be borrowed, and the fines to be paid for overdue books. 
+ **User**:
    + Each user has a name, a UserType of either student or teacher, and a list of book copies they have borrowed.
* **Author**:
    + Each author has a name and a list of books they have written.
* **Book**:
    + Each book has a title, an author, and a list of copies. Note that Book and Copy are different classes!
* **Copy**:
    + Each copy has a book that it is tied to, and is the actual 'book' borrowed by users. It stores its borrower, borrow time, and due date.

### views.py
Since views.py holds the vast majority of the program logic, it will have an entire section devoted to it. See [How It Works](#how-it-works).

### static
The static folder holds all static files, which in the case of VLib is all javascript and CSS files and all the images used in the help page. The [JQuery](https://jquery.com/) javascript library is already included through Bootstrap. The JQuery addon [select2](https://select2.org/) is used to create better select tags in webforms.

### templates
The templates folder holds all the jinja2 templates is used to create the html page sent to the client's computer. Note that although all the files in this folder end with the .html extension, they have included jinja2 template logic within.

## How It Works <a name="how-it-works"></a>
### Routes
Most of the program logic is held in views.py. The views file defines all the routes in the webapp. When a user clicks a link in the application, they are routed to the corresponding route, where the route function will perform some logic before either sending a redirect to another page or displaying a jinja2 template (stored in the templates folder) to be shown to the user. All routes are declared using Python decorater functions in their most basic form like so:

    @app.route('/some_path/<variable>', methods=['GET', POST'])
    def some_path(variable):
        #do logic here
        return render_template('template.html',
                               variable=variable)

### jinja2 templates
When rendering templates the route function can pass variables to be used by the jinja2 template engine. The jinja2 template engine can parse Python like syntax in brackets like `{% %}` or `{{ }}`, so template.html might look something like this:

    {% extends "base.html" %}
    <h1>Title</h1>
    <p>The value of the passed variable is {{ variable }}</p>
    {% if variable > 0 %}
        <!--Display something here-->
    {% endif %}
    {% endblock %}

Many templates have `{% extends "base.html" %}` as their first line. base.html includes all the required javascript and CSS files, and defines the navigation bar at the top of each page. By creating a base template from which all other templates are descended from, a large navigation bar will not have to be redefined in each template.

### Database queries
Near top of the views file is this line: `from app import models, db`. Database queries and changes are done using the models file and db (database) file respectively. Queries are done using SQLAlchemy, and take the form `object = models.Class.query.filter_by(attribute=some_value).first()`. New data can be added simply by creating a new instance of the class, adding to the session, and committing to the database: 

    object = models.Class(attribute=some_value)
    db.session.add(object)
    db.session.commit()

Database queries are done in SQLAlchemy either using the form:

    users = models.User.query.filter_by(total_fines = 0).all()

Or:

    users = models.User.query.filter(models.User.total_fines == 0).all()

The second form has much more versatility than the first, such as being able to use less than and greater than and various SQLAlchemy functions.

### The Session
Flask allows the user of the session dictionary, which allows data to be stored in cookies. VLib uses the session to store the current user. The session can be accessed like any other python dictionary: `session['userid']
