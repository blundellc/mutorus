import urllib2
import easyhttp

def article(title):
    resp = wp(action='query', titles=title, prop='revisions', rvprop='content',
            redirects=1)
    # i love the semantic web.
    return resp['query']['pages'].items()[0][1]['revisions'][0].items()[0][1]

def search(keywords):
    return wp(action='opensearch',search=keywords)[1]

def wp(http_options={'timeout': 30}, **kwargs):
    qu = urllib2.quote
    q = '&'.join([qu(str(k))+'='+qu(str(v)) for k,v in kwargs.iteritems()])
    return json.loads(easyhttp.get('http://en.wikipedia.org/w/api.php?format=json&'+q, **http_options))

