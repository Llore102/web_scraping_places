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


        lider = LiderMain(self.v_argument_file_name)
        lider.execute()
        jumbo = JumboMain(self.v_argument_file_name)
        jumbo.execute()


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



# #############################3
# # Librerias
# # Librerias
# import warnings
# warnings.filterwarnings('ignore')
# from web_scraper_jumbo.main import Main as JumboMain
# from web_scraper_lider.main import Main as LiderMain
# from web_scraper_tottus.main import Main as TottusMain
# from categories.main import Main as CategoriesMain
# from homologacion_smartbuy.main import Main as HomologacionMain
# import threading

# ################################################
# # Clase de ejecución
# ################################################
# class App(object):
#     def __init__(self, env_argument_file_name):
#         self.v_argument_file_name = env_argument_file_name
#         self.lider_finished = threading.Event()
#         self.jumbo_finished = threading.Event()

#     def execute(self):
#         print("Ejecutando Secuencia")

#         # Ejecutar CategoriesMain
#         # cats = CategoriesMain(self.v_argument_file_name)
#         # cats.execute()

#         # Crear hilos para ejecutar LiderMain y JumboMain en paralelo
#         lider_thread = threading.Thread(target=self.execute_lider)
#         jumbo_thread = threading.Thread(target=self.execute_jumbo)

#         # Iniciar hilos
#         lider_thread.start()
#         jumbo_thread.start()

#         # Esperar a que ambos hilos terminen
#         self.lider_finished.wait()
#         self.jumbo_finished.wait()

#         # Ejecutar HomologacionMain después de que los hilos terminen
#         homologacion = HomologacionMain(self.v_argument_file_name)
#         homologacion.execute()

#     def execute_lider(self):
#         lider = LiderMain(self.v_argument_file_name)
#         lider.execute()
#         # Monitorear el progreso del scraper LiderMain
#         while not lider.is_complete():
#             # Esperar un tiempo o realizar otras tareas
#             pass
#         self.lider_finished.set()  # Indicar que el hilo ha terminado

#     def execute_jumbo(self):
#         jumbo = JumboMain(self.v_argument_file_name)
#         jumbo.execute()
#         # Monitorear el progreso del scraper JumboMain
#         while not jumbo.is_complete():
#             # Esperar un tiempo o realizar otras tareas
#             pass
#         self.jumbo_finished.set()  # Indicar que el hilo ha terminado

# ################################################
# # Main Principal
# ################################################
# if __name__ == "__main__":
#     print("path iniciado:")
#     env_argument_name = "DEVELOPMENT"
#     print(f"path iniciado env_argument_name = {env_argument_name}")
#     app = App(env_argument_name)
#     app.execute()