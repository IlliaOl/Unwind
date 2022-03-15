import scrapy
from scrapy.spider import CrawlSpider
from scrapy.selector import Selector


class Multiplex_Spider(CrawlSpider):
    """
    A class used to scrape information from multiplex.ua

    Methods
    -------
    parse(response)
        Parses website home page

    Multiplex(response)
        Parses event page
    """

    name = "multiplex"
    start_urls = ['https://multiplex.ua/ua/']

    def parse(self, response):
        """Parses website home page.

        Parameters
        ----------
        response : str
            html page of a requested page
        """

        next_page = response.css('a[class="mpp_title"]::attr(href)').extract()
        if next_page:

            for name in next_page:
                yield scrapy.Request(
                    response.urljoin(name),

                    callback=self.Multiplex
                )

    def Multiplex(self, response):
        """Parses event page.

        Parameters
        ----------
        response : str
            html page of a requested page
        """

        select = Selector(response)
        resp = select.response.css('.movie_info')
        for scrap in resp:
                yield {
                    'name': scrap.css('div[class="column2"] h1 ::text').extract_first(),
                    'time': scrap.xpath('//div[@class="all_sessions_area"]/div[1]/div[1]/div/p/span/text()').extract(),
                    'cinema': scrap.xpath('//p[@class="cutted"]/span[1]/a[@class="brcr_link"]/span/text()').extract(),
                    'address': scrap.xpath('//div[@class="rm_clist"]/div[2]/div/p[@class="address"]/text()').extract_first(),
                }

