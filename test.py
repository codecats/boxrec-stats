# -*- coding: utf-8 -*-
import argparse
import requests
import lxml
import lxml.html
import lxml.cssselect
import lxml.html.clean as clean
import HTMLParser
import codecs

pars = HTMLParser.HTMLParser()

hi = u'<article>height<div>6&prime; 6&Prime; &nbsp; / &nbsp; 198cm</div></article>'
#pars.unescape(hi)
root = lxml.html.fromstring(hi)
user = {
    'name': root.xpath('//article//div')[0].text
}

with codecs.open('hi.txt', 'w', encoding='utf8') as f:
    for item, val in user.iteritems():
        f.write(u'{} {}'.format(item, val))

