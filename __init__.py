from feedgen.feed import FeedGenerator
import flask

import scrapper

app = flask.Flask(__name__)
app.config['debug'] = True


@app.route('/emol', methods=['GET'])
def emol():
    news = scrapper.get_emol_news()

    fg = FeedGenerator()

    fg.title(news['title'])
    fg.description(news['description'])
    fg.link(href=news['link'])

    for article in news['articles']:
        fe = fg.add_entry()
        fe.title(article['title'])
        fe.link(href=article['link'])
        fe.description(article['description'])
        fe.guid(article['link'], permalink=True)
        fe.author(name=article['author'])
        fe.pubDate(article['pubDate'])

    res = flask.make_response(fg.rss_str())
    res.headers.set('Content-Type', 'application/xml')
    return res


@app.route('/biobio', methods=['GET'])
def biobio():
    news = scrapper.get_biobio_news()

    fg = FeedGenerator()

    fg.title(news['title'])
    fg.description(news['description'])
    fg.link(href=news['link'])

    for article in news['articles']:
        fe = fg.add_entry()
        fe.title(article['title'])
        fe.link(href=article['link'])
        fe.description(article['description'])
        fe.guid(article['link'], permalink=True)
        fe.author(name=article['author'])
        fe.pubDate(article['pubDate'])

    res = flask.make_response(fg.rss_str())
    res.headers.set('Content-Type', 'application/xml')
    return res


@app.route('/lt3', methods=['GET'])
def lt3():
    news = scrapper.get_lt3_news()

    fg = FeedGenerator()

    fg.title(news['title'])
    fg.description(news['description'])
    fg.link(href=news['link'])

    for article in news['articles']:
        fe = fg.add_entry()
        fe.title(article['title'])
        fe.link(href=article['link'])
        fe.description(article['description'])
        fe.guid(article['link'], permalink=True)
        fe.author(name=article['author'])
        fe.pubDate(article['pubDate'])

    res = flask.make_response(fg.rss_str())
    res.headers.set('Content-Type', 'application/xml')
    return res


if __name__ == '__main__':
    app.run()
