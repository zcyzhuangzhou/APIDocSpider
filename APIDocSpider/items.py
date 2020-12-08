# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ApidocspiderItem(scrapy.Item):
    # define the fields for your item here like:
    api_id = scrapy.Field()
    api_type = scrapy.Field()
    qualified_name = scrapy.Field()
    full_declaration = scrapy.Field()
    short_description = scrapy.Field()

    html = scrapy.Field()
    clean_text = scrapy.Field()
    html_type = scrapy.Field()
