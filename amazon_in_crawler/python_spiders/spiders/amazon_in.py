import scrapy
from ..helper import format_date, remove_white_spaces, remove_unicode_char
from ..loaders import ListingLoader
import re
from word2number import w2n

class AmazonInSpider(scrapy.Spider):
    name = 'amazon_in'
    allowed_domains = ['amazon.in']
    start_url = ['https://www.amazon.in/']
    
    def start_requests(self):
        start_urls = input('Enter ASIN/URL:').split(',')
        for char in start_urls:
            if remove_white_spaces(char).isalnum()==True:
                base_url= self.start_url[0]+'dp/'+remove_white_spaces(char)
                asin=remove_white_spaces(char)
            else:
                base_url= remove_white_spaces(char)
                asin=re.search(r'(?<=dp/)\w+',base_url)
                if asin:
                    asin=asin.group()
            yield scrapy.Request(url=base_url,
                                 callback=self.parse,
                                 meta={'ASIN':asin,
                                       'URL':base_url}
                                 )
            
    def parse(self, response, **kwargs):
        asin = response.meta.get('ASIN')
        url = response.meta.get('URL')
        product_title = response.xpath('.//*[@id="productTitle"]/text()').extract_first().strip()
        brand = response.xpath('.//*[@id="bylineInfo"]/text()').extract_first()
        
        all_reviews = response.xpath(".//*[@data-hook='see-all-reviews-link-foot']/@href").extract_first()
        if all_reviews:
            yield scrapy.Request(
                    url='https://www.amazon.in'+all_reviews,
                    callback=self.get_reviews,
                    meta={'request_url': 'https://www.amazon.in' + all_reviews,
                          'ASIN': asin,
                          'URL': url,
                          'product_title': product_title,
                          'brand': brand})
        
    def get_reviews(self, response, **kwargs):
        asin = response.meta.get('ASIN')
        url = response.meta.get('URL')
        product_title = response.meta.get('product_title')
        brand = response.meta.get('brand')
        review_title_link = response.xpath('.//*[contains(@class,"review-title")]/@href').extract()
        for i in review_title_link:
            yield scrapy.Request(url='https://www.amazon.in'+i,
                                     callback = self.get_review_details,
                                     meta={'request_url': 'https://www.amazon.in'+i,
                                          'ASIN': asin,
                                          'URL': url,
                                          'product_title': product_title,
                                          'brand': brand}
                                     )
                
        next_page_url = response.xpath('.//a[contains(text(),"Next page")]/@href').extract_first()
        if next_page_url:
            yield scrapy.Request(url='https://www.amazon.in'+next_page_url,
                                     callback=self.get_reviews,
                                     meta={'request_url':'https://www.amazon.in'+next_page_url,
                                           'ASIN': asin,
                                           'URL': url,
                                           'product_title': product_title,
                                           'brand': brand})
                
    def get_review_details(self,response):
        item_loader = ListingLoader(response=response)
        item_loader.add_value('asin', response.meta.get('ASIN'))
        item_loader.add_value('url', response.meta.get('URL'))
        item_loader.add_value('review_url', response.meta.get('request_url'))
        item_loader.add_xpath('review_author','.//*[@class="a-profile-name"]/text()')
        item_loader.add_xpath('review_text','.//*[contains(@class,"review-text")]/span/text()')
        review_header = response.xpath('.//*[contains(@class,"review-title")]/span/text()').extract_first()
        if review_header:
            item_loader.add_value('review_header',remove_unicode_char(review_header))
        item_loader.add_value('product_title',response.meta.get('product_title'))
        brand = response.meta.get('brand')
        if brand:
            item_loader.add_value('brand',remove_white_spaces(brand.split(':')[-1]))   
        author_profile = response.xpath('.//*[@class="a-profile"]/@href').extract_first()
        if author_profile:
            item_loader.add_value('author_profile','https://www.amazon.in'+author_profile)
        attribute = response.xpath('.//*[@data-hook="format-strip"]/text()').extract()
        if attribute:
            item_loader.add_value('reviewed_product_attribute',' | '.join(attribute))
        rating = response.xpath('.//*[contains(@class,"review-rating")]//text()').extract_first()
        if rating:
            item_loader.add_value('review_rating',str(int(float(rating.split()[0]))))
        helpful_statement = response.xpath('.//*[contains(@class,"vote-text")]/text()').extract_first()
        if helpful_statement and helpful_statement.split()[0].isdigit()==True:
            item_loader.add_value('num_of_people_reacted',str(int(helpful_statement.split()[0])))
        elif helpful_statement and helpful_statement.split()[0].isalpha()==True:
            item_loader.add_value('num_of_people_reacted',str(w2n.word_to_num(helpful_statement.split()[0])))
            
        review_date = response.xpath('.//*[contains(@class,"review-date")]/text()').extract_first()
        date = re.search(r'(?<=\son\s).*',review_date)
        if date:
            date_str = remove_white_spaces(date.group())
            item_loader.add_value('review_date',format_date(date_str))
        
        yield item_loader.load_item()

        
        