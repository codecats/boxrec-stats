# -*- coding: utf-8 -*-
import argparse
import requests
import lxml
import lxml.html
import lxml.cssselect
import codecs
import collections
import pdb

DIVISIONS = {
    'h': 'Heavyweight',
}
domain = 'http://boxrec.com/'
pages = [1, 30]
url_boxrec = domain + 'ratings.php?sex=M&division={d}&pageID={}'

find_attrs = {
    'HEIGHT': True,
    'COUNTRY': True,
    'REACH': True,
}

def parseint(string):
    return int(''.join([x for x in string if x.isdigit()]))

def get_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--division', '-d', help='Choose division', default='h')
    args = arg_parser.parse_args()
    return args

def to_file(filename, users):
    with codecs.open(filename, 'w', encoding='utf8') as f:
        for user in users:
            for prop, val in user.iteritems():
                f.write(u'{}: {}, '.format(prop, val))
            f.write('\n')

if __name__ == '__main__':
    args = get_args()
    users = []

    max_limit = float(pages[1])
    progress = 1
    for page in xrange(pages[0], pages[1]):
        url_request = url_boxrec.format(page, d=DIVISIONS[args.division])
        request = requests.get(url_request)
        root = lxml.html.fromstring(request.text)
        links = root.xpath('//body//div[@id="mainContent"]//table//a')
        print('Progress {} %'.format(int(progress * 100. / max_limit)))
        print url_request
        progress += 1.
        for link in links:
            href = link.attrib.get('href')
            if href and 'human_id' in href:
                text = requests.get(domain + href).text
                boxer = lxml.html.fromstring(text)
                tds = boxer.xpath('//body//div[@id="bioContent"]//td')
                user = collections.OrderedDict([
                    ('name', boxer.xpath('//body//span[@itemprop="givenName"]')[0].text),
                    ('surname', boxer.xpath('//body//span[@itemprop="familyName"]')[0].text),
                ])
                #find generic
                for i in xrange(len(tds)):
                    if tds[i].text and find_attrs.get(tds[i].text.upper(), False):
                        user[tds[i].text.lower()] = tds[i + 1].text.strip()
                if user.get('height', False) and user.get('reach', False):
                    height = str(parseint(user['height']))[-3:]
                    reach = str(parseint(user['reach']))[-3:]
                    #import pdb;pdb.set_trace()
                    user['length'] = float(reach) - float(height)
                if user:
                    users.append(user)


    to_file('boxers.txt', users)
    sorted_users = filter(lambda x: x.get('length', False), users)
    sorted_users = sorted(
        sorted_users,
        key=lambda x: x.get('length', len(sorted_users)),
        reverse=True
    )


    to_file('by_lenght.txt', sorted_users)

    sorted_users = sorted(
        sorted_users,
        key=lambda x: x.get('reach', len(sorted_users)),
        reverse=True
    )
    to_file('by_reach.txt', sorted_users)

    sorted_users = sorted(
        sorted_users,
        key=lambda x: x.get('height', len(sorted_users)),
        reverse=True
    )
    to_file('by_height.txt', sorted_users)
    #pdb.set_trace()