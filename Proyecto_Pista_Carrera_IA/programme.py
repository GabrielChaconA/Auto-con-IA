from ursina import *
app = Ursina()


from src.modelos.modelos import DeloRean,pista,esfera

from src.Movimientos_Carro.movimientos import avanzar,mov_der,mov_izq,retroceder





def update():
    camera.position = DeloRean.position+Vec3(5,25,0)
    camera.look_at(DeloRean) 

    ADELANTE = 0.0   

    # Dirección HACIA la esfera usando POSICIÓN MUNDIAL
    direccion = (esfera.world_position - DeloRean.world_position)
    
    # Hacer que el carro mire a la esfera (solo yaw)
    DeloRean.look_at(esfera)

    # MOVER EL CARRO
    if held_keys['w']:
        print("hoLA")
        avanzar(direccion)
    if held_keys['s']:
        retroceder(direccion)
    if held_keys['a']: 
        mov_izq()
    if held_keys['d']:
        mov_der()

    origin = DeloRean.world_position + DeloRean.forward * ADELANTE + Vec3(0, 1, 0)

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
   

            

app.run()
