from copy import deepcopy
from random import choice, randint
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from busqueda import ListaPrioritaria



class Cubo:

    def __init__(self, estado_inicial:str=None, num_movs=10, verbose=False, restriccion=True):
        self.estado_objetivo = [[0, 0, 0, 0], [1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4], [5, 5, 5, 5]]

        if restriccion:
            self.movimientos = ["arriba", "!arriba", "2arriba", "!derecha", "derecha", "2derecha"]
        else:
            self.movimientos = ["arriba", "!arriba", "2arriba", "frente", "!frente", "2frente", "!derecha", "derecha", "2derecha"]

        if estado_inicial is None:
            self.estado_inicial = self.mezclar_cubo(aleatorio=True, num_movs=num_movs, verbose=verbose)
        else:
            self.estado_inicial = self.mezclar_cubo(aleatorio=False, pasos=estado_inicial, verbose=verbose)
        
        

    
    def giro(self, estado:list) -> list:
        """ 
            Realiza un giro en sentido horario en la cara superior del cubo
            
            - Input: Una matriz representando un estado del cubo
            - Output: Una matriz representando el estado del cubo después de que se le realizara el giro
        """
        s = deepcopy(estado)
        s[0] =  [s[0][3]] + s[0][:3]
        laterales = [x[:2] for x in s[1:5]]
        laterales = laterales[1:] + [laterales[0]]

        for i, lat in enumerate(laterales):
            s[i+1][:2] = lat
        return s
    
    
    def giro_superior(self, estado:list) -> list:
        """
            Wrapper para la funcion giro
            
            - Input: Una matriz representando un estado del cubo
            - Output: Una matriz representando el estado del cubo después de que se le realizara el giro
        """
        return self.giro(estado)
    

    def giro_superior_reves(self, estado:list) -> list:
        
        s = self.giro(estado)
        s = self.giro(s)
        s = self.giro(s)
        return s
    
    def giro_superior_doble(self, estado:list) -> list:
        
        s = self.giro(estado)
        s = self.giro(s)
        return s

    

    def giro_frontal(self, estado:list) -> list:
        """ 
            Realiza un giro en sentido horario en la cara frontal del cubo.
            Rota el cubo entero para que la cara forntal quede arriba, llama a la función "giro"
            y devuelve la rotación inicial.
            
            - Input: Una matriz representando un estado del cubo
            - Output: Una matriz representando el estado del cubo después de que se le realizara el giro
        """
        s = deepcopy(estado)

        s[3] = [s[3][3]] + s[3][:3]
        s[1] = s[1][1:] + [s[1][0]]
        s[0] = [s[0][2]] + [s[0][3]] + [s[0][0]] + [s[0][1]]

        s = [s[2]] + [s[1]] + [s[5]] + [s[3]] + [s[0]] + [s[4]]
        s = self.giro(s)
        s = [s[4]] + [s[1]] + [s[0]] + [s[3]] + [s[5]] + [s[2]]

        s[3] = s[3][1:] + [s[3][0]]
        s[1] = [s[1][3]] + s[1][:3]
        s[0] = [s[0][2]] + [s[0][3]] + [s[0][0]] + [s[0][1]]
        
        return s
    
    
    def giro_frontal_reves(self, estado:list) -> list:
        
        s = self.giro_frontal(estado)
        s = self.giro_frontal(s)
        s = self.giro_frontal(s)
        return s

    def giro_frontal_doble(self, estado:list) -> list:
        
        s = self.giro_frontal(estado)
        s = self.giro_frontal(s)
        return s

    
    def giro_derecho(self, estado:list) -> list:
        """ 
            Realiza un giro en sentido horario en la cara derecha del cubo.
            Rota el cubo entero para que la cara derecha quede arriba, llama a la función "giro"
            y devuelve la rotación inicial.
            
            - Input: Una matriz representando un estado del cubo
            - Output: Una matriz representando el estado del cubo después de que se le realizara el giro
        """

        s = deepcopy(estado)

        s[4] =  [s[4][3]] + s[4][:3]
        s[2] =   s[2][1:] + [s[2][0]]
        s[0] =   s[0][1:] + [s[0][0]]
        s[5] =   s[5][1:] + [s[5][0]]
        

        s = [s[3]] + [s[0]] + [s[2]] + [s[5]] + [s[4]] + [s[1]]
        s = self.giro(s)
        s = [s[1]] + [s[5]] + [s[2]] + [s[0]] + [s[4]] + [s[3]]

        s[4] =   s[4][1:] + [s[4][0]]
        s[2] =  [s[2][3]] + s[2][:3]
        s[0] =  [s[0][3]] + s[0][:3]
        s[5] =  [s[5][3]] + s[5][:3]
        

        return s
    

    def giro_derecho_reves(self, estado:list) -> list:
        
        s = self.giro_derecho(estado)
        s = self.giro_derecho(s)
        s = self.giro_derecho(s)
        return s
    
    def giro_derecho_doble(self, estado:list) -> list:
        
        s = self.giro_derecho(estado)
        s = self.giro_derecho(s)
        return s


    def pintar_estado_cmd(self, estado:list) -> None:
        """
            Imprime el estado del cubo
            
            - Input: Una matriz representando el estado del cubo
            - Output: None, imprime el cubo en consola 
            """
        s = deepcopy(estado)

        print("\n================================ESTADO=DEL=CUBO================================\n")

        print(" "*16 + "+---+---+")

        print(" "*16 + f"| {s[0][0]} | {s[0][1]} |")
        print(" "*16 + "+---+---+")
        print(" "*16 + f"| {s[0][3]} | {s[0][2]} |")

        print(" "*16  + "+---+---+")
        print(" "*6  + "+---+---+ "*4 )

        print(" "*6  + f"| {s[1][0]} | {s[1][1]} | | {s[2][0]} | {s[2][1]} | | {s[3][0]} | {s[3][1]} | | {s[4][0]} | {s[4][1]} |")
        print(" "*6  + "+---+---+ "*4 )
        print(" "*6  + f"| {s[1][3]} | {s[1][2]} | | {s[2][3]} | {s[2][2]} | | {s[3][3]} | {s[3][2]} | | {s[4][3]} | {s[4][2]} |")

        print(" "*6  + "+---+---+ "*4 )
        print(" "*16 + "+---+---+")

        print(" "*16 + f"| {s[5][0]} | {s[5][1]} |")
        print(" "*16 + "+---+---+")
        print(" "*16 + f"| {s[5][3]} | {s[5][2]} |")

        print(" "*16  + "+---+---+")

        print("\n===============================================================================\n")



    def pintar_estado(self, estado):

        s = deepcopy(estado)

        img =  [[0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 6, s[0][0], s[0][0], 6, s[0][1], s[0][1], 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 6, s[0][0], s[0][0], 6, s[0][1], s[0][1], 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 6, s[0][3], s[0][3], 6, s[0][2], s[0][2], 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 6, s[0][3], s[0][3], 6, s[0][2], s[0][2], 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
                [6, s[1][0], s[1][0], 6, s[1][1], s[1][1], 6, 6, s[2][0], s[2][0], 6, s[2][1], s[2][1], 6, 6, s[3][0], s[3][0], 6, s[3][1], s[3][1], 6, 6, s[4][0], s[4][0], 6, s[4][1], s[4][1], 6],
                [6, s[1][0], s[1][0], 6, s[1][1], s[1][1], 6, 6, s[2][0], s[2][0], 6, s[2][1], s[2][1], 6, 6, s[3][0], s[3][0], 6, s[3][1], s[3][1], 6, 6, s[4][0], s[4][0], 6, s[4][1], s[4][1], 6],
                [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
                [6, s[1][3], s[1][3], 6, s[1][2], s[1][2], 6, 6, s[2][3], s[2][3], 6, s[2][2], s[2][2], 6, 6, s[3][3], s[3][3], 6, s[3][2], s[3][2], 6, 6, s[4][3], s[4][3], 6, s[4][2], s[4][2], 6],
                [6, s[1][3], s[1][3], 6, s[1][2], s[1][2], 6, 6, s[2][3], s[2][3], 6, s[2][2], s[2][2], 6, 6, s[3][3], s[3][3], 6, s[3][2], s[3][2], 6, 6, s[4][3], s[4][3], 6, s[4][2], s[4][2], 6],
                [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
                [0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 6, s[5][0], s[5][0], 6, s[5][1], s[5][1], 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 6, s[5][0], s[5][0], 6, s[5][1], s[5][1], 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 6, s[5][3], s[5][3], 6, s[5][2], s[5][2], 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 6, s[5][3], s[5][3], 6, s[5][2], s[5][2], 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        cmap = ListedColormap(["white", "orange", "green", "red", "blue", "yellow", "black"])
        i = plt.matshow(img, cmap=cmap)



    def test_objetivo(self, estado):
        s = deepcopy(estado)

        for cara in s:
            colores = set(cara)
            if len(colores) > 1:
                return False
            
        return True

    def transicion(self, estado, accion):

        acciones = {"arriba":self.giro_superior,
                    "!arriba":self.giro_superior_reves,
                    "2arriba":self.giro_superior_doble,
                    "frente":self.giro_frontal,
                    "!frente":self.giro_frontal_reves,
                    "2frente":self.giro_frontal_doble,
                    "derecha":self.giro_derecho,
                    "!derecha":self.giro_derecho_reves,
                    "2derecha":self.giro_derecho_doble}
        
        return acciones[accion](estado)


    def acciones_aplicables(self, estado):
        return self.movimientos
    
    def costo(self, estado, accion):
        return 1
    
    def codigo(self, estado):

        s = deepcopy(estado)

        string = ""
        for cara in s:
            string += f"({cara[0]}{cara[1]}{cara[2]}{cara[3]})-"

        return string[:-1]

    def mezclar_cubo(self, aleatorio=True, pasos=[], num_movs=0, verbose=False):

        s = deepcopy(self.estado_objetivo)


        acciones = {"arriba":self.giro_superior,
                    "!arriba":self.giro_superior_reves,
                    "2arriba":self.giro_superior_doble,
                    "frente":self.giro_frontal,
                    "!frente":self.giro_frontal_reves,
                    "2frente":self.giro_frontal_doble,
                    "derecha":self.giro_derecho,
                    "!derecha":self.giro_derecho_reves,
                    "2derecha":self.giro_derecho_doble}

        movimientos_realizados = []

        if aleatorio:

            for i in range(num_movs):
                accion = choice(self.movimientos)
                movimientos_realizados.append(accion)

                s = acciones[accion](s)

        else:
            for paso in pasos:
                movimientos_realizados.append(paso)
                s = acciones[paso](s)

        if verbose:
            print(f"Movimientos realizados para mezclar el cubo: {movimientos_realizados}")
        return s
    

    



    

    

