from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/contacts/")
def contacts():
    return render_template('contacts.html')


@app.route("/search/")
def query():
    return render_template('search.html')


if __name__ == "__main__":
    app.run(debug=True)
