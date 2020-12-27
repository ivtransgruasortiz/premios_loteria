# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 16:30:40 2020

@author: iv
"""

###############################
## SELECT PLATFORM: ##########
#############################    
###-- WINDOWS OR LINUX --###
###########################
import sys
if sys.platform == 'win32':
    path = ''
    print ('\n#### Windows System ####')
    system = sys.platform
else:
    path = ''
    print ('\n#### Linux System ####')
    system = sys.platform

print ('#####################################')
print ('#####################################')
print ('\n### Importing Libraries... ###')

import os
import sys
import pandas as pd
import requests as rq
import json
from bs4 import BeautifulSoup

#import numpy as np
#import csv
#import time
#import datetime
#import pylab as pl
#import seaborn as sns
#import matplotlib as mpl
#import matplotlib.pyplot as plt
#import lxml
#import urllib
#import statsmodels
#import sklearn
#import nltk
#import scipy
#import tables
#import json, hmac, hashlib, time, requests, base64
#from requests.auth import AuthBase
#import datetime as dt
#import timeit
#import math
#from scipy import stats
#import base64
#import pyspark
#from pyspark import SparkConf, SparkContext
#from pyspark.sql import SparkSession

if '__file__' in locals():
    wd = os.path.dirname(__file__)
    sys.path.append(wd)
else:
    wd = os.path.abspath("./Documents/Repositorio_Iv/premios_loteria/working_folder/")
    wd = wd + '/'
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
    url = 'https://www.loteriasyapuestas.es/es/loteria-nacional/tablas-y-alambres?drawId=1113309102'
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
            listado.append([numero, premio])
            
        entradas = soup.find_all('tr', {'class': 'impar'})
        for entrada in entradas:
            numero = entrada.find('p').getText()
            premio = entrada.find('span').getText()
            listado.append([numero, premio])
            
        df_listado = pd.DataFrame(listado, columns=['numero', 'premio']) 
        df_listado = df_listado[df_listado['numero'] != '--']
        df_listado['numero'] = df_listado['numero'].astype('str')
        df_listado.to_csv(f'{wd}listado_loteria.csv', index=False)
        print(f'Lectura correcta, los .csv están en el working_folder: {wd}')
    else:
        print('## No existe la pagina err400 ##')
        pass
          
    return


if __name__ == '__main__':
    loteria_scraping()

## END ##