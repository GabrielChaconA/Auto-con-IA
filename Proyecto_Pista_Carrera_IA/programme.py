from ursina import *
app = Ursina()

from src.Machine_Learning.aprendizaje import *
from src.modelos.modelos import DeloRean,esfera









def update():
    camera.position = DeloRean.position+Vec3(5,25,0)
    camera.look_at(DeloRean) 
    DeloRean.look_at(esfera)
    lear_form()

    


       

app.run()
