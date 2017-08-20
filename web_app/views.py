from flask import render_template
from web_app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'name': 'Barna'}
    return render_template('index.html', user=user)