import scrapy
from scrapy.spider import CrawlSpider
from scrapy.selector import Selector


class Theatre_Spider(CrawlSpider):
    """
    A class used to scrape information from molodyytheatre.com

    Methods
    -------
    parse(response)
        Parses website page
    """

    name = "theatre"
    start_urls = ['http://molodyytheatre.com/afisha']

    def parse(self, response):
        """Parses website page.

        Parameters
        ----------
        response : str
            html page of a requested page
        """

        select = Selector(response)
        resp = select.response.css('div[class*="views-row"]')
        for scrap in resp:
                yield {
                    'name': scrap.css('div[class*="views-field-field-event-title"] div[class="field-content"] a ::text').extract(),
                    'time': scrap.css('div[class*="views-field-field-time"] div[class="field-content"] span ::text').extract(),
                    'place': 'Molodyy Theatre',
                    'address': 'st. Prorizna, 17'
                }
