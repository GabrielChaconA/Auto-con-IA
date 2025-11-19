from ursina import *
app = Ursina()

from src.Machine_Learning.aprendizaje import *
from src.modelos.modelos import DeloRean,esfera
cam = EditorCamera() 

def update():

    control_auto()

    


       

app.run()
