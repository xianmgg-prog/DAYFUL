import streamlit as st
import csv
from io import StringIO
import requests

# =====================================
# CONFIG GENERAL
# =====================================

st.set_page_config(page_title="Dayful Prospector Pro (Scoris)", page_icon="✨", layout="wide")

st.title("Dayful Prospector Pro (Scoris)")
st.caption("Prospección útil para branding, SEO, redes y ads, usando datos de empresas de Scoris.")

# URL base y API key de Scoris
SCORIS_BASE_URL = "https://scoris.eu/api/v1/company-search/"
SCORIS_API_KEY = "alyE_mjsIkDocXbQwWbYNJ6mgwcDm4SFo8NpUqrjS0I"  # ponla en st.secrets en producción


# =====================================
# FUNCIONES DE LÓGICA
# =====================================

def infer_sector(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["club", "deportivo", "futbol", "baloncesto", "tenis", "sport"]):
        return "club deportivo"
    if any(k in t for k in ["hotel", "hostel", "resort", "alojamiento"]):
        return "hotel"
    if any(k in t for k in ["restaurante", "burger", "pizza", "café", "food", "bar"]):
        return "restaurante"
    if any(k in t for k in ["moda", "ropa", "fashion", "gafas", "calzado", "retail"]):
        return "moda"
    return "general"


def fetch_empresas_scoris(query: str, country: str | None = None, limit: int = 50) -> list[dict]:
    """
    Llama al endpoint company-search de Scoris.
    - query: texto de búsqueda (nombre, código, dominio...)
    - country: código de país (UK, SE, FI, EE, LT, LV) o None
    """
    params = {
        "q": query,   # ajusta si los docs usan otro parámetro
        "limit": limit,
    }
    if country:
        params["country"] = country  # según docs de Scoris: country=LT/SE/...

    headers = {"X-API-Key": SCORIS_API_KEY}

    try:
        resp = requests.get(SCORIS_BASE_URL, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        st.error(f"Error al llamar a Scoris: {e}")
        return []

    empresas = []
    for item in data:
        # Ajusta los nombres de campo según la respuesta real de Scoris
        empresas.append(
            {
                "nombre": item.get("name", "Sin nombre"),
                "pais": item.get("country", item.get("country_code", "")),
                "regcode": item.get("regcode", ""),
                "sector_raw": item.get("nace_description", item.get("nace_code", "")),
                "web": item.get("website", ""),
                "ciudad": item.get("municipality", ""),
            }
        )
    return empresas


def compute_signals_for_item(item: dict, sector_inferido: str) -> dict:
    """
    Genera un scoring de branding/SEO/social/ads para cada empresa.
    Heurístico y simple; puedes refinarlo cuando veas datos reales.
    """
    # SEO: si tiene web => buena base
    base_seo = 75 if item.get("web") else 50

    # Social: si el sector que buscamos es B2C (restaurante/hotel/moda), subimos
    if sector_inferido in ("restaurante", "hotel", "moda"):
        base_social = 78
    else:
        base_social = 60

    # Branding: puedes usar sector_raw para afinar
    branding = 70
    if "sport" in (item.get("sector_raw", "").lower()):
        branding = 75

    signals = {
        "branding": branding,
        "seo": base_seo,
        "social": base_social,
        "ads": 65,
    }
    return signals


def compute_score(signals: dict, focus: str) -> int:
    if focus == "general":
        return round(sum(signals.values()) / len(signals))
    return signals.get(focus, 60)


def suggest_needs(signals: dict, focus: str) -> list[str]:
    needs = []
    if signals["branding"] >= 75:
        needs.append("Lavado de imagen, sistema visual y materiales comerciales.")
    if signals["seo"] >= 75:
        needs.append("SEO, arquitectura web y landings de conversión.")
    if signals["social"] >= 75:
        needs.append("Calendario editorial, comunidad y contenido social.")
    if signals["ads"] >= 75:
        needs.append("Campañas geolocalizadas y paid media orientado a resultados.")
    if not needs:
        needs.append("Propuesta integrada de branding, SEO, redes y ads.")
    if focus != "general":
        label = {
            "branding": "branding",
            "seo": "SEO y web",
            "social": "redes sociales",
            "ads": "publicidad digital",
        }
        needs.insert(0, f"Prioridad recomendada: {label.get(focus, 'general')}.")
    return needs


def best_action(score: int) -> str:
    if score >= 80:
        return "Contactar esta semana"
    if score >= 65:
        return "Investigar contacto y preparar propuesta"
    return "Mantener en seguimiento"


# =====================================
# UI STREAMLIT
# =====================================

with st.sidebar:
    st.subheader("Parámetros de búsqueda (Scoris)")
    query = st.text_input("Texto de búsqueda (nombre, dominio, etc.)", "restaurant")
    country = st.selectbox(
        "País (Scoris)",
        ["", "UK", "SE", "FI", "EE", "LT", "LV"],
        index=1,
    )
    focus = st.selectbox("Objetivo", ["general", "branding", "seo", "social", "ads"], index=1)
    priority = st.slider("Prioridad mínima (score)", 0, 100, 50, 5)
    limit = st.slider("Máximo de empresas desde Scoris", 10, 100, 50, 10)
    run = st.button("Buscar empresas (Scoris)")

if run:
    # Inferimos sector interno (para adaptar scoring)
    sector_inferido = infer_sector(query)

    empresas_api = fetch_empresas_scoris(query, country or None, limit=limit)

    if not empresas_api:
        st.info("No se han recibido empresas desde Scoris. Revisa parámetros, país o la API key.")
    else:
        rows = []
        for item in empresas_api:
            signals = compute_signals_for_item(item, sector_inferido)
            score = compute_score(signals, focus)
            if score < priority:
                continue
            needs_list = suggest_needs(signals, focus)
            rows.append(
                {
                    "Empresa": item["nombre"],
                    "País": item["pais"],
                    "Código registro": item["regcode"],
                    "Ciudad": item["ciudad"],
                    "Sector (NACE)": item["sector_raw"],
                    "Score": score,
                    "Web": item["web"],
                    "Necesidades": " | ".join(needs_list),
                    "Acción sugerida": best_action(score),
                }
            )

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Resultados", len(rows))
        col2.metric("Sector inferido", sector_inferido)
        col3.metric("Alta prioridad", sum(1 for r in rows if r["Score"] >= 75))
        col4.metric(
            "Acción recomendada",
            best_action(rows[0]["Score"]) if rows else "—",
        )

        st.subheader("Leads sugeridos (Scoris)")
        if not rows:
            st.info("No hay resultados con esos filtros. Prueba con menor prioridad o más límite.")
        else:
            st.dataframe(rows, use_container_width=True)

            # CSV export
            csv_buffer = StringIO()
            writer = csv.DictWriter(csv_buffer, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
            st.download_button(
                "Descargar CSV",
                data=csv_buffer.getvalue(),
                file_name="dayful_prospects_scoris.csv",
                mime="text/csv",
            )

            st.markdown("---")
            st.markdown("### Detalle de cada lead")
            for r in rows:
                with st.expander(f"{r['Empresa']} · {r['País']} · Score {r['Score']}"):
                    st.write(f"**Sector (NACE)**: {r['Sector (NACE)']}")
                    st.write("**Necesidades potenciales**")
                    for need in r["Necesidades"].split(" | "):
                        st.markdown(f"- {need}")
                    st.write("**Contacto**")
                    st.markdown(f"- Web: {r['Web']}" if r["Web"] else "- Web: (no disponible)")
                    if r["Ciudad"]:
                        st.markdown(f"- Ciudad: {r['Ciudad']}")
                    st.write(f"**Acción sugerida:** {r['Acción sugerida']}")
else:
    st.info("Configura los parámetros en la barra lateral y pulsa 'Buscar empresas (Scoris)'.")
