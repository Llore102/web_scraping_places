import pandas as pd
import os
from fuzzywuzzy import process

def crear_diccionario_mapeo(df_supermarket, nivel_supermarket):
    diccionario_mapeo = {}
    for _, fila in df_supermarket.iterrows():
        diccionario_mapeo[fila[nivel_supermarket]] = fila[nivel_supermarket]
    return diccionario_mapeo

def obtener_nombre_supermercado(ruta_archivo):
    return os.path.splitext(os.path.basename(ruta_archivo))[0].split('_')[-1]

def cargar_archivo(ruta_archivo):
    return pd.read_excel(ruta_archivo)

def ajustar_jerarquia_jumbo(categoria):
    # Ajusta la jerarquía de categorías para Jumbo según tu descripción
    categorias_mapping = {
        'Bebidas y Licores': 'Botillería',
        'Carnes y Pescados': 'Carnicería',
        'Congelados': 'Supermercado',
        'Frescos y Lácteos': 'Lácteos',
        'Limpieza y Aseo': 'Limpieza',
        'Panadería y Pastelería': 'Supermercado',
        'Desayunos y Dulces': 'Supermercado',
        'Platos Preparados': 'Supermercado',
        'Mascotas': 'Supermercado',
        # Agrega más categorías según sea necesario
    }

    # Excluye categorías que no existen en Jumbo
    categorias_excluidas = ['Colaciones']

    # Verifica si la categoría está en las categorías excluidas
    if categoria in categorias_excluidas:
        return None
    else:
        # Verifica si la categoría es de tipo cadena antes de aplicar lower()
        if isinstance(categoria, str):
            return categorias_mapping.get(categoria, categoria)
        else:
            return categoria


def ajustar_jerarquia_tottus(categoria):
    # Ajusta la jerarquía de categorías para Tottus según tu descripción
    return 'Despensa'  # Asigna todas las categorías de primer nivel a "Despensa"

def mapear_categorias(df, diccionario_mapeo, nivel_smartbuy, nivel_supermarket):
    df[nivel_supermarket] = df[nivel_smartbuy].apply(lambda x: diccionario_mapeo.get(x, encontrar_mejor_coincidencia(x, diccionario_mapeo.keys())))
    return df

def encontrar_mejor_coincidencia(categoria_smartbuy, categorias_supermarket):
    mejor_coincidencia, puntaje = process.extractOne(categoria_smartbuy, categorias_supermarket)

    # Filtra las coincidencias basándose en la Categoría nivel 1 - Smartbuy
    coincidencias_filtradas = [cat for cat in categorias_supermarket if categoria_smartbuy.lower() in cat.lower()]

    if coincidencias_filtradas:
        mejor_coincidencia, puntaje = process.extractOne(categoria_smartbuy, coincidencias_filtradas)
        # Ajusta el umbral de puntaje para aceptar la coincidencia
        if puntaje >= 80:  # Puedes ajustar este umbral según tus necesidades
            return mejor_coincidencia
    return None

def procesar_supermercado(base_df, supermarket_files):
    result_df = pd.DataFrame(columns=['COD_CAT_N1_SMT', 'Categoría nivel 1 - Smartbuy', 'COD_CAT_N2_SMT', 'Categoría nivel 2 - Smartbuy',
                                       'first_level_category', 'second_level_category', 'third_level_category', 'Supermercado'])

    for file in supermarket_files:
        # Generar ruta completa del archivo con rutas relativas
        file_path = os.path.join(os.path.dirname(__file__), '..', file)
        print(f'Ruta completa del archivo: {file_path}')
        df_supermarket = cargar_archivo(file_path)

        # Crear diccionario de mapeo para cada nivel
        diccionario_mapeo_n1 = crear_diccionario_mapeo(df_supermarket, 'first_level_category')
        diccionario_mapeo_n2 = crear_diccionario_mapeo(df_supermarket, 'second_level_category')
        diccionario_mapeo_n3 = crear_diccionario_mapeo(df_supermarket, 'third_level_category')

        # Mapear las categorías en base al diccionario de mapeo
        base_df = mapear_categorias(base_df, diccionario_mapeo_n1, 'Categoría nivel 1 - Smartbuy', 'first_level_category')
        base_df = mapear_categorias(base_df, diccionario_mapeo_n2, 'Categoría nivel 2 - Smartbuy', 'second_level_category')
        base_df = mapear_categorias(base_df, diccionario_mapeo_n3, 'Categoría nivel 2 - Smartbuy', 'third_level_category')

        supermercado_nombre = obtener_nombre_supermercado(file)
        base_df['Supermercado'] = supermercado_nombre

        # # Ajustar jerarquía específica para Tottus
        # if 'tottus' in supermercado_nombre.lower():
        #     base_df['first_level_category'] = base_df['Categoría nivel 1 - Smartbuy'].apply(ajustar_jerarquia_tottus)
        # Ajustar jerarquía específica para Jumbo
        if 'jumbo' in supermercado_nombre.lower():
            base_df['first_level_category'] = base_df['Categoría nivel 1 - Smartbuy'].apply(ajustar_jerarquia_jumbo)

        result_df = result_df.append(base_df[['COD_CAT_N1_SMT', 'Categoría nivel 1 - Smartbuy', 'COD_CAT_N2_SMT', 'Categoría nivel 2 - Smartbuy',
                                              'first_level_category', 'second_level_category', 'third_level_category', 'Supermercado']], ignore_index=True)

    return result_df

def main():
    ruta_archivo = 'categorías_smartbuy.xlsx'
    script_directory = os.path.dirname(os.path.abspath(__file__))
    ruta_completa = os.path.join(script_directory, ruta_archivo)
    base_df = cargar_archivo(ruta_completa)

    supermarket_files = ['web_scraper_lider/Output/df_categorias_lider.xlsx', 
                         'web_scraper_jumbo/Output/df_categorias_jumbo.xlsx', 
                         ] #'web_scraper_tottus/Output/df_categorias_tottus.xlsx'

    result_df = procesar_supermercado(base_df, supermarket_files)

    result_df = result_df.rename(columns={
        'first_level_category': 'Categoría nivel 1',
        'second_level_category': 'Categoría nivel 2',
        'third_level_category': 'Categoría nivel 3'
    })

    result_df = result_df[['COD_CAT_N1_SMT', 'Categoría nivel 1 - Smartbuy', 'COD_CAT_N2_SMT', 'Categoría nivel 2 - Smartbuy',
                           'Categoría nivel 1', 'Categoría nivel 2', 'Categoría nivel 3', 'Supermercado']]

    pivoted_df = result_df.pivot_table(index=['COD_CAT_N1_SMT', 'Categoría nivel 1 - Smartbuy', 'COD_CAT_N2_SMT', 'Categoría nivel 2 - Smartbuy'],
                                       columns='Supermercado',
                                       values=['Categoría nivel 1', 'Categoría nivel 2', 'Categoría nivel 3'],
                                       aggfunc='first')

    pivoted_df.reset_index(inplace=True)

    pivoted_df.columns = [col[0] if col[1] == '' else f'{col[0]} {col[1]}' for col in pivoted_df.columns]

    pivoted_df.to_excel('homologacion_smartbuy/Categorías_SmartBuy_v7.xlsx', index=False)

