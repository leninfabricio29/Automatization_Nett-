from datetime import datetime, UTC
import pandas as pd

def transform_turnos(df, filename: str) -> list[dict]:
    documentos = []

    for _, row in df.iterrows():
        area, ciudad = (row["area_id"].split(" - ") + [None])[:2]
        solucion = row["turn_solution"]
        if pd.isna(solucion) or str(solucion).strip() == "":
            solucion = None

        modulo = row["module_id"]
        if pd.isna(modulo) or str(modulo).strip() == "":
            modulo = None

        documentos.append({
            "turno_id": row["id"],
            "codigo": row["display_name"],
            "area": {
                "nombre": area,
                "ciudad": ciudad
            },
            "responsables": {
                "asignado": row["assigned_id"],
                "administrativo": row["user_id"]
            },
            "modulo": modulo,
            "estado": row["state"],
            "fecha_creacion": datetime.fromisoformat(row["time_create_turn"]),
            "solucion": solucion,
            "metadata": {
                "origen": "odoo",
                "archivo": filename,
                "fecha_proceso": datetime.now(UTC)
            }
        })

    return documentos


def transform_contracts(df, filename: str) -> list[dict]:
    contratos = []

    for _, row in df.iterrows():
        partner = row["partner_id"]
        if isinstance(partner, str) and partner.strip():
            cliente, nombres = (partner.split(" - ") + [None, None])[:2]
        else:
            cliente, nombres = None, None

        facture = row["recurring_next_date"]
        if isinstance(facture, str) and facture.strip():
            proxima_factura = datetime.fromisoformat(facture)
        else:
            proxima_factura = None   

        etiquetas = row["tag_ids"]
        if pd.isna(etiquetas) or str(etiquetas).strip() == "":
            etiquetas = None
        #activity = row["activity_ids"]
        #if pd.isna(activity) or str(activity).strip() == "":
            #activity = None

        contratos.append({
            "contrato_id": row["id"],
            #"actividades": activity,
            "fecha_creacion": datetime.fromisoformat(row["create_date"]),
            "cliente": {
                "cedula": cliente,
                "nombres": nombres
            },
            "codigo": row["name"],
            "estado_ct": row["state"],
            "etiquetas": etiquetas,
            "proxima_factura": proxima_factura,
            "forma_pago": row["payment_type_id"],
            "monto_deuda": row["contract_invoice_amount"],
            "plan_internet": row["contract_line_id"],
            "plan_internet_precio_unitario": row["contract_line_id/price_unit"],
            "estado_servicio": row["state_service"],
            "metadata": {
                "origen": "odoo",
                "archivo": filename,
                "fecha_proceso": datetime.now(UTC)
            }
        })

    return contratos

def transform_visits(df, filename: str) -> list[dict]:
    visitas = []

    for _, row in df.iterrows():
        
        #facture = row["recurring_next_date"]
        #if isinstance(facture, str) and facture.strip():
            #proxima_factura = datetime.fromisoformat(facture)
        #else:
            #proxima_factura = None   
        closed = row["closed_date"]
        if isinstance(closed, str) and closed.strip():
            closed = datetime.fromisoformat(closed)
        else:
            closed = None

        categoria = row["category_id"]
        if pd.isna(categoria) or str(categoria).strip() == "":
            categoria = None


        visitas.append({
            "ticket_id": row["id"],
            
            "categoria": categoria,
            "creado_en": datetime.fromisoformat(row["create_date"]),
            "email": row["partner_email"],
            "etapa": row["stage_id"],
            "fecha_asignacion": datetime.fromisoformat(row["assigned_date"]),
            "fecha_cierre": closed,
            "nombre_empresa": row["partner_name"],
            "numero_ticket": row["number"],
            "prioridad": row["priority"],
            "titulo": row["name"],
            "usuario_asignado": row["user_id"],
            "ultima_actualizacion_etapa": datetime.fromisoformat(row["last_stage_update"]),
            "metadata": {
                "origen": "odoo",
                "archivo": filename,
                "fecha_proceso": datetime.now(UTC)
            }

        })

    return visitas
