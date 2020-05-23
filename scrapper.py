import requests
import json
from bs4 import BeautifulSoup
import datetime
from dateutil import parser


def get_emol_news():
    r = requests.get(
        'https://cache-elastic-pandora.ecn.cl/emol/noticia/_search?q=publicada:true+AND+seccion:nacional&sort=fechaPublicacion:desc&size=60&from=0')

    news = {
        'title': 'Emol Nacional',
        'description': 'Ultimas noticias nacionales',
        'link': 'http://www.emol.com',
        'articles': []
    }

    if r.status_code == 200:
        json_data = r.json()
        news_data = json_data['hits']['hits']

        articles = []

        for article_data in news_data:
            article = {
                'title': article_data['_source']['titulo'],
                'link': article_data['_source']['permalink'],
                'description': article_data['_source']['texto'],
                'author': article_data['_source']['fuente'],
                'pubDate': parser.parse(
                    article_data['_source']['fechaPublicacion']+'Z')
            }

            articles.append(article)

        news['articles'] = articles

    return news


def get_biobio_news():
    news_requests = []

    for page in range(1, 4):
        news_requests.append(requests.get(
            'https://www.biobiochile.cl/lista/categorias/nacional?pag=' + str(page)))

    news = {
        'title': 'Radio Bio Bio - Nacional',
        'description': 'Ultimas noticias nacionales',
        'link': 'https://www.biobiochile.cl',
        'articles': []
    }

    articles = []
    for r in news_requests:
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "html.parser")

            for article_data in soup.find_all("div", {"class": "noticia row"}):
                article = {
                    'title': article_data.find("h1", {"class": "robotos"}).text,
                    'link':  article_data.a.get('href'),
                    'description': '',
                    'author': article_data.find("p", {"class": "autor"}).text.replace('Por: ', ''),
                    'pubDate': parser.parse(' '.join(list(map(lambda item: item.text if hasattr(item, 'text') else '', article_data.find("div", {"class": "fecha"}).contents))).strip() + 'Z', dayfirst=True)
                }

                articles.append(article)

    news['articles'] = articles

    return news


def get_lt3_news():
    news_requests = []

    for page in range(1, 2):
        news_requests.append(requests.get(
            'https://www.latercera.com/categoria/nacional/page/' + str(page) + '/'))

    news = {
        'title': 'La Tercera - Lo Ultimo',
        'description': 'Ultimas noticias',
        'link': 'https://www.latercera.com/',
        'articles': []
    }

    articles = []
    for r in news_requests:
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "html.parser")

            now = datetime.datetime.now(datetime.timezone.utc)

            for article_data in soup.find_all("div", {"class": "art-container image_headline_deck_byline"}):
                pubDateArray = article_data.find("div", {"class": "time"}).small.contents[1].string.strip(
                ).split(' ')

                minutes = 0
                if len(pubDateArray) > 2:
                    minutes = int(pubDateArray[1]) if pubDateArray[2] == 'minutes' else int(
                        pubDateArray[1])*60

                descriptionContainer = article_data.find(
                    "div", {"class": "deck | isText"})

                description = ''
                if hasattr(descriptionContainer, 'p'):
                    description = descriptionContainer.p.text

                article = {
                    'title': article_data.find("h3").a.contents[2].string,
                    'link': "https://www.latercera.com" + article_data.find("h3").a.get("href"),
                    'description': description,
                    'author': article_data.find("div", {"class": "name"}).small.text,
                    'pubDate': now - datetime.timedelta(minutes=minutes)
                }

                articles.append(article)

    news['articles'] = articles

    return news
