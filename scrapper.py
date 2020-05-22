import requests
import json
from bs4 import BeautifulSoup
import datetime
import dateutil.parser


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
                'pubDate': dateutil.parser.parse(
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
                    'pubDate': dateutil.parser.parse(' '.join(list(map(lambda item: item.text if hasattr(item, 'text') else '', article_data.find("div", {"class": "fecha"}).contents))).strip() + 'Z', dayfirst=True)
                }

                articles.append(article)

    news['articles'] = articles

    return news


def get_lt3_news():
    news_requests = []

    for page in range(1, 2):
        news_requests.append(requests.get(
            'https://www.latercera.com/lo-ultimo/page/' + str(page)))

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

            for article_data in soup.find_all("article", {"class": "card | border-bottom float"}):
                pubDateArray = article_data.find("div", {"class": "time"}).small.contents[1].string.strip(
                ).lower().replace('hace ', '').split(' ')
                minutes = int(pubDateArray[0]) if pubDateArray[1] == 'minutes' else int(
                    pubDateArray[0])*60

                article = {
                    'title': article_data.find("h3").find("a").contents[2].string.strip(),
                    'link': "https://www.latercera.com" + article_data.find("h3").a.get("href"),
                    'description': article_data.find("div", {"class": "deck | isText"}).p.text,
                    'author': article_data.find("div", {"class": "name"}).find("small").text,
                    'pubDate': datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=minutes)
                }

                articles.append(article)

    news['articles'] = articles

    return news
