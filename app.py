import streamlit as st

# Impostazioni grafiche della pagina
st.set_page_config(page_title="Preventivatore SLAM", page_icon="📐", layout="centered")

st.title("📐 Calcolatore Rilievi 3D SLAM")
st.write("Generatore rapido di preventivi per rilievi architettonici.")
st.divider()

# SEZIONE 1: Superficie e Prezzo Base
st.subheader("1. Dimensioni Immobile")
superficie = st.number_input("Inserisci la Superficie (mq)", min_value=1, value=150, step=10)

# Motore di calcolo scaglioni
if superficie <= 99:
    prezzo_base = 200
elif superficie <= 499:
    prezzo_base = 318
elif superficie <= 999:
    prezzo_base = 790
elif superficie <= 2999:
    prezzo_base = 1380
elif superficie <= 4999:
    prezzo_base = 3740
elif superficie <= 9999:
    prezzo_base = 6100
else:
    prezzo_base = 12000

st.info(f"Quota Base per {superficie} mq: **{prezzo_base} €**")

# SEZIONE 2: Tipologia Servizio
st.subheader("2. Tipologia Servizio")
servizio = st.selectbox("Seleziona il livello di restituzione grafica", [
    "SMART (Rilievo, elaborazione nuvola di punti)",
    "TECNICO (Smart + planimetrie CAD 2D di alta precisione)",
    "BIM (Smart + modellazione parametrica intelligente)",
    "VISUAL (Smart + Virtual Tour 360° immersivo)",
    "TECNICO + VISUAL",
    "BIM + VISUAL"
])

# Assegnazione dei parametri estratti dal tuo listino
dati_servizi = {
    "SMART (Rilievo, elaborazione nuvola di punti)": {"min": 1.2, "max": 3},
    "TECNICO (Smart + planimetrie CAD 2D di alta precisione)": {"min": 3.5, "max": 6},
    "BIM (Smart + modellazione parametrica intelligente)": {"min": 8, "max": 15},
    "VISUAL (Smart + Virtual Tour 360° immersivo)": {"min": 3, "max": 4.5},
    "TECNICO + VISUAL": {"min": 4.5, "max": 7},
    "BIM + VISUAL": {"min": 9, "max": 16}
}
molt_servizio_min = dati_servizi[servizio]["min"]
molt_servizio_max = dati_servizi[servizio]["max"]

# SEZIONE 3: Complessità del Rilievo
st.subheader("3. Complessità del Rilievo")
col1, col2, col3 = st.columns(3)

with col1:
    spazi = st.selectbox("Tipologia Spazi", ["Open Space", "Standard", "Frammentato"])
    molt_spazi = 1.0 if spazi == "Open Space" else (1.15 if spazi == "Standard" else 1.3)

with col2:
    luoghi = st.selectbox("Tipologia Luoghi", ["Al Grezzo", "Arredato", "Ingombrato/Riflessi"])
    molt_luoghi = 1.0 if luoghi == "Al Grezzo" else (1.1 if luoghi == "Arredato" else 1.25)

with col3:
    geometria = st.selectbox("Geometria", ["Ortogonale", "Storico / Irregolare"])
    molt_geom = 1.0 if geometria == "Ortogonale" else 1.4

# CALCOLO FINALE
totale_moltiplicatori_complessita = molt_spazi * molt_luoghi * molt_geom

# Calcolo del range (Prezzo Base * Moltiplicatore Servizio * Moltiplicatori Complessità)
preventivo_minimo = prezzo_base * molt_servizio_min * totale_moltiplicatori_complessita
preventivo_massimo = prezzo_base * molt_servizio_max * totale_moltiplicatori_complessita

st.divider()
st.subheader("💶 PREVENTIVO STIMATO:")
st.markdown(f"### Da **{preventivo_minimo:,.2f} €** a **{preventivo_massimo:,.2f} €**")
st.caption("Iva e cassa escluse. Il calcolo non include eventuali spese di trasferta con partenza da Noventa Vicentina in caso di distanze superiori a 100km.")
