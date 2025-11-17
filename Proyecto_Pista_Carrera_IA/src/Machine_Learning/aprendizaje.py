from src.Movimientos_Carro.movimientos import *
from collections import defaultdict
import random

# --- Parámetros de RL ---
n_actions = 4       # 0=adelante, 1=atrás, 2=izq, 3=der
alpha = 0.5         # qué tanto corrige lo aprendido (0–1)
gamma = 0.9         # importancia del futuro
epsilon = 0.3       # probabilidad de hacer algo al azar (explorar)

# Q: diccionario que acepta tuplas (x,z) como estado
Q = defaultdict(lambda: [0.0] * n_actions)

# Estado global actual y si el episodio terminó
state = None
done = False


# -----------------------------
#  Funciones de apoyo RL
# -----------------------------
def elegir_accion(estado):
    """Política ε-greedy: a veces explora, a veces explota lo aprendido."""
    if random.random() < epsilon:
        # Acción aleatoria (explorar)
        return random.randint(0, n_actions - 1)

    # Mejor acción según la tabla Q
    q_vals = Q[estado]
    max_q = max(q_vals)
    mejores = [a for a, q in enumerate(q_vals) if q == max_q]
    return random.choice(mejores)


def award():
    """Recompensa: tú decides la lógica.
       Aquí dejo tu idea de comprobar_() como ejemplo.
    """
    if comprobar_():
        return 0.5
    else:
        return -0.5


def ejecutar_acciones(accion):
    """Ejecuta la acción en el DeLorean."""
    direccion = direction()      # asumo que la tienes en movimientos.py

    if accion == 0:
        avanzar(direccion)
    elif accion == 1:
        retroceder(direccion)
    elif accion == 2:
        mov_izq()
    elif accion == 3:
        mov_der()


def normalizar():
    """Convierte la posición del carro a un estado discreto (x,z)."""
    x = int(DeloRean.x)
    z = int(DeloRean.z)
    return (x, z)


def step(accion):
    """Un paso del entorno:
       - ejecuta la acción,
       - calcula recompensa,
       - obtiene nuevo estado,
       - decide si el episodio terminó.
    """
    # 1. Ejecutar acción (mover carro)
    ejecutar_acciones(accion)

    # 2. Nuevo estado
    nuevo_estado = normalizar()

    # 3. Recompensa
    recompensa = award()

    # 4. ¿Terminó? (ajusta la lógica a lo que quieras)
    terminado = False
    # Por ejemplo, podrías usar:
    # terminado = comprobar_()   # si comprobar_() significa "llegó a la meta" o algo

    return nuevo_estado, recompensa, terminado


def reset_episode():
    """Reinicia el episodio (por ejemplo, reposiciona el carro si quieres)."""
    global state, done
    # Aquí podrías reposicionar el carro si quieres:
    # DeloRean.position = Vec3(0,0,0)
    state = normalizar()
    done = False


def lear_form():
    """Un paso de Q-learning. Llamar esta función una vez por frame en update()."""
    global state, done, Q

    # Si es la primera vez o ya terminó el episodio, reiniciar
    if state is None or done:
        reset_episode()

    # 1. Elegir acción según la política
    action = elegir_accion(state)

    # 2. Un paso en el entorno
    next_state, reward, done = step(action)

    # 3. Mejor valor Q futuro desde el nuevo estado
    best_next = max(Q[next_state])

    # 4. Actualizar Q (regla de Q-learning)
    Q[state][action] = Q[state][action] + alpha * (
        reward + gamma * best_next - Q[state][action]
    )

    # 5. Avanzar al siguiente estado
    state = next_state
