import re
from urllib.parse import urljoin
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
#scrapy crawl quotes -s JOBDIR=crawls/crawl1 -o quotes5.csv
    def start_requests(self):
        urls = [
            'https://www.russianfood.com/recipes/bytype/?fid=1660',
            # 'https://www.russianfood.com/recipes/bytype/?fid=1676',
            # 'https://www.russianfood.com/recipes/recipe.php?rid=125466',
            # 'https://www.russianfood.com/recipes/recipe.php?rid=116458',
            # 'https://www.russianfood.com/recipes/recipe.php?rid=113251', Коврижка!!!!
            # 'https://www.russianfood.com/recipes/recipe.php?rid=157024',
            # 'https://www.russianfood.com/recipes/recipe.php?rid=162162',
            # 'https://www.russianfood.com/recipes/recipe.php?rid=120468',
            # 'https://www.russianfood.com/recipes/recipe.php?rid=122523',
            # 'https://www.russianfood.com/recipes/recipe.php?rid=121840'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        find_all_links = response.xpath('//div[@class="recipe_list_new"]//div[@class="foto_o"]//a/@href').getall()
        for link in find_all_links:
            open_link = urljoin(response.url, link)
            yield response.follow(open_link, callback=self.parse_post)

    def parse_post(self, response):
        id = response.xpath('//div[@class="rcp_share_block_top"]').css('div::attr(data-url)').get()
        # hours = response.xpath('//div[@class="sub_info"]//div[@class="el"][2]//span/b[1]/text()').get()
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
            time_in_minutes = 'No time'
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
            # 'Desctiption_recipe': response.xpath('//div[@class="rcp_share_block_top"]').css('div::attr(data-description)').get(),
            # 'Time in minutes': time_in_minutes,
            # 'Number of servings': response.xpath('//*[@class="portion"]/text()').re('\d+'),
            # 'Products_table': response.xpath('//*[@class="ingr"]').get(),
            # 'Products_table_text': response.xpath('//*[@class="ingr"]//td//span/text()').getall(),
            # 'Cooking': response.xpath('//*[@class="step_n"]/p/text()').getall(),

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
