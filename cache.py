import os
import shutil

def remove_pycache(base_dir):
    # Recorre todos los directorios y subdirectorios
    for root, dirs, files in os.walk(base_dir):
        # Verifica si existe un directorio llamado __pycache__
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            print(f"Eliminando: {pycache_path}")
            # Elimina el directorio __pycache__ y su contenido
            shutil.rmtree(pycache_path)

if __name__ == "__main__":
    # Especifica el directorio base desde donde deseas eliminar los __pycache__
    base_directory = 'C:/Users/llore/Jupyter/Scrapers/smartbuy'  # Cambia 'ruta/a/tu/carpeta' por la ruta de tu directorio base
    
    # Llama a la función para eliminar los __pycache__
    remove_pycache(base_directory)
