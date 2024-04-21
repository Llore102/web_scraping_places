
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service

# # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/79.0.3945.117 Safari/537.36"}

# def get_driver_with_retry():
#     chrome_options = webdriver.ChromeOptions()
#     # chrome_options.add_argument(f"user-agent={headers['User-Agent']}")
#     chrome_options.add_argument("--window-size=1920,1080")  # Establecer el tamaño de la ventana
#     chrome_options.add_argument("--start-maximized")  # Maximizar la ventana al abrirse
#     chrome_options.add_argument("--disable-infobars")  # Deshabilitar la barra de información
#     chrome_options.add_argument("--disable-extensions")  # Deshabilitar las extensiones del navegador
#     # chrome_options.add_argument("--disable-gpu")  # Deshabilitar la aceleración de GPU
#     # chrome_options.add_argument("--disable-dev-shm-usage")  # Deshabilitar el uso compartido de memoria
#     chrome_options.add_argument("--no-sandbox") 
#     chrome_options.add_argument("--headless")  # Opcional: para ejecución en segundo plano

#             # Instanciar el controlador de Chrome y pasar las opciones como argumento
#     selenium_service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=selenium_service, options=chrome_options)
#     driver.maximize_window()
#     return driver


# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service

# # Define una variable global para almacenar la instancia del servicio
# chrome_service_instance = None

# def get_driver_with_retry():
#     global chrome_service_instance
    
#     # Configuración de opciones para Chrome
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument("--window-size=1920,1080")  # Establecer el tamaño de la ventana
#     chrome_options.add_argument("--start-maximized")  # Maximizar la ventana al abrirse
#     chrome_options.add_argument("--disable-infobars")  # Deshabilitar la barra de información
#     chrome_options.add_argument("--disable-extensions")  # Deshabilitar las extensiones del navegador
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--headless")  # Opcional: para ejecución en segundo plano

#     # Verifica si el servicio ya ha sido creado
#     if chrome_service_instance is None:
#         # Instancia un nuevo servicio si no existe
#         selenium_service = Service(ChromeDriverManager().install())
#         chrome_service_instance = selenium_service
#     else:
#         # Reutiliza el servicio existente
#         selenium_service = chrome_service_instance

#     # Crear una instancia de Chrome WebDriver con el servicio existente
#     driver = webdriver.Chrome(service=selenium_service, options=chrome_options)
#     return driver


# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# import time

# # Define una variable global para almacenar la instancia del servicio
# chrome_service_instance = None

# def get_driver_with_retry(retries=3, delay=2):
#     global chrome_service_instance
    
#     # Configuración de opciones para Chrome
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument("--window-size=1920,1080")
#     chrome_options.add_argument("--start-maximized")
#     chrome_options.add_argument("--disable-infobars")
#     chrome_options.add_argument("--disable-extensions")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--headless")  # Ejecución en segundo plano

#     # Verifica si el servicio ya ha sido creado
#     if chrome_service_instance is None:
#         # Crear un nuevo servicio si no existe
#         selenium_service = Service(ChromeDriverManager().install())
#         chrome_service_instance = selenium_service
#     else:
#         # Reutilizar el servicio existente
#         selenium_service = chrome_service_instance

#     for attempt in range(retries):
#         try:
#             # Crear una instancia de Chrome WebDriver con el servicio existente
#             driver = webdriver.Chrome(service=selenium_service, options=chrome_options)
#             return driver
#         except Exception as e:
#             print(f"Intento {attempt + 1} fallido: {e}")
#             if attempt < retries - 1:
#                 # Espera un tiempo antes de reintentar si hay más intentos restantes
#                 time.sleep(delay)
#             else:
#                 # Si se alcanzan los intentos máximos, informar el error
#                 print("Máximo de intentos alcanzado, no se pudo crear el driver.")
#                 raise

# # Importante: No olvides cerrar el driver cuando termines de usarlo.


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_driver_with_retry(retries=3, delay=2):
    # Configuración de opciones para Chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")  # Ejecución en segundo plano

    for attempt in range(retries):
        try:
            # Crear un nuevo servicio de Chrome para cada intento
            selenium_service = Service(ChromeDriverManager().install())
            
            # Crear una instancia de Chrome WebDriver con el servicio recién creado
            driver = webdriver.Chrome(service=selenium_service, options=chrome_options)
            return driver
        except Exception as e:
            print(f"Intento {attempt + 1} fallido: {e}")
            if attempt < retries - 1:
                # Esperar un tiempo antes de reintentar si hay más intentos restantes
                time.sleep(delay)
            else:
                # Si se alcanzan los intentos máximos, informar el error
                print("Máximo de intentos alcanzado, no se pudo crear el driver.")
                raise

# Importante: No olvides cerrar el driver cuando termines de usarlo.
