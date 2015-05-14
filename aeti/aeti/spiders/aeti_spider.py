# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector        import Selector
from scrapy.http import Request
import re
import json
from aeti.items import AetiItem

class AetiSpiderSpider(CrawlSpider):
    name = 'aeti_spider'
    allowed_domains = ['aeti.com']
    start_urls = ['http://www.aeti.com/careers/all']
    
    item={
            "company_name":"American Electric Technologies, Inc.",
            "company_url":"aeti.com"
        }
    job_title={}

    def parse(self,response):
        hxs1=Selector(response)
        hxs=hxs1.xpath('//div[@class="item-list"]/ul')
        links=hxs.xpath('li/div/span/a/@href').extract()
        crawledLinks=[]
        linkPattern = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")
        for link in links:
            link='http://www.aeti.com'+link
            print link

            # If it is a proper link and is not checked yet, yield it to the Spider
            if linkPattern.match(link) and not link in crawledLinks:
                crawledLinks.append(link)
                yield Request(link, self.parse1)
            else:
                print "InAppropriate Link" 


    def parse1(self,response):
        hxs =Selector(response)
        hxs1=hxs.xpath('//div[@class="content"]')

        i = AetiItem()
        i['company_name']="American Electric Technologies, Inc."
        i['company_url']="aeti.com"
        i['job_title']=hxs.xpath('//h1[@class="title"]/text()').extract()
        i['desc1']=hxs1.xpath('p/text()').extract()
        i['desc2']=hxs1.xpath('ul/li/text()').extract()
        self.job_title[str(i['job_title'][0])]=str(i['desc1'])+str(i['desc2'])
        self.item['jobs_opportunities']=self.job_title
        with open('data.json','w') as outfile:
            json.dump(self.item,outfile,)
