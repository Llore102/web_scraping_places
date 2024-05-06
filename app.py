# app.py

# Librerias
import warnings
warnings.filterwarnings('ignore')


from web_scraper_jumbo.main import Main as JumboMain
from web_scraper_lider.main import Main as LiderMain
from web_scraper_tottus.main import Main as TottusMain
from categories.main import Main as CategoriesMain
from homologacion_smartbuy.main import Main as HomologacionMain

#################################################
# Clase de ejecución
#################################################

class App(object):
    def __init__(self, env_argument_file_name):
        self.v_argument_file_name = env_argument_file_name

    def execute(self):
        # Ingresar lógica aquí!!
        print("Ejecutando Secuencia")

        # # # Ejecuta cada Main
        # cats = CategoriesMain(self.v_argument_file_name)
        # cats.execute()
        jumbo = JumboMain(self.v_argument_file_name)
        jumbo.execute()
        # lider = LiderMain(self.v_argument_file_name)
        # lider.execute()
        


        


        # tottus = TottusMain(self.v_argument_file_name)
        # tottus.execute()

        homologscion = HomologacionMain(self.v_argument_file_name)
        homologscion.execute()


        

#################################################
# Main Principal
#################################################

if __name__ == "__main__":
    print("path iniciado:")
    env_argument_name = "DEVELOPMENT"
    print(f"path iniciado env_argument_name = {env_argument_name}")

    # Instancia y ejecuta la clase App
    app = App(env_argument_name)
    app.execute()




# # Librerias
# import warnings
# from threading import Thread
# warnings.filterwarnings('ignore')

# from web_scraper_jumbo.main import Main as JumboMain
# from web_scraper_lider.main import Main as LiderMain
# from web_scraper_tottus.main import Main as TottusMain
# from categories.main import Main as CategoriesMain
# from homologacion_smartbuy.main import Main as HomologacionMain

# #################################################
# # Clase de ejecución
# #################################################

# class App(object):
#     def __init__(self, env_argument_file_name):
#         self.v_argument_file_name = env_argument_file_name

#     def execute(self):
#         # Ingresar lógica aquí!!
#         print("Ejecutando Secuencia")

#         # Ejecuta primero CategoriesMain
#         # cats = CategoriesMain(self.v_argument_file_name)
#         # cats.execute()

#         # Ejecuta en paralelo los scrapers
#         threads = []

#         lider = LiderMain(self.v_argument_file_name)
#         lider_thread = Thread(target=lider.execute)
#         threads.append(lider_thread)

#         jumbo = JumboMain(self.v_argument_file_name)
#         jumbo_thread = Thread(target=jumbo.execute)
#         threads.append(jumbo_thread)

#         # tottus = TottusMain(self.v_argument_file_name)
#         # tottus_thread = Thread(target=tottus.execute)
#         # threads.append(tottus_thread)

#         # Iniciar los threads en paralelo
#         for thread in threads:
#             thread.start()

#         # Esperar a que todos los threads finalicen
#         for thread in threads:
#             thread.join()

#         # Ejecuta HomologacionMain después de que terminen los scrapers
#         homologscion = HomologacionMain(self.v_argument_file_name)
#         homologscion.execute()

# # Main Principal
# if __name__ == "__main__":
#     print("path iniciado:")
#     env_argument_name = "DEVELOPMENT"
#     print(f"path iniciado env_argument_name = {env_argument_name}")

#     # Instancia y ejecuta la clase App
#     app = App(env_argument_name)
#     app.execute()



# import warnings
# from threading import Thread
# warnings.filterwarnings('ignore')

# from web_scraper_jumbo.main import Main as JumboMain
# from web_scraper_lider.main import Main as LiderMain
# from web_scraper_tottus.main import Main as TottusMain
# from categories.main import Main as CategoriesMain
# from homologacion_smartbuy.main import Main as HomologacionMain

# class App(object):
#     def __init__(self, env_argument_file_name):
#         self.v_argument_file_name = env_argument_file_name

#     def execute(self):
#         print("Ejecutando Secuencia")

#         # Define las funciones para ejecutar en subprocesos
#         # def execute_categories():
#         #     cats = CategoriesMain(self.v_argument_file_name)
#         #     cats.execute()
#         def execute_lider():
#             lider = LiderMain(self.v_argument_file_name)
#             lider.execute()

#         def execute_jumbo():
#             jumbo = JumboMain(self.v_argument_file_name)
#             jumbo.execute()

#         def execute_homologacion():
#             homologscion = HomologacionMain(self.v_argument_file_name)
#             homologscion.execute()

#         # Crea y ejecuta subprocesos para cada tarea
#         # categories_thread = Thread(target=execute_categories)
#         lider_thread = Thread(target=execute_lider)
#         jumbo_thread = Thread(target=execute_jumbo)
#         homologacion_thread = Thread(target=execute_homologacion)

#         # categories_thread.start()
#         # categories_thread.join()  # Espera a que se complete la ejecución de categorías antes de iniciar Jumbo
#         lider_thread.start()
#         lider_thread.join()  # Espera a que se complete la ejecución de Lider antes de iniciar Homologación
        
#         jumbo_thread.start()
#         jumbo_thread.join()  # Espera a que se complete la ejecución de Jumbo antes de iniciar Lider
        
#         homologacion_thread.start()
#         homologacion_thread.join()  # Espera a que se complete la ejecución de Homologación

# if __name__ == "__main__":
#     print("Path iniciado:")
#     env_argument_name = "DEVELOPMENT"
#     print(f"Path iniciado env_argument_name = {env_argument_name}")

#     app = App(env_argument_name)
#     app.execute()
