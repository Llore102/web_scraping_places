# Librerias
import warnings
warnings.filterwarnings('ignore')

from .cats import main


#################################################
# Clase de ejecución
#################################################

class Main(object):
    def __init__(self, env_argument_file_name):
        self.v_argument_file_name = env_argument_file_name
        
    def execute(self):
        # Ingresar logica aqui!!
        print("Ejecutando Valid Cats")
        
        main()


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
