import scrapy
import RoundwiseResultsSpider
import constituencyWiseSpider
from scrapy.crawler import CrawlerProcess



process = CrawlerProcess({
 'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
 'FEED_FORMAT': 'json',
 'FEED_URI': 'constituencywise.json'
 })
process.crawl(constituencyWiseSpider.constituencywiseSpider)

process = CrawlerProcess({
'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
'FEED_FORMAT': 'json',
'FEED_URI': 'RoundwiseResults.json'
})
process.crawl(RoundwiseResultsSpider.RoundwiseResultsSpider)

process.start()