import re
from urllib.parse import urljoin

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    delimiter = ";"

    def start_requests(self):
        urls = [
             'https://www.russianfood.com/recipes/recipe.php?rid=155166',
            'https://www.russianfood.com/recipes/recipe.php?rid=162162',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        id = response.xpath('//div[@class="rcp_share_block_top"]').css('div::attr(data-url)').get()

        yield {
            'ID': re.search(r'(?<==)\w+', id).group(0),
            'Name_recipe': response.xpath('//h1/text()').get(),
            'Desctiption_recipe': response.xpath('//div[@class="rcp_share_block_top"]').css('div::attr(data-description)').get()
        }

        # 'Print_version_LINK': response.xpath('//div[@class="print_ver padding_l"]//span/@href').get(),
        # 'Print_version_LINK2': response.css('script::attr(href)').get(),
        # 'Print_version4': response.xpath('//span/text()'),
        # 'title': response.css('div.col-12 a::attr(href)').extract(),
        # 'Page 2': response.xpath('//a[@class="btn btn-default no-hover mx-xs-0 mx-sm-1"]/text()').get(),
        # 'Page 3': response.xpath('(//a[last()][@class="btn btn-default no-hover mx-xs-0 mx-sm-1"])/@href').get()

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

# from urllib.parse import urljoin
#
# import scrapy
#
#
# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     #download_delay = 2
#
#     def start_requests(self):
#         urls = [
#             #'https://quotes.toscrape.com/tag/happiness/page/1/',
#             'https://parsemachine.com/sandbox/catalog/',
#         ]
#         for url in urls:
#             yield scrapy.Request(url=url, callback=self.parse)
#
#     def parse(self, response):
#         # for quote in response.css('.product-card .title::attr("href")').extract():
#         #     yield {
#         #         'Links': response.urljoin(quote),
#         #         #'title': response.css('div.col-12 a::attr(href)').extract(),
#         #         #'Page 2': response.xpath('//a[@class="btn btn-default no-hover mx-xs-0 mx-sm-1"]/text()').get(),
#         #         'Page 3': response.xpath('(//a[last()][@class="btn btn-default no-hover mx-xs-0 mx-sm-1"])/@href').get()
#         #     }
#         # next_page = response.xpath('(//a[last()][@class="btn btn-default no-hover mx-xs-0 mx-sm-1"])/@href').get()
#         #print(next_page)
#
#         yield {
#             #'Links': response.urljoin(quote),
#             # 'title': response.css('div.col-12 a::attr(href)').extract(),
#             # 'Page 2': response.xpath('//a[@class="btn btn-default no-hover mx-xs-0 mx-sm-1"]/text()').get(),
#             'Page 3': response.xpath('(//a[last()][@class="btn btn-default no-hover mx-xs-0 mx-sm-1"])/@href').get()
#         }
#
#         if next_page:
#             abs_url = f"https://parsemachine.com/sandbox/catalog/{next_page}"
#             print(abs_url)
#             yield scrapy.Request(
#                 url=abs_url,
#                 callback=self.parse
#             )
#         else:
#             print()
#             print('No Page Left')
#             print()
#
