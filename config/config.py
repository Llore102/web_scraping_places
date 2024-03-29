from pymongo import MongoClient
from dotenv import load_dotenv, dotenv_values


#DB local
#conn = MongoClient().Inventory


# Cargar las variables de entorno desde el archivo .env
load_dotenv()
env_vars = dotenv_values()

# Obtener la URL de conexión de MongoDB desde las variables de entorno
mongo_uri = env_vars["MONGO_URI"]

db_name = "Smartbuy"


# Conectarse a la base de datos
client = MongoClient(mongo_uri)
conn = client[db_name]

