import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#Supresses overhead warning. May need to delete later
SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = True
SECRET_KEY = 'Test'

CATALOG_POSTS_PER_PAGE = 10
USERS_POSTS_PER_PAGE = 10
SEARCH_POSTS_PER_PAGE = 10
