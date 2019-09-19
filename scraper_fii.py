import scrapy


class BrickSetSpider(scrapy.Spider):
    name = "fiis_extractor"
    start_urls = ['https://www.fundsexplorer.com.br']
    
    def parse(self, response):
        print('[FRX] Getting specific informations...')
        #Lendo a data de hoje no sistema
        from datetime import date
        today = date. today()    
        
        #Listando arquivos presentes no diretório
        from os import listdir
        from os.path import isfile, join
        path = 'tables/'
        
        files = [f for f in listdir(path) if isfile(join(path, f))]
        if(len(files)==0):
            print('[FRX] There is no files in directory. =(')
        else:
            #buscando o arquivo do dia
            try:
                filepath = [s for s in files if 'fii_'+str(today) in s][0]
            except:
                print('[FRX] There is no table today. =(')
                filepath = ''
            
            if(len(filepath)>0):
                import pandas as pd
                df = pd.read_csv(path+filepath)
                print('[FRX] Extracting...')
                for l in df.link:
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