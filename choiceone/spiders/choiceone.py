import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from choiceone.items import Article


class choiceoneSpider(scrapy.Spider):
    name = 'choiceone'
    start_urls = ['https://www.choiceone.com/news-resources/']

    def parse(self, response):
        links = response.xpath('//div[@class="post"]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//div[@class="section post-header"]/h1/span/text()').get()
        if title:
            title = title.strip()

        date = " ".join(response.xpath('//div[@id="hubspot-author_data"]/text()').getall())
        if date:
            date = " ".join(date.split()[1:])

        content = response.xpath('//div[@class="section post-body"]//text()').getall()
        content = [text for text in content if text.strip() and '{' not in text]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
