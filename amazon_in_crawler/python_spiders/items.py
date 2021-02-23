# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ListingItem(scrapy.Item):
    asin = scrapy.Field() # required
    product_title = scrapy.Field() # required
    brand = scrapy.Field()
    reviewed_product_attribute = scrapy.Field() # required
    review_author = scrapy.Field()
    review_date = scrapy.Field()
    review_header = scrapy.Field() # required
    review_text = scrapy.Field() # required
    review_rating = scrapy.Field()
    review_comment_count = scrapy.Field()
    num_of_people_reacted = scrapy.Field()
    author_profile = scrapy.Field()
    url = scrapy.Field()
    review_url = scrapy.Field()
    position = scrapy.Field()