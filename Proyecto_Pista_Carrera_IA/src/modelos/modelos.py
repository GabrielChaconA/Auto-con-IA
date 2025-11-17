
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
    model='sports stadium.obj',
    scale=0.05,
    position=(-1, -1, -1),
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


