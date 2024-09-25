from ambiente import Cubo
from busqueda import *

cubo = Cubo()
solucion_dijkstra = dijkstra(cubo)
camino_anchura = [cubo.estado_inicial] + solucion(solucion_dijkstra)
print('La solución mediante el algoritmo de Dijkstra es:')
print(camino_anchura)
print('El costo de la solución es:', solucion_dijkstra.costo_camino)
