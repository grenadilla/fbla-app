#!/home/jeffrey/fbla-app/venv/bin/python3
from threading import Thread, Lock, Timer
from time import sleep
import webview
import run

def url_ok(url, port):
    try:
        from http.client import HTTPConnection
    except ImportError:
        from httplib import HTTPConnection

    try:
        conn = HTTPConnection(url, port)
        conn.request("GET","/")
        r = conn.getresponse()
        if r.status == 200:
            return True
    except:
        return False

def window():
    webview.create_window("Flask Test", "http://127.0.0.1:5000", min_size=(600,800))

if __name__ == '__main__':
    t = Thread(target=run.run_app, args=("127.0.0.1",))
    t.daemon = True
    t.start()

    while not url_ok("127.0.0.1", 5000):
        sleep(0.1)

    Timer(1,window).start()
    webview.load_url("http://127.0.0.1:5000")
