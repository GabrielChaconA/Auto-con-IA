# src/control_auto.py

from ursina import Vec3, distance, raycast, scene, time
import math

# Ajusta este import a donde tengas definidas estas cosas:
# Deben existir: DeloRean (carro) y pista (Entity de la pista)
from src.Movimientos_Carro.movimientos import DeloRean, pista

# =========================
#   CONFIGURACIÓN
# =========================

ALTURA_COCHE    = 0.5     # separación vertical sobre la pista
VEL_AVANCE      = 6.0     # velocidad de avance (unidades/seg)
VEL_GIRO_MAX    = 90.0    # giro máximo por segundo (grados/seg)
ANGLE_DEADZONE  = 5.0     # si el ángulo es menor, no gira (solo avanza)
WAYPOINT_RADIUS = 2.5     # distancia para considerar que llegó a un waypoint

# Puntos de la pista (EJEMPLOS – CAMBIA ESTOS POR LOS DE TU PISTA)
# Pon puntos siguiendo el recorrido de la pista en orden.
WAYPOINTS = [
    Vec3(0,   0,   0),
    Vec3(10,  0,   5),
    Vec3(20,  0,   0),
    Vec3(30,  0, -10),
    Vec3(20,  0, -20),
    Vec3(10,  0, -18),
    # Ejemplo: meta aproximada
    # Vec3(13.9, 0, -18.4),
]

current_wp = 0   # índice del waypoint actual


# =========================
#   BUSCAR PISTA ARRIBA / ABAJO
# =========================
def encontrar_pista_vertical(pos: Vec3, altura_busqueda=10) -> Vec3 | None:
    """
    Busca la pista arriba o abajo del punto 'pos'.

    1. Lanza un raycast desde ARRIBA hacia ABAJO.
    2. Si no encuentra, lanza desde ABAJO hacia ARRIBA.

    Si encuentra la pista, devuelve el punto de impacto (world_point).
    Si no encuentra nada, devuelve None.
    """

    # 1) Desde arriba hacia abajo
    origin_up = pos + Vec3(0, altura_busqueda, 0)
    hit_down = raycast(
        origin=origin_up,
        direction=Vec3(0, -1, 0),
        distance=altura_busqueda * 2,
        ignore=(DeloRean,),
        traverse_target=scene
    )

    if hit_down.hit and hit_down.entity == pista:
        return hit_down.world_point

    # 2) Desde abajo hacia arriba (por si el coche está debajo de la pista)
    origin_down = pos - Vec3(0, altura_busqueda, 0)
    hit_up = raycast(
        origin=origin_down,
        direction=Vec3(0, 1, 0),
        distance=altura_busqueda * 2,
        ignore=(DeloRean,),
        traverse_target=scene
    )

    if hit_up.hit and hit_up.entity == pista:
        return hit_up.world_point

    return None


def ajustar_altura_sobre_pista() -> bool:
    """
    Ajusta la altura del coche para que quede encima de la pista,
    buscando tanto arriba como abajo de su posición actual.

    Devuelve True si encontró pista y ajustó altura,
    False si no hay pista ni arriba ni abajo.
    """
    pos = DeloRean.world_position
    hit_point = encontrar_pista_vertical(pos)

    if hit_point is not None:
        DeloRean.y = hit_point.y + ALTURA_COCHE
        return True

    return False


# =========================
#   RECUPERACIÓN SI SE SALE
# =========================
def recuperar_si_fuera_de_pista() -> bool:
    """
    Si el coche NO tiene pista ni arriba ni abajo:

      - Mira un poco ENFRENTE (adelante) y realiza la misma búsqueda
        vertical (arriba/abajo) en ese punto.
      - Si hay pista enfrente, avanza hacia allí.
      - Si tampoco hay, gira sobre sí mismo buscando pista.

    Devuelve:
      True  -> ya está sobre la pista (ok, se puede seguir lógica normal).
      False -> sigue intentando recuperarse.
    """
    # 1. Intentar ajustar altura justo donde está el coche.
    if ajustar_altura_sobre_pista():
        return True  # ya está sobre la pista

    # 2. No hay pista ni arriba ni abajo -> mirar ENFRENTE
    forward = DeloRean.forward
    forward_flat = Vec3(forward.x, 0, forward.z).normalized()

    pos = DeloRean.world_position
    pos_frente = pos + forward_flat * 3   # un poco al frente en XZ

    hit_frente = encontrar_pista_vertical(pos_frente)

    if hit_frente is not None:
        # Hay pista enfrente (arriba o abajo):
        # -> movemos el coche un poco hacia adelante en XZ,
        # y ajustamos altura hacia ese punto.
        DeloRean.position += forward_flat * VEL_AVANCE * time.dt

        # Ajustar altura hacia el punto de pista encontrado
        DeloRean.y = hit_frente.y + ALTURA_COCHE
        return False  # seguimos en recuperación este frame

    # 3. No hay pista ni donde está ni enfrente -> girar en su lugar
    DeloRean.rotation_y += VEL_GIRO_MAX * time.dt  # gira a la izquierda
    return False


# =========================
#   CONTROL PRINCIPAL
# =========================
def control_auto():
    """
    Lógica simple para que el carro siga la pista hasta la meta,
    SIN ML, usando:

      - Waypoints.
      - Raycasts arriba/abajo.
      - Búsqueda de pista enfrente si se sale.

    Llamar esta función en tu update():

        from src.control_auto import control_auto

        def update():
            control_auto()
    """
    global current_wp

    if not WAYPOINTS:
        return  # por seguridad

    # 1. Asegurarnos de estar sobre la pista o en recuperación
    if not recuperar_si_fuera_de_pista():
        # Todavía está intentando regresar a la pista,
        # este frame NO hacemos lógica de waypoints.
        return

    # 2. Ya está sobre la pista → seguir waypoints
    target = WAYPOINTS[current_wp]

    # Posición actual en XZ
    pos = DeloRean.world_position
    pos_flat = Vec3(pos.x, 0, pos.z)
    target_flat = Vec3(target.x, 0, target.z)

    # 2.1. ¿Llegamos al waypoint actual?
    dist_wp = distance(pos_flat, target_flat)
    if dist_wp < WAYPOINT_RADIUS:
        # Modo "llega a la meta una sola vez"
        current_wp = min(current_wp + 1, len(WAYPOINTS) - 1)

        # Si quieres bucle infinito, usa:
        # current_wp = (current_wp + 1) % len(WAYPOINTS)

        target = WAYPOINTS[current_wp]
        target_flat = Vec3(target.x, 0, target.z)

    # 3. Calcular ángulo hacia el waypoint
    to_target = (target_flat - pos_flat).normalized()

    forward = DeloRean.forward
    forward_flat = Vec3(forward.x, 0, forward.z).normalized()

    dot = forward_flat.x * to_target.x + forward_flat.z * to_target.z
    det = forward_flat.x * to_target.z - forward_flat.z * to_target.x

    angle_deg = math.degrees(math.atan2(det, dot))
    # angle_deg > 0  → waypoint a la izquierda
    # angle_deg < 0  → waypoint a la derecha

    # 4. Girar suavemente hacia el waypoint
    if abs(angle_deg) > ANGLE_DEADZONE:
        max_step = VEL_GIRO_MAX * time.dt
        giro = max(-max_step, min(max_step, angle_deg))
        DeloRean.rotation_y += giro

    # 5. Avanzar hacia adelante
    forward = DeloRean.forward
    forward_flat = Vec3(forward.x, 0, forward.z).normalized()
    DeloRean.position += forward_flat * VEL_AVANCE * time.dt

    # 6. Volver a ajustar altura (por si cambió ligeramente el nivel)
    ajustar_altura_sobre_pista()
