from flask import Flask, render_template, request, url_for
app = Flask(__name__)
app.debug = True

@app.route("/", methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		if 'query' in request.form:
			return render_template('index.html', 
								   searched=request.form['query'])
		if 'filename' in request.form:
			return render_template('index.html',
								   uploaded=request.form['filename'])
	else:
		return render_template('index.html')


if __name__ == "__main__":
    app.run()
