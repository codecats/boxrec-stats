# -*- coding: utf-8 -*-
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from boxrec.items import BoxrecItem
import pdb

class BoxrecSpider(Spider):
    page_start = 1
    page_stop = 12
    name = 'boxrec'
    BASE_DOMAIN = 'http://boxrec.com'
    allowed_domains = ['boxrec.com']
    start_urls = []


    def __init__(self):
        for i in xrange(self.page_start, self.page_stop):
            url = 'http://boxrec.com/ratings.php?sex=M&division={d}&pageID={}'
            url = url.format(i, d='Heavyweight')
            self.start_urls.append(url)

        super(BoxrecSpider, self).__init__()

    def parse(self, response):
        sel = Selector(response)
        anchors = sel.xpath('.//a')
        for anchor in anchors:
            #pdb.set_trace()
            href = anchor.xpath('@href').extract()
            href = '{}/{}'.format(self.BASE_DOMAIN, href[0]) if len(href) else None
            if href and not 'human_id' in href:
                href = None
            if href is not None:
                #if 'human_id=35680' in href:
                yield Request(href, callback=self.parse_boxer)

    def parse_boxer(self, response):
        sel = Selector(response)
        boxer = BoxrecItem()
        self.log('RESP')
        self.log(response)
        names = sel.xpath("descendant-or-self::*[@class and contains(concat(' ', normalize-space(@class), ' '), ' title ')]/span/span/text()")
        boxer['name'] = names[0].extract()
        boxer['surname'] = names[1].extract()

        height = sel.xpath(".//*[@id='bioContent']/div/table/tr[11]/td[2]/text()")
        if height:
            boxer['height'] = height[0].extract()
        reach = sel.xpath(".//*[@id='bioContent']/div/table/tr[12]/td[2]/text()")
        if reach:
            boxer['reach'] = reach[0].extract()

        return boxer