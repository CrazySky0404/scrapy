import re
from urllib.parse import urljoin
from urllib.request import Request

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    #DOWNLOAD_DELAY = 0,3
    start_urls = [
        'https://www.russianfood.com/recipes/bytype/?fid=1660',
    ]

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url, headers=headers)
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
        # headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        # for url in self.start_urls:
        #     yield scrapy.Request(url, headers=headers)
        # yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url, headers=headers)
        print(f"Зішкрібаємо дані")

        find_links = response.xpath('//div[@class="recipe_list_new"]//div[@class="foto_o"]//a/@href').getall()
        print(find_links)
        for link in find_links:
            open_link = urljoin(response.url, link)
            yield response.follow(open_link, callback=self.parse_post)

        next_page = response.xpath('//*[tr(@class,"pages") and not(tr(@class, "notactiv")]/a/text()').get()
        print(f"Переход на страницу {next_page}")
        abs_url = f"https://www.russianfood.com{next_page}"
        print(abs_url)
        open_link2 = urljoin(response.url, abs_url)
        yield response.follow(open_link2, callback=self.parse)

    def parse_post(self, response):
        yield {
            'Name_recipe': response.xpath('//h1/text()').get()
        }

# next_page = response.xpath('(//a[last()][@class="btn btn-default no-hover mx-xs-0 mx-sm-1"])/@href').get()
# #print(next_page)
#
# if next_page:
#     abs_url = f"https://parsemachine.com/sandbox/catalog/{next_page}"
#     print(abs_url)
#     yield scrapy.Request(
#         url=abs_url,
#         callback=self.parse
#     )
# else:
#     print()
#     print('No Page Left')
#     print()
