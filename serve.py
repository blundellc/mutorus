from flask import Flask, render_template, g, request, jsonify
import gdata.youtube
import gdata.youtube.service
import random

app = Flask(__name__)

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
    qs = [mkquery(keyword, o) for keyword in keywords]
    results = [{'title':v.media.title.text,
                'duration':v.media.duration.seconds,
                'url':v.GetSwfUrl()}
               for qq in qs
               for v in yt.YouTubeQuery(qq).entry]
    random.shuffle(results)
    return jsonify(vs=results)

def mkquery(keywords, offset):
    qq = gdata.youtube.service.YouTubeVideoQuery()
    qq.vq = keywords
    qq.orderby = 'relevance'
    qq.racy = 'exclude'
    qq.start_index = offset
    return qq

if __name__ == '__main__':
    app.debug = True
    app.run()

