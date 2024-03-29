import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import lxml
import json
import tqdm 
from PIL import Image
from urllib.request import urlopen,Request
from io import BytesIO
from datetime import datetime
import time
import psutil
import multiprocessing as mp
# import istarmap  # import to apply patch
from web_scraper_tottus import istarmap

from selenium import webdriver

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import warnings
warnings.filterwarnings('ignore')

n = mp.cpu_count()

try:
   mp.set_start_method('spawn', force=True)
#   print("spawned")
except RuntimeError:
   pass

def get_url_tottus(pais:str):
    
    if pais == 'CL':
        url_tottus = 'https://tottus.falabella.com/tottus-cl'
    elif pais == 'PE':
        url_tottus = 'https://tottus.falabella.com.pe/tottus-pe'
    else:
        return('País incorrecto')

    return(url_tottus)

def get_url(pais:str, url=''):

    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"}

    if url == '':
        url = get_url_tottus(pais)
    else:
        url = url

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    all_data = soup.find_all("script", {"type": "application/json"})

    for data in all_data:
        jsn = json.loads(data.string)

    return jsn



def get_info_category(pais:str):

    first_level_category = list()
    url_first_level_category = list()
    second_level_category = list()
    url_second_level_category = list()
    third_level_category = list()
    url_third_level_category = list()

    try:

        categories = get_url(pais)['props']['pageProps']['serverData']['headerData']['sisNavigationMenu']['entry']['categories']

        for i in categories:
            for j in i['second_level_categories']:
                for k in j['third_level_categories']:

                    first_level_category.append(i['item_name'])
                    url_first_level_category.append(i['item_url']['href'])
                    second_level_category.append(j['item_name'])
                    url_second_level_category.append(j['item_url'])
                    third_level_category.append(k['item_name'])
                    url_third_level_category.append(k['item_url'])

    except:

        df_url_cat = pd.DataFrame()

    df_url_cat = pd.DataFrame()

    df_url_cat['first_level_category'] = first_level_category
    df_url_cat['url_first_level_category'] = url_first_level_category
    df_url_cat['second_level_category'] = second_level_category
    df_url_cat['url_second_level_category'] = url_second_level_category
    df_url_cat['third_level_category'] = third_level_category
    df_url_cat['url_third_level_category'] = url_third_level_category

    return df_url_cat, len(third_level_category)

def get_pages_category(pais:str, i:str, first:str, second:str, third:str):

    total_url_cat = list()

    total_categories = get_url(pais, url=i)

    try:
        per_page, count = total_categories['props']['pageProps']['pagination']['perPage'], total_categories['props']['pageProps']['pagination']['count']
        n_paginas = int(np.ceil(count/per_page))
        
        if n_paginas>1:
            url_cat_page = [[i + '?subdomain=tottus&page=' + str(j) + '&store=tottus', first, second, third] for j in range(2, n_paginas+1)]
            total_url_cat.append([i, first, second, third])
            total_url_cat.extend(url_cat_page)
        else:
            total_url_cat.append([i, first, second, third])
    
    except:
        total_url_cat.append([i, first, second, third])
    
    return(total_url_cat)

def get_pages_categories(pais:str, df_categories:pd.DataFrame):

    list_res = list()

    with mp.Pool(n) as pool:
        iterable = [(pais, i, first, second, third) for i, first, second, third in zip(df_categories.url_third_level_category, df_categories.first_level_category, df_categories.second_level_category, df_categories.third_level_category)]
        results = list(tqdm.tqdm(pool.istarmap(get_pages_category, iterable), total=len(iterable)))
        pool.close()
        pool.join()
    
    for res in results:
        list_res = list_res + res
    
    return(pd.DataFrame(list_res, columns=['url_category', 'first_level_category', 'second_level_category', 'third_level_category']).drop_duplicates().values.tolist())

def get_info_product(pais:str, list_pages_category:list):

    url_category = list()
    name_product = list()
    url_product = list()
    first_level_category = list()
    second_level_category = list()
    third_level_category = list()

    sku = get_url(pais, url=list_pages_category[0])

    try:

        for j in sku['props']['pageProps']['results']:
            url_category.append(list_pages_category[0])
            name_product.append(j['displayName'])
            url_product.append(j['url'])
            first_level_category.append(list_pages_category[1])
            second_level_category.append(list_pages_category[2])
            third_level_category.append(list_pages_category[3])

    except:
        print('ERROR: url not found')
    
    df_url_sku = pd.DataFrame()

    df_url_sku['url_category'] = url_category
    df_url_sku['name_product'] = name_product
    df_url_sku['url_product'] = url_product
    df_url_sku['first_level_category'] = first_level_category
    df_url_sku['second_level_category'] = second_level_category
    df_url_sku['third_level_category'] = third_level_category

    return(df_url_sku.drop_duplicates())

def get_info_products(pais:str, df_info_category:list):

    with mp.Pool(n) as pool:
        iterable = [(pais, i) for i in df_info_category]
        results = list(tqdm.tqdm(pool.istarmap(get_info_product, iterable), total=len(iterable)))
        pool.close()
        pool.join()
    
    return(pd.concat(results).drop_duplicates())

def validate_url_cat(total_url_sku:pd.DataFrame, df_categories:pd.DataFrame):

    cat_validate = total_url_sku[['url_category']].drop_duplicates()
    cat_validate['url_down'] = 0

    cat_validate = df_categories.merge(cat_validate.rename(columns = {'url_category':'url_third_level_category'}), how='left')
    cat_validate['url_down'] = cat_validate.url_down.fillna(1)

    return cat_validate

def get_info_image(df_info_sku:list):

    img_url = ''
    px_url = ''

    n_imagenes = len(df_info_sku)

    for i in range(n_imagenes):

        try:

            url_img = Request(df_info_sku[i]['url'],headers={'User-Agent': 'Mozilla/5.0'})

            u = urlopen(url_img)
            raw_data = u.read()
            u.close()

            img = Image.open(BytesIO(raw_data))

            if i == n_imagenes-1:
                img_url = img_url + df_info_sku[i]['url'] 
                px_url = px_url + str(img.size) 
            
            else:
                img_url = img_url + df_info_sku[i]['url'] + '; '
                px_url = px_url + str(img.size) + '; '

        except:
            
            if i == n_imagenes-1:

                img_url = img_url + 'url_image not found'
                px_url = px_url + ''

            else:

                img_url = img_url + 'url_image not found' + '; '
                px_url = px_url + '; '

    return img_url, px_url

def get_scraping_sku(pais_sku:str, url_sku:list):

    try:

        df_producto = get_url(pais_sku,url_sku[0])['props']['pageProps']['productData']

        try:
            id_url = df_producto['id']
        except:
            id_url = ''

        try: 
            name_url = df_producto['name']
        except:
            name_url = ''

        try:
            description_url =  df_producto['description']
        except:
            description_url = ''

        try:
            n_attributes = len(df_producto['attributes']['specifications'])
            atr_sku = ''

            for i in range(n_attributes):

                if i == n_attributes-1:
                    atr_sku = atr_sku+df_producto['attributes']['specifications'][i]['name']+': '+df_producto['attributes']['specifications'][i]['value']
                else:
                    atr_sku = atr_sku + df_producto['attributes']['specifications'][i]['name']+': '+df_producto['attributes']['specifications'][i]['value']+'; '

        except:
            atr_sku = ''
            
        try:

            normal_price = '' 
            internet_price = ''
            cmr_price = ''

            if len(df_producto['variants'][0]['prices'])>0:
            
                for j in df_producto['variants'][0]['prices']:

                    if j['type'] == 'normalPrice':
                        normal_price = j['price'][0]
                    elif j['type'] == 'internetPrice':
                        internet_price = j['price'][0]
                    elif j['type'] == 'cmrPrice':
                        cmr_price = j['price'][0]

        except:
                normal_price = ''
                internet_price = ''
                cmr_price = ''

        try:    
            id_client_sku = df_producto['variants'][0]['offerings'][0]['offeringId']
        except:
            id_client_sku = ''

        try:
            cod_sku = df_producto['variants'][0]['offerings'][0]['sellerSkuId']
        except:
            cod_sku = ''

        try:
            image_info_1,image_info_2 = get_info_image(df_producto['variants'][0]['medias'])
        except:
            image_info_1,image_info_2 = '',''

        try:
            first = url_sku[1]
        except:
            first = ''
        
        try:
            second = url_sku[2]
        except:
            second = ''
        
        try:
            third = url_sku[3]
        except:
            third = ''
        
        try:
            category_1 = df_producto['breadCrumb'][1]['label']
        except:
            category_1 = ''

        try:
            category_2 = df_producto['breadCrumb'][0]['label']
        except:
            category_2 = ''

    except:
        
        id_url = ''
        name_url = ''
        description_url = ''
        atr_sku = ''
        normal_price = ''
        internet_price = ''
        cmr_price = ''
        id_client_sku = ''
        cod_sku = ''
        image_info_1 = ''
        image_info_2 = ''
        first = ''
        second = ''
        third = ''
        category_1 = ''
        category_2 = ''

    return pais_sku, url_sku[0], id_url, name_url, description_url, id_client_sku, cod_sku, first, second, third, category_1, category_2, atr_sku, normal_price, internet_price, cmr_price, image_info_1, image_info_2


def get_df_scraping(pais:str, list_url:list):

    with mp.Pool(n) as pool:
        iterable = [(pais, li) for li in list_url]
        results = list(tqdm.tqdm(pool.istarmap(get_scraping_sku, iterable), total=len(iterable)))
        pool.close()
        pool.join()

    return(pd.DataFrame(results, columns=['pais', 'url_sku', 'id', 'name', 'description', 'id_client', 'cod_sku', 'first_category',
                                        'second_category', 'third_category', 'category_1', 'category_2', 'attributes', 'normal_price',
                                        'internet_price', 'cmr_price', 'url_image', 'pixel_image']))


########################################################
##################### REPORTE TOTAL ####################
########################################################

def total_report(pais:str,df_scraping:pd.DataFrame):

    print('#################################################')
    print('REPORTE TOTAL')
    print('#################################################')

    ###- REPORTE

    print('')
    print('Se arma el reporte total...')
    print('')

    start_time = time.time()

    df_reporte = df_scraping.copy()

    df_reporte['ID_DIARUNNING'] = datetime.now()
    
    df_reporte['pais'] = pais

    print(str('['+time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time)))+'],', 'Memory % Used:', psutil.virtual_memory()[2])

    return df_reporte.drop_duplicates()


########################################################
################### EXPORTAR REPORTES ##################
########################################################

def export_reports(pais:str,ruta:str,df1:pd.DataFrame,df2:pd.DataFrame,df3:pd.DataFrame,df4:pd.DataFrame):

    print('')
    print('Se exporta los reportes a la ruta...')
    print('')

    #try: 

    start_time = time.time()

    actual_date = str(datetime.now())[0:10]

    df1.to_excel(ruta + f'df_categorias_tottus.xlsx'.format(actual_date), index=0)

    df2.to_excel(ruta + f'cat_validate_tottus.xlsx'.format(actual_date), index=0)

    df3.to_excel(ruta + f'results_ws_tottus.xlsx'.format(actual_date), index=0)

    df4.to_excel(ruta + f'REPORTE_WS_TOTTUS.xlsx'.format(actual_date), index=0)

    print(str('['+time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time)))+'],', 'Memory % Used:', psutil.virtual_memory()[2])
    print('')

    #except:
    #    print('Reports not export')