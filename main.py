from flask import Flask, render_template, request
import json

from modules.parser import parser, get_history

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/history/', methods=['GET'])
def history():
    if request.method == 'POST':
        print('POST')
    history_db = get_history()
    return render_template('history.html', req=history_db)


@app.route('/history/', methods=['POST'])
def history_result():
    print(request.form)
    return render_template('result.html')


@app.route('/search/', methods=['GET'])
def search():
    if request.method == 'POST':
        print('POST')
    return render_template('search.html')


@app.route('/search/', methods=['POST'])
def results():
    info = parser(request.form['vacancy'], request.form['region'])
    return render_template('result.html', info=info)


@app.route('/result/')
def get_results():
    # TODO : обработка пустого или отсутствующего файла json
    with open('last_call.json', 'r', encoding='utf-8') as f:
        info = json.load(f)
    return render_template('result.html', info=info)


@app.route('/contacts/')
def contacts():
    return render_template('contacts.html')


if __name__ == '__main__':
    app.run(debug=True)
