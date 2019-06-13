# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging,requests,re

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

URL = 'https://discovery-stb3.ertelecom.ru/api/v3/pages/search?text=зик&limit=10'

DEFAULT_HEADERS = {
        'View': 'stb3',
        'X-Auth-Token': 'eyJkYXRhIjoie1wiZXhwaXJlc1wiOjE1NjA2OTA3MDQsXCJsaWZlc3BhblwiOjI1OTIwMDAsXCJwcmluY2lwYWxcIjp7XCJmcmVlbWl1bVwiOjAsXCJleHRpZFwiOlwibWFjOkY4OkYwOjgyOjQwOjg3OjkxXCIsXCJzdWJzY3JpYmVyXCI6e1wiaXNfZ3Vlc3RcIjpmYWxzZSxcInR5cGVcIjpcInN1YnNjcmliZXJcIixcImlkXCI6MzczMTQzNzcsXCJncm91cHNcIjpbe1wiaWRcIjozNTAzNyxcImV4dGlkXCI6XCJlcjpkb21haW46cGVybVwifV0sXCJleHRpZFwiOlwicGVybTo1OTAwMTc1ODcwNjRcIn0sXCJwbGF0Zm9ybVwiOntcIm9wZXJhdG9yXCI6e1widGl0bGVcIjpcIlwiLFwiaWRcIjoyLFwiZXh0aWRcIjpcImVyXCJ9LFwidGl0bGVcIjpcIlwiLFwiaWRcIjo0NCxcImV4dGlkXCI6XCJhbmRyb2lkX2lwdHZcIn0sXCJhdHRyc1wiOm51bGwsXCJncm91cHNcIjpbe1wiaWRcIjozNDE5NyxcImV4dGlkXCI6XCJlcjpldmVyeW9uZVwifV0sXCJvcGVyYXRvclwiOntcInRpdGxlXCI6XCJcIixcImlkXCI6MixcImV4dGlkXCI6XCJlclwifSxcInR5cGVcIjpcImRldmljZVwiLFwiaWRcIjo1ODA0MDI4NH19Iiwic2lnbmF0dXJlIjoiZFNSYXRkU25vNTQ0NHhDNjNDSkExXC9lRFVoa3RHb0RvV0JuOFgzVHgweFk9In0='
}

results = ''
# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])

def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']
    global results

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.


        res['response']['text'] = 'Привет! Чего желаешь?'
        return

    # Обрабатываем ответ пользователя.
    if req['request']['original_utterance'].lower() in [
        'фильм',
        'фильмы',
        'хочу фильм',
        'фильм посмотреть',
        'хочу посмотреть фильм',
        'фильм хочу',
        'фильмец',
        'хочу фильмец',
        'кино',
        'хочу кино',
        'хочу посмотреть кино',
        'кино хочу',
        'кинчик',
        'хочу кинчик',
        'кино посмотреть',
        'кинцо',
        'хочу кинцо',
        'хочу посмотреть кинцо',
        'кинцо хочу',
        'кинцо посмотреть',
        'хочу кинцо глянуть',
        'хочу кинцо посмотреть',
        'хочу фильм глянуть',
        'хочу фильмец глянуть',
        'хочу глянуть кинцо',
        'хочу глянуть фильмец'

    ]:
        res['response']['text'] = 'Какой фильм будет сегодня?'
        return
    elif results == '':
        searchURL = 'https://discovery-stb3.ertelecom.ru/api/v3/pages/search?text="%s"&limit=10' % req['request']['original_utterance']
        results += findMovie(searchURL)
        res['response']['text'] = 'Вот что нашлось:\n\n%s\nКакой из найденных хочешь?' % results
        return
    else:
        searchURL = 'https://discovery-stb3.ertelecom.ru/api/v3/pages/search?text="%s"&limit=10' % req['request']['original_utterance']
        id = movieLink(searchURL) 
        res['response']['text'] = 'Можешь найти его здесь http://movix.ru/movies/%s' % id
        return
    
    


def findMovie(findURL):
    global searchURL
    global DEFAULT_HEADERS
    found = requests.get(url=findURL,headers=DEFAULT_HEADERS)
    s = ''
    for i in found.json()['data']['showcases'][0]['items']:
        s += str(i['title'])+'\n'
    return s

def movieLink(movieURL):
    global searchURL
    global DEFAULT_HEADERS
    found = requests.get(url=movieURL,headers=DEFAULT_HEADERS)
    s = ''
    for i in found.json()['data']['showcases'][0]['items']:
        s += str(i['id'])+'\n'
    return s
