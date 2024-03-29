# from chromedriver_py import binary_path

import multiprocessing as mp
# import istarmap  # import to apply patch
from web_scraper_lider import istarmap
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import multiprocessing as mp

import tqdm

import numpy as np
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import re

from datetime import datetime

from PIL import Image
from urllib.request import urlopen,Request
from io import BytesIO

import time
import psutil
# from driver.driver import get_driver_with_retry

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

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/79.0.3945.117 Safari/537.36"}

def get_driver_with_retry():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-agent={headers['User-Agent']}")
    chrome_options.add_argument("--window-size=1920,1080")  # Establecer el tamaño de la ventana
    chrome_options.add_argument("--start-maximized")  # Maximizar la ventana al abrirse
    chrome_options.add_argument("--disable-infobars")  # Deshabilitar la barra de información
    chrome_options.add_argument("--disable-extensions")  # Deshabilitar las extensiones del navegador
    chrome_options.add_argument("--disable-gpu")  # Deshabilitar la aceleración de GPU
    chrome_options.add_argument("--disable-dev-shm-usage")  # Deshabilitar el uso compartido de memoria
    chrome_options.add_argument("--no-sandbox") 
    # chrome_options.add_argument("--headless")  # Opcional: para ejecución en segundo plano

            # Instanciar el controlador de Chrome y pasar las opciones como argumento
    selenium_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=selenium_service, options=chrome_options)
    driver.maximize_window()
    return driver


def get_url_lider():
    
    url_lider = 'https://www.lider.cl/supermercado'

    return(url_lider)

def get_info_category():


    driver = get_driver_with_retry()
    
    #Vamos a la dirección web de la página objetivo
    driver.get(get_url_lider())

    time.sleep(10)

    
    driver.save_screenshot('screenshotL.png')
    
        #Click en categorías
    try:
        boton = wait(driver, 4).until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div/header/div/div[1]/button')))
        boton.click()
    except TimeoutException:
        print("Botón categorías no encontrado")

    list_categories = []

    #Espera de 5 seg
    time.sleep(5)

    #Obtener las categorías
    try:
        wait(driver, 30).until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div/div/div/div[1]")))
        first_level_categories = driver.find_elements("xpath", "/html/body/div[7]/div/div/div/div[1]/div")
        
        for first in first_level_categories:
            
            first_level_category = first.text

            #scroll para visualizar
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);", first)
            
            #click en la categoria
            first.click()

            wait(driver, 8).until(ec.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div/div[1]")))
            second_level_categories = driver.find_elements("xpath", "/html/body/div[4]/div/div/div/div[1]/div")

            for second in second_level_categories:
                
                wait(second, 4).until(ec.presence_of_element_located((By.XPATH, "a")))
                second_level_category = second.find_elements("xpath", "a")[0].text
                url_first_level_category = second.find_elements("xpath", "a")[0].get_attribute("href")

                third_level_categories = second.find_elements("xpath", "div")

                for third in third_level_categories:
                    
                    wait(third, 4).until(ec.presence_of_element_located((By.XPATH, "a")))
                    third_level_category = third.find_elements("xpath", "a")[0].text
                    url_third_level_category = third.find_elements("xpath", "a")[0].get_attribute("href")

                    list_categories.append([first_level_category, second_level_category, url_first_level_category, third_level_category, url_third_level_category])
            
            
    except TimeoutException:
        print("Categorias no encontradas")
    
    driver.close()
    
    return(pd.DataFrame(list_categories, columns = ['first_level_category', 'second_level_category', 'url_second_level_category', 'third_level_category', 'url_third_level_category']), len(list_categories))

def get_pages_category(pais:str, i:str, first:str, second:str, third:str):

    driver = get_driver_with_retry()

    total_url_cat = list()

    driver.get(i)
    
    time.sleep(3)

    try:

        wait(driver, 16).until(ec.visibility_of_element_located((By.CLASS_NAME, "products-qantity-and-order-desktop__quantity-shown")))
        per_page_count = driver.find_elements(By.CLASS_NAME, "products-qantity-and-order-desktop__quantity-shown")[0].text
        per_page_count_list = [int(s) for s in re.findall(r'-?\d+\.?\d*', per_page_count)]
        per_page = per_page_count_list[1]
        count = per_page_count_list[2]
        n_paginas = int(np.ceil(count/per_page))
        
        if n_paginas>1:
            url_cat_page = [[i + '?page=' + str(j) + '&hitsPerPage=16', first, second, third] for j in range(2, n_paginas+1)]
            total_url_cat.append([i, first, second, third])
            total_url_cat.extend(url_cat_page)
        else:
            total_url_cat.append([i, first, second, third])
    
    except:
        total_url_cat.append([i, first, second, third])
        
    driver.close()
    
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

    driver = get_driver_with_retry()

    url_category = list()
    name_product = list()
    url_product = list()
    first_level_category = list()
    second_level_category = list()
    third_level_category = list()

    driver.get(list_pages_category[0])

    time.sleep(3)

    try:

        wait(driver, 16).until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[@id='root']/div[@class='wrapper']/div[1]/div[3]/div[@class='app-container app-container--category-page']/div[@class='bs__grid__container']/div[@class='shop-wrapper']/div[@class='app-container--category-page__walstore-back-button-container']/div[@class='mb-4 ']/div[@class='shop-wrapper']/div[@class='d-flex']/div[@class='col-lg-9 col-md-8 bs__product-list__container']/div[@class='shop-content']/div[@class='ais-Hits']/ul[@class='ais-Hits-list']/li[@class='ais-Hits-item']/div[1]/div[1]")))
        sku = driver.find_elements("xpath", "/html/body/div[@id='root']/div[@class='wrapper']/div[1]/div[3]/div[@class='app-container app-container--category-page']/div[@class='bs__grid__container']/div[@class='shop-wrapper']/div[@class='app-container--category-page__walstore-back-button-container']/div[@class='mb-4 ']/div[@class='shop-wrapper']/div[@class='d-flex']/div[@class='col-lg-9 col-md-8 bs__product-list__container']/div[@class='shop-content']/div[@class='ais-Hits']/ul[@class='ais-Hits-list']/li[@class='ais-Hits-item']/div[1]/div[1]")

        for j in sku:
            url_category.append(list_pages_category[0])

            wait(j, 4).until(ec.presence_of_element_located((By.XPATH, "div[@class=' product-info']/h2/div[@class='product-card_description-wrapper']/div[1]/span[2]")))
            name_product.append(j.find_elements("xpath", "div[@class=' product-info']/h2/div[@class='product-card_description-wrapper']/div[1]/span[2]")[0].text)

            wait(j, 4).until(ec.presence_of_element_located((By.XPATH, "a")))
            url_product.append(j.find_elements("xpath", "a")[0].get_attribute("href"))
            
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
    
    driver.close()

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

    cat_validate = df_categories.merge(cat_validate.rename(columns={'url_category': 'url_third_level_category'}), how='left')
    cat_validate['url_down'] = cat_validate.url_down.fillna(1)

    return(cat_validate)

def get_scraping_sku(pais_sku:str, url_sku:list):

    driver = get_driver_with_retry()

    driver.get(url_sku[0])

    try:

        wait(driver, 64).until(ec.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[1]/div/div[1]/div/div/div/div/div/div')))
        df_producto = driver.find_elements((By.XPATH, '//*[@id="root"]/div[1]/div/div[1]/div/div/div/div/div/div/div'))[0]

        try:
            id_url = df_producto.find_elements((By.XPATH, "div[@class='m-auto pb-20 product-detail__card-section']/div[@class='product-detail-page__container']/div[1]/div[1]/div[@class='product-detail-card__product-detail-container']/div[@class='product-detail-card__product']/div[@class='product-detail-card__product-info']/div[@class='product-detail-card__product-detail']"))[0].text
        except:
            id_url = ''

        try: 
            name_url = df_producto.find_elements((By.XPATH, '//*[@id="root"]/div[1]/div/div[1]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/h1'))[0].text
        except:
            name_url = ''

        try:
            description_url =  df_producto.find_elements((By.XPATH, '//*[@id="OKTS_div"]/div/p[2]'))[0].text
        except:
            description_url = ''

        try:
            atr_sku =  df_producto.find_elements((By.XPATH, '//*[@id="root"]/div[1]/div/div[1]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[2]/span'))[0].text
        except:
            atr_sku = ''
            
        try:

            normal_price = '' 
            internet_price = ''
            cmr_price = ''
            
            try:
                normal_price = df_producto.find_elements((By.XPATH, '//*[@id="root"]/div[1]/div/div[1]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[4]/div/div[2]/span'))[0].text
            
            except:
                
                try:
                    normal_price = df_producto.find_elements((By.XPATH, '//*[@id="root"]/div[1]/div/div[1]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[4]/div/div[2]/span'))[0].text
                
                except:
                    normal_price = ''

            internet_price = df_producto.find_elements((By.XPATH, '//*[@id="root"]/div[1]/div/div[1]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[4]/div/div[1]/span'))[0].text

        except:
            normal_price = ''
            internet_price = ''
            cmr_price = ''

        try:
            wait(df_producto, 4).until(ec.presence_of_element_located((By.XPATH, "div[@class='m-auto pb-20 product-detail__card-section']/div[@class='product-detail-page__container']/div[1]/div[1]/div[@class='product-detail-card__product-detail-container']/div[@class='product-detail-card__product']/div[@class='product-detail-card__product-info']/div[@class='product-detail-card__product-detail']")))
            id_client_sku = df_producto.find_elements((By.XPATH, "div[@class='m-auto pb-20 product-detail__card-section']/div[@class='product-detail-page__container']/div[1]/div[1]/div[@class='product-detail-card__product-detail-container']/div[@class='product-detail-card__product']/div[@class='product-detail-card__product-info']/div[@class='product-detail-card__product-detail']"))[0].text
        except:
            id_client_sku = ''

        try:
            cod_sku = df_producto.find_elements((By.XPATH, '//*[@id="root"]/div[1]/div/div[1]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[2]/span'))[0].text
        except:
            cod_sku = ''

        try:
            images = df_producto.find_elements((By.XPATH, '//*[@id="root"]/div[1]/div/div[1]/div/div/div/div/div/div/div/div/div[1]/div[2]/div/div/div/div[1]/div/div[2]/figure'))
            
            img_url = ''
            px_url = ''

            n_imagenes = len(images)

            for im, i in zip(images, range(n_imagenes)):

                try:

                    url_img = Request(im.get_attribute("src"), headers={'User-Agent': 'Mozilla/5.0'})

                    u = urlopen(url_img)
                    raw_data = u.read()
                    u.close()

                    img = Image.open(BytesIO(raw_data))

                    if i == n_imagenes-1:
                        img_url = img_url + im.get_attribute("src")
                        px_url = px_url + str(img.size) 
                
                    else:
                        img_url = img_url + im.get_attribute("src") + '; '
                        px_url = px_url + str(img.size) + '; '

                except:
                    
                    if i == n_imagenes-1:

                        img_url = img_url + 'url_image not found'
                        px_url = px_url + ''

                    else:

                        img_url = img_url + 'url_image not found' + '; '
                        px_url = px_url + '; '
            
            image_info_1, image_info_2 = img_url, px_url

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
            category_1 = url_sku[1]
        except:
            category_1 = ''

        try:
            category_2 = url_sku[2]
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
    
    driver.close()

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

    df1.to_excel(ruta + f'df_categorias_lider.xlsx'.format(actual_date), index=0)

    df2.to_excel(ruta + f'cat_validate_lider.xlsx'.format(actual_date), index=0)

    df3.to_excel(ruta + f'results_ws_lider.xlsx'.format(actual_date), index=0)

    df4.to_excel(ruta + f'REPORTE_WS_LIDER.xlsx'.format(actual_date), index=0)

    print(str('['+time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time)))+'],', 'Memory % Used:', psutil.virtual_memory()[2])
    print('')

    #except:
    #    print('Reports not export')