''' This script implements a flask bibtex database application '''

# homework 10, python seminar fall 2013
# Ryan Janish

import os

from flask import Flask, render_template, request, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from pybtex.database.input.bibtex import Parser as btxparser

# initialize flask app
app = Flask(__name__)
app.debug = True

# initialize list of all collections and bib database
collections = []
db_filename = "references.db"
try:
    os.remove(db_filename)
except:
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_filename)
db = SQLAlchemy(app)

class Reference(db.Model): 
    ''' database object to hold uploaded references'''
    id = db.Column(db.Integer, primary_key=True)
    ref_tag = db.Column(db.String)
    author = db.Column(db.String)
    journal = db.Column(db.String)
    volume = db.Column(db.String)
    pages = db.Column(db.String)
    year = db.Column(db.String)
    title = db.Column(db.String)
    collection = db.Column(db.String)

    def __init__(self, ref_tag, author, journal, volume,
                 pages, year, title, collection):
        self.ref_tag = ref_tag
        self.author = author
        self.journal = journal
        self.volume = volume
        self.pages = pages
        self.year = year
        self.title = title
        self.collection = collection

    def __repr__(self):
        return '<{}>'.format(self.ref_tag)

# create database
db.create_all()

# action of site
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'collection_name' in request.form:
            # upload a file
            collection_name = request.form['collection_name']
            collections.append(collection_name)
            bib_filename = request.files['filename'].filename
            parser = btxparser()
            bib_data = parser.parse_file(bib_filename)
            for ref_tag in bib_data.entries:
                entry = [ref_tag]
                ref = bib_data.entries[ref_tag]
                for key in ['author', 'journal', 'volume', 
                            'pages', 'year', 'title']:
                    try:
                        entry.append(ref.fields[key])
                    except:
                        entry.append(unicode('unknown', 'utf-8'))
                entry.append(collection_name)
                db.session.add(Reference(*entry))
            db.session.commit()
            return render_template('index.html', 
                                   collections=collections)
        elif len(request.form) > 0:
            # search current database
            full_results = []
            for key, descriptor in zip(['ref_tag', 'author', 'journal', 
                                        'volume', 'pages', 'year', 
                                        'title', 'collection'], 
                                       [Reference.ref_tag, Reference.author, 
                                        Reference.journal, Reference.volume, 
                                        Reference.pages, Reference.year, 
                                        Reference.title, Reference.collection]):
                key_results = []
                searches = [s.strip() for s in request.form[key].split(',')]
                for search in searches:
                    if ((search == '') or 
                        (key in ['ref_tag', 'author', 'journal', 'title'])):
                        search = "%{}%".format(search)
                    results = Reference.query.filter(descriptor.ilike(search))
                    key_results += results.all()
                full_results.append(set(key_results))
            full_results = list(set.intersection(*full_results))
            return render_template('index.html', 
                                   collections=collections,
                                   results=full_results,
                                   display_results=True)
        else:
            return render_template('index.html', 
                                   collections=collections)
    else:
        return render_template('index.html', 
                               collections=collections)

# run app and clean-up
try:
    app.run(use_reloader=False)    
except KeyboardInterrupt:
    os.remove(db_filename)
