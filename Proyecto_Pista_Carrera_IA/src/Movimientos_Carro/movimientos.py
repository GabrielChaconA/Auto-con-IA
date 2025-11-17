from ursina import *
from src.modelos.modelos import DeloRean,pista,esfera


def avanzar(direccion):
    DeloRean.position += direccion * 0.5
    
def retroceder(direccion):
    DeloRean.position -= direccion * 0.5
    
    
def mov_izq():
    DeloRean.rotation_y -= 1
    
def mov_der():
    DeloRean.rotation_y += 1


def comprobar_():
    flag = False
    origin = DeloRean.world_position + DeloRean.forward * 0.0 + Vec3(0, 1, 0)
    hit = raycast(
        origin=origin,
        direction=Vec3(0, -1, 0),
        distance=100,
        ignore=(DeloRean,),
        traverse_target=scene
    )

    if hit.hit and hit.entity == pista:
        
        DeloRean.y = hit.world_point.y
        DeloRean.rotation.x = hit.world_point.y
        flag = True
    return flag

def direction():
    direccion = (esfera.world_position - DeloRean.world_position)
    return direccion