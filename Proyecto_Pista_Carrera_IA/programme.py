# pip install ursina
from ursina import *
from pathlib import Path

app = Ursina()


# Ruta de assets relativa al .py
base_path = Path(__file__).parent
application.asset_folder = base_path / "Modelos 3d"


# === PISTA ===
pista = Entity(
    model='FullTrack.obj',
    texture='Main.png',
    color=color.light_gray,
    scale=15,
    position=(0, 0, 0),
    rotation=(0, 0, 0),
    double_sided=True,
    shadows=True,
    collider='mesh'        
)


# === CARRO ===
DeloRean = Entity(
    model='DeLorean.obj',
    color=color.light_gray,
    scale=(-0.02, 0.02, 0.02 ),
    position=(4.5, 2.90, 0),
    rotation=(0, 0, 0),
    double_sided=True
)

# Esfera a cierta distancia delante del carro (hija del pivot)
lead_dist = 6
esfera = Entity(parent=DeloRean, model='sphere', color=color.red, scale=.3, position=(0,0,6))

# Cámara
EditorCamera(pivot=DeloRean, position=(4.5, 2.90, 0), rotation=(25,0,0))

vel = 0.25
def update():
    EPS = 0.02        # tolerancia para considerar y≈0
    ADELANTE = 0.0    # pon 2.0 si quieres medir un poco al frente del carro
    i =0


    # Dirección HACIA la esfera usando POSICIÓN MUNDIAL
    direccion = (esfera.world_position - DeloRean.world_position)
    
    # Hacer que el carro mire a la esfera (solo yaw)
    DeloRean.look_at(esfera)

    # MOVER EL CARRO
    if held_keys['w']:
        DeloRean.position += direccion * vel
    if held_keys['s']:
        DeloRean.position -= direccion * vel
    if held_keys['a']: 
        DeloRean.rotation_y -= 1
    if held_keys['d']:
        DeloRean.rotation_y += 1

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
        
        


           
    
     
    

            

app.run()
