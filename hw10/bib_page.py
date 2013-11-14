
from flask import Flask, render_template, request, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from pybtex.database.input.bibtex import Parser as btxparser

# initialize flask app
app = Flask(__name__)
app.debug = True

# initialize list of all collections and bib database
collections = []
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///references.db'
db = SQLAlchemy(app)

class Reference(db.Model): 
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

db.create_all()

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'collection_name' in request.form:
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
        if len(request.form) > 0:
            results = Reference.query.filter(Reference.ref_tag.ilike("%{}%".format(request.form["ref_tag"])) & 
                                             Reference.author.ilike("%{}%".format(request.form["author"])) & 
                                             Reference.journal.ilike("%{}%".format(request.form["journal"])) & 
                                             Reference.volume.ilike("%{}%".format(request.form["volume"])) & 
                                             Reference.pages.ilike("%{}%".format(request.form["pages"])) & 
                                             Reference.year.ilike("%{}%".format(request.form["year"])) & 
                                             Reference.title.ilike("%{}%".format(request.form["title"])) &
                                             Reference.collection.ilike("{}".format(request.form["collection"])))
            return render_template('index.html', 
                                   collections=collections,
                                   results=results.all())
        else:
            return render_template('index.html', 
                                   collections=collections)
    else:
        return render_template('index.html', 
                               collections=collections)

app.run(use_reloader=False)    
