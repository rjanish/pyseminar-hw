from flask import Flask, render_template, request, url_for

app = Flask(__name__)
app.debug = True

collections = []

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'collection_name' in request.form:
            collections.append(request.form['collection_name'])
            # upload file
            return render_template('index.html', 
                                   collections=collections)
        if 'query' in request.form:
            return render_template('index.html', 
                                   collections=collections)
        else:
            return render_template('index.html', 
                                   collections=collections)
    else:
        return render_template('index.html', 
                               collections=collections)


if __name__ == "__main__":
    app.run()
