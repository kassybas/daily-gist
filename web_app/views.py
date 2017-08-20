from flask import render_template
from web_app import app
from src.models import db

@app.route('/')
@app.route('/index')
def index():
    database = db.MongoDB("reddit", "entries")
    news = database.get_entries_of_collection()
    return render_template('index.html', news=news)