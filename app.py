# # app.py

# # Librerias
# import warnings
# warnings.filterwarnings('ignore')


# from web_scraper_jumbo.main import Main as JumboMain
# from web_scraper_lider.main import Main as LiderMain
# from web_scraper_tottus.main import Main as TottusMain
# from categories.main import Main as CategoriesMain
# from homologacion_smartbuy.main import Main as Homologacion

# #################################################
# # Clase de ejecución
# #################################################

# class App(object):
#     def __init__(self, env_argument_file_name):
#         self.v_argument_file_name = env_argument_file_name

#     def execute(self):
#         # Ingresar lógica aquí!!
#         print("Ejecutando Secuencia")

#         # Ejecuta cada Main
#         cats = CategoriesMain(self.v_argument_file_name)
#         cats.execute()

#         jumbo = JumboMain(self.v_argument_file_name)
#         jumbo.execute()

#         tottus = TottusMain(self.v_argument_file_name)
#         tottus.execute()

#         lider = LiderMain(self.v_argument_file_name)
#         lider.execute()

        

# #################################################
# # Main Principal
# #################################################

# if __name__ == "__main__":
#     print("path iniciado:")
#     env_argument_name = "DEVELOPMENT"
#     print(f"path iniciado env_argument_name = {env_argument_name}")

#     # Instancia y ejecuta la clase App
#     app = App(env_argument_name)
#     app.execute()


##! secuencial concurent

# import concurrent.futures
# from web_scraper_jumbo.main import Main as JumboMain
# from web_scraper_lider.main import Main as LiderMain
# from web_scraper_tottus.main import Main as TottusMain
# from categories.main import Main as CategoriesMain
# from homologacion_smartbuy.main import Main as Homologacion

# class App(object):
#     def __init__(self, env_argument_file_name):
#         self.v_argument_file_name = env_argument_file_name

#     def execute(self):
#         print("Ejecutando Secuencia")

#         # Ejecutar cada scraper de manera secuencial
#         with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
#             cats = CategoriesMain(self.v_argument_file_name)
#             future_cats = executor.submit(cats.execute)
#             future_cats.result()
            

#             lider = LiderMain(self.v_argument_file_name)
#             future_lider = executor.submit(lider.execute)
#             future_lider.result()

#             jumbo = JumboMain(self.v_argument_file_name)
#             future_jumbo = executor.submit(jumbo.execute)
#             future_jumbo.result()

#             tottus = TottusMain(self.v_argument_file_name)
#             future_tottus = executor.submit(tottus.execute)
#             future_tottus.result()

            

#         # Ejecutar Homologacion
#         homologacion = Homologacion(self.v_argument_file_name)
#         homologacion.execute()

# if __name__ == "__main__":
#     print("path iniciado:")
#     env_argument_name = "DEVELOPMENT"
#     print(f"path iniciado env_argument_name = {env_argument_name}")

#     # Instancia la clase App
#     app = App(env_argument_name)

#     # Ejecuta los scrapers de manera secuencial utilizando ThreadPoolExecutor
#     app.execute()
    

# import concurrent.futures
# from web_scraper_jumbo.main import Main as JumboMain
# from web_scraper_lider.main import Main as LiderMain
# from web_scraper_tottus.main import Main as TottusMain
# from categories.main import Main as CategoriesMain
# from homologacion_smartbuy.main import Main as Homologacion
# class App(object):
#     def __init__(self, env_argument_file_name):
#         self.v_argument_file_name = env_argument_file_name

#     def execute(self):
#         print("Ejecutando Secuencia")

        # # Ejecutar cada scraper de manera secuencial
        # cats = CategoriesMain(self.v_argument_file_name)
        # cats.execute()

#         jumbo = JumboMain(self.v_argument_file_name)
#         jumbo.execute()

#         tottus = TottusMain(self.v_argument_file_name)
#         tottus.execute()

#         lider = LiderMain(self.v_argument_file_name)
#         lider.execute()

#         # Ejecutar Homologacion
#         # homologacion = Homologacion(self.v_argument_file_name)
#         # homologacion.execute()

#     def execute_parallel(self, scraper_class):
#         instance = scraper_class(self.v_argument_file_name)
#         instance.execute()

# if __name__ == "__main__":
#     print("path iniciado:")
#     env_argument_name = "DEVELOPMENT"
#     print(f"path iniciado env_argument_name = {env_argument_name}")

#     # Instancia la clase App
#     app = App(env_argument_name)

#     # Ejecuta los scrapers en paralelo utilizando ThreadPoolExecutor
#     with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
#         futures = [executor.submit(app.execute_parallel, scraper_class) for scraper_class in [JumboMain, LiderMain, TottusMain]]

#         # Esperar a que todos los hilos hayan terminado
#         for future in futures:
#             future.result()


###!!! paralelo


import concurrent.futures
from web_scraper_jumbo.main import Main as JumboMain
from web_scraper_lider.main import Main as LiderMain
from web_scraper_tottus.main import Main as TottusMain
from homologacion_smartbuy.main import Main as Homologacion
from selenium.common.exceptions import WebDriverException

class App(object):
    def __init__(self, env_argument_file_name):
        self.v_argument_file_name = env_argument_file_name

    def execute(self):
        print("Ejecutando Secuencia")

        

        # Crear instancias de cada scraper
        lider = LiderMain(self.v_argument_file_name)
        jumbo = JumboMain(self.v_argument_file_name)
        tottus = TottusMain(self.v_argument_file_name)

        # Ejecutar cada scraper en paralelo
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(scraper.execute) for scraper in [ jumbo]]

            # Esperar a que todas las ejecuciones terminen
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except WebDriverException as e:
                    print(f"Excepción durante la ejecución del WebDriver: {e}")

        # Ejecutar Homologacion después de que todos los futuros hayan terminado
        homologacion = Homologacion(self.v_argument_file_name)
        homologacion.execute()

if __name__ == "__main__":
    print("path iniciado:")
    env_argument_name = "DEVELOPMENT"
    print(f"path iniciado env_argument_name = {env_argument_name}")

    # Instancia la clase App
    app = App(env_argument_name)

    # Ejecuta los scrapers de manera secuencial y paralela, y luego Homologacion
    app.execute()
