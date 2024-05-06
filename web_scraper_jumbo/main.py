# Librerias
from datetime import date, datetime
import warnings
warnings.filterwarnings('ignore')
import os
# from web_scraper_jumbo.init_scraping import scraping
from web_scraper_jumbo.init_scraping import scraping


#################################################
# Clase de ejecución
#################################################

class Main(object):
    def __init__(self, env_argument_file_name):
        self.v_argument_file_name = env_argument_file_name
        
    def execute(self):
        # Ingresar logica aqui!!
        print("Ejecutando Scraper Jumbo")
        
        scraping()


#################################################
# Main Principal
#################################################
# if __name__ == "__main__":
#     print("path inicinado:")
#     #env_argument_name = os.environ["ENV_ARGUMENTS_NAME"]
#     env_argument_name = "DEVELOPMENT"
#     print("path imicnado env_argument_name = {}".format(env_argument_name))
#     cwl = Main(env_argument_name)
#     cwlout = cwl.execute()
