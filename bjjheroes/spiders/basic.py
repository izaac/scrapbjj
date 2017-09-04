# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request

from bjjheroes.items import BjjheroesItem

base_url = 'http://www.bjjheroes.com'


class BasicSpider(scrapy.Spider):
    name = "basic"
    allowed_domains = ["bjjheroes.com"]
    start_urls = (
        'http://www.bjjheroes.com/a-z-bjj-fighters-list',
    )

    def parse(self, response):

        sel = Selector(response)
        rows = sel.xpath('//tr[position()>1]')

        for row in rows:
            item = BjjheroesItem()

            # name
            item['name'] = row.xpath('./td[1]/a/text()').extract()[0]

            # last name
            item['lastname'] = row.xpath('./td[2]/a/text()').extract()[0]

            # url
            url = row.xpath('./td[1]/a/@href').extract()
            url = str(url[0])
            if not url.startswith('http'):
                url = base_url + url
            request = Request(url, callback=self.parse_info)
            request.meta['item'] = item
            yield request

    @staticmethod
    def parse_info(response):
        item = response.meta['item']
        item['url'] = response.url
        sel = Selector(response)
        raw = sel.xpath('//*[@id="post-2729"]/div/*/text()').extract()
        content = [x for x in raw if x != '\n' and x != ' ' and '\r\n' not in x and x != '\n \n \n']
        item['content'] = content
        yield item
