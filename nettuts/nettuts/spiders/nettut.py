# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector        import Selector
from nettuts.items import NettutsItem
from scrapy.http import Request
import re

class NettutSpider(CrawlSpider):
    name = 'nettut'
    allowed_domains = ['code.tutsplus.com']

    start_urls = ['http://code.tutsplus.com/']

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    # def parse_item(self, response):
    #     i = NettutsItem()
    #     #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
    #     #i['name'] = response.xpath('//div[@id="name"]').extract()
    #     #i['description'] = response.xpath('//div[@id="description"]').extract()
    #     return i
    def parse(self,response):
        hxs=Selector(response)
        links=hxs.xpath('//a[@class="posts__post-title"]/@href').extract()
        crawledLinks=[]
        linkPattern = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")
        for link in links:
            print link
            # If it is a proper link and is not checked yet, yield it to the Spider
            if linkPattern.match(link) and not link in crawledLinks:
                crawledLinks.append(link)
                yield Request(link, self.parse1)


        titles=hxs.xpath('//a[@class="posts__post-title"]/text()').extract()
        for title in titles:
            item = NettutsItem()
            item["title"] = title
            yield item

    def parse1(self,response):
        print "hhhhhhhhhhhhhhhhhhhhhhhhhh"
        print str(response)
        hxs =Selector(response)
        p=hxs.xpath('//p/text()').extract()
        #print p

