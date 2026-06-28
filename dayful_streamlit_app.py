import requests
import streamlit as st

OPENMERCANTIL_BASE_URL = "https://openmercantil.es/api/companies"  # revisa la doc real

def fetch_empresas_openmercantil(query: str, province: str | None = None, limit: int = 50) -> list[dict]:
    """
    Llama a la API de OpenMercantil para obtener empresas españolas
    que coincidan con el criterio `query` (nombre, actividad, etc.).
    Ajusta parámetros y parsing según la documentación real.
    """
    params = {
        "query": query,
        "limit": limit,
    }
    if province:
        params["province"] = province  # TODO: ajusta al parámetro real (provincia, comunidad, etc.)

    try:
        resp = requests.get(OPENMERCANTIL_BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        st.error(f"Error al llamar a OpenMercantil: {e}")
        return []

    empresas = []
    for item in data:
        # Ajusta según el modelo que devuelva OpenMercantil
        empresas.append(
            {
                "nombre": item.get("name", "Sin nombre"),
                "pais": "España",
                "ciudad": item.get("municipality", ""),
                "sector": item.get("cnae_description", ""),  # puedes mapearlo luego a club/hotel/restaurante
                "web": "",  # OpenMercantil probablemente no da web; la tendrías que añadir tú
                "direccion": item.get("address", ""),
                "nif": item.get("nif", ""),
            }
        )
    return empresas
