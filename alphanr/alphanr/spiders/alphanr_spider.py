# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from alphanr.items import AlphanrItem
from scrapy.selector import Selector
import re

class AlphanrSpiderSpider(CrawlSpider):
    name = 'alphanr_spider'
    allowed_domains = ['alphanr.com']
    start_urls = ['https://alphanr.mua.hrdepartment.com/hr/ats/JobSearch/viewAll']

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    # def parse_item(self, response):
    #     i = AlphanrItem()
    #     #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
    #     #i['name'] = response.xpath('//div[@id="name"]').extract()
    #     #i['description'] = response.xpath('//div[@id="description"]').extract()
    #     return i
    def parse(self,response):
        print "hush hush ---- "+ str(response)
        hxs1=Selector(response)
        hxs=hxs1.xpath('//table[@id="jobSearchResultsGrid_table"]/tbody/tr/td')
        links=hxs.xpath('a/@href').extract()
        print links
        crawledLinks=[]
        linkPattern = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")
        for link in links:
            link='https://alphanr.mua.hrdepartment.com'+link
            item=AlphanrItem()
            item['linkk']=link
            # If it is a proper link and is not checked yet, yield it to the Spider
            if linkPattern.match(link) and not link in crawledLinks:
                crawledLinks.append(link)
                print "link= " + item['linkk']
                yield Request(item['linkk'], callback=self.parse1,method='GET')
            else:
                print "ding dong!"


        titles=hxs.xpath('a/span/text()').extract()
        for title in titles:
            item = AlphanrItem()
            item["title"] = title
            yield item

    def parse1(self,response):
        print "hhhhhhhhhhhhhhhhhhhhhhhhhh"

