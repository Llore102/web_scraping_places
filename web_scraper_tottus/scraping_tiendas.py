from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.chrome.options import Options
import multiprocessing as mp
import istarmap  # import to apply patch
from webdriver_manager.chrome import ChromeDriverManager

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

# def get_driver():
#     # chrome_options = Options()
#     # chrome_options.add_argument("--headless")
#     # prefs = {"profile.default_content_setting_values.notifications" : 2}
#     # chrome_options.add_experimental_option("prefs",prefs)
#     # s = ChromeService(executable_path="chromedriver")
#     # driver = webdriver.Chrome(service=s, options=chrome_options)
#     # driver.maximize_window()
#     # options = webdriver.ChromeOptions()
#     # driver = webdriver.Remote(command_executor='http://localhost:4444', options=options)
#     chrome_driver_path = 'C:/Users/llore/Scrapers/smartbuy/chromedriver.exe'
#     driver = webdriver.Chrome(executable_path=chrome_driver_path)
#     return driver

def get_driver():
    chrome_options = webdriver.ChromeOptions()
    service = webdriver.ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_direccion(r, c, dir):

    driver = get_driver()

    direccion = dir[:dir.index("\n")] + ', ' + c + ", " + r + ", Chile, Tottus"

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

    return(r, c, dir, imagen, latitud, longitud, comentario)

def scraping_tiendas():

    url = 'https://tottus.falabella.com/tottus-cl/page/horario_tiendas'

    driver = get_driver()

    list_direcciones = list()

    driver.get(url)

    #Obtener las tiendas
    try:
        wait(driver, 64).until(ec.presence_of_element_located((By.XPATH, "/html/body/div[@id='__next']/div/div[@class='container-fluid container-xl']/div[@class='row BaseTemplate-module_main-row__1dr8i']/div[@class='AccordeonItems-module_container__0Tqsb pb-3 col-md-12']/div[@class='AccordeonItems-module_container-desktop__sN1qw']")))
        regiones = driver.find_elements("xpath", "/html/body/div[@id='__next']/div/div[@class='container-fluid container-xl']/div[@class='row BaseTemplate-module_main-row__1dr8i']/div[@class='AccordeonItems-module_container__0Tqsb pb-3 col-md-12']/div[@class='AccordeonItems-module_container-desktop__sN1qw']")
        
        for reg in tqdm.tqdm(regiones):
            
            #scroll para visualizar
            driver.execute_script("arguments[0].scrollIntoView();", reg)

            region = reg.find_elements("xpath", "div[@class='AccordeonItems-module_title-container__qQktq']/div[@class='AccordeonItems-module_title-component-container__4Bx-S']/div[@class='AccordeonItems-module_title-component-title-wrapper__xQHlp']/span[@class='AccordeonItems-module_title-accordion__355b5']")[0].text
            
            comunas = reg.find_elements("xpath", "div[@class='AccordeonItems-module_accordeon-desktop__UEDBa']/ul/li[@class='AccordeonItems-module_card-item__8URy3']/div[@class='Accordion-module_toggler__hOkhR']")

            for com in comunas:
                
                #scroll para visualizar
                driver.execute_script("arguments[0].scrollIntoView();", com)
                
                comu = com.find_elements("xpath", "div[@class='Accordion-module_list-item__sXhcF']/div[@class='Accordion-module_title-item__-WbJb']")[0]
                
                comu.click()

                comuna = comu.text
                
                direccion = com.find_elements("xpath", "div[@class='Accordion-module_content__eS3R7']/div[@class='Accordion-module_content-text__OwYKK']/span")[0].text

                list_direcciones.append([region, comuna, direccion])

    except:
            print("Regiones no encontradas")

    driver.close()
    

    with mp.Pool(n) as pool:
        iterable = [(r, c, dir) for r, c, dir in list_direcciones]
        list_direcciones_final = list(tqdm.tqdm(pool.istarmap(get_direccion, iterable), total=len(iterable)))
        pool.close()
        pool.join()


    df_tiendas_tottus = pd.DataFrame(list_direcciones_final, columns=['region', 'comuna', 'direccion', 'imagen', 'latitud', 'longitud', 'comentario'])

    actual_date = str(datetime.now())[0:10]

    df_tiendas_tottus.to_excel(ruta + f'/df_tiendas_tottus.xlsx'.format(actual_date), index=0)