# VLib <a name="vlib"></a>
Vlib is a database program written in the Python programming language using the micro web framework Flask and a SQLite database. VLib stores data on books, book copies, borrowers (both students and teachers), and authors. Various data, such as books borrowed by students, are connected in the relational SQL database. Various parts of the program are implemented as webpages, with numerous links between pages to aid in navigation.

## Contents
1. [Summary](#vlib)
1. [Tools Used](#tools-used)
1. [How It Works](#how-it-works)

## Tools Used <a name="tools-used"></a>
VLib was written mainly using Python 3, using the the following modules and their dependencies (a full list can be found in [requirements.txt](requirements.txt)):

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

## How It Works <a name="how-it-works"></a>
The basic structure of the application is as follows:

    VLib/
      run.py
      config.py
      app.db
      app/
        __init__.py
        views.py
        models.py
        forms.py
        static/
          scripts.js
          select2.min.js
          style.css
          select2.min.css
        templates\
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
\_\_init\_\_.py declares the app folder to be a package folder. \_\_init\_\_.py initializes the app with `app = Flask(__name__)' and also imports various variables at the package level for easier access in the rest of the code. the `app` variable created here is the variable used in run.py to start the server
