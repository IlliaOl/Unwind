import scrapy
from scrapy.spider import CrawlSpider
from scrapy.selector import Selector


class Aladin_Spider(CrawlSpider):
    """
    A class used to scrape information liniakino.com

    Methods
    -------
    parse(response)
        Parses website home page

    Pages(response)
        Iterates over website pages

    Aladin(response)
        Parses event page
    """

    name = "aladin"
    start_urls = ['http://liniakino.com/movies/']

    def parse(self, response):
        """Parses website page.

        Parameters
        ----------
        response : str
            html page of a requested page
        """

        next_page = response.css('div[class="poster"] a::attr(href)').extract()
        if next_page:

            for name in next_page:
                yield scrapy.Request(
                    response.urljoin(name),

                    callback=self.Pages
                )

    def Pages(self, response):
        """Iterates over website pages.

        Parameters
        ----------
        response : str
            html page of a requested page
        """

        next_page = response.css('div[class="buttons"] input ::attr(href)').extract()
        if next_page:

            for name in next_page:
                yield scrapy.Request(
                    response.urljoin(name),

                    callback=self.Aladin
                )

    def Aladin(self, response):
        """Parses event page.

        Parameters
        ----------
        response : str
            html page of a requested page
        """

        select = Selector(response)
        resp = select.response.css('.showtime-movie')
        for scrap in resp:
                yield {

                    'name': scrap.css('h1 a ::text').extract_first(),
                    'time': scrap.xpath('//div[@class="showtime"]/div[1]/div[1]/ul/li/a/text()').extract(),
                    'cinema': scrap.xpath('//div[@class="showtime"]/div[1]/div[1]/label/text()').extract(),
                    'address': 'st. Grishka, 5'
                }


