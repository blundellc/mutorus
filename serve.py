from flask import Flask, render_template, g, request, jsonify
from werkzeug.contrib.cache import SimpleCache
import gdata.youtube
import gdata.youtube.service
import random, re
from db import init_db, db_session
from log import Scrob, Vote, Query


app = Flask(__name__)
cache = SimpleCache()

@app.route('/')
def index():
    return render_template('index.html')

@app.after_request
def shutdown_db(response):
    db_session.remove()
    return response

@app.route('/z')
def suggest():
    q = request.args.get('q', '', type=str)
    o = request.args.get('o', 1, type=int)
    if not q or not o:
        return jsonify(vs=[], last=0)
    yt = gdata.youtube.service.YouTubeService()
    yt.ssl = False
    keywords = [keyword.strip() for keyword in q.split(',')]
    results = [res
               for keyword in keywords
               for res in ytquery(yt, keyword, o)]
    record(Query(default_user, q, o))
    if len(keywords):
        last = len(results)//len(keywords)
    else:
        last = 0
    random.shuffle(results)
    return jsonify(vs=results, last=last)

watch_url_hash = re.compile(r'^http:..www.youtube.com(.watch)?.v.([^&?]+)([?&].*)?$')
vid_timeout = 6 * 60 * 60

def ytquery(yt, keywords, offset):
    res = cache.get((keywords, offset))
    if res is None:
        qq = gdata.youtube.service.YouTubeVideoQuery()
        qq.vq = keywords
        qq.orderby = 'relevance'
        qq.racy = 'exclude'
        qq.start_index = offset
        qq.max_results = 5
        res = []
        for v in yt.YouTubeQuery(qq).entry:
            url = v.GetSwfUrl()
            if url is None:
                url = v.media.player.url
                if url is None:
                    continue
            hh = watch_url_hash.sub(r'\2', url)
            res.append({'title':v.media.title.text,
                        'duration':v.media.duration.seconds,
                        'watch':v.media.player.url,
                        'hash':hh})
        cache.set((keywords,offset), res, timeout=vid_timeout)
    return res

default_user = 'cb'

@app.route('/vote')
def vote():
    h = request.args.get('h', '', type=str)
    v = request.args.get('v', None, type=str)
    if v is None:
        jsonify(result='err')
    record(Vote(default_user, h, v))
    return jsonify(result='ok')

@app.route('/scrob')
def scrob():
    h = request.args.get('h', '', type=str)
    if not h:
        return jsonify(result='err')
    # time remaining
    r = request.args.get('r', 0, type=int)
    record(Scrob(default_user, h, r))
    return jsonify(result='ok')

def record(obj):
    db_session.add(obj)
    db_session.commit()

if __name__ == '__main__':
    init_db()
    app.debug = True
    app.run()

