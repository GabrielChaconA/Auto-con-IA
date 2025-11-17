from src.Movimientos_Carro.movimientos import *
from ursina import Vec3, distance, raycast, scene
from collections import defaultdict
import random

n_actions = 4
alpha = 0.5
gamma = 0.9
epsilon = 0.3

Q = defaultdict(lambda: [0.0] * n_actions)

state = None
done = False

meta = Vec3(13.918956, 2.683757, -18.438091)
last_distance = None


def elegir_accion(estado):
    if random.random() < epsilon:
        return random.randint(0, n_actions - 1)
    q_vals = Q[estado]
    max_q = max(q_vals)
    mejores = [a for a, q in enumerate(q_vals) if q == max_q]
    return random.choice(mejores)


def award():
    global last_distance

    origin = DeloRean.world_position + Vec3(0, 1, 0)
    hit = raycast(
        origin=origin,
        direction=Vec3(0, -1, 0),
        distance=100,
        ignore=(DeloRean,),
        traverse_target=scene
    )

    if not hit.hit or hit.entity != pista:
        return -1.0

    d = distance(DeloRean.world_position, meta)

    if last_distance is None:
        last_distance = d
        return 0.0

    if d < last_distance:
        last_distance = d
        return 0.5

    last_distance = d
    return -0.2


def ejecutar_acciones(accion):
    direccion = direction()
    if accion == 0:
        avanzar(direccion)
    elif accion == 1:
        retroceder(direccion)
    elif accion == 2:
        mov_izq()
    elif accion == 3:
        mov_der()


def normalizar():
    x = int(DeloRean.x)
    z = int(DeloRean.z)
    return (x, z)


def step(accion):
    ejecutar_acciones(accion)
    nuevo_estado = normalizar()
    recompensa = award()
    terminado = False
    return nuevo_estado, recompensa, terminado


def reset_episode():
    global state, done, last_distance
    state = normalizar()
    done = False
    last_distance = None


def lear_form():
    global state, done, Q

    if state is None or done:
        reset_episode()

    action = elegir_accion(state)
    next_state, reward, done = step(action)
    best_next = max(Q[next_state])

    Q[state][action] = Q[state][action] + alpha * (
        reward + gamma * best_next - Q[state][action]
    )

    state = next_state


