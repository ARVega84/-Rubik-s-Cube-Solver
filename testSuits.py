import numpy as np
from ambiente import Cubo
from types import MethodType

def crea_test(num_movs, heuristica):
    '''
    Toma un estado y una heurística y devuelve un
    rompecabezas con estado como estado inicial y
    con heurística heuristica.
    Input:
        - estado, una matriz con el estado inicial del rompecabezas
        - heuristica, una función para convertirla en método del rompecabezas
    Output:
        - puz, un objeto rompecabezas
    '''
    cubo = Cubo(num_movs=num_movs)
    cubo.heuristica = MethodType(heuristica, cubo)
    return cubo


def test_suit_heuristicas_cubo(lista_estados:list, lista_heuristicas:list, nombres:list) -> list:
    '''
    Toma una lista de estados y de heurísticas y crea una
    lista de tests donde cada heurística se evalúa sobre
    cada uno de los estados.
    Input:
        - lista_estados, una lista de estados como matrices
        - lista_heuristicas, una lista de heurísticas para incluir como métodos
        - lista_nombres, una lista de los nombres de las heurísticas
    Output:
        - lista_tests, una lista con los rompecabezas
        - lista_nombres, una lista con el nombre correspondiente
                         a la heurística del test
    '''
    lista_tests = []
    lista_nombres = []
    for i, heuristica in enumerate(lista_heuristicas):
        for estado in lista_estados:
            test = crea_test(estado, heuristica)
            lista_tests.append([test])
            lista_nombres.append(nombres[i])
    return lista_tests, lista_nombres