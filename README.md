# VLib <a name="vlib"></a>
Vlib is a database program written in the Python programming language using the micro web framework Flask and a SQLite database. VLib stores data on books, book copies, borrowers (both students and teachers), and authors. Various data, such as books borrowed by students, are connected in the relational SQL database. Various parts of the program are implemented as webpages, with numerous links between pages to aid in navigation.

## Contents
1. [Summary](#vlib)
1. [How To Use](#how-to-use)
1. [Tools Used](#tools-used)
1. [File Structure](#file-structure)
1. [How It Works](#how-it-works)

## How To Use <a name="how-to-use"></a>


## Tools Used <a name="tools-used"></a>
VLib was written mainly using Python 3, using the following modules and their dependencies (a full list can be found in [requirements.txt](requirements.txt)):

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
      config.py
      app.db
      app/
        __init__.py
        models.py
        forms.py
        views.py
        static/
          scripts.js
          select2.min.js
          style.css
          select2.min.css
        templates/
          base.html
          index.html
          ...
          etc.

### run.py
run.py first imports the app created in the app package. Note that 'app' the variable and 'app' the package are different things, which is why `from app import app` is used. Then the app is run, starting the server.

### config.py
config.py holds all the configuration options.

### app.db
app.db is the SQLite database that holds all the data.

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
The static folder holds all static files, which in the case of VLib is all javascript and CSS files. The [JQuery](https://jquery.com/) javascript library is already included through Bootstrap. The JQuery addon [select2](https://select2.org/) is used to create better select tags in webforms.

### templates
The templates folder holds all the jinja2 templates is used to create the html page sent to the client's computer. Note that although all the files in this folder end with the .html extension, they have included jinja2 template logic within.

## How It Works <a name="how-it-works"></a>
Most of the program logic is held in views.py. The views file defines all the routes in the webapp. When a user clicks a link in the application, they are routed to the corresponding route, where the route function will perform some logic before either sending a redirect to another page or displaying a jinja2 template (stored in the templates folder) to be shown to the user. All routes are declared using Python decorater functions in their most basic form like so:

    @app.route('/some_path/<variable>', methods=['GET', POST'])
    def some_path(variable):
        #do logic here
        return render_template('template.html',
                               variable=variable)

When rendering templates the route function can pass variables to be used by the jinja2 template engine. The jinja2 template engine can parse Python like syntax in brackets like `{% %}` or `{{ }}`, so template.html might look something like this:

    {% extends "base.html" %}
    <h1>Title</h1>
    <p>The value of the passed variable is {{ variable }}</p>
    {% if variable > 0 %}
        <!--Display something here-->
    {% endif %}
    {% endblock %}

Many templates have `{% extends "base.html" %}` as their first line. base.html includes all the required javascript and CSS files, and defines the navigation bar at the top of each page. By creating a base template from which all other templates are descended from, a large navigation bar will not have to be redefined in each template.

Near top of the views file is this line: `from app import models, db`. Database queries and changes are done using the models file and db (database) file respectively. Queries are done using SQLAlchemy, and take the form `object = models.Class.query.filter_by(attribute=some_value).first()`. New data can be added simply by creating a new instance of the class, adding to the session, and committing to the database: 

    object = models.Class(attribute=some_value)
    db.session.add(object)
    db.session.commit()
