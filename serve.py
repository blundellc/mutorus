from flask import Flask, render_template, g, request, jsonify
import gdata.youtube
import gdata.youtube.service

app = Flask(__name__)

@app.route('/z')
def suggest():
    q = request.args.get('q', '', type=str)
    if not q:
        return jsonify(vs=[])
    yt = gdata.youtube.service.YouTubeService()
    yt.ssl = False
    qq = gdata.youtube.service.YouTubeVideoQuery()
    qq.vq = q
    qq.orderby = 'relevance'
    qq.racy = 'exclude'
    return jsonify(vs=[{'title':v.media.title.text,
                        'duration':v.media.duration.seconds,
                        'url':v.GetSwfUrl()} for v in yt.YouTubeQuery(qq).entry])

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()

