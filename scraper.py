import scrapy


class BrickSetSpider(scrapy.Spider):
    name = "fiis_ranking_extractor"
    start_urls = ['https://www.fundsexplorer.com.br/ranking']
    
    def parse(self, response):
        print('===== INÍCIO =====')
        xp_head = '//*[@id="table-ranking"]//thead/tr/th'
        head = response.xpath(xp_head)
        columns = []
        for i,h in enumerate(head):
            columns.append(' '.join(h.xpath('text()').extract()))
        print(columns)
            
        
        xp_body = '//*[@id="table-ranking"]//tbody/tr'
        
        for row in response.xpath(xp_head):
            pass
        
        for brickset in response.xpath(xp_body):
            pass
        print('===== FIM =====')
