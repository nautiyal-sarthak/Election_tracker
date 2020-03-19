import scrapy


class constituencywiseSpider(scrapy.Spider):
    name = "constituencywiseResults"
    start_urls = ['http://results.eci.gov.in/DELHITRENDS2020/statewiseU051.htm']


    def parse(self, response):
        main_url = "http://results.eci.gov.in/DELHITRENDS2020/"
        links = response.xpath('//*[@id="ElectionResult"]/tr[4]//a/@href')

        for link in links:
            link_str = link.get()
            if ".htm" in link_str:
                self.logger.info('starting spider for ' + link_str)
                yield scrapy.Request(main_url + link_str, callback=self.parse_constituency)


    def parse_constituency(self, response):
        rows = response.xpath('//*[@id="ElectionResult"]//tr[@style="font-size:12px;"]')
        for row in rows:
            constituency = row.xpath('./td[1]/text()').get()
            leadingCandidate = row.xpath('./td[3]/text()').get()
            leadingParty = row.xpath('./td[4]/table/tbody/tr/td[1]/text()').get()
            trailingCandidate = row.xpath('./td[5]/text()').get()
            trailingParty = row.xpath('./td[6]/table/tbody/tr/td[1]/text()').get()
            margin = row.xpath('./td[7]/text()').get()
            status = row.xpath('./td[8]/text()').get()
            last_winning_can = row.xpath('./td[9]/text()').get()
            last_winning_party = row.xpath('./td[10]/text()').get()
            last_margin = row.xpath('./td[11]/text()').get()


            yield {'constituency': constituency,
                   'leadingCandidate': leadingCandidate,
                   'leadingParty': leadingParty,
                   'trailingCandidate': trailingCandidate,
                   'trailingParty': trailingParty,
                   'margin': margin,
                   'status':status,
                   'last_winning_can':last_winning_can,
                   'last_winning_party':last_winning_party,
                   'last_margin':last_margin
                   }
