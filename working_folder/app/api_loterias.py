# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 17:41:19 2020

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
import pandas as pd
import numpy as np
import requests as rq
import csv
import json
import glob
import pymongo
from flask import Flask, request, render_template, jsonify

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
#print(os.path.dirname(os.path.realpath(__file__)))

print('\n')
print('Poner en el navegador "http://localhost:5000/api/v1/premios/bbdd/<numero1-numero2-...etc> or http://localhost:5000/api/v1/premios/csv/<numero1-numero2-...etc>" donde los numeros van separados por guiones')
print('Poner en el navegador "http://Iv36.pythonanywhere.com/api/v1/premios/csv/<numero1-numero2-...etc> or http://Iv36.pythonanywhere.com/api/v1/premios/bbdd/<numero1-numero2-...etc> " donde los numeros van separados por guiones')
print('Tambien desde una consola python "request.get("http://localhost:5000/api/v1/premios/<numero1-numero2-...etc>")", donde los numeros van separados por guiones')
print('Pulsar ctrl+c para cancelar')
print('\n')


if '__file__' in locals():
    wd = os.path.dirname(__file__)
    wd = wd + '/'
    sys.path.append(wd)
    sep = '/'
else:
    wd = os.path.abspath('./Documents/Repositorio_Iv/premios_loteria/working_folder/app/')
    wd = os.path.abspath(os.path.join(wd, os.pardir))
    wd = wd + '/'
    sys.path.append(wd)
    sep = '/'

lectura_bbdd = False

if lectura_bbdd == True:
    ### Conexion a la bbdd 
    # 
    user = 'ivan_1'
    password = 'mantga43'
    dabase_name = 'loteria_navidad_db'
    client = pymongo.MongoClient("mongodb+srv://%s:%s@cluster0.vsp3s.mongodb.net/%s?retryWrites=true&w=majority" %(user, password, dabase_name))
    db = client.get_database(dabase_name)

## Creacion de la app
#
app = Flask(__name__) 

@app.route('/api/v1/premios/bbdd/<str_numeros>', methods=['GET'])
def api_loterias_bbdd(str_numeros):
    lista_numeros = str_numeros.split('-')
    records = 'db.premios_records'
    records = eval(records)
    results = list(records.find({}, {"_id": 0})) # Asi omitimos el _id que por defecto nos agrega mongo
    df_results = pd.DataFrame.from_dict(results)
    
    # new
    df_results['premio'] = df_results['premio'].str.replace('.', '')
    df_results['premio'] =  df_results['premio'].astype(int)
    ## Otros Premios
    df_results_4_primeros = df_results.sort_values('premio').iloc[-5:]
    primero = df_results_4_primeros.iloc[-1,0]
    segundo = df_results_4_primeros.iloc[-2,0]
    tercero = df_results_4_primeros.iloc[-3,0]
    cuarto_1 = df_results_4_primeros.iloc[-4,0]
    cuarto_2 = df_results_4_primeros.iloc[-5,0]
    lista_premios = [primero, segundo, tercero, cuarto_1, cuarto_2]
    aprox_1 = [str(int(primero)-1), str(int(primero)+1)]
    aprox_2 = [str(int(segundo)-1), str(int(segundo)+1)]
    aprox_3 = [str(int(tercero)-1), str(int(tercero)+1)]
    centenas_1 = [primero[:-2]]
    centenas_2 = [segundo[:-2]]
    centenas_3 = [tercero[:-2]]
    centenas_4 = [cuarto_1[:-2], cuarto_2[:-2]]
    centenas = centenas_1 + centenas_2 + centenas_3 + centenas_4
    decenas_1 = [primero[-2:]]
    decenas_2 = [segundo[-2:]]
    decenas_3 = [tercero[-2:]]
    decenas = decenas_1 + decenas_2 + decenas_3
    reintegros = [primero[-1]]
    # fin new    
    
    df_results = df_results.set_index('numero')
    dicc_results = df_results.to_dict('index')
    lista_results = []
    
    for item in lista_numeros:
        suma_premios = []
        causa = []
        try:
            suma_premios.append(dicc_results[item]['premio'])
            causa.append('Extracción')
        except:
            suma_premios.append(0)
        if (item in aprox_1):
            suma_premios.append(20000)
            causa.append('Aproximación')
        elif (item in aprox_2):
            suma_premios.append(12500)
            causa.append('Aproximación')
        elif (item in aprox_3):
            suma_premios.append(9600)
            causa.append('Aproximación')
        if (item[:-2] in centenas) & (item not in lista_premios):
            suma_premios.append(1000)
            causa.append('Centenas')
        elif (item[-2:] in decenas) & (item not in lista_premios):
            suma_premios.append(1000)
            causa.append('Terminación')
        if (item[-1] in reintegros) & (item != primero):
            suma_premios.append(200)
            causa.append('Reintegro')
            
        suma_premios = sum(suma_premios)
        causa = '-'.join(causa)
        
        dicc = {item:{'premio':suma_premios, 'causa':causa}}   
        lista_results.append(dicc)
            
    return jsonify(lista_results)
    

@app.route('/api/v1/premios/csv/<str_numeros>', methods=['GET'])
def api_loterias_csv(str_numeros):
    lista_numeros = str_numeros.split('-')
    lista_ficheros = glob.glob(wd + '*.csv')
    
    for item in lista_ficheros:
        df = pd.read_csv(item, dtype=str)
        
    df_json = df.to_json(orient="records")
    df_json = json.loads(df_json)
    df_results = pd.DataFrame.from_dict(df_json)
   
    # new
    df_results['premio'] = df_results['premio'].str.replace('.', '')
    df_results['premio'] =  df_results['premio'].astype(int)
    ## Otros Premios
    df_results_4_primeros = df_results.sort_values('premio').iloc[-5:]
    primero = df_results_4_primeros.iloc[-1,0]
    segundo = df_results_4_primeros.iloc[-2,0]
    tercero = df_results_4_primeros.iloc[-3,0]
    cuarto_1 = df_results_4_primeros.iloc[-4,0]
    cuarto_2 = df_results_4_primeros.iloc[-5,0]
    lista_premios = [primero, segundo, tercero, cuarto_1, cuarto_2]
    aprox_1 = [str(int(primero)-1), str(int(primero)+1)]
    aprox_2 = [str(int(segundo)-1), str(int(segundo)+1)]
    aprox_3 = [str(int(tercero)-1), str(int(tercero)+1)]
    centenas_1 = [primero[:-2]]
    centenas_2 = [segundo[:-2]]
    centenas_3 = [tercero[:-2]]
    centenas_4 = [cuarto_1[:-2], cuarto_2[:-2]]
    centenas = centenas_1 + centenas_2 + centenas_3 + centenas_4
    decenas_1 = [primero[-2:]]
    decenas_2 = [segundo[-2:]]
    decenas_3 = [tercero[-2:]]
    decenas = decenas_1 + decenas_2 + decenas_3
    reintegros = [primero[-1]]
    # fin new
    
    df_results = df_results.set_index('numero')
    dicc_results = df_results.to_dict('index')
    
    lista_results = []
    
    for item in lista_numeros:
        suma_premios = []
        causa = []
        try:
            suma_premios.append(dicc_results[item]['premio'])
            causa.append('Extracción')
        except:
            suma_premios.append(0)
        if (item in aprox_1):
            suma_premios.append(20000)
            causa.append('Aproximación')
        elif (item in aprox_2):
            suma_premios.append(12500)
            causa.append('Aproximación')
        elif (item in aprox_3):
            suma_premios.append(9600)
            causa.append('Aproximación')
        if (item[:-2] in centenas) & (item not in lista_premios):
            suma_premios.append(1000)
            causa.append('Centenas')
        elif (item[-2:] in decenas) & (item not in lista_premios):
            suma_premios.append(1000)
            causa.append('Terminación')
        if (item[-1] in reintegros) & (item != primero):
            suma_premios.append(200)
            causa.append('Reintegro')
            
        suma_premios = sum(suma_premios)
        causa = '-'.join(causa)
        
        dicc = {item:{'premio':suma_premios, 'causa':causa}}   
        lista_results.append(dicc)
            
    return jsonify(lista_results)

###############################################################################################################
#         INFINITY LOOP LISTENING TO PORT 80 (port=int("80")) TO THE OUTSIDE WORLD (host="0.0.0.0") - START   #
###############################################################################################################
if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(
	host="0.0.0.0",
        port=int("5000")
    )
###############################################################################################################
#         INFINITY LOOP LISTENING TO PORT 80 (port=int("80")) TO THE OUTSIDE WORLD (host="0.0.0.0") - END     #
###############################################################################################################

## END ##     