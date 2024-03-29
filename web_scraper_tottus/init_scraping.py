#################################################
# Paquetes y librerías Python
#################################################

import os
import errno
import re

import warnings
warnings.filterwarnings('ignore')

#################################################
# Python Librerias reutilizables
#################################################

# import utils_scraping as st
from web_scraper_tottus import utils_scraping as st
from datetime import datetime
import pandas as pd
import string
import unicodedata

#################################################
# Parámetros
#################################################
max_length = 32767  
def remove_non_ascii(text):
    cleaned_text = ''.join(char if unicodedata.category(char)[0] == 'L' or char.isdigit() or char.isspace() else ' ' for char in text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text) 
    return cleaned_text


pais = 'CL'
actual_date = str(datetime.now())[0:10].replace('-','')
ruta = os.path.dirname(os.path.abspath(__file__)) + '/Output/'
ruta_actual = ruta+actual_date+'/'

try:
    os.mkdir(ruta_actual)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise



def scraping():
    
    #################################################
    # Ejecución Web Scraping
    #################################################

    ###- Extracción URL Categorías

    print('')
    print('Se extraen las URL de las categorías de Tottus...')

    df_categories, n_categories = st.get_info_category(pais)

    df_categories.to_excel(ruta + f'df_categorias_tottus.xlsx'.format(actual_date), index=0)

    df_categories.to_excel(ruta_actual + f'df_categorias_tottus'+'_'+actual_date+'.xlsx'.format(actual_date), index=0)

    print('')
    print('Total de categorias Tottus: ' + str(n_categories))

    print('')
    print('Categorias primer nivel Tottus:')

    categories = df_categories['first_level_category'].unique()

    #categories = categories[1:6]

    print(categories)

    ###- Total de páginas por categoría

    print('')
    print('Se extraen los totales de páginas por categoría de Tottus...')

    total_url_cat = st.get_pages_categories(pais, df_categories)  # Cambiar a df_categories.iloc[:5,:] para pruebas

    ###- Extracción URL Producto

    print('')
    print('Se extraen las URL de los productosde Tottus...')

    total_url_sku = st.get_info_products(pais,total_url_cat)

    ###- Total de categorías validas

    print('')
    print('Se genera el reporte de validación de categorías de Tottus...')

    cat_validate = st.validate_url_cat(total_url_sku,df_categories)

    cat_validate.to_excel(ruta + f'cat_validate_tottus.xlsx'.format(actual_date), index=0)

    cat_validate.to_excel(ruta_actual + f'cat_validate_tottus'+'_'+actual_date+'.xlsx'.format(actual_date), index=0)

    print('')
    print('Distribución de categorías Tottus')
    print('')
    print(cat_validate.url_down.value_counts(normalize=True).reset_index())

    ###- Extracción de atributos por producto

    url_sku_list = total_url_sku[['url_product', 'first_level_category', 'second_level_category', 'third_level_category']].values.tolist()  # agregar [0:5] al final para pruebas
    #print(url_sku_list)

    print('')
    print('Se obtiene información de Tottus' + str(len(url_sku_list)) + ' SKU')

    print('')
    print('Se extraen los atributos de cada producto de Tottus...')
    print('')

    df_producto_t = st.get_df_scraping(pais, url_sku_list)

    # Nombre de la columna que deseas limpiar
    columna_a_limpiar = 'attributes'

    # Aplicar la limpieza solo a la columna específica
    df_producto_t[columna_a_limpiar] = df_producto_t[columna_a_limpiar].apply(lambda x: remove_non_ascii(str(x))[:max_length])


    df_producto_t.to_excel(ruta + f'results_ws_tottus.xlsx'.format(actual_date), index=0)

    df_producto_t.to_excel(ruta_actual + f'results_ws_tottus'+'_'+actual_date+'.xlsx'.format(actual_date), index=0)


    #################################################
    # Reporte ADMINISTRACION WEB
    #################################################

    df_report = st.total_report(pais,df_producto_t)

    df_report.to_excel(ruta + f'REPORTE_WS_TOTTUS.xlsx'.format(actual_date), index=0)

    df_report.to_excel(ruta_actual + f'REPORTE_WS_TOTTUS'+'_'+actual_date+'.xlsx'.format(actual_date), index=0)


    #################################################
    # Carga a STORAGE
    #################################################

    st.export_reports(pais, ruta,
                                df_categories,cat_validate,df_producto_t,df_report)



