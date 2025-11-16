from ursina import *
from src.modelos.modelos import DeloRean


def avanzar(direccion):
    DeloRean.position += direccion * 0.5
    
def retroceder(direccion):
    DeloRean.position -= direccion * 0.5
    
    
def mov_izq():
    DeloRean.rotation_y -= 1
    
def mov_der():
    DeloRean.rotation_y += 1
  