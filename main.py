from flask import Flask, render_template
from datetime import datetime
import sqlite3


app = Flask('app')

@app.route('/')
def home():
    return render_template('index.html')


app.run()

