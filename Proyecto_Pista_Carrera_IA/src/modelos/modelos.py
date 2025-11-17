
from ursina import *
from pathlib import Path



# Ruta de assets relativa al .py
base_path = Path(__file__).resolve().parents[2]
application.asset_folder = base_path / "Modelos_3d"


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
# === Estadio ===
Estadio = Entity(
    color=color.light_gray,
    model='Estadio.obj',
    scale=0.13,
    position=(30, 0, 30),
    rotation=(0, 0, 0),
    double_sided=True,
       
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

esfera = Entity(
    parent=DeloRean, 
    model='sphere',
      color=color.red, 
      scale=.3, 
      position=(0,0,6))


# === SUELO VERDE ===
suelo = Entity(
    model='plane',
    scale=250,                 # grande para cubrir toda la pista
    color=color.gray,         # color verde
    position=(0, -0.1, 0),     # un poquito abajo de la pista para que no parpadee
    rotation=(0, 0, 0),       # para que quede horizontal
    collider=None
)
