from flask import Flask, render_template, g, request, jsonify
from werkzeug.contrib.cache import SimpleCache
import gdata.youtube
import gdata.youtube.service
import random, re

app = Flask(__name__)
cache = SimpleCache()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/z')
def suggest():
    q = request.args.get('q', '', type=str)
    o = request.args.get('o', 1, type=int)
    if not q or not o:
        return jsonify(vs=[])
    yt = gdata.youtube.service.YouTubeService()
    yt.ssl = False
    keywords = [keyword.strip() for keyword in q.split(',')]
    results = [res
               for keyword in keywords
               for res in ytquery(yt, keyword, o)]
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

if __name__ == '__main__':
    app.debug = True
    app.run()

