from chromedriver_py import binary_path

import multiprocessing as mp
# import istarmap  # import to apply patch
import web_scraper_lider.istarmap
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import multiprocessing as mp
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
import ssl
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
import random

import time
import psutil
# from driver.driver import get_driver_with_retry

import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import undetected_chromedriver as uc

import warnings
warnings.filterwarnings('ignore')

n = mp.cpu_count()

try:
   mp.set_start_method('spawn', force=True)
#   print("spawned")
except RuntimeError:
   pass

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/80.0.3987.132 Safari/537.36"}


def get_driver_():
    chrome_options = Options()
    #chrome_options.add_argument(f"user-agent={headers['User-Agent']}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-notifications")

    driver = uc.Chrome(service=ChromeService(binary_path), options=chrome_options)
    # Ofuscar propiedades de Selenium
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_script('navigator.permissions.query = (parameters) => parameters.name === "notifications" ? Promise.resolve({ state: Notification.permission }) : Promise.resolve({ state: "denied" });')

    # driver.maximize_window()
    return driver

def get_driver_aux():
    chrome_options = Options()
    #chrome_options.add_argument(f"user-agent={headers['User-Agent']}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-notifications")

    driver = uc.Chrome(service=ChromeService(binary_path), options=chrome_options)
    # Ofuscar propiedades de Selenium
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_script('navigator.permissions.query = (parameters) => parameters.name === "notifications" ? Promise.resolve({ state: Notification.permission }) : Promise.resolve({ state: "denied" });')

    driver.maximize_window()
    return driver

# def get_driver():
#     chrome_options = Options()
#     prefs = {"profile.default_content_setting_values.notifications" : 2}
#     # chrome_options.add_argument(f"user-agent={headers['User-Agent']}")
#     chrome_options.add_argument("--disable-blink-features=AutomationControlled")
#     chrome_options.add_experimental_option("prefs",prefs)

#     s = ChromeService(binary_path)
#     driver = webdriver.Chrome(service=s, options=chrome_options)

#     driver.maximize_window()
#     return driver

def get_driver():
    chrome_options = Options()
    #chrome_options.add_argument(f"user-agent={headers['User-Agent']}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-notifications")

    driver = uc.Chrome(service=ChromeService(binary_path), options=chrome_options)
    # Ofuscar propiedades de Selenium
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_script('navigator.permissions.query = (parameters) => parameters.name === "notifications" ? Promise.resolve({ state: Notification.permission }) : Promise.resolve({ state: "denied" });')

    driver.maximize_window()
    return driver

# manager = WebDriverManager()

def get_url_lider():
    
    url_lider = 'https://www.lider.cl/supermercado'

    return(url_lider)


def eliminar_captcha(driver):
    try:
        iframe_element = wait(driver, 3).until(
            ec.presence_of_element_located((By.ID, "px-captcha-modal"))
        )
        driver.execute_script("""
            var iframe = arguments[0];
            iframe.parentNode.removeChild(iframe);
        """, iframe_element)
        print("CAPTCHA eliminado")
    except Exception as e:
        print("CAPTCHA no encontrado o no pudo ser eliminado")




def get_info_category():
    list_cat = ['Despensa', 'Carnes y Pescados', 'Frutas y Verduras', 'Frescos y Lácteos',
                'Limpieza y Aseo', 'Bebidas y Licores', 'Congelados', 'Desayunos y Dulces',
                'Colaciones', 'Panadería y Pastelería', 'Platos Preparados', 'Mascotas']
    
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={headers['User-Agent']}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-notifications")

    driver = uc.Chrome(service=ChromeService(binary_path), options=chrome_options)
    # Ofuscar propiedades de Selenium
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_script('navigator.permissions.query = (parameters) => parameters.name === "notifications" ? Promise.resolve({ state: Notification.permission }) : Promise.resolve({ state: "denied" });')

    time.sleep(random.uniform(2, 5))  # Esperar un tiempo aleatorio
    driver.maximize_window()

    driver.get(get_url_lider())
    time.sleep(random.uniform(2, 5)) 
    #driver.save_screenshot('screenshotL.png')
    

    list_categories = []

    try:
        eliminar_captcha(driver)
        # try:
        #     iframe_element = driver.find_element(By.ID, "px-captcha-modal")
        #     driver.execute_script("""
        #         var iframe = arguments[0];
        #         iframe.parentNode.removeChild(iframe);
        #     """, iframe_element)
        # except Exception as es:
        #     print("CAPTCHA")
        #     pass


        wait(driver, 8).until(ec.element_to_be_clickable((By.XPATH, ".//header//button[text()='Categorías']")))
        driver.find_element(By.XPATH, ".//header//button[text()='Categorías']").click()

        wait(driver, 8).until(ec.element_to_be_clickable((By.XPATH, './/div[@data-testid="main-categories-test-id"]')))
        first_level_categories = driver.find_elements("xpath", './/div[contains(@class,"styled__FirstLevelContainer")]/div')


        time.sleep(3)
        for first in first_level_categories:
            first_level_category = first.text
            if first_level_category not in list_cat:
                continue  # Saltar categorías que no están en la lista

            div_desplazable = driver.find_element("xpath", './/div[contains(@class,"styled__FirstLevelContainer")]')
            driver.execute_script( "arguments[0].scrollTop = arguments[1];" , div_desplazable , 0 )
            posicion_y = first.location['y']
            driver.execute_script( "arguments[0].scrollTop = arguments[1];" , div_desplazable , posicion_y )
            first_level_category = first.text
            first.click()
            time.sleep(3)
            wait(driver, 8).until(ec.presence_of_all_elements_located((By.XPATH, './/div[contains(@class,"styled__ThirdLevelSection")]/div/a')))
            second_level_categories = driver.find_elements("xpath", './/div[contains(@class,"styled__ThirdLevelSection")]/div/a')

            for second in second_level_categories:
                second_level_category = second.text
                time.sleep(random.uniform(2, 5))
                url_second_level_category = second.get_attribute("href")
                time.sleep(random.uniform(2, 5))
                eliminar_captcha(driver)
                time.sleep(3)

                second = second.find_element("xpath", "..")  # volvemos al div padre
                element_third_level_categorie = second.find_elements("xpath", "div/a")  # tomamos el primer elemento

                if element_third_level_categorie:
                    subcategory = element_third_level_categorie[0]
                    try:
                        driver_aux = get_driver_aux()

                        time.sleep(random.uniform(1, 2)) 
                        driver_aux.get(subcategory.get_attribute("href"))
                        time.sleep(random.uniform(1, 2))

                        eliminar_captcha(driver_aux)
                        time.sleep(3)

                        wait(driver_aux, 8).until(ec.element_to_be_clickable((By.XPATH, './/ul[@class="sister-categories__list"]')))
                        third_level_categories = driver_aux.find_elements("xpath", './/ul[@class="sister-categories__list"]/li/a')

                        time.sleep(5)
                        for third in third_level_categories:
                            third_level_category = third.text
                            time.sleep(random.uniform(1, 2)) 
                            url_third_level_category = third.get_attribute("href")
                            time.sleep(random.uniform(1, 2)) 
                            eliminar_captcha(driver_aux)
                            
                            list_categories.append([first_level_category, second_level_category, url_second_level_category, third_level_category, url_third_level_category])

                    except TimeoutException:
                        print("Timeout al cargar las subcategorías")
                    finally:
                        driver_aux.close()
                else:
                    list_categories.append([first_level_category, second_level_category, url_second_level_category, None, None])

    except TimeoutException:
        print("Categorías no encontradas")
    finally:
        
        driver.close()

    return pd.DataFrame(list_categories, columns=['first_level_category', 'second_level_category', 'url_second_level_category', 'third_level_category', 'url_third_level_category']), len(list_categories)

def get_pages_category(pais:str, i:str, first:str, second:str, third:str):
    driver = None
    total_url_cat = list()
    try:

        driver = get_driver()

        

        # driver.maximize_window()

        time.sleep(random.uniform(2, 5)) 
        driver.get(i)
        time.sleep(random.uniform(2, 5)) 
        eliminar_captcha(driver)
        

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
            
    except WebDriverException as e:
            print("Error en WebDriver:", e)
    except Exception as e:
            print("Error:", e)
    finally:
        if driver is not None:
            driver.close()
    
    return(total_url_cat)

def get_pages_categories(pais:str, df_categories:pd.DataFrame):

    list_res = list()

    with mp.Pool(4) as pool:
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

        # driver.maximize_window()
        time.sleep(random.uniform(2, 5)) 
        driver.get(list_pages_category[0])
        time.sleep(random.uniform(2, 5)) 
        eliminar_captcha(driver)


        try:

            wait( driver, 64).until(ec.element_to_be_clickable((By.XPATH, './/ul[@class="ais-Hits-list"]//li[@class="ais-Hits-item"]')))
            sku = driver.find_elements("xpath", './/ul[@class="ais-Hits-list"]//li[@class="ais-Hits-item"]')
            
            for producto in sku:
                url_category.append( list_pages_category[0] )
                
                indiv_nombre_product = producto.find_element( "xpath" , './/div[@class="product-card_description-wrapper"]/div/span[2]' ).text
                time.sleep(random.uniform(1, 2))
                indiv_url_producto = producto.find_element("xpath", ".//a").get_attribute("href")
                time.sleep(random.uniform(1, 2))
                eliminar_captcha(driver)


                name_product.append( indiv_nombre_product )
                url_product.append( indiv_url_producto )

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
            driver.close()

    # Filtrar filas con valores vacíos
    data = list(zip(url_category, name_product, url_product, first_level_category, second_level_category, third_level_category))
    filtered_data = [row for row in data if all(row)]

    # Crear DataFrame con filas filtradas
    df_url_sku = pd.DataFrame(filtered_data, columns=['url_category', 'name_product', 'url_product', 'first_level_category', 'second_level_category', 'third_level_category'])
    
    return(df_url_sku.drop_duplicates())

def get_info_products(pais:str, df_info_category:list):

    with mp.Pool(4) as pool:
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
    driver = None

    try:

        driver = get_driver()

        time.sleep(random.uniform(2, 5)) 
        driver.get(url_sku[0])
        time.sleep(random.uniform(2, 5)) 
        eliminar_captcha(driver)


        try:
            try:
                wait(driver, 64).until(ec.presence_of_element_located( (By.XPATH, './/div[@class="product-detail-card__product-detail-container"]' ) ))        
                df_producto = driver.find_element( By.XPATH, './/div[@class="product-detail-card__product-detail-container"]')
            except TimeoutException:
                print("Timeout al intentar encontrar el elemento en la página.")  
            try:
                id_url = df_producto.find_element(By.XPATH, './/span[@class="product-detail-card__product-item-number"]' ).text
                # id_url = id_url.replace("item","").replace(" ","")
            except:
                id_url = ''
            
            try: 
                name_url = df_producto.find_element(By.XPATH, './/h1[@class="product-detail-display-name"]' ).text
            except:
                name_url = ''


            try:
                div_detalles_producto = driver.find_element( By.XPATH , './/div[@data-testid="product-specifications-testid"]' )
                
                obj_button_description = div_detalles_producto.find_element( By.XPATH , '//button/span[text()="Descripción"]' )
                obj_button_description.click()
                
                obj_panel_info = div_detalles_producto.find_element( By.XPATH , './/div/div/div[2]' )
                description_url = obj_panel_info.text

            except:
                description_url = ''
            

            try:
                atr_sku =  "https://www.lider.cl/supermercado/product/sku/829152/koyle-vino-tinto-gran-reserva-cabernet-sauvignon-botella-750-ml"
                patron = r"/sku/(\d+)/"
                atr_sku = re.search(patron, url_sku[0]).group(1)
            except:
                atr_sku = ''
                
            
            try:

                normal_price = '' 
                internet_price = ''
                cmr_price = ''
                
                try:
                    try:
                        normal_price = df_producto.find_element(By.XPATH, './/div[@class="regular-unit-price__price-default"]/span').text
                    except:
                        normal_price = df_producto.find_element(By.XPATH, './/span[@class="pdp-mobile-sales-price"]').text
                    # normal_price = normal_price.replace("$","").replace(".","").replace(" ","")
                except:
                    normal_price = ''

                try:
                    try:
                        internet_price = df_producto.find_element(By.XPATH, './/div[@class="regular-unit-price__price-default"]/span').text
                    except:
                        internet_price = df_producto.find_element(By.XPATH, './/span[@class="pdp-mobile-sales-price"]').text
                    # internet_price = internet_price.replace("$","").replace(".","").replace(" ","")
                except:
                    internet_price = ''

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
                cod_sku = df_producto.find_element(By.XPATH, './/span[@class="product-detail-card__product-item-number"]' ).text
            except:
                cod_sku = ''


            try:
                
                img_url = ''
                px_url = ''

                images = df_producto.find_elements(By.XPATH, './/div[@class="image-preview__figure-wrapper"]/figure')

                n_imagenes = len(images)

                for im, i in zip(images, range(n_imagenes)):

                    try:
                        stile_img = im.get_attribute("style") #la url no esta en figure, sino en su style
                        expre_regular = r'url\("([^"]+)"\)'
                        im_url = re.search( expre_regular , stile_img ).group(1)

                        request_img = Request( im_url , headers={'User-Agent': 'Mozilla/5.0'})
                        
                        u = urlopen( request_img )
                        raw_data = u.read()
                        u.close()
                        
                        img = Image.open(BytesIO(raw_data))
                        
                        if i == n_imagenes-1:
                            img_url = img_url + im_url
                            px_url = px_url + str(img.size) 
                            
                        else:
                            img_url = img_url + im_url + '; '
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

        except Exception as error:
            print("Error..")
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
    
    except TimeoutException:
        print("Timeout al intentar encontrar el elemento en la página.")
    except NoSuchElementException:
        print("Elemento no encontrado en la página.")
    except WebDriverException as e:
        print("Error en WebDriver:", e)
    except Exception as e:
        print("Error:", e)
    finally:
        if driver is not None:
            try:
                driver.close()
            except (WebDriverException, Exception) as e:
                print(f"Error al cerrar el driver: {e}")
        
    return pais_sku, url_sku[0], id_url, name_url, description_url, id_client_sku, cod_sku, first, second, third, category_1, category_2, atr_sku, normal_price, internet_price, cmr_price, image_info_1, image_info_2


# def get_scraping_sku(pais_sku:str, url_sku:list):

#     driver = None

#     try:
#         driver = get_driver_()

#         driver.maximize_window()

#         driver.get( url_sku[0] )
#         try:

#             try:
#                 wait(driver, 64).until(ec.presence_of_element_located( (By.XPATH, './/div[@class="product-detail-card__product-detail-container"]' ) ))        
#                 df_producto = driver.find_element( By.XPATH, './/div[@class="product-detail-card__product-detail-container"]')
#             except TimeoutException:
#                 print("Timeout al intentar encontrar el elemento en la página.")  
#             try:
#                 id_url = df_producto.find_element(By.XPATH, './/span[@class="product-detail-card__product-item-number"]' ).text
#                 # id_url = id_url.replace("item","").replace(" ","")
#             except:
#                 id_url = ''
            
#             try: 
#                 name_url = df_producto.find_element(By.XPATH, './/h1[@class="product-detail-display-name"]' ).text
#             except:
#                 name_url = ''


#             try:
#                 div_detalles_producto = driver.find_element( By.XPATH , './/div[@data-testid="product-specifications-testid"]' )
                
#                 obj_button_description = div_detalles_producto.find_element( By.XPATH , '//button/span[text()="Descripción"]' )
#                 obj_button_description.click()
                
#                 obj_panel_info = div_detalles_producto.find_element( By.XPATH , './/div/div/div[2]' )
#                 description_url = obj_panel_info.text

#             except:
#                 description_url = ''
            

#             try:
#                 atr_sku =  "https://www.lider.cl/supermercado/product/sku/829152/koyle-vino-tinto-gran-reserva-cabernet-sauvignon-botella-750-ml"
#                 patron = r"/sku/(\d+)/"
#                 atr_sku = re.search(patron, url_sku[0]).group(1)
#             except:
#                 atr_sku = ''
                
            
#             try:

#                 normal_price = '' 
#                 internet_price = ''
#                 cmr_price = ''
                
#                 try:
#                     try:
#                         normal_price = df_producto.find_element(By.XPATH, './/div[@class="regular-unit-price__price-default"]/span').text
#                     except:
#                         normal_price = df_producto.find_element(By.XPATH, './/span[@class="pdp-mobile-sales-price"]').text
#                     # normal_price = normal_price.replace("$","").replace(".","").replace(" ","")
#                 except:
#                     normal_price = ''

#                 try:
#                     try:
#                         internet_price = df_producto.find_element(By.XPATH, './/div[@class="regular-unit-price__price-default"]/span').text
#                     except:
#                         internet_price = df_producto.find_element(By.XPATH, './/span[@class="pdp-mobile-sales-price"]').text
#                     # internet_price = internet_price.replace("$","").replace(".","").replace(" ","")
#                 except:
#                     internet_price = ''

#             except:
#                 normal_price = ''
#                 internet_price = ''
#                 cmr_price = ''


#             try:
#                 wait(df_producto, 4).until(ec.presence_of_element_located((By.XPATH, "div[@class='m-auto pb-20 product-detail__card-section']/div[@class='product-detail-page__container']/div[1]/div[1]/div[@class='product-detail-card__product-detail-container']/div[@class='product-detail-card__product']/div[@class='product-detail-card__product-info']/div[@class='product-detail-card__product-detail']")))
#                 id_client_sku = df_producto.find_elements((By.XPATH, "div[@class='m-auto pb-20 product-detail__card-section']/div[@class='product-detail-page__container']/div[1]/div[1]/div[@class='product-detail-card__product-detail-container']/div[@class='product-detail-card__product']/div[@class='product-detail-card__product-info']/div[@class='product-detail-card__product-detail']"))[0].text
#             except:
#                 id_client_sku = ''

#             try:
#                 cod_sku = df_producto.find_element(By.XPATH, './/span[@class="product-detail-card__product-item-number"]' ).text
#             except:
#                 cod_sku = ''


#             try:
                
#                 img_url = ''
#                 px_url = ''

#                 images = df_producto.find_elements(By.XPATH, './/div[@class="image-preview__figure-wrapper"]/figure')

#                 n_imagenes = len(images)

#                 for im, i in zip(images, range(n_imagenes)):

#                     try:
#                         stile_img = im.get_attribute("style") #la url no esta en figure, sino en su style
#                         expre_regular = r'url\("([^"]+)"\)'
#                         im_url = re.search( expre_regular , stile_img ).group(1)

#                         request_img = Request( im_url , headers={'User-Agent': 'Mozilla/5.0'})
                        
#                         u = urlopen( request_img )
#                         raw_data = u.read()
#                         u.close()
                        
#                         img = Image.open(BytesIO(raw_data))
                        
#                         if i == n_imagenes-1:
#                             img_url = img_url + im_url
#                             px_url = px_url + str(img.size) 
                            
#                         else:
#                             img_url = img_url + im_url + '; '
#                             px_url = px_url + str(img.size) + '; '
                        
#                     except:
                        
#                         if i == n_imagenes-1:

#                             img_url = img_url + 'url_image not found'
#                             px_url = px_url + ''

#                         else:

#                             img_url = img_url + 'url_image not found' + '; '
#                             px_url = px_url + '; '
                
#                 image_info_1, image_info_2 = img_url, px_url
            
#             except:
#                 image_info_1,image_info_2 = '',''

#             try:
#                 first = url_sku[1]
#             except:
#                 first = ''
            
#             try:
#                 second = url_sku[2]
#             except:
#                 second = ''
            
#             try:
#                 third = url_sku[3]
#             except:
#                 third = ''
            
#             try:
#                 category_1 = url_sku[1]
#             except:
#                 category_1 = ''

#             try:
#                 category_2 = url_sku[2]
#             except:
#                 category_2 = ''

#         except Exception as error:
#             print("Error..")
#             id_url = ''
#             name_url = ''
#             description_url = ''
#             atr_sku = ''
#             normal_price = ''
#             internet_price = ''
#             cmr_price = ''
#             id_client_sku = ''
#             cod_sku = ''
#             image_info_1 = ''
#             image_info_2 = ''
#             first = ''
#             second = ''
#             third = ''
#             category_1 = ''
#             category_2 = ''
        
#     except TimeoutException:
#         print("Timeout al intentar encontrar el elemento en la página.")
#     except NoSuchElementException:
#         print("Elemento no encontrado en la página.")
#     except WebDriverException as e:
#         print("Error en WebDriver:", e)
#     except Exception as e:
#         print("Error:", e)
#     finally:
#         if driver is not None:
#             try:
#                 driver.quit()
#             except WebDriverException as e:
#                 print("Error al cerrar el driver:", e)

#     return pais_sku, url_sku[0], id_url, name_url, description_url, id_client_sku, cod_sku, first, second, third, category_1, category_2, atr_sku, normal_price, internet_price, cmr_price, image_info_1, image_info_2

def get_df_scraping(pais:str, list_url:list):
    try:
        with mp.Pool(4) as pool:
            iterable = [(pais, li) for li in list_url]
            results = list(tqdm.tqdm(pool.istarmap(get_scraping_sku, iterable), total=len(iterable)))
            pool.close()
            pool.join()
    except Exception as e:
        print(f"Error en get_df_scraping: {e}")
        results = []

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