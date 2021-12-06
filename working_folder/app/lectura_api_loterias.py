# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 17:41:19 2020

@author: iv
"""


import sys
import os
import pandas as pd
import requests as rq


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
    wd = os.path.abspath("./Documents/Repositorio_Iv/premios_loteria/working_folder/app/")
    wd += '/'
    sys.path.append(wd)

if sys.platform == 'win32':
    system = sys.platform
else:
    system = sys.platform


def peticion_api(lista_str=None):
    url = 'http://localhost:5000/api/v1/premios/bbdd/'
    # url = 'http://iv36.pythonanywhere.com/api/v1/premios/csv/'
    if lista_str is None:
        lista_str = input('Dame la lista de numeros a comprobar separados por guiones sin espacios: ')
        respuesta = rq.get(url+f'{lista_str}').json()
    else:
        respuesta = rq.get(url+f'{lista_str}').json()
    # print(respuesta)
    for item in respuesta:
        for numero, premio in item.items():
            numero = numero
            cantidad = premio['premio']
            causa = premio['causa']
            causa = str.replace(causa, '-', ', ')
            if cantidad == '0':
                print(f'El número {numero} no está premiado')
            else:
                print(f'El número {numero} está premiado con  --> {cantidad} euros y acumula los siguientes premios: {causa}')
    return respuesta


lista_str = '-'.join([str(x) for x in pd.read_csv(wd + 'numeros_jugados.csv')['numeros_jugados'].tolist()])


if __name__ == '__main__':
    peticion_api(lista_str)
