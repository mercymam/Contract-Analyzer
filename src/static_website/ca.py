
from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html', message='Welcome To')
