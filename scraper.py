import scrapy


class BrickSetSpider(scrapy.Spider):
    name = "fiis_ranking_extractor"
    start_urls = ['https://www.fundsexplorer.com.br/ranking']
    
    def parse(self, response):
        print('[FRX] Extracting...')
        xp_head = '//*[@id="table-ranking"]//thead/tr/th'
        head = response.xpath(xp_head)
        columns = []
        for i,h in enumerate(head):
            columns.append(' '.join(h.xpath('text()').extract()))
        #print(columns)
            
        
        xp_body = '//*[@id="table-ranking"]//tbody/tr'
                
        fiis = []
        for row in response.xpath(xp_body):
            fii = {}
            fii['link'] = row.xpath('td[1]/a/@href').extract_first()
            for i, cell in enumerate(columns):
                fii[columns[i]] = row.xpath('td[' + str(i+1) + ']//text()').extract_first()
            fiis.append(fii)
        print('[FRX] Saving...')
        import pandas as pd
        df = pd.DataFrame()
        
        links = []
        for fii in fiis:
            links.append(fii['link'])
        df['link'] = links
        
        for column in columns:
            serie = []
            for fii in fiis:
                serie.append(fii[column])
            df[column] = serie
        df.to_csv('teste.csv', index=False)
        print('[FRX] Saved')
