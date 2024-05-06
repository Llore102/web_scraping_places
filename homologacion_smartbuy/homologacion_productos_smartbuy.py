import pandas as pd
import numpy as np
import glob
import tqdm
import string
import os
from io import BytesIO
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
import asyncio
from dotenv import load_dotenv
from config.s3_aws import s3_client
from config.mongodb import insert_data_products
sw = stopwords.words('spanish')



#from thefuzz import fuzz
#from thefuzz import process

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import multiprocessing as mp
# import istarmap  # import to apply patch
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
load_dotenv()


n = mp.cpu_count()

s3_bucket_name = os.getenv("S3_BUCKET_NAME")


try:
   mp.set_start_method('spawn', force=True)
#   print("spawned")
except RuntimeError:
   pass

ruta = os.path.dirname(os.path.abspath(__file__))

def marca_tottus(x):
    if x.find('marca: ')==-1:
        return('')
    elif x.find(';', x.find('marca: ')+1)==-1:
        return(x[x.find('marca: ')+7:])
    else:
        return(x[x.find('marca: ')+7: x.find(';', x.index('marca: ')+1)])
    
def formato_tottus(x):
    if x.find('formato: ')==-1:
        return('')
    elif x.find(';', x.find('formato: ')+1)==-1:
        return(x[x.find('formato: ')+9:])
    else:
        return(x[x.find('formato: ')+9: x.find(';', x.find('formato: ')+1)])

def format(x):
    if x[-2:]=='gr':
        return(x[:-1])
    elif x[-2:]=='lt':
        return(x[:-1])
    else:
        return(x)

def formato_lider(x):
    if x[x.rfind(',')+1:x.rfind(',')+2]!=' ':
        return(x[x.rfind(',', 0, x.rfind(','))+2:])
    else:
        return(x[x.rfind(',')+2:])

def remove_stopwords(lines, sw = sw):
    '''
    The purpose of this function is to remove stopwords from a given array of 
    lines.
    
    params:
        lines (Array / List) : The list of lines you want to remove the stopwords from
        sw (Set) : The set of stopwords you want to remove
        
    example:
        lines = remove_stopwords(lines = lines, sw = sw)
    '''
    
    res = []
    for line in lines:
        original = line
        line = [w for w in line if w not in sw]
        if len(line) < 1:
            line = original
        res.append(line)
    return res
    
def matching(id_smart, product, empresa, collection_tottus, collection_lider, collection_jumbo):
    tottus = process.extractOne(product, collection_tottus, scorer=fuzz.ratio)
    if tottus==None:
        tottus = ('', np.nan)
    lider = process.extractOne(product, collection_lider, scorer=fuzz.ratio)
    if lider==None:
        lider = ('', np.nan)
    jumbo = process.extractOne(product, collection_jumbo, scorer=fuzz.ratio)
    if jumbo==None:
        jumbo = ('', np.nan)
    return([id_smart, product, empresa, tottus[0], tottus[1], lider[0], lider[1], jumbo[0], jumbo[1]])

def homologacion():

    df_cat_smartbuy = pd.read_excel(ruta + "/Categorías_SmartBuy_v7.xlsx")

    # df_tottus = pd.read_excel(ruta[:-22] + "/web_scraper_tottus/Output/REPORTE_WS_TOTTUS.xlsx", converters={'internet_price':str})
    # df_tottus['id_smart'] = 'T' + df_tottus['id'].fillna(0).astype(int).astype(str)
    # df_tottus['name'] = df_tottus['name'].astype(str).replace('nan', 'no info')
    # df_tottus['description'] = df_tottus['description'].astype(str).map(lambda x:x[x.find('>', x.find('h3'))+1:x.find('</h3>')] if x[0]=='<' else x).replace('nan', 'no info')
    # df_tottus['marca'] = df_tottus['attributes'].astype(str).str.lower().map(lambda x:marca_tottus(x)).replace('nan', 'no info')
    # df_tottus['formato'] = df_tottus['attributes'].astype(str).str.lower().map(lambda x:formato_tottus(x)).replace('nan', 'no info')
    # df_tottus['formato'] = df_tottus['formato'].map(lambda x:format(x))
    # df_tottus['image1'] = df_tottus['url_image'].astype(str).map(lambda x:x if x.find(';')==-1 else x[:x.find(';')]).replace('nan', 'no info')
    # df_tottus['image2'] = df_tottus['url_image'].astype(str).map(lambda x:'' if x.find(';')==-1 else x[x.find(';')+2:x.find(';', x.find(';')+1)]).replace('nan', 'no info')
    # df_tottus['image3'] = df_tottus['url_image'].astype(str).map(lambda x:'' if x.find(';', x.find(';')+1)==-1 else x[:x.find(';')]).replace('nan', 'no info')
    # df_tottus['internet_price'] = df_tottus['internet_price'].astype(str).str.replace('.', '').str.replace('nan', '0').astype(float)
    # df_tottus['empresa'] = 'Tottus'

    # #3 niveles
    # df_tottus = pd.merge(df_tottus, 
    #                 df_cat_smartbuy[df_cat_smartbuy['Categoría nivel 3 tottus'].notnull()][['Categoría nivel 1 tottus', 'Categoría nivel 2 tottus', 'Categoría nivel 3 tottus', 'COD_CAT_N1_SMT', 'Categoría nivel 1 - Smartbuy', 'COD_CAT_N2_SMT', 'Categoría nivel 2 - Smartbuy']]\
    #                 .rename(columns={'Categoría nivel 1 tottus': 'first_category',
    #                                 'Categoría nivel 2 tottus': 'second_category',
    #                                 'Categoría nivel 3 tottus': 'third_category'}).drop_duplicates(), 
    #                 on=['first_category', 'second_category', 'third_category'], 
    #                 how='left').drop_duplicates()
    
    # #2 niveles
    # df_tottus = pd.merge(df_tottus, 
    #                 df_cat_smartbuy[(df_cat_smartbuy['Categoría nivel 3 tottus'].isnull()) &
    #                                 (df_cat_smartbuy['Categoría nivel 2 tottus'].notnull())][['Categoría nivel 1 tottus', 'Categoría nivel 2 tottus', 'COD_CAT_N1_SMT', 'Categoría nivel 1 - Smartbuy', 'COD_CAT_N2_SMT', 'Categoría nivel 2 - Smartbuy']]\
    #                 .rename(columns={'Categoría nivel 1 tottus': 'first_category',
    #                                 'Categoría nivel 2 tottus': 'second_category'}).drop_duplicates(), 
    #                 on=['first_category', 'second_category'], 
    #                 how='left').drop_duplicates()
    
    # #creando campos 
    # df_tottus['COD_CAT_N1_SMT'] = np.where(df_tottus['COD_CAT_N1_SMT_x'].isnull(), df_tottus['COD_CAT_N1_SMT_y'], df_tottus['COD_CAT_N1_SMT_x'])
    # df_tottus['Categoría nivel 1 - Smartbuy'] = np.where(df_tottus['Categoría nivel 1 - Smartbuy_x'].isnull(), df_tottus['Categoría nivel 1 - Smartbuy_y'], df_tottus['Categoría nivel 1 - Smartbuy_x'])
    # df_tottus['COD_CAT_N2_SMT'] = np.where(df_tottus['COD_CAT_N2_SMT_x'].isnull(), df_tottus['COD_CAT_N2_SMT_y'], df_tottus['COD_CAT_N2_SMT_x'])
    # df_tottus['Categoría nivel 2 - Smartbuy'] = np.where(df_tottus['Categoría nivel 2 - Smartbuy_x'].isnull(), df_tottus['Categoría nivel 2 - Smartbuy_y'], df_tottus['Categoría nivel 2 - Smartbuy_x'])
    
    # #base final
    # df_tottus = df_tottus[df_tottus['COD_CAT_N1_SMT'].notnull()].drop(['COD_CAT_N1_SMT_x',
    #                                                                 'Categoría nivel 1 - Smartbuy_x', 'COD_CAT_N2_SMT_x',
    #                                                                 'Categoría nivel 2 - Smartbuy_x', 'COD_CAT_N1_SMT_y',
    #                                                                 'Categoría nivel 1 - Smartbuy_y', 'COD_CAT_N2_SMT_y',
    #                                                                 'Categoría nivel 2 - Smartbuy_y'], axis=1).drop_duplicates()

    filenames = glob.glob(ruta[:-22] + "/web_scraper_lider/Output/REPORTE_WS_*")
    df_lider = pd.concat(pd.read_excel(file, converters={'internet_price':str}) for file in filenames).reset_index(drop=True)
    df_lider['id_smart'] = 'L' + df_lider['id'].fillna('item 0').map(lambda x:x[5:])
    #df_lider['id_smart'] = 'L' + df_lider['id'].fillna('0').astype(str).map(lambda x: x[5:])
    df_lider['name'] = df_lider['name'].astype(str).replace('nan', 'no info')
    df_lider['description'] = df_lider['description'].astype(str).replace('nan', 'no info')
    df_lider['marca'] = df_lider['attributes'].astype(str).str.lower().str.replace('á', 'a').str.replace('é', 'e').str.replace('í', 'i').str.replace('ó', 'o').str.replace('ú', 'u').replace('nan', 'no info')
    df_lider['formato'] = df_lider['name'].astype(str).str.lower().map(lambda x:formato_lider(x)).replace('nan', 'no info')
    df_lider['formato'] = df_lider['formato'].map(lambda x:format(x))
    df_lider['image1'] = df_lider['url_image'].astype(str).map(lambda x:x if x.find(';')==-1 else x[:x.find(';')]).replace('nan', 'no info')
    df_lider['image2'] = df_lider['url_image'].astype(str).map(lambda x:'' if x.find(';')==-1 else x[x.find(';')+2:x.find(';', x.find(';')+1)]).replace('nan', 'no info')
    df_lider['image3'] = df_lider['url_image'].astype(str).map(lambda x:'' if x.find(';', x.find(';')+1)==-1 else x[:x.find(';')]).replace('nan', 'no info')
    df_lider['internet_price'] = np.where(df_lider['internet_price'].astype(str).map(lambda x:x[0].isdigit()), df_lider['normal_price'], df_lider['internet_price'])
    df_lider['internet_price'] = df_lider['internet_price'].astype(str).map(lambda x:x[x.find('$')+1:]).str.replace('.', '').str.replace('nan', '0').astype(float)
    df_lider['empresa'] = 'Lider'

    #2 categorias
    df_lider = pd.merge(df_lider, 
                    df_cat_smartbuy[['Categoría nivel 1 lider', 'Categoría nivel 2 lider', 'COD_CAT_N1_SMT', 'Categoría nivel 1 - Smartbuy', 'COD_CAT_N2_SMT', 'Categoría nivel 2 - Smartbuy']]\
                    .rename(columns={'Categoría nivel 1 lider': 'first_category',
                                    'Categoría nivel 2 lider': 'second_category'}).drop_duplicates(), 
                    on=['first_category', 'second_category'], 
                    how='inner').drop_duplicates()

    filenames = glob.glob(ruta[:-22] + "/web_scraper_jumbo/Output/REPORTE_WS_*")
    df_jumbo = pd.concat(pd.read_excel(file, converters={'internet_price':str}) for file in filenames).reset_index(drop=True)
    df_jumbo['id_smart'] = 'J' + df_jumbo['id'].fillna('Código: 0').map(lambda x:x[8:])
    df_jumbo['name'] = df_jumbo['name'].astype(str).replace('nan', 'no info')
    df_jumbo['description'] = df_jumbo['description'].astype(str).replace('nan', 'no info')
    df_jumbo['marca'] = df_jumbo['attributes'].astype(str).str.lower().str.replace('á', 'a').str.replace('é', 'e').str.replace('í', 'i').str.replace('ó', 'o').str.replace('ú', 'u').replace('nan', 'no info')
    df_jumbo['formato'] = df_jumbo['name'].astype(str).str.lower().map(lambda x:x[x[:x.rfind(" ")].rfind(" ")+1:]).replace('nan', 'no info')
    df_jumbo['formato'] = df_jumbo['formato'].map(lambda x:format(x))
    df_jumbo['image1'] = df_jumbo['url_image'].astype(str).map(lambda x:x if x.find(';')==-1 else x[:x.find(';')]).replace('nan', 'no info')
    df_jumbo['image2'] = df_jumbo['url_image'].astype(str).map(lambda x:'' if x.find(';')==-1 else x[x.find(';')+2:x.find(';', x.find(';')+1)]).replace('nan', 'no info')
    df_jumbo['image3'] = df_jumbo['url_image'].astype(str).map(lambda x:'' if x.find(';', x.find(';')+1)==-1 else x[:x.find(';')]).replace('nan', 'no info')
    df_jumbo['internet_price'] = df_jumbo['internet_price'].astype(str).map(lambda x:x[x.find('$')+1:]).str.replace('.', '').str.replace('nan', '0').astype(float)
    df_jumbo['empresa'] = 'Jumbo'

    #3 niveles
    df_jumbo = pd.merge(df_jumbo, 
                    df_cat_smartbuy[df_cat_smartbuy['Categoría nivel 3 jumbo'].notnull()][['Categoría nivel 1 jumbo', 'Categoría nivel 2 jumbo', 'Categoría nivel 3 jumbo', 'COD_CAT_N1_SMT', 'Categoría nivel 1 - Smartbuy', 'COD_CAT_N2_SMT', 'Categoría nivel 2 - Smartbuy']]\
                    .rename(columns={'Categoría nivel 1 jumbo': 'first_category',
                                    'Categoría nivel 2 jumbo': 'second_category',
                                    'Categoría nivel 3 jumbo': 'third_category'}).drop_duplicates(), 
                    on=['first_category', 'second_category', 'third_category'], 
                    how='left').drop_duplicates()
    
    #2 niveles
    df_jumbo = pd.merge(df_jumbo, 
                    df_cat_smartbuy[(df_cat_smartbuy['Categoría nivel 3 jumbo'].isnull()) &
                                    (df_cat_smartbuy['Categoría nivel 2 jumbo'].notnull())][['Categoría nivel 1 jumbo', 'Categoría nivel 2 jumbo', 'COD_CAT_N1_SMT', 'Categoría nivel 1 - Smartbuy', 'COD_CAT_N2_SMT', 'Categoría nivel 2 - Smartbuy']]\
                    .rename(columns={'Categoría nivel 1 jumbo': 'first_category',
                                    'Categoría nivel 2 jumbo': 'second_category'}).drop_duplicates(), 
                    on=['first_category', 'second_category'], 
                    how='left').drop_duplicates()
    
    #creando campos 
    df_jumbo['COD_CAT_N1_SMT'] = np.where(df_jumbo['COD_CAT_N1_SMT_x'].isnull(), df_jumbo['COD_CAT_N1_SMT_y'], df_jumbo['COD_CAT_N1_SMT_x'])
    df_jumbo['Categoría nivel 1 - Smartbuy'] = np.where(df_jumbo['Categoría nivel 1 - Smartbuy_x'].isnull(), df_jumbo['Categoría nivel 1 - Smartbuy_y'], df_jumbo['Categoría nivel 1 - Smartbuy_x'])
    df_jumbo['COD_CAT_N2_SMT'] = np.where(df_jumbo['COD_CAT_N2_SMT_x'].isnull(), df_jumbo['COD_CAT_N2_SMT_y'], df_jumbo['COD_CAT_N2_SMT_x'])
    df_jumbo['Categoría nivel 2 - Smartbuy'] = np.where(df_jumbo['Categoría nivel 2 - Smartbuy_x'].isnull(), df_jumbo['Categoría nivel 2 - Smartbuy_y'], df_jumbo['Categoría nivel 2 - Smartbuy_x'])
    
    #base final
    df_jumbo = df_jumbo[df_jumbo['COD_CAT_N1_SMT'].notnull()].drop(['COD_CAT_N1_SMT_x',
                                                                    'Categoría nivel 1 - Smartbuy_x', 'COD_CAT_N2_SMT_x',
                                                                    'Categoría nivel 2 - Smartbuy_x', 'COD_CAT_N1_SMT_y',
                                                                    'Categoría nivel 1 - Smartbuy_y', 'COD_CAT_N2_SMT_y',
                                                                    'Categoría nivel 2 - Smartbuy_y'], axis=1).drop_duplicates()

    df_prod = pd.concat([ df_lider, df_jumbo]).reset_index(drop=True) #df_tottus,

    vars_productos = ['id_smart', 'name', 'description', 'first_category', 'second_category', 'third_category', 'marca', 'formato', 'internet_price', 'image1', 'image2', 'image3', 'empresa', 'COD_CAT_N1_SMT', 'Categoría nivel 1 - Smartbuy', 'COD_CAT_N2_SMT', 'Categoría nivel 2 - Smartbuy']

    df_prod_1 = df_prod[vars_productos].reset_index(drop=True)

    print("Total: ",df_prod_1.shape)
    df_prod_1 = df_prod_1.drop_duplicates()
    print("Total sin duplicados: ",df_prod_1.shape)

    df_prod_2 = df_prod_1.groupby(['id_smart', 'name', 'marca', 'formato', 'empresa'], as_index=False, dropna=False).size()

    df = df_prod_1[~((df_prod_1['id_smart'].isin(df_prod_2[df_prod_2['size']>1]['id_smart'].unique())) & (df_prod_1['third_category'].fillna('sin info').str.lower().str.contains('ver todo')))]

    vars_productos_2 = ['id_smart', 'name', 'description', 'marca', 'formato', 'internet_price', 'image1', 'image2', 'image3', 'empresa', 'COD_CAT_N1_SMT', 'Categoría nivel 1 - Smartbuy', 'COD_CAT_N2_SMT', 'Categoría nivel 2 - Smartbuy']

    df = df[vars_productos_2].reset_index(drop=True)

    print("Total: ",df.shape)
    df = df.drop_duplicates()
    print("Total sin duplicados: ",df.shape)

    df['product'] = df['name'].astype(str) + ' ' +\
                    df['marca'].astype(str) + ' ' +\
                    df['formato'].astype(str)

    lines = df['product'].tolist()

    # remove new lines
    lines = [line.rstrip('\n') for line in lines]

    # make all characters lower
    lines = [line.lower() for line in lines]

    # remove punctuations from each line
    lines = [line.translate(str.maketrans('', '', string.punctuation)) for line in lines]

    # tokenize
    lines = [word_tokenize(line) for line in lines]
        
    filtered_lines = remove_stopwords(lines = lines, sw = sw)

    filtered_lines = [TreebankWordDetokenizer().detokenize(line) for line in filtered_lines]

    df['product'] = filtered_lines

    categorias_smt = df[['COD_CAT_N1_SMT', 'Categoría nivel 1 - Smartbuy', 'COD_CAT_N2_SMT', 'Categoría nivel 2 - Smartbuy']].drop_duplicates().values.tolist()

    results = []

    i = 1

    df_res = pd.DataFrame()

    for cat1, cat_1, cat2, cat_2 in categorias_smt:

        print(cat_1, ' ', cat_2)
        print(i, ' de ', len(categorias_smt))

        collection_tottus = df[(df['empresa']=='Tottus') & (df['COD_CAT_N1_SMT']==cat1) & (df['COD_CAT_N2_SMT']==cat2)]['product'].values
        collection_lider = df[(df['empresa']=='Lider') & (df['COD_CAT_N1_SMT']==cat1) & (df['COD_CAT_N2_SMT']==cat2)]['product'].values
        collection_jumbo = df[(df['empresa']=='Jumbo') & (df['COD_CAT_N1_SMT']==cat1) & (df['COD_CAT_N2_SMT']==cat2)]['product'].values

        products = df[(df['COD_CAT_N1_SMT']==cat1) & (df['COD_CAT_N2_SMT']==cat2)][['id_smart', 'product', 'empresa']].drop_duplicates().values

        with mp.Pool(n) as pool:
            iterable = [(id_smart, product, empresa, collection_tottus, collection_lider, collection_jumbo) for id_smart, product, empresa in products] #
            results = list(tqdm.tqdm(pool.istarmap(matching, iterable), total=len(iterable)))
            pool.close()
            pool.join()

        df_temp = pd.DataFrame(results, columns=['id_smart', 'product', 'empresa', 'name_tottus', 'score_tottus', 'name_lider', 'score_lider', 'name_jumbo', 'score_jumbo'])

        df_res = df_res.append(df_temp)

        i = i+1

    df_res_0 = pd.merge(df_res, df[['id_smart', 'product', 'empresa', 'name', 'description', 'COD_CAT_N1_SMT', 'Categoría nivel 1 - Smartbuy', 'COD_CAT_N2_SMT', 'Categoría nivel 2 - Smartbuy', 'marca', 'formato', 'internet_price', 'image1', 'image2', 'image3']].drop_duplicates(), how='left', on=['id_smart', 'product', 'empresa']).reset_index(drop=True)
    df_res_0 = df_res_0[['id_smart', 'name', 'description', 'COD_CAT_N1_SMT', 'Categoría nivel 1 - Smartbuy', 'COD_CAT_N2_SMT', 'Categoría nivel 2 - Smartbuy', 'marca', 'formato', 'internet_price', 'image1', 'image2', 'image3', 'product', 'empresa', 'name_tottus', 'score_tottus', 'name_lider', 'score_lider', 'name_jumbo', 'score_jumbo']].drop_duplicates()

    df_res_1 = pd.merge(df_res_0, df[df['empresa']=='Tottus'][['product', 'marca', 'formato', 'internet_price']].rename(columns={'product': 'name_tottus',
                                                                                                                                'marca': 'marca_tottus',
                                                                                                                                'formato': 'formato_tottus',
                                                                                                                                'internet_price': 'precio_tottus'}), how='left', on='name_tottus')

    df_res_2 = pd.merge(df_res_1, df[df['empresa']=='Lider'][['product', 'marca', 'formato', 'internet_price']].rename(columns={'product': 'name_lider',
                                                                                                                                'marca': 'marca_lider',
                                                                                                                                'formato': 'formato_lider',
                                                                                                                                'internet_price': 'precio_lider'}), how='left', on='name_lider')

    df_res_3 = pd.merge(df_res_2, df[df['empresa']=='Jumbo'][['product', 'marca', 'formato', 'internet_price']].rename(columns={'product': 'name_jumbo',
                                                                                                                                'marca': 'marca_jumbo',
                                                                                                                                'formato': 'formato_jumbo',
                                                                                                                                'internet_price': 'precio_jumbo'}), how='left', on='name_jumbo')

    df_res_4 = df_res_3[['id_smart', 'name', 'description', 'COD_CAT_N1_SMT', 'Categoría nivel 1 - Smartbuy', 'COD_CAT_N2_SMT', 'Categoría nivel 2 - Smartbuy', 'marca', 'formato', 'internet_price', 'image1', 'image2', 'image3', 'empresa', 'name_tottus', 'score_tottus', 'marca_tottus', 'formato_tottus', 'precio_tottus', 'name_lider', 'score_lider', 'marca_lider', 'formato_lider', 'precio_lider', 'name_jumbo', 'score_jumbo', 'marca_jumbo', 'formato_jumbo', 'precio_jumbo']].drop_duplicates()
    
    df_res_4['score_fuzz_tottus'] = df_res_4['score_tottus'].copy()
    df_res_4['score_fuzz_lider'] = df_res_4['score_lider'].copy()
    df_res_4['score_fuzz_jumbo'] = df_res_4['score_jumbo'].copy()
    
    penalidad_formato = 5
    penalidad_marca = 2
    umbral_precio = 0.5
    penalidad_precio = 5

    df_res_4['penalidad_formato_tottus'] = np.where(df_res_4['formato'] == df_res_4['formato_tottus'], 0, penalidad_formato)
    df_res_4['penalidad_formato_lider'] = np.where(df_res_4['formato'] == df_res_4['formato_lider'], 0, penalidad_formato)
    df_res_4['penalidad_formato_jumbo'] = np.where(df_res_4['formato'] == df_res_4['formato_jumbo'], 0, penalidad_formato)

    df_res_4['penalidad_marca_tottus'] = np.where(df_res_4['marca'] == df_res_4['marca_tottus'], 0, penalidad_marca)
    df_res_4['penalidad_marca_lider'] = np.where(df_res_4['marca'] == df_res_4['marca_lider'], 0, penalidad_marca)
    df_res_4['penalidad_marca_jumbo'] = np.where(df_res_4['marca'] == df_res_4['marca_jumbo'], 0, penalidad_marca)

    df_res_4['penalidad_precio_tottus'] = np.where((abs((df_res_4['precio_tottus']-df_res_4['internet_price'])/df_res_4['internet_price'])<=umbral_precio), 0, penalidad_precio)
    df_res_4['penalidad_precio_lider'] = np.where((abs((df_res_4['precio_tottus']-df_res_4['internet_price'])/df_res_4['internet_price'])<=umbral_precio), 0, penalidad_precio)
    df_res_4['penalidad_precio_jumbo'] = np.where((abs((df_res_4['precio_tottus']-df_res_4['internet_price'])/df_res_4['internet_price'])<=umbral_precio), 0, penalidad_precio)

    df_res_4['score_tottus'] = df_res_4['score_fuzz_tottus'] - df_res_4['penalidad_formato_tottus'] - df_res_4['penalidad_marca_tottus'] - df_res_4['penalidad_precio_tottus']
    df_res_4['score_lider'] = df_res_4['score_fuzz_lider'] - df_res_4['penalidad_formato_lider'] - df_res_4['penalidad_marca_lider'] - df_res_4['penalidad_precio_lider']
    df_res_4['score_jumbo'] = df_res_4['score_fuzz_jumbo'] - df_res_4['penalidad_formato_jumbo'] - df_res_4['penalidad_marca_jumbo'] - df_res_4['penalidad_precio_jumbo']

    umbral_score = 60

    # Tottus
    df_res_4['name_tottus_inicial'] = df_res_4['name_tottus'].copy()
    df_res_4['score_tottus_inicial'] = df_res_4['score_tottus'].copy()
    df_res_4['marca_tottus_inicial'] = df_res_4['marca_tottus'].copy()
    df_res_4['formato_tottus_inicial'] = df_res_4['formato_tottus'].copy()
    df_res_4['precio_tottus_inicial'] = df_res_4['precio_tottus'].copy()

    df_res_4['name_tottus'] = np.where((df_res_4['score_tottus_inicial']>=umbral_score), df_res_4['name_tottus'], '')
    df_res_4['score_tottus'] = np.where((df_res_4['score_tottus_inicial']>=umbral_score), df_res_4['score_tottus'], np.nan)
    df_res_4['marca_tottus'] = np.where((df_res_4['score_tottus_inicial']>=umbral_score), df_res_4['marca_tottus'], '')
    df_res_4['formato_tottus'] = np.where((df_res_4['score_tottus_inicial']>=umbral_score), df_res_4['formato_tottus'], '')
    df_res_4['precio_tottus'] = np.where((df_res_4['score_tottus_inicial']>=umbral_score), df_res_4['precio_tottus'], np.nan)

    # Lider
    df_res_4['name_lider_inicial'] = df_res_4['name_lider'].copy()
    df_res_4['score_lider_inicial'] = df_res_4['score_lider'].copy()
    df_res_4['marca_lider_inicial'] = df_res_4['marca_lider'].copy()
    df_res_4['formato_lider_inicial'] = df_res_4['formato_lider'].copy()
    df_res_4['precio_lider_inicial'] = df_res_4['precio_lider'].copy()

    df_res_4['name_lider'] = np.where((df_res_4['score_lider_inicial']>=umbral_score), df_res_4['name_lider'], '')
    df_res_4['score_lider'] = np.where((df_res_4['score_lider_inicial']>=umbral_score), df_res_4['score_lider'], np.nan)
    df_res_4['marca_lider'] = np.where((df_res_4['score_lider_inicial']>=umbral_score), df_res_4['marca_lider'], '')
    df_res_4['formato_lider'] = np.where((df_res_4['score_lider_inicial']>=umbral_score), df_res_4['formato_lider'], '')
    df_res_4['precio_lider'] = np.where((df_res_4['score_lider_inicial']>=umbral_score), df_res_4['precio_lider'], np.nan)

    # Jumbo
    df_res_4['name_jumbo_inicial'] = df_res_4['name_jumbo'].copy()
    df_res_4['score_jumbo_inicial'] = df_res_4['score_jumbo'].copy()
    df_res_4['marca_jumbo_inicial'] = df_res_4['marca_jumbo'].copy()
    df_res_4['formato_jumbo_inicial'] = df_res_4['formato_jumbo'].copy()
    df_res_4['precio_jumbo_inicial'] = df_res_4['precio_jumbo'].copy()

    df_res_4['name_jumbo'] = np.where((df_res_4['score_jumbo_inicial']>=umbral_score), df_res_4['name_jumbo'], '')
    df_res_4['score_jumbo'] = np.where((df_res_4['score_jumbo_inicial']>=umbral_score), df_res_4['score_jumbo'], np.nan)
    df_res_4['marca_jumbo'] = np.where((df_res_4['score_jumbo_inicial']>=umbral_score), df_res_4['marca_jumbo'], '')
    df_res_4['formato_jumbo'] = np.where((df_res_4['score_jumbo_inicial']>=umbral_score), df_res_4['formato_jumbo'], '')
    df_res_4['precio_jumbo'] = np.where((df_res_4['score_jumbo_inicial']>=umbral_score), df_res_4['precio_jumbo'], np.nan)

    df_res_4 = df_res_4.drop_duplicates()

    df_res_4 = df_res_4.rename(columns={'COD_CAT_N1_SMT': 'cod_cat_n1_smt',
                                    'Categoría nivel 1 - Smartbuy': 'categoria_nivel_1',
                                    'COD_CAT_N2_SMT': 'cod_cat_n2_smt',
                                    'Categoría nivel 2 - Smartbuy': 'categoria_nivel_2',
                                    'internet_price': 'precio'})

    actual_date = str(datetime.now())[0:10]

    df_res_4.to_excel(ruta + f'df_matching_total.xlsx'.format(actual_date), index=0)

    df_res_5 = df_res_4[['id_smart', 'name', 'description', 'cod_cat_n1_smt', 'categoria_nivel_1', 'cod_cat_n2_smt', 'categoria_nivel_2', 'marca', 'formato', 'precio', 'image1', 'image2', 'image3', 'empresa', 'name_tottus', 'score_tottus', 'marca_tottus', 'formato_tottus', 'precio_tottus', 'name_lider', 'score_lider', 'marca_lider', 'formato_lider', 'precio_lider', 'name_jumbo', 'score_jumbo', 'marca_jumbo', 'formato_jumbo', 'precio_jumbo']].drop_duplicates()

    cols_key = ['id_smart', 'cod_cat_n1_smt', 'cod_cat_n2_smt']
    cols_tottus = ['name_tottus', 'score_tottus', 'marca_tottus', 'formato_tottus', 'precio_tottus']
    cols_lider = ['name_lider', 'score_lider', 'marca_lider', 'formato_lider', 'precio_lider']
    cols_jumbo = ['name_jumbo', 'score_jumbo', 'marca_jumbo', 'formato_jumbo', 'precio_jumbo']

    # Tottus
    df_det_tottus = df_res_5[cols_key + cols_tottus]
    df_det_tottus.sort_values(['score_tottus'], ascending=[False], inplace=True)
    df_det_tottus['rank'] = 1
    df_det_tottus['rank'] = df_det_tottus.groupby(cols_key, dropna=False)['rank'].cumsum()
    df_det_tottus = df_det_tottus[df_det_tottus['rank']==1]
    del df_det_tottus['rank']

    # Lider
    df_det_lider = df_res_5[cols_key + cols_lider]
    df_det_lider.sort_values(['score_lider'], ascending=[False], inplace=True)
    df_det_lider['rank'] = 1
    df_det_lider['rank'] = df_det_lider.groupby(cols_key, dropna=False)['rank'].cumsum()
    df_det_lider = df_det_lider[df_det_lider['rank']==1]
    del df_det_lider['rank']

    # Jumbo
    df_det_jumbo = df_res_5[cols_key + cols_jumbo]
    df_det_jumbo.sort_values(['score_jumbo'], ascending=[False], inplace=True)
    df_det_jumbo['rank'] = 1
    df_det_jumbo['rank'] = df_det_jumbo.groupby(cols_key, dropna=False)['rank'].cumsum()
    df_det_jumbo = df_det_jumbo[df_det_jumbo['rank']==1]
    del df_det_jumbo['rank']

    df_res_6 = df_res_5.drop(cols_tottus, axis=1).drop(cols_lider, axis=1).drop(cols_jumbo, axis=1).drop_duplicates()

    df_res_6.sort_values(['image1'], ascending=[True], inplace=True)
    df_res_6['rank'] = 1
    df_res_6['rank'] = df_res_6.groupby(cols_key, dropna=False)['rank'].cumsum()
    df_res_6 = df_res_6[df_res_6['rank']==1]
    del df_res_6['rank']

    df_res_7 = pd.merge(df_res_6, df_det_tottus, on=cols_key, how='left')
    df_res_8 = pd.merge(df_res_7, df_det_lider, on=cols_key, how='left')
    df_res_9 = pd.merge(df_res_8, df_det_jumbo, on=cols_key, how='left')

    # Directorio actual del script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta del archivo
    ruta_completa = os.path.join(script_dir, '..', 'data',  'mmpp.xlsx')

    
    if os.path.exists(ruta_completa):
        df_mmpp = pd.read_excel(ruta_completa)
        # Procede con el uso de df_categorias_lider según tus necesidades
    else:
        print(f'El archivo df_categorias_lider.xlsx no se encuentra en la ruta: {ruta_completa}')

    lista_mmpp = df_mmpp['mmpp'].values.tolist()

    df_res_9['flag_mmpp'] = 0

    for mmpp in lista_mmpp:
        df_res_9['flag_mmpp'] = np.where(df_res_9['marca'].str.contains(mmpp), 1, df_res_9['flag_mmpp'])

    df_res_9['flag_mmpp'] = np.where(df_res_9['marca'].isnull(), 0, df_res_9['flag_mmpp'])

    df_final = df_res_9.copy()
    
    print(df_final.shape)

    print(df_final[['id_smart', 'name', 'empresa', 'cod_cat_n1_smt', 'cod_cat_n2_smt']].drop_duplicates().shape)

    fecha_creacion = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo_parquet = f"df_matching_{fecha_creacion}.parquet"

    # df_final[['id_smart', 'name', 'description', 'cod_cat_n1_smt', 'categoria_nivel_1', 'cod_cat_n2_smt', 'categoria_nivel_2', 'marca', 'formato', 'precio', 'image1', 'image2', 'image3', 'empresa', 'name_tottus', 'score_tottus', 'marca_tottus', 'formato_tottus', 'precio_tottus', 'name_lider', 'score_lider', 'marca_lider', 'formato_lider', 'precio_lider', 'name_jumbo', 'score_jumbo', 'marca_jumbo', 'formato_jumbo', 'precio_jumbo', 'flag_mmpp']].drop_duplicates().to_csv(ruta + f'/df_matching.csv', index=False, sep=';')
    # df_final[['id_smart', 'name', 'description', 'cod_cat_n1_smt', 'categoria_nivel_1', 'cod_cat_n2_smt', 'categoria_nivel_2', 'marca', 'formato', 'precio', 'image1', 'image2', 'image3', 'empresa', 'name_tottus', 'score_tottus', 'marca_tottus', 'formato_tottus', 'precio_tottus', 'name_lider', 'score_lider', 'marca_lider', 'formato_lider', 'precio_lider', 'name_jumbo', 'score_jumbo', 'marca_jumbo', 'formato_jumbo', 'precio_jumbo', 'flag_mmpp']].drop_duplicates().to_parquet(nombre_archivo_parquet, index=False)
    df_final[['id_smart', 'name', 'description', 'cod_cat_n1_smt', 'categoria_nivel_1', 'cod_cat_n2_smt', 'categoria_nivel_2', 'marca', 'formato', 'precio', 'image1', 'image2', 'image3', 'empresa',  'name_lider', 'score_lider', 'marca_lider', 'formato_lider', 'precio_lider', 'name_jumbo', 'score_jumbo', 'marca_jumbo', 'formato_jumbo', 'precio_jumbo', 'flag_mmpp']].drop_duplicates().to_csv(ruta + f'/df_matching.csv', index=False, sep=';')
    df_final[['id_smart', 'name', 'description', 'cod_cat_n1_smt', 'categoria_nivel_1', 'cod_cat_n2_smt', 'categoria_nivel_2', 'marca', 'formato', 'precio', 'image1', 'image2', 'image3', 'empresa',  'name_lider', 'score_lider', 'marca_lider', 'formato_lider', 'precio_lider', 'name_jumbo', 'score_jumbo', 'marca_jumbo', 'formato_jumbo', 'precio_jumbo', 'flag_mmpp']].drop_duplicates().to_parquet(nombre_archivo_parquet, index=False)


    ##! LEER Y GUARDAR DATOS EN LA DB
    csv_file_path = ruta + '/df_matching.csv'

    # Call the insert_data_products function with the file path
    loop = asyncio.get_event_loop()

    # Llama a la función asíncrona dentro del bucle
    result = loop.run_until_complete(insert_data_products(csv_file_path))
    print(result)

    # Cierra el bucle de eventos asíncronos
    loop.close()


    ##! SUBIR DATOS HISTORICOS A AWS S3
    # Ruta completa del archivo local
    ruta_completa_local = os.path.abspath(nombre_archivo_parquet)

    # Subir el archivo Parquet a S3
    try:
        s3_client.upload_file(ruta_completa_local, s3_bucket_name, nombre_archivo_parquet)
        print(f"Archivo Parquet '{nombre_archivo_parquet}' subido exitosamente a S3.")
    except Exception as e:
        print(f"Error al subir el archivo Parquet a S3: {str(e)}")

    # Eliminar el archivo Parquet local después de subirlo a S3 (opcional)
    os.remove(ruta_completa_local)