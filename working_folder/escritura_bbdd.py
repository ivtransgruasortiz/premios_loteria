# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 18:45:36 2020

@author: iv
"""

import sys
import os
import pandas as pd
import json
import glob
import pymongo
import yaml


### SYSTEM DATA ###
if '__file__' in locals():
    print('estamos en el aire')
    try:
        with open("config.yaml", "r") as stream:
            auth_ddbb = yaml.safe_load(stream)
            stream.close()
        SECRET_USER = auth_ddbb["SECRET_USER"]
        SECRET_PASS = auth_ddbb["SECRET_PASS"]
    except:
        SECRET_USER = os.getenv("SECRET_USER")
        SECRET_PASS = os.getenv("SECRET_PASS")
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
    wd = os.path.abspath("./working_folder/")
    wd += '/'
    sys.path.append(wd)
    with open("config.yaml", "r") as stream:
        auth_ddbb = yaml.safe_load(stream)
        stream.close()
    SECRET_USER = auth_ddbb["SECRET_USER"]
    SECRET_PASS = auth_ddbb["SECRET_PASS"]

#ConexionBBDD
conexion_bbdd = True
if conexion_bbdd:
    dabase_name = 'loteria_navidad_db'
    client = pymongo.MongoClient("mongodb+srv://%s:%s@cluster0.vsp3s.mongodb.net/%s?retryWrites=true&w=majority"
                                 % (SECRET_USER, SECRET_PASS, dabase_name))
    db = client.get_database(dabase_name)


def escritura_bbdd():
    lista_ficheros = glob.glob(wd + '*.csv')
    for item in lista_ficheros:
        item_str = 'premios_records'
        df = pd.read_csv(f'{item}', dtype=str)
        df_json = df.to_json(orient="records")
        df_json = json.loads(df_json)
        exec('records = db.' + item_str)
        exec('records.remove()')
        exec('records.insert(df_json)')
    print('Se han leído los .csv y se han subido como documentos a la base de datos MongoDB Atlas')
    return


if __name__ == '__main__':
    escritura_bbdd()
