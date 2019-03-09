# -*- coding: utf-8 -*-
import scrapy
from src.crawler.crawler.items import CrawlerItem

class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/top250']

    def parse(self, response):
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']//li")
        for i_item in movie_list:
            item = CrawlerItem()
            item['serial_number'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            item['movie_name'] = i_item.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
            contents = i_item.xpath(".//div[@class='info']//div[@class='bd']/p[1]/text()").extract()
            for content in contents:
                item['introduce'] = ''.join(content.split())
            item['star'] = i_item.xpath(".//span[@class='rating_num']/text()").extract_first()
            item['evaluate'] = i_item.xpath(".//div[@class='star']//span[4]/text()").extract_first()
            item['describe'] = i_item.xpath(".//p[@class='quote']/span[1]/text()").extract_first()
            print(item)
