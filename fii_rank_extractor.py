import scrapy

class BrickSetSpider(scrapy.Spider):
    name = "fiis_ranking_extractor"
    start_urls = ['https://www.fundsexplorer.com.br/ranking']
    details_columns = ['constituição', 'Tipo Gestão', 'Publico-alvo', 'Prazo duração', 'Fundo x Poupança']
    mask = [1,5,9,12]
    content = {}
    
    def parse(self, response):
        print('[FRX] Extracting...')
        
        #Identificando a cabeça
        xp_head = '//*[@id="table-ranking"]//thead/tr/th'
        head = response.xpath(xp_head)
        
        #Extraíndo os nomes das colunas
        columns = []
        for i,h in enumerate(head):
            columns.append(' '.join(h.xpath('text()').extract()))
        
        #Extraíndo o conteúdo das linhas
        xp_body = '//*[@id="table-ranking"]//tbody/tr'
        fiis = []
        
        for row in response.xpath(xp_body):
            fii = {}
            fii['link'] = row.xpath('td[1]/a/@href').extract_first()
            
            #Extraindo detalhes
            url = 'https://www.fundsexplorer.com.br' + str(fii['link'])
            request = fii.update(scrapy.Request(url= url, callback= self.parse_datails))
            
            for i, cell in enumerate(columns):
                fii[columns[i]] = row.xpath('td[' + str(i+1) + ']//text()').extract_first()
            
            
            
            
            print(self.content)
            #fii.update()
            
            
            fiis.append(fii)
            
        
        #Savando em csv
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
        print('[FRX] Finished.')
    
    #Percorre a página de detalhes de cada fundo da lista
    def parse_datails(self, response):
        
        print('Getting details')
        
        path_title = '//span[@class="title"]/text()'
        path_description = '//span[@class="description"]/text()'
        path_content_up = '//span[@class="content up"]/text()'
        
        titles = response.xpath(path_title).getall()
        descriptions = response.xpath(path_description).getall()
        content_up = response.xpath(path_content_up).getall()
        
        #filtro dos dados coletados
        values = []
        for e in self.mask:
            values.append(descriptions[e])
            print(descriptions[e])
        
        values.append(content_up[-1])
        
        content = {}
        for i,c in enumerate(self.details_columns):
            content[c] = values[i]
        
        return content
        #yield self.content