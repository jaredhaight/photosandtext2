import re
from unicodedata import normalize
import datetime

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def slugify(text, delim=u'-'):
    """
    Generates an slightly worse ASCII-only slug.
    Aped from: http://flask.pocoo.org/snippets/5/
    """
    if isinstance(text, str):
        text = unicode(text)
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))