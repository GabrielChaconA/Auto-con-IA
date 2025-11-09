# pip install ursina
from ursina import *
from pathlib import Path

class Programme: 
        """ AQUI HAY QUE HACER TODO EL CODE """
        app = Ursina()

        #Carpeta 
        application.asset_folder = Path(r"C:\Users\gaboc\OneDrive\Documentos\TECMORELIA\Quinto semestre\Proyecto de graficación\Proyecto_Pista_Carrera_IA\Modelos 3d")

        #Pista 2d
        pista = Entity(
            model='FullTrack.obj',
            texture = 'Main.png',
            color=color.light_gray,
            scale=10,           
            position=(0.1, 0.5, 0),   
            rotation=(0, 0, 0),
            double_sided=True,
            shadows = True
        )

        #Modelo del carro 
        modelo = Entity(
            model='DeLorean.obj',
            color=color.light_gray,
            scale=0.02,           
            position=(0.1, 0.5, 0),   
            rotation=(0, 0, 0),
            double_sided=True
        )

        # === CÁMARA LIBRE ===
# Mueve con W/A/S/D/Q/E y gira con clic derecho + ratón
        cam = EditorCamera(rotation=(35, 0, 0), position=(0, 10, -20))
     

        # aqui se realizaran los updates del movimiento del carro
        def update():
            pass

        app.run()
