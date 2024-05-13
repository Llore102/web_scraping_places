from chromedriver_py import binary_path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
import multiprocessing as mp
import web_scraper_jumbo.istarmap  # import to apply patch
import tqdm

import numpy as np
import pandas as pd

from datetime import datetime

from PIL import Image
from urllib.request import urlopen,Request
from io import BytesIO

import time
import psutil
import os

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

ruta = os.path.dirname(os.path.abspath(__file__))

# def get_driver():
#     firefox_options = FirefoxOptions()
#     # firefox_options.add_argument("--headless")
#     s = FirefoxService(ruta[:-17]+'geckodriver')
#     driver = webdriver.Firefox(service=s, options=firefox_options)
#     driver.maximize_window()
#     return driver

def get_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)

    s = ChromeService(binary_path)
    driver = webdriver.Chrome(service=s, options=chrome_options)

    # driver.maximize_window()
    return driver

# def get_driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--headless=new")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-gpu")
#     # chrome_options.add_argument("--remote-debugging-port=9222")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--disable-extensions")
#     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     chrome_options.add_experimental_option('useAutomationExtension', False)
#     chrome_options.add_experimental_option('extensionLoadTimeout', 300000)
#     prefs = {"profile.default_content_setting_values.notifications" : 2}
#     chrome_options.add_experimental_option("prefs",prefs)
#     s = ChromeService(binary_path)
#     driver = webdriver.Chrome(service=s, options=chrome_options)
#     driver.maximize_window()
#     return driver

def get_url_jumbo():
    
    url_jumbo = 'https://www.jumbo.cl'

    return(url_jumbo)

def get_info_category():

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)

    s = ChromeService(binary_path)
    driver = webdriver.Chrome(service=s, options=chrome_options)

    driver.maximize_window()

    #Vamos a la dirección web de la página objetivo
    driver.get(get_url_jumbo())

    time.sleep(20)
    driver.save_screenshot('screenshotJ.png')


    #Espera de 3 seg
    
    #Cerrar pop ups
    try:
        boton = wait(driver, 4).until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[@id='root']/div[@class='app-content']/header[@class='new-header-v2']/div[@class='header-content-v2 ']/div[@class='content-menu-wrapper-v2 ']/div[@class='popover-container undefined']/div[@class='popover-select-delivery-method-v2']/div[@class='popover-delivery-info']/button[@class='popover-delivery-close jumbo-icon-new-close']")))
        boton.click()
    except TimeoutException:
        print("Pop up no encontrado")

    #Click en categorías
    try:
        boton = wait(driver, 8).until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[@id='root']/div[@class='app-content']/header[@class='new-header-v2']/div[@class='header-content-v2 ']/div[@class='main-categories-offers-wrapper']/div[@class='content-categories-offers-wrapper']/div[@class='categories-offers-header']/button[@class='categories-dropdown-button']")))
        boton.click()
    except TimeoutException:
        print("Botón categorías no encontrado")

    list_categories = []

    #Obtener las categorías
    try:
        wait(driver, 8).until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[@id='root']/div[@class='app-content']/header[@class='new-header-v2']/div[@class='header-content-v2 ']/div[@class='main-categories-offers-wrapper']/div[@class='content-categories-offers-wrapper']/div[@class='categories-offers-header']/div[@class='categories-menu-container']/div[@class='categories-menu-dropdown']/ul[@class='categories-menu-list']/li/a")))
        first_level_categories = driver.find_elements("xpath", "/html/body/div[@id='root']/div[@class='app-content']/header[@class='new-header-v2']/div[@class='header-content-v2 ']/div[@class='main-categories-offers-wrapper']/div[@class='content-categories-offers-wrapper']/div[@class='categories-offers-header']/div[@class='categories-menu-container']/div[@class='categories-menu-dropdown']/ul[@class='categories-menu-list']/li/a")
        
        for first, i in zip(first_level_categories, range(len(first_level_categories))):
            
            first_level_category = first.text
            url_first_level_category = first.get_attribute("href")

            ActionChains(driver).move_to_element(first).perform()

            wait(driver, 8).until(ec.presence_of_element_located((By.XPATH, "/html/body/div[@id='root']/div[@class='app-content']/header[@class='new-header-v2']/div[@class='header-content-v2 ']/div[@class='main-categories-offers-wrapper']/div[@class='content-categories-offers-wrapper']/div[@class='categories-offers-header']/div[@class='categories-menu-container']/div[@class='categories-menu-dropdown']/div[@class='sub-categories-container']/ul[@class='sub-categories-wrapper']/li[@class='sub-categories-menu-list']")))
            second_level_categories = driver.find_elements("xpath", "/html/body/div[@id='root']/div[@class='app-content']/header[@class='new-header-v2']/div[@class='header-content-v2 ']/div[@class='main-categories-offers-wrapper']/div[@class='content-categories-offers-wrapper']/div[@class='categories-offers-header']/div[@class='categories-menu-container']/div[@class='categories-menu-dropdown']/div[@class='sub-categories-container']/ul[@class='sub-categories-wrapper']/li[@class='sub-categories-menu-list']")

            for second in second_level_categories:

                try:
                    second_level_category = second.find_elements("xpath", "a[@class='sub-categories-title']")[0].text
                    url_second_level_category = second.find_elements("xpath", "a[@class='sub-categories-title']")[0].get_attribute("href")
        
                except:
                    print("Segundas categorias no encontradas")
                    second_level_category = ''
                    url_second_level_category = ''
                
                try:
                    third_level_categories = second.find_elements("xpath", "a[@class='sub-categories-title-childrens']")

                    for third in third_level_categories:

                        third_level_category = third.text
                        url_third_level_category = third.get_attribute("href")

                        list_categories.append([first_level_category, url_first_level_category, second_level_category, url_second_level_category, third_level_category, url_third_level_category])
                
                except:
                    print("Terceras categorias no encontradas")
                    third_level_category = ''
                    url_third_level_category = ''
                    list_categories.append([first_level_category, url_first_level_category, second_level_category, url_second_level_category, third_level_category, url_third_level_category])
                
                try:
                    third_level_category = second.find_elements("xpath", "a[@class='sub-categories-link-show-all']")[0].text
                    url_third_level_category = second.find_elements("xpath", "a[@class='sub-categories-link-show-all']")[0].get_attribute("href")
                    
                    list_categories.append([first_level_category, url_first_level_category, second_level_category, url_second_level_category, third_level_category, url_third_level_category])
                
                except:
                    print("Ver todos no encontrado")

    except TimeoutException:
        print("Categorias no encontradas")

    driver.quit()

    return(pd.DataFrame(list_categories, columns = ['first_level_category', 'url_first_level_category', 'second_level_category', 'url_second_level_category', 'third_level_category', 'url_third_level_category']), len(list_categories))

def get_pages_category(pais:str, i:str, first:str, second:str, third:str):

    try:

        driver = get_driver()

        total_url_cat = list()

        driver.maximize_window()

        driver.get(i)

        time.sleep(3)

        #Cerrar pop ups
        # try:
        #     boton = wait(driver, 4).until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[@id='root']/div[@class='app-content']/header[@class='new-header-v2']/div[@class='header-content-v2 ']/div[@class='content-menu-wrapper-v2 ']/div[@class='popover-container undefined']/div[@class='popover-select-delivery-method-v2']/div[@class='popover-delivery-info']/button[@class='popover-delivery-close jumbo-icon-new-close']")))
        #     boton.click()
        # except TimeoutException:
        #     print("Pop up no encontrado")

        per_page = 40

        try:

            wait(driver, 16).until(ec.visibility_of_element_located((By.XPATH, "/html/body/div[@id='root']/div[@class='app-content']/div[@class='catalog-page page']/div[@class='container']/div[@class='catalog-page-content']/main[@class='shelf-main']/div[@class='shelf-header']/div[@class='shelf-header-title-wrapper']/div[@class='title-with-bar title-with-bar-medium shelf-header-title']/div[@class='title-with-bar-wrapper']/span[@class='title-with-bar-aditional-text']")))
            count = int(driver.find_elements("xpath", "/html/body/div[@id='root']/div[@class='app-content']/div[@class='catalog-page page']/div[@class='container']/div[@class='catalog-page-content']/main[@class='shelf-main']/div[@class='shelf-header']/div[@class='shelf-header-title-wrapper']/div[@class='title-with-bar title-with-bar-medium shelf-header-title']/div[@class='title-with-bar-wrapper']/span[@class='title-with-bar-aditional-text']")[0].text.replace(' productos', ''))
            n_paginas = int(np.ceil(count/per_page))
            
            if n_paginas>1:
                url_cat_page = [[i + '?page=' + str(j), first, second, third] for j in range(2, n_paginas+1)]
                url_cat_page_2 = [[i + '&page=' + str(j), first, second, third] for j in range(2, n_paginas+1)]
                total_url_cat.append([i, first, second, third])
                total_url_cat.extend(url_cat_page)
                total_url_cat.extend(url_cat_page_2)
            else:
                total_url_cat.append([i, first, second, third])
        
        except:
            total_url_cat.append([i, first, second, third])
            
    except WebDriverException as e:
            print("Error en WebDriver:", e)
    except Exception as e:
            print("Error:", e)
    finally:
            # Asegúrate de cerrar el driver al finalizar
            driver.quit()
    
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

    driver = None
    
    try:
        driver = get_driver()
        driver.maximize_window()
        driver.get(list_pages_category[0])
        time.sleep(3)

            #Cerrar pop ups
        # try:
        #     boton = wait(driver, 4).until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[@id='root']/div[@class='app-content']/header[@class='new-header-v2']/div[@class='header-content-v2 ']/div[@class='content-menu-wrapper-v2 ']/div[@class='popover-container undefined']/div[@class='popover-select-delivery-method-v2']/div[@class='popover-delivery-info']/button[@class='popover-delivery-close jumbo-icon-new-close']")))
        #     boton.click()
        # except TimeoutException:
        #     print("Pop up no encontrado")

        try:

            wait(driver, 4).until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[@id='root']/div[@class='app-content']/div[@class='catalog-page page']/div[@class='container']/div[@class='catalog-page-content']/main[@class='shelf-main']/div[@class='shelf-wrapper']/div[@class='shelf-products-wrap']/div[@class='shelf-content']/div[@class='product-card']/div[@class='product-card-wrap']")))
            sku = driver.find_elements("xpath", "/html/body/div[@id='root']/div[@class='app-content']/div[@class='catalog-page page']/div[@class='container']/div[@class='catalog-page-content']/main[@class='shelf-main']/div[@class='shelf-wrapper']/div[@class='shelf-products-wrap']/div[@class='shelf-content']/div[@class='product-card']/div[@class='product-card-wrap']")

            for j in sku:
                url_category.append(list_pages_category[0])

                wait(j, 4).until(ec.presence_of_element_located((By.XPATH, "a[@class='product-card-name']")))
                name_product.append(j.find_elements("xpath", "a[@class='product-card-name']")[0].text)

                wait(j, 4).until(ec.presence_of_element_located((By.XPATH, "a[@class='product-card-name']")))
                url_product.append(j.find_elements("xpath", "a[@class='product-card-name']")[0].get_attribute("href"))
                
                first_level_category.append(list_pages_category[1])
                second_level_category.append(list_pages_category[2])
                third_level_category.append(list_pages_category[3])

        except TimeoutException:
            print('ERROR: Timeout waiting for element')
        except WebDriverException as e:
            print('ERROR: WebDriverException -', e)
    except Exception as e:
        print('ERROR:', e)
    finally:
        if driver is not None:
            driver.quit()

    # Filtrar filas con valores vacíos
    data = list(zip(url_category, name_product, url_product, first_level_category, second_level_category, third_level_category))
    filtered_data = [row for row in data if all(row)]

    # Crear DataFrame con filas filtradas
    df_url_sku = pd.DataFrame(filtered_data, columns=['url_category', 'name_product', 'url_product', 'first_level_category', 'second_level_category', 'third_level_category'])
    
    return df_url_sku.drop_duplicates()

def get_info_products(pais:str, df_info_category:list):

    with mp.Pool(n) as pool:
        iterable = [(pais, i) for i in df_info_category]
        results = list(tqdm.tqdm(pool.istarmap(get_info_product, iterable), total=len(iterable)))
        pool.close()
        pool.join()
    
    if len(results)==0:
        return(pd.DataFrame(columns=['url_category', 'name_product', 'url_product', 'first_level_category', 'second_level_category', 'third_level_category']))
    elif len(results)>0:
        return(pd.concat(results).drop_duplicates())

def validate_url_cat(total_url_sku:pd.DataFrame, df_categories:pd.DataFrame):

    cat_validate = total_url_sku[['url_category']].drop_duplicates()
    cat_validate['url_down'] = 0

    cat_validate = df_categories.merge(cat_validate.rename(columns={'url_category': 'url_third_level_category'}), how='left')
    cat_validate['url_down'] = cat_validate.url_down.fillna(1)

    return(cat_validate)

def get_scraping_sku(pais_sku:str, url_sku:list):

    # chrome_options = Options()
    # # chrome_options.add_argument("--headless")
    # prefs = {"profile.default_content_setting_values.notifications" : 2}
    # chrome_options.add_experimental_option("prefs",prefs)

    # s = ChromeService(binary_path)
    # driver = webdriver.Chrome(service=s, options=chrome_options)
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

    try:
        driver = get_driver()

        driver.maximize_window()

        driver.get( url_sku[0] )

        #Cerrar pop ups
        # try:
        #     boton = wait(driver, 4).until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[@id='root']/div[@class='app-content']/header[@class='new-header-v2']/div[@class='header-content-v2 ']/div[@class='content-menu-wrapper-v2 ']/div[@class='popover-container undefined']/div[@class='popover-select-delivery-method-v2']/div[@class='popover-delivery-info']/button[@class='popover-delivery-close jumbo-icon-new-close']")))
        #     boton.click()
        # except TimeoutException:
        #     print("Pop up no encontrado")
        try:

            try:
                wait(driver, 64).until(ec.presence_of_element_located( (By.XPATH, './/main[ contains( @class , "product-content" ) ]' ) ))
                df_producto = driver.find_element( By.XPATH, './/main[ contains( @class , "product-content" ) ]' )
            except TimeoutException:
                print("Timeout al intentar encontrar el elemento en la página.")
                
            try:
                id_url = df_producto.find_element( By.XPATH, '//div[ contains( @class,"derecha") ]/.//span[ contains( @class,"product-code") ]' ).text
            except:
                id_url = ''

            try:
                name_url = df_producto.find_element( By.XPATH, '//div[ contains( @class,"derecha") ]/.//h1[ contains( @class ,"product-name") ]' ).text
            except:
                name_url = ''

            try:
                obj_button_description = df_producto.find_element( By.XPATH , '//div[ contains( @class,"izquierda") ]/.//li/span[text()="Descripción"]' )
                obj_button_description.click()
                
                obj_panel_info = df_producto.find_element( By.XPATH , '//div[ contains( @class,"izquierda") ]/.//div[@class="panel-content-style-for-jumbo"]' )
                description_url = obj_panel_info.text

            except:
                description_url = ''

            try:
                atr_sku =  df_producto.find_elements((By.XPATH, "div[@class='product-info']/div[@class='product-info-wrapper']/div[@class='product-aditional-info']/div[@class='aditional-info']/a"))[0].text
            except:
                atr_sku = ''
                
            try:

                normal_price = '' 
                internet_price = ''
                cmr_price = ''
                
                try:
                    normal_price = df_producto.find_elements( By.XPATH, '//div[ contains( @class,"derecha") ]/.//*[@id="scraping-tmp"]' )[0].text
                    #normal_price = normal_price.replace("$","").replace(".","").replace(" ","")
                except:
                    normal_price = ''
                
                try:
                    internet_price = df_producto.find_elements(By.XPATH, '//div[ contains( @class,"derecha") ]/.//*[@id="scraping-tmp"]')[0].text
                    # internet_price = internet_price.replace("$","").replace(".","").replace(" ","")
                except:
                    internet_price = ''

            except:
                normal_price = ''
                internet_price = ''
                cmr_price = ''

            try:
                wait(df_producto, 4).until(ec.presence_of_element_located((By.XPATH, "div[@class='product-info']/div[@class='product-info-wrapper']/div[@class='product-aditional-info']/div[@class='aditional-info']/span[@class='product-code']")))
                id_client_sku = df_producto.find_elements((By.XPATH, "div[@class='product-info']/div[@class='product-info-wrapper']/div[@class='product-aditional-info']/div[@class='aditional-info']/span[@class='product-code']"))[0].text
            except:
                id_client_sku = ''

            try:
                cod_sku = df_producto.find_element( By.XPATH, '//div[ contains( @class,"derecha") ]/.//span[ contains( @class,"product-code") ]' ).text
            except:
                cod_sku = ''

            try:
                images = df_producto.find_elements(By.XPATH, '//div[ contains( @class,"izquierda") ]/.//div[contains( @class,"relative")]/.//img')
                img_url = ''
                px_url = ''

                n_imagenes = len(images)

                for im, i in zip(images, range(n_imagenes)):

                    try:
                        
                        url = im.get_attribute("src")
                        url_img = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        u = urlopen(url_img)
                        raw_data = u.read()
                        u.close()

                        img = Image.open(BytesIO(raw_data))

                        if i == n_imagenes-1:
                            img_url = img_url + url
                            px_url = px_url + str(img.size) 
                            
                        else:
                            img_url = img_url + url + '; '
                            px_url = px_url + str(img.size) + '; '

                    except Exception as error:
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

        except Exception as error:
            
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
        
    except WebDriverException as e:
        print("Error en WebDriver:", e)
    except Exception as e:
        print("Error:", e)
    finally:
        # Asegúrate de cerrar el driver al finalizar
        driver.quit()

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

    df1.to_excel(ruta + f'df_categorias_jumbo.xlsx'.format(actual_date), index=0)

    df2.to_excel(ruta + f'cat_validate_jumbo.xlsx'.format(actual_date), index=0)

    df3.to_excel(ruta + f'results_ws_jumbo.xlsx'.format(actual_date), index=0)

    df4.to_excel(ruta + f'REPORTE_WS_JUMBO.xlsx'.format(actual_date), index=0)

    print(str('['+time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time)))+'],', 'Memory % Used:', psutil.virtual_memory()[2])
    print('')

    #except:
    #    print('Reports not export')