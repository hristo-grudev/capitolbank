import scrapy

from scrapy.loader import ItemLoader

from ..items import CapitolbankItem
from itemloaders.processors import TakeFirst


class CapitolbankSpider(scrapy.Spider):
	name = 'capitolbank'
	start_urls = ['https://www.capitolbank.com/about/news/']

	def parse(self, response):
		post_links = response.xpath('//h3[@class="title"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="next page-numbers"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="content-inner"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[contains(@class, "meta-date date")]//text()').get()

		item = ItemLoader(item=CapitolbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
