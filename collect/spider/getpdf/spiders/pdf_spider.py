import scrapy
import time
from scrapy.http import Request

class PdfSpider(scrapy.Spider):
    name = "interspeech"
    # notice: not thread-safe
    
    def start_requests(self):
        """
        We start our requests at the [root website](https://www.isca-speech.org/archive/), 
        """
        urls = ['https://www.isca-speech.org/archive/',]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        """ Parse the root website and extract links for annual achives.
        We use *xpath* to locate the block which contains 
        all the links to each year's archive websides. We loop over 
        each year's archive link, and only process the target year's 
        link at one time.
        """
        urls = response.xpath('/html/body/div[8]/div[3]/div/a')
        year_links = []
        for url in urls:
            year = url.xpath('text()').extract()[0]
            link = url.xpath('@href').extract()[0]
            if year != self.target_year:
                continue
            year_links.append((year, link))

        for year, link in year_links:
            self.log(f'---Year {year}, link:{link}')
            new_link = response.urljoin(link)
            yield scrapy.Request(url=new_link, callback=self.download_one_year)

    
    def download_one_year(self, response):
        """ Download meta data within one year 
        After moving to the target year's archive link(an example), we 
        use xpath to locate the block that contains all the paper links.
        """
        papers = response.xpath('/html/body/div[4]/div[2]/div/div/div/a')
        for paper in papers:
            title = paper.xpath('p/text()').extract()
            title = ' '.join(title)
            title = title.strip()
            href = paper.xpath('@href').extract()[0]
            new_link = response.urljoin(href)
            yield scrapy.Request(url=new_link, callback=self.download_one_pdf)

    def download_one_pdf(self, response):
        """ Download meta data from a paper's descriptive page
        For each paper link, we navigate to its description page. And again 
        with xapth, we locate and extract the content needed(e.g. title, 
        author, abstract, url), and return a python dictionary object 
        containing all this information.
        """
        link = response.xpath('/html/body/div[3]/div/div/div/a/@href').get()
        new_link = response.urljoin(link)
        yield {
            'title': response.xpath('/html/body/div[3]/div/div/div/h3/text()').get(),
            'author': response.xpath('/html/body/div[3]/div/div/div/h5/text()').get(),
            'abstract': response.xpath('/html/body/div[3]/div/div/div/p[1]/text()').get(),
            'url': new_link
        }
