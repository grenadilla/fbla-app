#!flask/bin/python3
from app import app


def run_app(url):
    app.run(debug=True, use_reloader=False, host=url)


if __name__ == '__main__':
    run_app('0.0.0.0')
