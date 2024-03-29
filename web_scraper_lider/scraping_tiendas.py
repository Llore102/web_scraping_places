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

import re

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

def get_direccion(s, c, dir, dis, r, ha, hc):

    driver = get_driver()

    direccion = dir + ', ' + c + ", " + r + ", Chile, Lider"

    driver.get("https://www.google.com/maps/search/"+direccion)

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

    return(s, c, dir, dis, r, ha, hc, imagen, latitud, longitud, comentario)

def scraping_tiendas():

    url = 'https://www.lider.cl/tiendas'

    driver = st.get_driver()

    list_direcciones = list()

    driver.get(url)

    try:

        wait(driver, 32).until(ec.presence_of_element_located((By.XPATH, "/html/body/div[@id='placeholder']/iframe")))

        iframe = driver.find_element(By.XPATH, "/html/body/div[@id='placeholder']/iframe")

        # switch to selected iframe
        driver.switch_to.frame(iframe)

        wait(driver, 32).until(ec.presence_of_element_located((By.XPATH, "/html/body/div[@class='container-landing']/div[@class='content-info']/div[@class='table-responsive']/div[@id='dtBasicExample_wrapper']/div[@id='dtBasicExample_info']")))
        per_page_count = driver.find_elements("xpath", "/html/body/div[@class='container-landing']/div[@class='content-info']/div[@class='table-responsive']/div[@id='dtBasicExample_wrapper']/div[@id='dtBasicExample_info']")[0].text
        per_page_count_list = [int(s) for s in re.findall(r'-?\d+\.?\d*', per_page_count)]
        per_page = per_page_count_list[1]
        count = per_page_count_list[2]
        n_paginas = int(np.ceil(count/per_page))

        for i in tqdm.tqdm(range(n_paginas-1)):
            
            wait(driver, 32).until(ec.presence_of_element_located((By.XPATH, "/html/body/div[@class='container-landing']/div[@class='content-info']/div[@class='table-responsive']/div[@id='dtBasicExample_wrapper']/table[@id='dtBasicExample']/tbody/tr")))
            rows = driver.find_elements("xpath", "/html/body/div[@class='container-landing']/div[@class='content-info']/div[@class='table-responsive']/div[@id='dtBasicExample_wrapper']/table[@id='dtBasicExample']/tbody/tr")

            for row in rows:
                supermercado = row.find_elements("xpath", "td[1]")[0].text
                comuna = row.find_elements("xpath", "td[2]")[0].text
                direccion = row.find_elements("xpath", "td[3]")[0].text
                disponibilidad = row.find_elements("xpath", "td[4]")[0].text
                region = row.find_elements("xpath", "td[5]")[0].text
                hora_apertura = row.find_elements("xpath", "td[6]")[0].text
                hora_cierre = row.find_elements("xpath", "td[7]")[0].text

                list_direcciones.append([supermercado, comuna, direccion, disponibilidad, region, hora_apertura, hora_cierre])

            wait(driver, 32).until(ec.presence_of_element_located((By.XPATH, "/html/body/div[@class='container-landing']/div[@class='content-info']/div[@class='table-responsive']/div[@id='dtBasicExample_wrapper']/div[@class='dataTables_paginate paging_simple_numbers']/a[@id='dtBasicExample_next']")))
            boton = driver.find_elements("xpath", "/html/body/div[@class='container-landing']/div[@class='content-info']/div[@class='table-responsive']/div[@id='dtBasicExample_wrapper']/div[@class='dataTables_paginate paging_simple_numbers']/a[@id='dtBasicExample_next']")[0]
            boton.click()
            
            
    except:
        print("Cantidad de páginas no encontradas")

    driver.close()


    with mp.Pool(n) as pool:
        iterable = [(s, c, dir, dis, r, ha, hc) for s, c, dir, dis, r, ha, hc in list_direcciones]
        list_direcciones_final = list(tqdm.tqdm(pool.istarmap(get_direccion, iterable), total=len(iterable)))
        pool.close()
        pool.join()


    df_tiendas_lider = pd.DataFrame(list_direcciones_final, columns=['supermercado', 'comuna', 'direccion', 'disponibilidad', 'region', 'hora_apertura', 'hora_cierre', 'imagen', 'latitud', 'longitud', 'comentario'])

    actual_date = str(datetime.now())[0:10]

    df_tiendas_lider.to_excel(ruta + f'/df_tiendas_lider.xlsx'.format(actual_date), index=0)
