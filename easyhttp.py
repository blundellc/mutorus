import urllib2, gzip, StringIO
# parsing stuff
import xml.dom.minidom
try:
# funky stuff we need (more complicated than necessary? old code):
# - for parsing (python-html5lib)
    import html5lib
# - for dealing with character sets (python-chardet)
    import chardet
# - for making a dom (python-4suite-xml)
    import Ft.Xml.Domlette as domlette
# 4suite xml's ConvertDocument only supports a very limited set of nodeType's:
# let's delete these nodes completely for now.
    hack_4suite_md = xml.dom.minidom.Node
    hack_4suite_ok = set([hack_4suite_md.ELEMENT_NODE,
                          hack_4suite_md.ATTRIBUTE_NODE,
                          hack_4suite_md.TEXT_NODE,
                          hack_4suite_md.COMMENT_NODE,
                          hack_4suite_md.DOCUMENT_FRAGMENT_NODE,
                          hack_4suite_md.PROCESSING_INSTRUCTION_NODE])
    tree_builder = html5lib.treebuilders.getTreeBuilder("dom")
    have_html_parse = True
except:
    hack_4suite_ok = None
    hack_4suite_md = None
    tree_builder = None
    have_html_parse = False


def get(url, referer=None, user_agent='pyhttpget', compression=True,
        cookies=None, proxy=None, timeout=None, http_debug=0):
    """
    httpget(url, options)

    XXX: no support for ETag or If-Modified-Since
    XXX: no support for robots.txt
    XXX: no support for redirections or limiting the number of them

    options:
    referer      - url or None
    cookies      - instance of cookielib.CookieJar or None
    proxy        - proxy url or None
    timeout      - timeout in seconds or None
    http_debug   - positive integer or 0
    """
    req = urllib2.Request(url,unverifiable=True)
    if referer is not None:
        req.add_header('Referer',referer)
    req.add_header('User-Agent', user_agent)
    if compression:
        req.add_header('Accept-Encoding','gzip')
    handlers = [urllib2.HTTPHandler(debuglevel=http_debug)
               ,urllib2.HTTPSHandler(debuglevel=http_debug)]
    if cookies is not None:
        handlers.append(urllib2.HTTPCookieProcessor(cookies))
    if proxy is not None:
        handlers.append(urlib2.ProxyHandler({'http': proxy, 'https': proxy}))
    url_open = urllib2.build_opener(*handlers)
    resp = url_open.open(req,timeout=timeout)
    data = resp.read()
    if resp.headers.get('Content-Encoding', None) == 'gzip':
        data = gzip.GzipFile(fileobj=StringIO.StringIO(data)).read()
    resp.close()
    return data



def parse_html(html):
    if not have_html_parse:
        raise RuntimeError,'missing html parser. maybe you need to install some packages, eh?'
    guess = chardet.detect(html)
    if guess is None:
        # http/1.1 says this is the default
        encoding = 'ISO-8859-1'
    else:
        encoding = guess['encoding']

    def filter_types(root):
        fringe=[root]
        while len(fringe) != 0:
            cur = fringe.pop()
            for child in cur.childNodes:
                if child.nodeType not in hack_4suite_ok:
                    cur.removeChild(child)
                    for grandchild in child.childNodes:
                        cur.appendChild(grandchild)
            fringe.extend(cur.childNodes)
        return root

    return domlette.ConvertDocument(filter_types(html5lib.HTMLParser(tree=tree_builder).parse(unicode(html,encoding))))

