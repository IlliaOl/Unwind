import scrapy
from scrapy.spider import CrawlSpider
from scrapy.selector import Selector


class Freedom_Spider(CrawlSpider):
    """
    A class used to scrape information from freedomhall.com.ua

    Methods
    -------
    parse(response)
        Parses website page
    """

    name = "freedom"
    start_urls = ['http://www.freedomhall.com.ua/']

    def parse(self, response):
        """Parses website page.

        Parameters
        ----------
        response : str
            html page of a requested page
        """

        select = Selector(response)
        resp = select.response.css('.description')
        for scrap in resp:
                yield {
                    'name': scrap.css('div[class="artist"] ::text').extract_first(),
                    'time': scrap.css('div[class="time"] ::text').extract(),
                    'date': scrap.css('div[class="date"] ::text').extract(),
                    'place': scrap.xpath('//div[@class="row"]/*/p[1]/strong/text()').extract(),
                    'address': 'st. Kirillovskaya 134'
                }
