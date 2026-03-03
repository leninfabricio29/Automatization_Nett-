# etl/repository/metricas_repository.py

from datetime import datetime, UTC
from config.db_config import DatabaseConfig


def save_metricas_mensuales(
    anio: int,
    mes: int,
    area: str,
    dia: int,
    metricas: dict
) -> None:
    """
    Guarda o actualiza métricas mensuales de turnos.

    - Un documento por (anio, mes, area)
    - Un nodo por día
    - Sobrescribe si el día ya existe
    """

    db = DatabaseConfig.get_database()

    filtro = {
        "anio": anio,
        "mes": mes,
        "area": area
    }

    update = {
        "$set": {
            f"dias.{dia}": metricas,
            "ultima_actualizacion":  datetime.now(UTC)
        }
    }

    db.metricas_operaciones.update_one(
        filtro,
        update,
        upsert=True
    )
