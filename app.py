import streamlit as st

# Impostazioni grafiche della pagina
st.set_page_config(page_title="Preventivatore SLAM", page_icon="📐", layout="centered")

# --- SEZIONE LOGO ---
st.image("logo.png", width=150)
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
    prezzo_base = 298
elif superficie <= 999:
    prezzo_base = 690
elif superficie <= 2999:
    prezzo_base = 1180
elif superficie <= 4999:
    prezzo_base = 3140
elif superficie <= 9999:
    prezzo_base = 5100
else:
    prezzo_base = 10000

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

# Assegnazione del moltiplicatore fisso per ogni servizio
dati_servizi = {
    "SMART (Rilievo, elaborazione nuvola di punti)": 1.0,
    "TECNICO (Smart + planimetrie CAD 2D di alta precisione)": 2,
    "BIM (Smart + modellazione parametrica intelligente)": 3,
    "VISUAL (Smart + Virtual Tour 360° immersivo)": 1.5,
    "TECNICO + VISUAL": 2.5,
    "BIM + VISUAL": 3.5
}
molt_servizio = dati_servizi[servizio]

# SEZIONE 3: Complessità del Rilievo
st.subheader("3. Complessità del Rilievo")
col1, col2, col3 = st.columns(3)

with col1:
    spazi = st.selectbox("Tipologia Spazi", ["Open Space", "Standard", "Frammentato"])
    molt_spazi = 1.0 if spazi == "Open Space" else (1.15 if spazi == "Standard" else 1.3)

# --- IMMAGINE DINAMICA CHE CAMBIA ---
    if spazi == "Open Space":
        st.image("open.jpg", caption="Esempio Open Space")
    elif spazi == "Standard":
        st.image("standard.jpg", caption="Esempio Residenziale Standard")
    else:
        st.image("frammentato.jpg", caption="Esempio Spazi Frammentati")

with col2:
    luoghi = st.selectbox("Tipologia Luoghi", ["Al Grezzo", "Arredato", "Ingombrato/Riflessi"])
    molt_luoghi = 1.0 if luoghi == "Al Grezzo" else (1.1 if luoghi == "Arredato" else 1.25)

with col3:
    geometria = st.selectbox("Geometria", ["Ortogonale", "Storico / Irregolare"])
    molt_geom = 1.0 if geometria == "Ortogonale" else 1.4

# CALCOLO FINALE
totale_moltiplicatori_complessita = molt_spazi * molt_luoghi * molt_geom

# Calcolo totale (Prezzo Base * Moltiplicatore Servizio * Moltiplicatori Complessità)
preventivo_totale = prezzo_base * molt_servizio * totale_moltiplicatori_complessita

st.divider()
st.subheader("💶 PREVENTIVO STIMATO:")
st.markdown(f"### **{preventivo_totale:,.2f} €**")
st.caption("Iva e cassa escluse. Il calcolo non include eventuali spese di trasferta con partenza da Noventa Vicentina se distanza superiore a 100km.")
