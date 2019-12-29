#Lendo a data de hoje no sistema
from datetime import date
today = date. today()    

#Listando arquivos presentes no diretório
from os import listdir
from os.path import isfile, join
path = 'tables/'

print('[TFG] Started..')

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
        
        #  0 - link                     -
        #  1 - Código do fundo          -
        #  2 - Setor                    -
        #  3 - Preço Atual              -
        #  4 - Liquidez Diária          -
        #  5 - Dividendo                -
        #  6 - Dividend Yield           -
        #  7 - DY (3M) Acumulado        -
        #  8 - DY (6M) Acumulado        -
        #  9 - DY (12M) Acumulado
        # 10 - DY (3M) Média
        # 11 - DY (6M) Média
        # 12 - DY (12M) Média
        # 13 - DY Ano
        # 14 - Variação Preço
        # 15 - Rentab. Período
        # 16 - Rentab. Acumulada
        # 17 - Patrimônio Líq.
        # 18 - VPA
        # 19 - P/VPA
        # 20 - DY Patrimonial
        # 21 - Variação Patrimonial
        # 22 - Rentab. Patr. no Período
        # 23 - Rentab. Patr. Acumulada
        # 24 - Vacância Física
        # 25 - Vacância Financeira
        # 26 - Quantidade Ativos

        #Categorias
        df['Código do fundo'] = df['Código do fundo'].astype('category')
        df['link'] = df['link'].astype('category')
        df['Setor'] = df['Setor'].astype('category')
        
        #int32
        df['Quantidade Ativos'] = df['Quantidade Ativos'].astype('int32')
        
        #float64
        float_mask = [4,19]
        for f in float_mask:
            #df[df.columns[f]] = pd.to_numeric(df[df.columns[f]].str.replacece(',','.',regex=False), errors='coerce')
            df[df.columns[f]] = df[df.columns[f]].apply(lambda x: float(str(x).replace(',','.')))
        
        #moedas
        df['Preço Atual'] = pd.to_numeric(df['Preço Atual'].str.replace('.','', regex=False).str.replace("R$ ","", regex=False).str.replace(',','.',regex=False),errors='coerce')
        df['Dividendo'] = pd.to_numeric(df['Dividendo'].str.replace('.','', regex=False).str.replace("R$ ","", regex=False).str.replace(',','.',regex=False),errors='coerce')
        df['Patrimônio Líq.'] = pd.to_numeric(df['Patrimônio Líq.'].str.replace('.','', regex=False).str.replace("R$ ","", regex=False).str.replace(',','.',regex=False),errors='coerce')
        df['VPA'] = pd.to_numeric(df['VPA'].str.replace('.','', regex=False).str.replace("R$ ","", regex=False).str.replace(',','.',regex=False),errors='coerce')
        
        
        #porcentagens
        percent_mask = [6,7,8,9,10,11,12,13,14,15,16,20,21,22,23,24,25]
        
        for p in percent_mask:
            df[df.columns[p]] = pd.to_numeric(df[df.columns[p]].str.replace("%","",regex=False).str.replace(',','.',regex=False),errors='coerce')

            #Distância P/VPA = 1

df['Dif 1'] = abs(df['P/VPA']-1)

#Intervalo aceitável do P/VPA
pvpa_m = df['P/VPA'].median()
pvpa_des = abs(1-pvpa_m)
pvpa_max = 1 + pvpa_des
#pvpa_min = 0
pvpa_min = 1 - pvpa_des

#Score
df['Score'] = (
    (df['Dividend Yield ']-df['Dividend Yield '].min())/(df['Dividend Yield '].max()-df['Dividend Yield '].min()))*0.15+(
    (df['DY (12M) Acumulado']-df['DY (12M) Acumulado'].min())/(df['DY (12M) Acumulado'].max()-df['DY (12M) Acumulado'].min()))*0.1+(
    (df['DY (12M) Média']-df['DY (12M) Média'].min())/(df['DY (12M) Média'].max()-df['DY (12M) Média'].min()))*0.3+(
    (df['Rentab. Acumulada']-df['Rentab. Acumulada'].min())/(df['Rentab. Acumulada'].max()-df['Rentab. Acumulada'].min()))*0.1+(
    (df['Liquidez Diária']-df['Liquidez Diária'].min())/(df['Liquidez Diária'].max()-df['Liquidez Diária'].min()))*0.1+(
    1-((df['Dif 1']-df['Dif 1'].min())/(df['Dif 1'].max()-df['Dif 1'].min())))*0.1+(
    (df['Quantidade Ativos']-df['Quantidade Ativos'].min())/(df['Quantidade Ativos'].max()-df['Quantidade Ativos'].min()))*0.15

#Lista Desesejos
wish_list =['HGRE11','GGRC11','VILG11','XPML11']

carteira_michelle = ['MGFF11','CBOP11','XPIN11','MALL11','RBRF11','FLMA11','HFOF11','KNRI11','VISC11','MXRF11', 'MFII11']
carteira_wesley = ['MGFF11','CBOP11','XPIN11','MALL11','RBRF11','FLMA11','HFOF11','HGBS11','HGLG11', 'FOFT11']

#Lista Negra
black_list = ['XPCM11','PORD11','FAMB11B','RBCB11','TFOF11','BBFI11B','CXCE11B','NVIF11B','CPTS11B','VTLT11','RBVO11','CEOC11','KNIP11','RBBV11','MBRF11','MFII11']
black_list_setor = ['Hospital','Residencial']


#liquidez Diária mínima
ld_min = df['Liquidez Diária'].quantile(0.25)

#DY com tesouro selic
selic_am = 0.54
selic_aa = 6.5

#Vacância mínima (%)
vfisica_max = 10
vfinanc_max = 10

#Filtro
#dff = df[df['P/VPA']<=pvpa_max][df['P/VPA']>=pvpa_min][df['Liquidez Diária']>ld_min][df['Dividend Yield ']>selic_am][df['DY (12M) Acumulado']>selic_aa][~df['Código do fundo'].isin(black_list)][~df['Setor'].isin(black_list_setor)][~(df['Vacância Física']>=10)][~(df['Vacância Financeira']>=10)].sort_values(by='Score', ascending=False, na_position='last')
pvpa_max_limit = 1+df['Dif 1'].quantile(0.25)
print('p/vpa max: ', pvpa_max_limit)

dff = df[df['P/VPA']<=pvpa_max_limit][df['Liquidez Diária']>ld_min][
    df['Dividend Yield ']>selic_am][df['DY (12M) Acumulado']>selic_aa][
    ~df['Código do fundo'].isin(black_list)][~df['Setor'].isin(black_list_setor)][
    ~(df['Vacância Física']>=10)][~(df['Vacância Financeira']>=10)].sort_values(
    by='Score', ascending=False, na_position='last')

#dff = df[df['P/VPA']>=pvpa_min][df['P/VPA']<=pvpa_max][df['Liquidez Diária']>ld_min][
#    df['Dividend Yield ']>selic_am][df['DY (12M) Acumulado']>selic_aa][
#    ~df['Código do fundo'].isin(black_list)][~df['Setor'].isin(black_list_setor)][
#    ~(df['Vacância Física']>=10)][~(df['Vacância Financeira']>=10)].sort_values(
#    by='Score', ascending=False, na_position='last')



dff['Preço Compra MAX'] = dff['VPA']+dff['VPA']*df['Dif 1'].quantile(0.25)
dff['Preço Compra MIN'] = dff['VPA']-dff['VPA']*df['Dif 1'].quantile(0.5)

#dff['Michelle'] = dff['Código do fundo'].isin(carteira_michelle)
#dff['Wesley'] = dff['Código do fundo'].isin(carteira_wesley)
#dff['Desejado'] = dff['Código do fundo'].isin(wish_list)
dff['Carteira'] = dff['Código do fundo'].apply(lambda x: 'Desejado' if x in wish_list else 'Michelle e Wesley' if x in carteira_michelle and x in carteira_wesley else 'Michelle' if x in carteira_michelle else 'Wesley' if x in carteira_wesley else ' - ')

df['Carteira'] = dff['Código do fundo'].apply(lambda x: 'Desejado' if x in wish_list else 'Michelle e Wesley' if x in carteira_michelle and x in carteira_wesley else 'Michelle' if x in carteira_michelle else 'Wesley' if x in carteira_wesley else ' - ')

filtro_colunas = ['link',
                  'DY (3M) Acumulado',
                  'DY (6M) Acumulado',
                  'DY (3M) Média',
                  'DY (6M) Média',
                  'DY Ano',
                  'Patrimônio Líq.',
                  'DY Patrimonial',
                  'Variação Patrimonial',
                  'Rentab. Patr. no Período',
                  'Rentab. Patr. Acumulada',
                  'Variação Preço',
                  'Dif 1']

dff = dff.drop(filtro_colunas, axis =1)

dfwl = df[df['Código do fundo'].isin(wish_list)].drop(filtro_colunas, axis = 1).sort_values(by='Score', ascending=False, na_position='last')

#Simulador WESLEY
setores = ['Títulos e Val. Mob.','Outros','Lajes Corporativas','Híbrido','Shoppings','Logística']

#Dados manuais
saldo_disponivel = 3943.94
carteira = [3323.52, 234.20, 891.22, 33.68, 2656.90,2566.15]

#Estratégia de carteira
p_carteira = [0.25, 0.05, 0.20, 0.10, 0.20, 0.20]

dcw = pd.DataFrame({'Setor': setores, '%': p_carteira, 'Investido': carteira})
dcw['Distribuição Ideal'] = round((saldo_disponivel+dcw['Investido'].sum())*dcw['%'],2)
#dcw['Compra Recomendada'] = dcw['Distribuição Ideal'].apply(lambda x: x-dcw['Investido'] if x-dcw['Investido'] > 0 else 0)
dcw['Comprar'] = dcw['Distribuição Ideal']-dcw['Investido'] >= 0

if dcw[dcw['Distribuição Ideal']-dcw['Investido'] < 0].shape[0]>0:
    dcw.loc[(dcw['Distribuição Ideal']-dcw['Investido'] >= 0), 'Disponível para compra'] = round(saldo_disponivel*(dcw['%']/dcw[dcw['Comprar'] == True]['%'].sum()),2)
else:
    dcw.loc[(dcw['Distribuição Ideal']-dcw['Investido'] >= 0), 'Disponível para compra'] = dcw['Distribuição Ideal']-dcw['Investido']
dcw.loc[(dcw['Distribuição Ideal']-dcw['Investido'] < 0), 'Disponível para compra'] = 0.0

#Simulador MICHELLE
setores = ['Títulos e Val. Mob.','Outros','Lajes Corporativas','Híbrido','Shoppings','Logística']


#Dados manuais
saldo_disponivel = 6436.76
carteira = [8652.86, 1735.50, 8502.58, 2458.40, 6901.32, 0.0]

#Estratégia de carteira
p_carteira = [0.25, 0.05, 0.20, 0.10, 0.20, 0.20]

dcm= pd.DataFrame({'Setor': setores, '%': p_carteira, 'Investido': carteira})
dcm['Distribuição Ideal'] = round((saldo_disponivel+dcm['Investido'].sum())*dcm['%'],2)
dcm['Comprar'] = dcm['Distribuição Ideal']-dcm['Investido'] >= 0

if dcm[dcm['Distribuição Ideal']-dcm['Investido'] < 0].shape[0]>0:
    dcm.loc[(dcm['Distribuição Ideal']-dcm['Investido'] >= 0), 'Disponível para compra'] = round(saldo_disponivel*(dcm['%']/dcm[dcm['Comprar'] == True]['%'].sum()),2)
else:
    dcm.loc[(dcm['Distribuição Ideal']-dcm['Investido'] >= 0), 'Disponível para compra'] = dcm['Distribuição Ideal']-dcm['Investido']

dcm.loc[(dcm['Distribuição Ideal']-dcm['Investido'] < 0), 'Disponível para compra'] = 0.0


import xlwt
import xlsxwriter

writer = pd.ExcelWriter('tables/top_fii_' + str(today) + '.xls', engine='xlsxwriter')

dff.to_excel(writer,'top_fii','-','%.2f', index=False, encoding='xlwt')
df.sort_values(by='Score', ascending=False, na_position='last').drop(filtro_colunas, axis = 1).to_excel(writer,'ranking_geral','-','%.2f', index=False, encoding='xlwt')
#dfwl.to_excel(writer,'lista_desejos','-','%.2f', index=False, encoding='xlwt')
#dcm.drop('Comprar', axis = 1).to_excel(writer,'rec_michelle','-','%.2f', index=False, encoding='xlwt')
#dcw.drop('Comprar', axis = 1).to_excel(writer,'rec_wesley','-','%.2f', index=False, encoding='xlwt')
df[df['Código do fundo'].isin(carteira_michelle)].drop(filtro_colunas, axis = 1).sort_values(by='Score', ascending=False, na_position='last').to_excel(writer,'carteira_michelle','-','%.2f', index=False, encoding='xlwt')
df[df['Código do fundo'].isin(carteira_wesley)].drop(filtro_colunas, axis = 1).sort_values(by='Score', ascending=False, na_position='last').to_excel(writer,'carteira_wesley','-','%.2f', index=False, encoding='xlwt')

writer.save()
print('[TFG] Done!')