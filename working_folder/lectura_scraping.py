# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 16:30:40 2020

@author: iv
"""


import os
import sys
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup


### SYSTEM DATA ###
if '__file__' in locals():
    if locals()['__file__'] == '<input>':
        wd = os.path.split(os.path.realpath(__file__))[0]
        wd += '/'
        sys.path.append(wd)
        os.chdir(wd)
        del locals()['__file__']
    else:
        wd = os.path.dirname(__file__)
        wd += '/'
        sys.path.append(wd)
        os.chdir(wd)
else:
    wd = os.path.abspath("./Documents/Repositorio_Iv/premios_loteria/working_folder/")
    wd += '/'
    sys.path.append(wd)

def loteria_scraping():
    '''
    La ejecucion seria "python lectura_scraping.py"
    Este primer script scrapea la pagina de loterias y apuestas del estado
    y escribe la tabla resultante de premios en 
    los .csv correspondientes en la carpeta "working_folder"
    '''

    ### Conexion URL ###
    #
    # url = 'https://www.loteriasyapuestas.es/es/loteria-nacional/tablas-y-alambres?drawId=1113309102' ## 2020
    # url = 'https://www.loteriasyapuestas.es/es/loteria-nacional/tablas-y-alambres?drawId=1149809102' ## 2021
    url = 'https://www.loteriasyapuestas.es/es/loteria-nacional/tablas-y-alambres.provisional'  ## 2021

    html_doc = rq.get(url)
    statusCode = html_doc.status_code
    if statusCode == 200:
        soup = BeautifulSoup(html_doc.text, 'html.parser')
        # print(soup.prettify())
        listado = []
        
        entradas = soup.find_all('tr', {'class': 'par'})
        for entrada in entradas:
            numero = entrada.find('p').getText()
            premio = entrada.find('span').getText()
            listado.append([numero.strip(), premio.strip()])
            
        entradas = soup.find_all('tr', {'class': 'impar'})
        for entrada in entradas:
            numero = entrada.find('p').getText()
            premio = entrada.find('span').getText()
            listado.append([numero.strip(), premio.strip()])
            
        df_listado = pd.DataFrame(listado, columns=['numero', 'premio']) 
        df_listado = df_listado[df_listado['numero'] != '--']
        # df_listado['numero'] = df_listado['numero'].astype(str)
        df_listado.to_csv(f'{wd}listado_loteria.csv', index=False, quotechar='"')
        print(f'Lectura correcta, los .csv están en el working_folder: {wd}')
    else:
        print('## No existe la pagina err400 ##')
        pass
          
    return


if __name__ == '__main__':
    loteria_scraping()

## END ##