from flask import Flask, render_template, request, flash
import requests
import json

DOMAIN = 'https://api.hh.ru/'
URL_VACANCIES = f'{DOMAIN}vacancies'
URL_AREA = f'{DOMAIN}suggests/areas'

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
    # TODO : вынести def results()  в отдельный модуль
    req = []
    skills = {}
    total = 0
    qnt_skills = 0
    area = '1'  # по умолчанию Москва
    vacancy = request.form['vacancy']
    if not vacancy:
        vacancy = 'python developer'  # по умолчанию ищем python developer
    region = request.form['region']
    # TODO заполнить info данными по умолчанию
    # TODO : необходимо запоминать дату и время на которое сделан запрос, ситуация ао вакансиям может измениться
    info = {'region': region, 'vacancy': vacancy}  # передаем в html

    # находим код региона для последущего запроса
    # TODO Если region = Москва, то запрос не нужен
    params = {'text': f'{region}'}
    ra = requests.get(URL_AREA, params=params)
    if ra.status_code == 200:
        area_result = ra.json()
        if area_result['items']:
            area = area_result['items'][0]['id']
        else:
            print('Такого региона нет!')
    else:
        print('Ищем вакансию по умолчанию в Москве')

    par = {'text': vacancy, 'area': area}
    rv = requests.get(URL_VACANCIES, params=par)
    if rv.status_code == 200:
        result = rv.json()
        found = result['found']
        info['count'] = found
        # идем по страницам и считаем навыки
        # TODO : нужен прогресс-бар
        if result['items']:
            for p in range(1 + (found // 20)):
                params = {'text': vacancy, 'area': area, 'page': p}
                res = requests.get(URL_VACANCIES, params=params).json()
                # страница {p}
                for j in res['items']:
                    resj = requests.get(j['url']).json()
                    for i in resj['key_skills']:
                        if i['name'] in skills:
                            skills[i['name']] += 1
                        else:
                            skills.setdefault(i['name'], 1)
                            qnt_skills += 1
                        total += 1
            # статистика
            for k, v in sorted(skills.items(), key=lambda x: int(x[1]), reverse=True):
                skill = {'name': k, 'count': v, 'percent': round(v / total * 100, 2)}  # в формате как в задании
                req.append(skill)

            info['requirement'] = req
            # сохраняем в файл запрос и результат
            with open('last_call.json', 'w', encoding='utf-8') as f:
                json.dump(info, f, ensure_ascii=False)
        else:
            print(f'В регионе {region} вакансии {vacancy} не найдено.')
    else:
        print('Ошибка поиска!')
    return render_template('result.html', info=info)


@app.route('/result/')
def get_results():
    # TODO : обработка пустого или отсутствующего файла json
    # TODO : необходимо запоминать дату и время на которое сделан запрос, ситуация ао вакансиям может измениться
    with open('last_call.json', 'r', encoding='utf-8') as f:
        info = json.load(f)
    return render_template('result.html', info=info)


if __name__ == '__main__':
    app.run(debug=True)
