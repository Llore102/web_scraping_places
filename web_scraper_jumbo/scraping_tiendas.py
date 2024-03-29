from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.chrome.options import Options
import multiprocessing as mp
import istarmap  # import to apply patch

import utils_scraping as st

import tqdm

import numpy as np
import pandas as pd

from datetime import datetime

import time
import os

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


ruta = os.path.dirname(os.path.abspath(__file__))

n = mp.cpu_count()

def get_driver():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    s = ChromeService("chromedriver")
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.maximize_window()
    return driver

def get_direccion(l, direccion, url, lat, lon):

    driver = get_driver()

    dir = direccion + ", Chile, Jumbo"

    driver.get("https://www.google.com/maps/search/"+dir)

    time.sleep(3)

    try:
        wait(driver, 4).until(ec.visibility_of_element_located((By.XPATH, "html/body/div[@id='app-container']/div[@id='content-container']/div[@id='QA0Szd']/div/div[@class='XltNde tTVLSc']/div[@class='w6VYqd']/div[@class='bJzME tTVLSc']/div[@class='k7jAl lJ3Kh miFGmb']/div[@tabindex='-1']/div[@class='aIFcqe']/div[@class='m6QErb WNBkOb ']/div[@class='TIHn2 ']/div[@class='tAiQdd']/div[@class='lMbq3e']")))

        coordenadas = driver.find_element(By.CSS_SELECTOR, 'meta[itemprop=image]').get_attribute('content')

        latitud = float(coordenadas[coordenadas.find('-'):coordenadas.find("%")])
        longitud =float(coordenadas[coordenadas.find('-', coordenadas.find("-")+1):coordenadas.find("&")])

        wait(driver, 4).until(ec.visibility_of_element_located((By.XPATH, "html/body/div[@id='app-container']/div[@id='content-container']/div[@id='QA0Szd']/div/div[@class='XltNde tTVLSc']/div[@class='w6VYqd']/div[@class='bJzME tTVLSc']/div[@class='k7jAl lJ3Kh miFGmb']/div[@tabindex='-1']/div[@class='aIFcqe']/div[@class='m6QErb WNBkOb ']/div[@class='ZKCDEc']/div[@class='RZ66Rb FgCUCc']/button[@class='aoRNLd kn2E5e NMjTrf lvtCsd ']/img")))
        imagen = driver.find_element(By.XPATH, "html/body/div[@id='app-container']/div[@id='content-container']/div[@id='QA0Szd']/div/div[@class='XltNde tTVLSc']/div[@class='w6VYqd']/div[@class='bJzME tTVLSc']/div[@class='k7jAl lJ3Kh miFGmb']/div[@tabindex='-1']/div[@class='aIFcqe']/div[@class='m6QErb WNBkOb ']/div[@class='ZKCDEc']/div[@class='RZ66Rb FgCUCc']/button[@class='aoRNLd kn2E5e NMjTrf lvtCsd ']/img").get_attribute('src')

        comentario = 'Dirección encontrada'
        
    except:

        try:
            wait(driver, 4).until(ec.element_to_be_clickable((By.CLASS_NAME, "hfpxzc")))
            boton = driver.find_element(By.CLASS_NAME, "hfpxzc")
            boton.click()

            time.sleep(3)

            coordenadas = driver.find_element(By.CSS_SELECTOR, 'meta[itemprop=image]').get_attribute('content')

            latitud = float(coordenadas[coordenadas.find('-'):coordenadas.find("%")])
            longitud =float(coordenadas[coordenadas.find('-', coordenadas.find("-")+1):coordenadas.find("&")])

            wait(driver, 4).until(ec.visibility_of_element_located((By.XPATH, "html/body/div[@id='app-container']/div[@id='content-container']/div[@id='QA0Szd']/div/div[@class='XltNde tTVLSc']/div[@class='w6VYqd']/div[@class='bJzME Hu9e2e tTVLSc']/div[@class='k7jAl lJ3Kh miFGmb']/div[@tabindex='-1']/div[@class='aIFcqe']/div[@class='m6QErb WNBkOb ']/div[@class='m6QErb DxyBCb kA9KIf dS8AEf ']/div[@class='ZKCDEc']/div[@class='RZ66Rb FgCUCc']/button[@class='aoRNLd kn2E5e NMjTrf lvtCsd ']/img")))
            imagen = driver.find_element(By.XPATH, "html/body/div[@id='app-container']/div[@id='content-container']/div[@id='QA0Szd']/div/div[@class='XltNde tTVLSc']/div[@class='w6VYqd']/div[@class='bJzME Hu9e2e tTVLSc']/div[@class='k7jAl lJ3Kh miFGmb']/div[@tabindex='-1']/div[@class='aIFcqe']/div[@class='m6QErb WNBkOb ']/div[@class='m6QErb DxyBCb kA9KIf dS8AEf ']/div[@class='ZKCDEc']/div[@class='RZ66Rb FgCUCc']/button[@class='aoRNLd kn2E5e NMjTrf lvtCsd ']/img").get_attribute('src')

            comentario = 'Más de una dirección encontrada, toma la primera'
            
            print(comentario)

        except:
            
            comentario = "Dirección no encontrada"
            print(comentario)
        
            latitud = np.nan
            longitud = np.nan

            imagen = ''
            
            driver.get("https://www.google.com/maps")
    
    driver.close()

    return(l, direccion, url, lat, lon, imagen, latitud, longitud, comentario)

def scraping_tiendas():

    url = 'https://www.jumbo.cl/locales'

    driver = st.get_driver()

    list_direcciones = list()

    driver.get(url)

    try:

        wait(driver, 32).until(ec.presence_of_element_located((By.XPATH, "html/body/div[@id='root']/div[@class='app-content']/div[@class='localities-page page']/main[@class='localities-page-container']/div[@class='slider paginator-slider']/div[@class='slides']/button")))
        pages = driver.find_elements("xpath", "html/body/div[@id='root']/div[@class='app-content']/div[@class='localities-page page']/main[@class='localities-page-container']/div[@class='slider paginator-slider']/div[@class='slides']/button")
        n_paginas = len(pages)

        for i in tqdm.tqdm(range(1, n_paginas+1)):

            if i>1:

                boton = driver.find_elements("xpath", "html/body/div[@id='root']/div[@class='app-content']/div[@class='localities-page page']/main[@class='localities-page-container']/div[@class='slider paginator-slider']/div[@class='slides']/button["+str(i)+"]")[0]
                
                #scroll para visualizar
                driver.execute_script("arguments[0].scrollIntoView();", boton)

                time.sleep(2)

                boton.click()

                time.sleep(3)
            
            wait(driver, 64).until(ec.presence_of_element_located((By.XPATH, "html/body/div[@id='root']/div[@class='app-content']/div[@class='localities-page page']/main[@class='localities-page-container']/section[@class='localities-list']/article[@class='local']")))
            articulos = driver.find_elements("xpath", "html/body/div[@id='root']/div[@class='app-content']/div[@class='localities-page page']/main[@class='localities-page-container']/section[@class='localities-list']/article[@class='local']")

            for art in articulos:
                local = art.find_elements("xpath", "div[@class='title-with-bar local-title']/div[@class='title-with-bar-wrapper']/h1[@class='title-with-bar-text']")[0].text
                direccion = art.find_elements("xpath", "div[@class='local-content']/div[@class='local-content-col']/div[@class='local-info'][1]/div[@class='local-info-content']")[0].text
                url_maps = art.find_elements("xpath", "div[@class='local-content']/div[@class='local-content-col']/div[@class='local-info'][2]/div[@class='link-map']/a[@class='new-link']")[0].get_attribute('href')
                lat = url_maps[url_maps.find('-'):url_maps.find(',')]
                lon = url_maps[url_maps.find('-', url_maps.find('-')+1):]
                

                list_direcciones.append([local, direccion, url_maps, lat, lon])

    except:
        print("Cantidad de páginas no encontradas")

    driver.close()

    
    with mp.Pool(n) as pool:
        iterable = [(l, direccion, url, lat, lon) for l, direccion, url, lat, lon in list_direcciones]
        list_direcciones_final = list(tqdm.tqdm(pool.istarmap(get_direccion, iterable), total=len(iterable)))
        pool.close()
        pool.join()


    df_tiendas_jumbo = pd.DataFrame(list_direcciones_final, columns=['local', 'direccion', 'url_maps', 'lat', 'lon', 'imagen', 'latitud', 'longitud', 'comentario'])

    df_tiendas_jumbo['comuna'] = df_tiendas_jumbo['direccion'].map(lambda x:x[x.find(',')+2:x.find(',', x.find(',')+1)])
    df_tiendas_jumbo['region'] = df_tiendas_jumbo['direccion'].map(lambda x:x[x.find(',', x.find(',')+1)+2:])

    actual_date = str(datetime.now())[0:10]

    df_tiendas_jumbo.to_excel(ruta + f'/df_tiendas_jumbo.xlsx'.format(actual_date), index=0)
