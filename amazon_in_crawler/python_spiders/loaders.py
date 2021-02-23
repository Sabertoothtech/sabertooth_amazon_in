from scrapy.loader import ItemLoader
from itemloaders.processors import Join, MapCompose, TakeFirst, Identity
from w3lib.html import remove_tags
from .items import ListingItem
from .helper import convert_to_numeric


def filter_empty(_s):
    return _s or None

class ListingLoader(ItemLoader):
    default_item_class = ListingItem
    # default_input_processor = MapCompose()
    default_output_processor = TakeFirst()

    review_text_in = MapCompose(remove_tags, str.strip, filter_empty)
    review_text_out = Join(' ')
    product_title_in = MapCompose(remove_tags, str.strip, filter_empty)
    product_title_out = Join(' ')

    # title_in = MapCompose(remove_tags)
    product_title_in = MapCompose(remove_tags, str.strip)
    review_header_in = MapCompose(remove_tags, str.strip)
    brand_in = MapCompose(remove_tags, str.strip)

    review_rating_in = MapCompose(convert_to_numeric)
    review_comment_count_in = MapCompose(convert_to_numeric)
    num_of_people_reacted_in = MapCompose(convert_to_numeric)

    author_profile_out = TakeFirst()
    review_url_out = TakeFirst()
    url_out = TakeFirst()
    asin_out = Join()

    # PK
    review_author_in = MapCompose(str.strip, filter_empty)
    review_author_out = Join('')
    position = Identity()

    def __init__(self, response):
        super(ListingLoader, self).__init__(response=response)
        # self.images_in = MapCompose(response.urljoin)
        self.images_in = MapCompose(response.urljoin, str.strip)  # PK
