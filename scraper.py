import scrapy

class BrickSetSpider(scrapy.Spider):
    name = "fiis_ranking_extractor"
    start_urls = ['https://www.fundsexplorer.com.br/ranking']
    coluna = ['constituição', 'Tipo Gestão', 'Publico-alvo', 'Prazo duração', 'Fundo x Poupança']
    
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
        
        #Extraindo detalhes
        for fii in fiis:
            url = 'https://www.fundsexplorer.com.br' + str(fii['link'])
            #yield scrapy.Request(url= url, callback= self.parse_datails)
            
            request = scrapy.Request(url= url, callback= self.parse_datails)
            
        
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
        
        
        
        
        from datetime import date
        today = date. today()
        df.to_csv('tables/fii_' + str(today) + '.csv', index=False)
        print('[FRX] Saved')
    
    def parse_datails(self, response, content):
        
        print(self.coluna)
        
        path_title = '//span[@class="title"]/text()'
        path_description = '//span[@class="description"]/text()'
        path_content_up = '//span[@class="content up"]/text()'
        
        titles = response.xpath(path_title).getall()
        descriptions = response.xpath(path_description).getall()
        content_up = response.xpath(path_content_up).getall()
        
        #filtro dos dados coletados
        mask = [1,5,9,12]
        #self.coluna = ['constituição', 'Tipo Gestão', 'Publico-alvo', 'Prazo duração', 'Fundo x Poupança']
       
        values = []
        for e in mask:
            values.append(descriptions[e])
        
        values.append(content_up[-1])
        
        content = {}
        for i,c in enumerate(self.coluna):
            content[c] = values[i]
            print(content[c])
    
            
        yield content
                                 