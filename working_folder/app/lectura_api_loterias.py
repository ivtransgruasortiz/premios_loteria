# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 17:41:19 2020

@author: iv
"""

import sys
import os
import pandas as pd
import requests as rq

from working_folder.app.functions import api_loterias_csv_local

# SYSTEM DATA ###
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


def peticion_api(lista_str=None):
    # url = 'http://localhost:5000/api/v1/premios/bbdd/'
    url = 'http://localhost:5000/api/v1/premios/csv/'
    # url = 'http://iv36.pythonanywhere.com/api/v1/premios/csv/'
    if lista_str is None:
        lista_str = input('Dame la lista de numeros a comprobar separados por guiones sin espacios: ')
        respuesta = rq.get(url + f'{lista_str}').json()
    else:
        respuesta = rq.get(url + f'{lista_str}').json()
    for item in respuesta:
        for numero, premio in item.items():
            numero = numero
            cantidad = premio['premio']
            causa = premio['causa']
            causa = str.replace(causa, '-', ', ')
            if cantidad == '0':
                print(f'El número {numero} no está premiado')
            else:
                print(
                    f'El número {numero} está premiado con  --> {cantidad} euros a la serie ({int(int(cantidad) / 10)} '
                    f'euros al décimo) y acumula los siguientes premios: {causa}')
    return respuesta


def peticion_csv_file(lista_str=None):
    if lista_str is None:
        lista_str = input('Dame la lista de numeros a comprobar separados por guiones sin espacios: ')
        respuesta = api_loterias_csv_local(lista_str)
    else:
        respuesta = api_loterias_csv_local(lista_str)
    for item in respuesta:
        for numero, premio in item.items():
            numero = numero
            cantidad = premio['premio']
            causa = premio['causa']
            causa = str.replace(causa, '-', ', ')
            if cantidad == '0':
                print(f'El número {numero} no está premiado')
            else:
                print(
                    f'El número {numero} está premiado con  --> {cantidad} euros a la serie ({int(int(cantidad) / 10)} '
                    f'euros al décimo) y acumula los siguientes premios: {causa}')
    return respuesta


name_csv = 'numeros_jugados.csv'
lista_str = [x for x in pd.read_csv(wd + name_csv, dtype=object)['numeros_jugados']]
# lista_str.append('2')  # PRUEBA
# lista_str = '-'.join(['0' * (5 - len(x)) + x if len(x) < 5 else x for x in lista_str])
lista_str = '-'.join([f"{int(x):05}" for x in lista_str])

if __name__ == '__main__':
    valid = True
    while valid:
        remote = input("Ejecución online?? Y/N: ")
        if remote.lower() == "y":
            peticion_api(lista_str)
            valid = False
        elif remote.lower() == "n":
            peticion_csv_file(lista_str)
            valid = False
        else:
            print("No es una seleccion válida...")
            valid = True
