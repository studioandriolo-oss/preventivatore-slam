import streamlit as st

# Impostazioni grafiche della pagina
st.set_page_config(page_title="Preventivatore SLAM", page_icon="logo.png", layout="centered")

# --- SEZIONE LOGO CENTRATO ---
st.markdown('<style>[data-testid="stImage"] {display: flex; justify-content: center;}</style>', unsafe_allow_html=True)
st.image("logo.png", width=150)
st.title("Calcolatore Rilievi 3D")
st.write("Generatore rapido di preventivi per rilievi architettonici con tecnologia SLAM.")
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

# --- IMMAGINE DINAMICA CHE CAMBIA 2 ---
    if geometria == "Ortogonale":
        st.image("ortogonale.jpg", caption="Esempio edificio ortogonale")
    else:
        st.image("irregolare.jpg", caption="Esempio Spazi Storico / Irregolare")

# CALCOLO FINALE
totale_moltiplicatori_complessita = molt_spazi * molt_luoghi * molt_geom

# Calcolo totale (Prezzo Base * Moltiplicatore Servizio * Moltiplicatori Complessità)
preventivo_totale = prezzo_base * molt_servizio * totale_moltiplicatori_complessita

st.divider()

# --- MOTORE CALCOLO TEMPI DI CONSEGNA ---
# Calcolo moltiplicatore tempo in base alla superficie
if superficie <= 499:
    molt_superficie_tempo = 1.0
elif superficie <= 999:
    molt_superficie_tempo = 1.5
elif superficie <= 2999:
    molt_superficie_tempo = 2.0
elif superficie <= 4999:
    molt_superficie_tempo = 2.5
else:
    molt_superficie_tempo = 3.0

# Matrice: [Riga Servizio] incrocia [Colonna Spazi]
matrice_tempi = {
    "SMART (Rilievo, elaborazione nuvola di punti)": {"Open Space": 3, "Standard": 3, "Frammentato": 3},
    "TECNICO (Smart + planimetrie CAD 2D di alta precisione)": {"Open Space": 5, "Standard": 7, "Frammentato": 7},
    "BIM (Smart + modellazione parametrica intelligente)": {"Open Space": 5, "Standard": 10, "Frammentato": 15},
    "VISUAL (Smart + Virtual Tour 360° immersivo)": {"Open Space": 5, "Standard": 5, "Frammentato": 5},
    "TECNICO + VISUAL": {"Open Space": 7, "Standard": 9, "Frammentato": 9},
    "BIM + VISUAL": {"Open Space": 8, "Standard": 13, "Frammentato": 18}
}

# Estrapolazione giorni base e calcolo finale arrotondato per eccesso
giorni_base = matrice_tempi[servizio][spazi]
giorni_stimati = int((giorni_base * molt_superficie_tempo) + 0.99)

# --- BOX RISULTATI IMPAGINATO ---
res_col1, res_col2 = st.columns(2)
with res_col1:
    st.subheader("💶 PREVENTIVO STIMATO")
    st.markdown(f"### **{preventivo_totale:,.2f} €**")
    
with res_col2:
    st.subheader("⏳ TEMPI DI CONSEGNA")
    st.markdown(f"### **{giorni_stimati} giorni**")
    
st.caption("Iva e cassa escluse.")
st.caption("Il calcolo non include eventuali spese di trasferta con partenza da Noventa Vicentina se distanza superiore a 100km.")


# --- SEZIONE RICHIESTA SOPRALLUOGO (INVIO EMAIL) ---
st.divider()
st.subheader("📍 Richiedi un Sopralluogo")
st.write("Inserisci l'indirizzo dell'immobile e inviaci i dati calcolati per fissare un sopralluogo.")

# Campo per inserire l'indirizzo
indirizzo = st.text_input("Indirizzo esatto dell'immobile da rilevare (Via, Civico, Città):")

# Il pulsante appare solo se l'utente ha scritto un indirizzo
if indirizzo:
    # Costruiamo il testo dell'email
    oggetto = f"Richiesta Sopralluogo Rilievo 3D - {indirizzo}"
    corpo_email = f"""Buongiorno,
desidero richiedere un sopralluogo per un rilievo architettonico.

L'immobile si trova in: {indirizzo}

Di seguito il riepilogo dei parametri inseriti nel calcolatore:
- Superficie: {superficie} mq
- Tipologia Servizio: {servizio}
- Complessita': Spazi {spazi}, Luoghi {luoghi}, Geometria {geometria}

- PREVENTIVO STIMATO: {preventivo_totale:,.2f} Euro
- TEMPI STIMATI: {giorni_stimati} giorni

In attesa di un vostro riscontro per definire i dettagli, porgo cordiali saluti.
"""
    
    # Importiamo la libreria per trasformare il testo in formato "Link" 
    import urllib.parse
    corpo_codificato = urllib.parse.quote(corpo_email)
    oggetto_codificato = urllib.parse.quote(oggetto)
    
    # Creiamo il link che fa aprire il programma di posta
    link_mail = f"mailto:studioandriolo@gmail.com?subject={oggetto_codificato}&body={corpo_codificato}"
    
    # Pulsante per inviare
    st.link_button("✉️ Invia Richiesta Sopralluogo", link_mail, use_container_width=True)
else:
    st.info("👆 Inserisci l'indirizzo qui sopra per abilitare il pulsante di invio email.")
