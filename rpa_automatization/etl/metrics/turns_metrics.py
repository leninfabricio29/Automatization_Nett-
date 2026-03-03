# etl/metrics/turnos_metrics.py

from typing import List, Dict
from collections import defaultdict

TURNO_PERDIDO_VALUE = {
    "TURNO PERDIDO",
    "TURNO USADOPOR OTRO ASESOR, TURNO PERDIDO",
    None
}



def calcular_metricas_turnos(turnos: List[Dict]) -> Dict:
    """
    Calcula métricas de turnos a partir de una lista de turnos transformados.

    Reglas:
    - turnos_entregados: total de turnos
    - turnos_perdidos: solucion == "Turno Perdido"
    - turnos_atendidos: entregados - perdidos
    - porcentaje_turnos_perdidos: (perdidos / entregados) * 100

    Args:
        turnos (List[Dict]): lista de turnos transformados

    Returns:
        Dict: métricas calculadas
    """

    turnos_entregados = len(turnos)

    turnos_perdidos = sum(
        1 for turno in turnos
        #if turno.get("solucion") == TURNO_PERDIDO_VALUE
        if turno.get("solucion") in TURNO_PERDIDO_VALUE
    )

    turnos_atendidos = turnos_entregados - turnos_perdidos

    porcentaje_turnos_perdidos = (
        round((turnos_perdidos / turnos_entregados) * 100, 2)
        if turnos_entregados > 0
        else 0.0
    )

    return {
        "turnos_entregados": turnos_entregados,
        "turnos_atendidos": turnos_atendidos,
        "turnos_perdidos": turnos_perdidos,
        "porcentaje_turnos_perdidos": porcentaje_turnos_perdidos
    }


AREA_MAPPING = {
    "SERVICIO AL CLIENTE": "Gestión Ventas y Servicio",
    "SOPORTE TECNICO": "Gestión Soporte Técnico",
    "PAGOS Y COBRANZAS": "Gestión Pagos"
}

def agrupar_turnos_por_area(turnos: list[dict]) -> dict:
    """
    Agrupa turnos transformados por área destino.
    """
    agrupados = defaultdict(list)

    for turno in turnos:
        area_origen = turno.get("area", {}).get("nombre")

        area_destino = AREA_MAPPING.get(area_origen)
        if not area_destino:
            continue  # área no reconocida

        agrupados[area_destino].append(turno)

    return agrupados