import scrapy


class RoundwiseResultsSpider(scrapy.Spider):
    name = "roundwiseResults"
    start_urls = ['http://results.eci.gov.in/DELHITRENDS2020/RoundwiseU051.htm?ac=1']


    def parse(self, response):
        delhi_url = "http://results.eci.gov.in/DELHITRENDS2020/RoundwiseU05<seatCode>.htm?ac=<seatCode>"
        seats_str = response.xpath('//*[@id="U05"]//@value[1]').get()
        seats_details = seats_str.split(";")
        seat_codes = [x.split(",")[0] for x in seats_details]


        for seat in seat_codes:
            self.logger.info('start scraping for ' + seat)
            yield scrapy.Request(delhi_url.replace("<seatCode>", seat), callback=self.parse_seat)




    def parse_seat(self, response):
        self.logger.info('hello this is my first spider')
        rounds = response.xpath("//div[@class='tabcontent']//table[@class='round-tbl']")
        for round in rounds:
            seat = str(round.xpath(".//thead//tr[2]//th//text()").get()).strip()
            round_txt = str(round.xpath(".//thead//tr[1]//th//text()").get()).strip()

            for candidate in round.xpath("./tbody/tr[@style='font-size:12px;']"):
                yield {'seat': seat,
                       'round': round_txt.replace("Round-",""),
                       'candidate': candidate.xpath("./td[1]/text()").get(),
                       'party': candidate.xpath("./td[2]/text()").get(),
                       'total': candidate.xpath("./td[5]/text()").get(),
                       }