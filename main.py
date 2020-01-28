from flask import Flask, render_template, request
import json


from modules.parser import parser

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contacts/')
def contacts():
    return render_template('contacts.html')


@app.route('/search/', methods=['GET'])
def search():
    if request.method == 'POST':
        print('POST')
    return render_template('search.html')


@app.route('/search/', methods=['POST'])
def results():
    # TODO : необходимо запоминать дату и время на которое сделан запрос, ситуация ао вакансиям может измениться
    info = parser(request.form['vacancy'], request.form['region'])
    return render_template('result.html', info=info)


@app.route('/result/')
def get_results():
    # TODO : обработка пустого или отсутствующего файла json
    with open('last_call.json', 'r', encoding='utf-8') as f:
        info = json.load(f)
    return render_template('result.html', info=info)


if __name__ == '__main__':
    app.run(debug=True)
