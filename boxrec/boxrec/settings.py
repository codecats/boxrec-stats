# -*- coding: utf-8 -*-

# Scrapy settings for boxrec project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'boxrec'

SPIDER_MODULES = ['boxrec.spiders']
NEWSPIDER_MODULE = 'boxrec.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'boxrec (+http://www.yourdomain.com)'
#boxrec checks user agent
USER_AGENT = 'Safari/7534.48.3'
