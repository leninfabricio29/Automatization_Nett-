#from config.db_config import DatabaseConfig

#def save_turnos(documents: list[dict]) -> int:
#    db = DatabaseConfig.get_database()
#    result = db.turnos.insert_many(documents, ordered=False)
#    return len(result.inserted_ids)
from pymongo import UpdateOne
from config.db_config import DatabaseConfig

def save_turnos(documents: list[dict]) -> int:
    db = DatabaseConfig.get_database()
    collection = db.turnos

    operaciones = []

    for turno in documents:


        
        operaciones.append(
            UpdateOne(
                {"turno_id": turno["turno_id"]},
                {
                    
                    "$setOnInsert": {
                        "turno_id": turno["turno_id"],
                        
                    },

                    #Si turno Asignado y solucion Null entonces estado @pendiente

                    

                    # Campos que pueden CAMBIAR con el tiempo
                    "$set": {

                        "codigo": turno.get("codigo"),
                        "area": turno.get("area"),
                        "responsables": turno.get("responsables"),
                        "modulo": turno.get("modulo"),
                        "estado": turno.get("estado"),
                        "fecha_creacion": turno.get("fecha_creacion"),
                        "solucion": turno.get("solucion"),
                        "metadata": turno.get("metadata"),

                    }
                
                },
                upsert=True
            )
        )

    if not operaciones:
        return 0, 0

    result = collection.bulk_write(operaciones, ordered=False)

    # Devuelve cuántos turnos NUEVOS se insertaron
    return result.upserted_count, result.modified_count


def save_contracts(documents: list[dict]) -> int:
    db = DatabaseConfig.get_database()
    collection = db.contratos

    operaciones = []

    for contrato in documents:

        
        operaciones.append(
            UpdateOne(
                {"contrato_id": contrato["contrato_id"]},
                {
                    
                    "$setOnInsert": {
                        "contrato_id": contrato["contrato_id"],

                    },


                    # Campos que pueden CAMBIAR con el tiempo
                    "$set": {

                        #"actividades": contrato.get("actividades"),
                        "fecha_creacion": contrato.get("fecha_creacion"),
                        "cliente": contrato.get("cliente"),
                        "codigo": contrato.get("codigo"),
                        "estado_ct": contrato.get("estado_ct"),
                        "etiquetas": contrato.get("etiquetas"),
                        "proxima_factura": contrato.get("proxima_factura"),
                        "forma_pago": contrato.get("forma_pago"),
                        "monto_deuda": contrato.get("monto_deuda"),
                        "plan_internet": contrato.get("plan_internet"),
                        "plan_internet_precio_unitario": contrato.get("plan_internet_precio_unitario"),
                        "estado_servicio": contrato.get("estado_servicio"),
                        "metadata": contrato.get("metadata"),

                    }
                
                },
                upsert=True
            )
        )

    if not operaciones:
        return 0, 0

    result = collection.bulk_write(operaciones, ordered=False)

    # Devuelve cuántos turnos NUEVOS se insertaron
    return result.upserted_count, result.modified_count

def save_visits(documents: list[dict]) -> int:
    db = DatabaseConfig.get_database()
    collection = db.visitas

    operaciones = []

    for visita in documents:

        
        operaciones.append(
            UpdateOne(
                {"ticket_id": visita["ticket_id"]},
                {
                    
                    "$setOnInsert": {
                        "ticket_id": visita["ticket_id"],

                    },


                    # Campos que pueden CAMBIAR con el tiempo
                    "$set": {

                        #"actividades": contrato.get("actividades"),
                        "categoria": visita.get("categoria"),
                        "creado_en": visita.get("creado_en"),
                        "email": visita.get("email"),
                        "etapa": visita.get("etapa"),
                        "fecha_asignacion": visita.get("fecha_asignacion"),
                        "fecha_cierre": visita.get("fecha_cierre"),
                        "nombre_empresa": visita.get("nombre_empresa"),
                        "numero_ticket": visita.get("numero_ticket"),
                        "prioridad": visita.get("prioridad"),
                        "titulo": visita.get("titulo"),
                        "usuario_asignado": visita.get("usuario_asignado"),
                        "ultima_actualizacion_etapa": visita.get("ultima_actualizacion_etapa"),
                        "metadata": visita.get("metadata"),

                    }
                
                },
                upsert=True
            )
        )

    if not operaciones:
        return 0, 0

    result = collection.bulk_write(operaciones, ordered=False)

    # Devuelve cuántos turnos NUEVOS se insertaron
    return result.upserted_count, result.modified_count