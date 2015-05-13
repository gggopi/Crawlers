# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector        import Selector
from scrapy.http import Request
import re
import json
from aeti.items import AetiItem
from json import JSONEncoder
import pickle

# def _default(self, obj):
#     return {'_python_object': pickle.dumps(obj)}

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
       if isinstance(obj, set):
          return list(obj)
       return json.JSONEncoder.default(self, obj)
class CustomEncoder(json.JSONEncoder):
    def _default(self, obj):
        return {'_python_object': pickle.dumps(obj)}
    # def default(self, obj):
    #     if isinstance(obj, AetiItem):
    #         return obj.to_json()

        return json.JSONEncoder.default(self, obj)

class AetiSpiderSpider(CrawlSpider):
    name = 'aeti_spider'
    allowed_domains = ['aeti.com']
    start_urls = ['http://www.aeti.com/careers/all']


    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    # def parse_item(self, response):
    #     i = AetiItem()
    #     #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
    #     #i['name'] = response.xpath('//div[@id="name"]').extract()
    #     #i['description'] = response.xpath('//div[@id="description"]').extract()
    #     return i
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
                print "ding dong!"

        titles=hxs.xpath('//a[@class="posts__post-title"]/text()').extract()
        for title in titles:
            item = NettutsItem()
            item["title"] = title
            yield item

    def parse1(self,response):
        print "hhhhhhhhhhhhhhhhhhhhhhhhhh"
        hxs =Selector(response)
        hxs1=hxs.xpath('//div[@class="content"]')
        # p=hxs1.xpath('p/text()').extract()
        # for p1 in p:
        #      i = AetiItem()
        #      i['desc']= p1
        #      yield i
        i = AetiItem()
        i['company_name']="American Electric Technologies, Inc."
        i['company_url']="aeti.com"
        i['job_title']=hxs.xpath('//h1[@class="title"]/text()').extract()
        i['desc1']=hxs1.xpath('p/text()').extract()
        #yield i
        
        #j= AetiItem()
        i['desc2']=hxs1.xpath('ul/li/text()').extract()
        yield i

        # with open('data.json','a') as outfile:
        #     json.dump(i1.__dict__ for i1 in i,outfile,)#p.__dict__