import streamlit as st
import csv
from io import StringIO

st.set_page_config(page_title="Dayful Prospector Pro", page_icon="✨", layout="wide")

st.title("Dayful Prospector Pro")
st.caption("Prospección útil para branding, SEO, redes y ads.")

DB = {
    "club deportivo": [
        {
            "name": "RC Celta",
            "country": "España",
            "sector": "Club deportivo",
            "signals": {"branding": 82, "seo": 70, "social": 78, "ads": 60},
            "notes": "Buena base de marca, margen para empaquetar mejor activos comerciales.",
            "web": "https://www.rccelta.es",
            "linkedin": "LinkedIn empresa / club",
            "email": "Contacto comercial institucional",
        },
        {
            "name": "Boavista FC",
            "country": "Portugal",
            "sector": "Club deportivo",
            "signals": {"branding": 88, "seo": 58, "social": 69, "ads": 52},
            "notes": "Narrativa histórica potente; oportunidad clara de refresh visual y comercial.",
            "web": "https://boavistafc.pt",
            "linkedin": "LinkedIn / comunicación",
            "email": "Email de administración o prensa",
        },
        {
            "name": "Real Oviedo",
            "country": "España",
            "sector": "Club deportivo",
            "signals": {"branding": 76, "seo": 74, "social": 71, "ads": 57},
            "notes": "Puede mejorar sponsor decks, tienda y embudo digital para abonados.",
            "web": "https://www.realoviedo.es",
            "linkedin": "LinkedIn club",
            "email": "Departamento comercial",
        },
        {
            "name": "Genoa CFC",
            "country": "Italia",
            "sector": "Club deportivo",
            "signals": {"branding": 80, "seo": 63, "social": 77, "ads": 55},
            "notes": "Club histórico con recorrido para campañas editoriales y fan engagement.",
            "web": "https://genoacfc.it",
            "linkedin": "Corporate / media",
            "email": "Área media o corporate",
        },
        {
            "name": "Racing de Ferrol",
            "country": "España",
            "sector": "Club deportivo",
            "signals": {"branding": 84, "seo": 61, "social": 67, "ads": 49},
            "notes": "Gran encaje para elevar imagen, material comercial y narrativa regional.",
            "web": "https://racingclubferrol.net",
            "linkedin": "Club / prensa",
            "email": "Contacto institucional",
        },
    ],
    "hotel": [
        {
            "name": "Memmo Hotels",
            "country": "Portugal",
            "sector": "Hoteles",
            "signals": {"branding": 72, "seo": 84, "social": 79, "ads": 73},
            "notes": "Ideal para SEO internacional y campañas de reserva directa.",
            "web": "https://www.memmohotels.com",
            "linkedin": "LinkedIn empresa",
            "email": "Partnerships / marketing",
        },
        {
            "name": "Room Mate Hotels",
            "country": "España",
            "sector": "Hoteles",
            "signals": {"branding": 68, "seo": 79, "social": 74, "ads": 81},
            "notes": "Muy buen caso para performance, landings y campañas por destino.",
            "web": "https://room-matehotels.com",
            "linkedin": "LinkedIn empresa",
            "email": "Corporate contact",
        },
        {
            "name": "Generator",
            "country": "Europa",
            "sector": "Hostelería",
            "signals": {"branding": 66, "seo": 75, "social": 82, "ads": 78},
            "notes": "Marca urbana que puede explotar más comunidad y paid media geográfica.",
            "web": "https://staygenerator.com",
            "linkedin": "Corporate",
            "email": "Press / partnerships",
        },
        {
            "name": "The Hoxton",
            "country": "Europa",
            "sector": "Hoteles",
            "signals": {"branding": 70, "seo": 77, "social": 80, "ads": 69},
            "notes": "Oportunidad para contenidos de experiencia y activación local.",
            "web": "https://thehoxton.com",
            "linkedin": "Corporate",
            "email": "Marketing contact",
        },
        {
            "name": "Pestana",
            "country": "Portugal",
            "sector": "Hoteles",
            "signals": {"branding": 74, "seo": 83, "social": 65, "ads": 76},
            "notes": "Grupo amplio; mucho potencial para arquitectura de marca y SEO por verticales.",
            "web": "https://www.pestana.com",
            "linkedin": "LinkedIn empresa",
            "email": "Media / partnerships",
        },
    ],
    "restaurante": [
        {
            "name": "Goiko",
            "country": "España",
            "sector": "Restauración",
            "signals": {"branding": 73, "seo": 78, "social": 84, "ads": 80},
            "notes": "Ideal para campañas locales, aperturas y social ads.",
            "web": "https://www.goiko.com",
            "linkedin": "LinkedIn empresa",
            "email": "Expansión / marketing",
        },
        {
            "name": "Honest Greens",
            "country": "Europa",
            "sector": "Restauración",
            "signals": {"branding": 67, "seo": 72, "social": 86, "ads": 77},
            "notes": "Marca fuerte; encaje en paid media local y narrativa por ciudad.",
            "web": "https://www.honestgreens.com",
            "linkedin": "Corporate",
            "email": "Partnerships",
        },
        {
            "name": "Big Mamma",
            "country": "Europa",
            "sector": "Restauración",
            "signals": {"branding": 71, "seo": 69, "social": 82, "ads": 74},
            "notes": "Muy buen caso para employer branding y campañas de eventos.",
            "web": "https://www.bigmammagroup.com",
            "linkedin": "Corporate",
            "email": "Press",
        },
        {
            "name": "Vicio",
            "country": "España",
            "sector": "Restauración",
            "signals": {"branding": 75, "seo": 71, "social": 88, "ads": 84},
            "notes": "Nacida en digital; puede sistematizar marca y performance.",
            "web": "https://vicio.com",
            "linkedin": "LinkedIn empresa",
            "email": "Prensa / corporate",
        },
        {
            "name": "La Mafia se sienta a la mesa",
            "country": "España",
            "sector": "Restauración",
            "signals": {"branding": 83, "seo": 66, "social": 63, "ads": 58},
            "notes": "Buen caso de refresh visual y coordinación por franquicias.",
            "web": "https://lamafia.es",
            "linkedin": "Empresa",
            "email": "Marketing / franquicias",
        },
    ],
    "moda": [
        {
            "name": "Scalpers",
            "country": "España",
            "sector": "Moda",
            "signals": {"branding": 65, "seo": 82, "social": 78, "ads": 80},
            "notes": "Gran encaje para SEO e-commerce y campañas de colección.",
            "web": "https://scalperscompany.com",
            "linkedin": "LinkedIn empresa",
            "email": "Corporate",
        },
        {
            "name": "Parfois",
            "country": "Portugal",
            "sector": "Moda",
            "signals": {"branding": 69, "seo": 80, "social": 75, "ads": 82},
            "notes": "Retail visual ideal para performance y contenidos de producto.",
            "web": "https://www.parfois.com",
            "linkedin": "LinkedIn empresa",
            "email": "Media / partnerships",
        },
        {
            "name": "Sandro",
            "country": "Francia",
            "sector": "Moda",
            "signals": {"branding": 74, "seo": 68, "social": 71, "ads": 66},
            "notes": "Moda premium con potencial en narrativa editorial.",
            "web": "https://fr.sandro-paris.com",
            "linkedin": "Corporate",
            "email": "Press office",
        },
        {
            "name": "Bimba y Lola",
            "country": "España",
            "sector": "Moda",
            "signals": {"branding": 72, "seo": 77, "social": 79, "ads": 73},
            "notes": "Puede reforzar campañas especiales y experiencias digitales.",
            "web": "https://www.bimbaylola.com",
            "linkedin": "Corporate",
            "email": "PR / partnerships",
        },
        {
            "name": "Hackett London",
            "country": "Reino Unido",
            "sector": "Moda",
            "signals": {"branding": 78, "seo": 64, "social": 68, "ads": 62},
            "notes": "Marca heritage con oportunidad de activar mejor social y lanzamientos.",
            "web": "https://www.hackett.com",
            "linkedin": "Corporate",
            "email": "Marketing / media",
        },
    ],
    "general": [
        {
            "name": "Clínica Baviera",
            "country": "España",
            "sector": "Salud",
            "signals": {"branding": 64, "seo": 86, "social": 58, "ads": 79},
            "notes": "Muy buen encaje para SEO local, reputación y campañas lead-gen.",
            "web": "https://www.clinicabaviera.com",
            "linkedin": "LinkedIn empresa",
            "email": "Marketing contact",
        },
        {
            "name": "Spotahome",
            "country": "España",
            "sector": "Proptech",
            "signals": {"branding": 66, "seo": 81, "social": 70, "ads": 83},
            "notes": "Digital-first; buen caso para CRO, paid media y contenidos SEO.",
            "web": "https://www.spotahome.com",
            "linkedin": "Corporate",
            "email": "Partnerships",
        },
        {
            "name": "Hawkers",
            "country": "España",
            "sector": "Moda / e-commerce",
            "signals": {"branding": 79, "seo": 69, "social": 82, "ads": 77},
            "notes": "Caso perfecto para refresh narrativo y nuevas campañas creativas.",
            "web": "https://www.hawkersco.com",
            "linkedin": "LinkedIn empresa",
            "email": "Corporate contact",
        },
        {
            "name": "PortobelloStreet.es",
            "country": "España",
            "sector": "Decoración",
            "signals": {"branding": 74, "seo": 84, "social": 65, "ads": 72},
            "notes": "Muy buen encaje para SEO transaccional y campañas de colección.",
            "web": "https://www.portobellostreet.es",
            "linkedin": "Empresa",
            "email": "Atención comercial",
        },
        {
            "name": "Cabify",
            "country": "España",
            "sector": "Movilidad",
            "signals": {"branding": 61, "seo": 70, "social": 73, "ads": 85},
            "notes": "Gran recorrido para campañas segmentadas, employer branding y landings.",
            "web": "https://cabify.com",
            "linkedin": "Corporate",
            "email": "Prensa / partnerships",
        },
    ],
}


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


def compute_score(signals: dict, focus: str) -> int:
    if focus == "general":
        return round(sum(signals.values()) / len(signals))
    return signals.get(focus, 60)


def suggest_needs(item: dict, focus: str) -> list[str]:
    s = item["signals"]
    needs = []
    if s["branding"] >= 75:
        needs.append("Lavado de imagen, sistema visual y materiales comerciales.")
    if s["seo"] >= 75:
        needs.append("SEO, arquitectura web y landings de conversión.")
    if s["social"] >= 75:
        needs.append("Calendario editorial, comunidad y contenido social.")
    if s["ads"] >= 75:
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


# Sidebar
with st.sidebar:
    st.subheader("Parámetros de búsqueda")
    query = st.text_input("Empresa o sector", "club deportivo")
    country = st.selectbox(
        "País",
        ["", "España", "Portugal", "Francia", "Italia", "Alemania", "Reino Unido", "Países Bajos"],
        index=1,
    )
    focus = st.selectbox("Objetivo", ["general", "branding", "seo", "social", "ads"], index=1)
    priority = st.slider("Prioridad mínima (score)", 0, 100, 50, 5)
    run = st.button("Buscar similares")

if run:
    sector = infer_sector(query)
    base = DB.get(sector, DB["general"])
    rows = []
    for item in base:
        score = compute_score(item["signals"], focus)
        if score < priority:
            continue
        if country and item["country"] not in (country, "Europa"):
            continue
        rows.append(
            {
                "Empresa": item["name"],
                "País": item["country"],
                "Sector": item["sector"],
                "Score": score,
                "Notas": item["notes"],
                "Web": item["web"],
                "LinkedIn": item["linkedin"],
                "Email": item["email"],
                "Necesidades": " | ".join(suggest_needs(item, focus)),
                "Acción sugerida": best_action(score),
            }
        )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Resultados", len(rows))
    col2.metric("Sector", sector)
    col3.metric("Alta prioridad", sum(1 for r in rows if r["Score"] >= 75))
    col4.metric(
        "Acción recomendada",
        best_action(rows[0]["Score"]) if rows else "—",
    )

    st.subheader("Leads sugeridos")
    if not rows:
        st.info("No hay resultados con esos filtros. Prueba con menos prioridad o sin país.")
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
            file_name="dayful_prospects.csv",
            mime="text/csv",
        )

        st.markdown("---")
        st.markdown("### Detalle de cada lead")
        for r in rows:
            with st.expander(f"{r['Empresa']} · {r['País']} · Score {r['Score']}"):
                st.write(r["Notas"])
                st.write("**Necesidades potenciales**")
                for need in r["Necesidades"].split(" | "):
                    st.markdown(f"- {need}")
                st.write("**Contacto**")
                st.markdown(f"- Web: {r['Web']}")
                st.markdown(f"- LinkedIn: {r['LinkedIn']}")
                st.markdown(f"- Email: {r['Email']}")
                st.write(f"**Acción sugerida:** {r['Acción sugerida']}")
else:
    st.info("Configura los parámetros en la barra lateral y pulsa 'Buscar similares'.")
