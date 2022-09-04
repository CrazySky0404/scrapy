import re
from urllib.parse import urljoin
from urllib.request import Request

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [#]
    visited_urls = []

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=headers)

    def parse(self, response):
        if response.url not in self.visited_urls:
            self.visited_urls.append(response.url)
        for link in response.xpath('//*[@class="foto"]//a/@href').extract():
            open_link = urljoin(response.url, link)
            yield response.follow(open_link, callback=self.parse_post)
        next_page = response.xpath('//*[@class="page_selector"]//tr//td[1]/a[2]/@href').get()
        if next_page == None:
            next_page = response.xpath('//*[@class="page_selector"]//tr//td[1]/a[1]/@href').get()
            open_link2 = urljoin(response.url, next_page)
            yield response.follow(open_link2, callback=self.parse)
        open_link2 = urljoin(response.url, next_page)
        yield response.follow(open_link2, callback=self.parse)
        print(f"Пройдені лінки: {self.visited_urls}")

    def parse_post(self, response):
        id = response.xpath('//div[@class="rcp_share_block_top"]').css('div::attr(data-url)').get()
        hours = response.xpath('//div[@class="sub_info"]//div[@class="el"][2]//span/b[1]/text()').get()
        times = response.xpath('//div[@class="sub_info"]//div[@class="el"]//b/text()').getall(),
        world_portion = response.xpath('//div[@class="sub_info"]//div[@class="el"]/text()').re(
            r'\w+'),  # " ,порций, , (ваши ,) "
        all_numbers = response.xpath('//div[@class="sub_info"]//div[@class="el"]//b/text()').getall()
        str = (' '.join(world_portion[0]))
        list_w = str.split()
        checklist = {'порции', 'порций', 'порция', 'порции по', 'ваши', 'по'}
        common_words = set(str.split()) & checklist

        if 'порций' or 'порции' or 'порция' in common_words:
            if 'по' in common_words:
                if 'ваши' in common_words:
                    result_time = all_numbers[2:-1]
                else:
                    result_time = all_numbers[2:0]
            elif 'ваши' in common_words:
                result_time = all_numbers[1:-1]
            else:
                result_time = all_numbers
        elif 'по' in common_words:
            result_time = all_numbers[2:]
        elif 'ваши' in common_words:
            result_time = all_numbers[:-1]
        elif None in common_words:
            result_time = "hello"
        else:
            result_time = 'Oooops!'

        if len(result_time) == 0:
            time_in_minutes = ' '
        else:
            x = int(result_time[0])
            if x < 10:
                if len(result_time) == 2:
                    hours = int(result_time[0])
                    minutes = int(result_time[1])
                    time_in_minutes = hours * 60 + minutes
                else:
                    hours = int(result_time[0])
                    time_in_minutes = hours * 60
            else:
                time_in_minutes = result_time

        yield {
            'ID': re.search(r'(?<==)\w+', id).group(0),
            'Name_recipe': response.xpath('//h1/text()').get(),
            'Desctiption_recipe': response.xpath('//div[@class="rcp_share_block_top"]').css('div::attr(data-description)').get(),
            'Time in minutes': time_in_minutes,
            'Number of servings': response.xpath('//*[@class="portion"]/text()').re('\d+'),
            'Products_table': response.xpath('//*[@class="ingr"]').get(),
            'Products_table_text': response.xpath('//*[@class="ingr"]//td//span/text()').getall(),
            'Cooking': response.xpath('//*[@class="step_n"]/p/text()').getall(),

        }


