#################################################
# Paquetes y librerías Python
#################################################

import os
import errno

import warnings
warnings.filterwarnings('ignore')

#################################################
# Python Librerias reutilizables
#################################################

# import utils_scraping as st
from web_scraper_lider import utils_scraping as st

from datetime import datetime
import pandas as pd

#################################################
# Parámetros
#################################################

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
    print('Se extraen las URL de las categorías de Lider...')

    df_categories, n_categories = st.get_info_category()

    df_categories.to_excel(ruta + f'df_categorias_lider.xlsx'.format(actual_date), index=0)

    df_categories.to_excel(ruta_actual + f'df_categorias_lider'+'_'+actual_date+'.xlsx'.format(actual_date), index=0)

    print('')
    print('Total de categorias Lider: ' + str(n_categories))

    print('')
    print('Categorias primer nivel Lider:')

    categories = df_categories['first_level_category'].unique()

    #categories = categories[8:]

    df_cat_smartbuy = pd.read_excel(ruta + "../../homologacion_smartbuy/Categorías_SmartBuy_v7.xlsx")

    categories = df_categories[df_categories['first_level_category'].isin(df_cat_smartbuy['Categoría nivel 1 lider'].unique())]['first_level_category'].unique()

    print(categories)

    print('')
    for cat in categories:

        cat1 = cat.lower().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace(' ','_')

        print('Scraping de Categorias Lider'+str(cat)+':')

        #df_categories_1 = df_categories[(df_categories['third_level_category']=='ver todo') & (df_categories['first_level_category']==cat)]
        df_categories_1 = df_categories[(df_categories['first_level_category']==cat)]

        print('')
        print('Se extraen los totales de páginas por categoría de Lider...')

        total_url_cat = st.get_pages_categories(pais, df_categories_1)  # Cambiar a df_categories_1.iloc[:5,:] para pruebas

        pd.DataFrame(total_url_cat, columns=['url', 'first_category', 'second_category', 'third_category']).to_excel(ruta + f'df_pages_categories_'+str(cat1)+'_lider.xlsx'.format(actual_date), index=0)

        pd.DataFrame(total_url_cat, columns=['url', 'first_category', 'second_category', 'third_category']).to_excel(ruta_actual + f'df_pages_categories_'+str(cat1)+'_lider'+'_'+actual_date+'.xlsx'.format(actual_date), index=0)

        ###- Extracción URL Producto

        print('')
        print('Se extraen las URL de los productos de Lider...')

        total_url_sku = st.get_info_products(pais,total_url_cat)

        total_url_sku.to_excel(ruta + f'df_info_products_'+str(cat1)+'_lider.xlsx'.format(actual_date), index=0)

        total_url_sku.to_excel(ruta_actual + f'df_info_products_'+str(cat1)+'_lider'+'_'+actual_date+'.xlsx'.format(actual_date), index=0)
        
        ###- Total de categorías validas

        #print('')
        #print('Se genera el reporte de validación de categorías...')

        #cat_validate = st.validate_url_cat(total_url_sku,df_categories)

        #cat_validate.to_excel(ruta + f'cat_validate_lider.xlsx'.format(actual_date), index=0)

        #print('')
        #print('Distribución de categorías')
        #print('')
        #print(cat_validate.url_down.value_counts(normalize=True).reset_index())

        ###- Extracción de atributos por producto

        url_sku_list = total_url_sku[['url_product', 'first_level_category', 'second_level_category', 'third_level_category']].values.tolist()  # agregar [0:5] al final para pruebas
        #print(url_sku_list)

        print('')
        print('Se obtiene información de Lider: ' + str(len(url_sku_list)) + ' SKU')

        print('')
        print('Se extraen los atributos de cada producto de Lider...')
        print('')

        df_producto_t = st.get_df_scraping(pais, url_sku_list)

        df_producto_t.to_excel(ruta + f'results_ws_'+str(cat1)+'_lider.xlsx'.format(actual_date), index=0)

        df_producto_t.to_excel(ruta_actual + f'results_ws_'+str(cat1)+'_lider'+'_'+actual_date+'.xlsx'.format(actual_date), index=0)


        #################################################
        # Reporte ADMINISTRACION WEB
        #################################################

        df_report = st.total_report(pais,df_producto_t)

        df_report.to_excel(ruta + f'REPORTE_WS_'+str(cat1)+'_LIDER.xlsx'.format(actual_date), index=0)

        df_report.to_excel(ruta_actual + f'REPORTE_WS_'+str(cat1)+'_LIDER'+'_'+actual_date+'.xlsx'.format(actual_date), index=0)


        #################################################
        # Carga a STORAGE
        #################################################

        #st.export_reports(pais, ruta, df_categories,cat_validate,df_producto_t,df_report)