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
