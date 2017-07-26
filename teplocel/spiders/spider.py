# -*- coding: utf-8 -*-
from scrapy import Spider, Request
import csv


class ItemSpider(Spider):
    name = "teplocel"
    start_urls = ["http://www.teplocel.ru/catalog/",]

    def parse(self, response):
        with open('items.csv', 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(['Title', 'Price', 'URL'])
        links = response.xpath('//div[@class="catalog-main-categories"]/div/ul/li/a/@href').extract()
        for link in links:
            yield Request(response.urljoin(link), callback=self.get_pages)

    def get_pages(self, response):
        pages = response.xpath('//div[@class="pager"]/ul/li[last()]/a/@data-page').extract_first()
        if pages is not None:
            for page in range(int(pages)):
                page_link = response.url + "?PAGEN_1={}".format(page)
                yield Request(page_link, callback=self.parse_items)
        else:
            yield Request(response.url, callback=self.parse_items)

    def parse_items(self, response):
        items = response.xpath('//div[@class="items"]/ul/li').extract()
        for item in items:
            item_title = item.split('-title">')[1].split('</a>')[0].encode('utf-8').replace('\t', '')
            try:
                item_price = item.split('-price">')[1].split(' <span')[0].encode('utf-8')
            except IndexError:
                item_price = 'n/a'
            item_url = item.split('href="')[1].split('">')[0].encode('utf-8')

            with open('items.csv', 'a') as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                writer.writerow([item_title, item_price, item_url])
            print "Saved: ", item_title, item_price, item_url