# -*- coding: utf-8 -*-
from scrapy import Spider, Request, FormRequest
import csv


class ItemSpider(Spider):
    name = "teplocel"
    start_urls = ["http://www.teplocel.ru/catalog"]



    # def parse(self, response):
    #     return FormRequest.from_response(
    #         response,
    #         formdata={'username': '2632803528', 'password': '112265'},
    #         callback=self.after_login
    #     )

    # def after_login(self, response):
    def parse(self, response):
        # if "authentication failed" in response.body:
        #     self.logger.error("Login failed")
        #     return
        with open('items.csv', 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(['Title', 'Price', 'URL'])
        links = response.xpath('//div[@class="catalog-main-categories"]/div/ul/li/a/@href').extract()
        for link in links:
            # yield Request(response.urljoin(link),
            yield Request(response.urljoin(link), cookies={'_ym_uid': '1500296968748492942',
                                                           'BITRIX_SM_SOUND_LOGIN_PLAYED': 'Y',
                                                           '_ym_isad': '2',
                                                           'PHPSESSID': 'b37udeo0ru06kao7qjl93gbgs3',
                                                           '_ga': 'GA1.2.2028308846.1500296968',
                                                           '_gid': 'GA1.2.1841182279.1501513499',
                                                           '_gat': '1', '_ym_visorc_33143708':'w',
                                                           'BITRIX_SM_SALE_UID': '1193853',
                                                           'BITRIX_SM_LOGIN': '2632803528'},
                          callback=self.get_pages)

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