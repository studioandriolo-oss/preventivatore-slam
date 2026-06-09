import streamlit as st

# Impostazioni grafiche della pagina
st.set_page_config(page_title="Preventivatore SLAM", page_icon="logo.png", layout="centered")

# --- SEZIONE LOGO CENTRATO ---
st.markdown('<style>[data-testid="stImage"] {display: flex; justify-content: center;}</style>', unsafe_allow_html=True)
st.image("logo.png", width=150)
st.title("Calcolatore Rilievi 3D")
st.write("Generatore rapido preventivi per scansioni architettoniche con tecnologia SLAM.")
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

# --- IMMAGINE DINAMICA CHE CAMBIA SPAZI ---
    if spazi == "Open Space":
        st.image("open.jpg", caption="Esempio Open Space")
    elif spazi == "Standard":
        st.image("standard.jpg", caption="Esempio Residenziale Standard")
    else:
        st.image("frammentato.jpg", caption="Esempio Spazi Frammentati")

with col2:
    luoghi = st.selectbox("Tipologia Luoghi", ["Al Grezzo", "Arredato", "Ingombrato/Riflessi"])
    molt_luoghi = 1.0 if luoghi == "Al Grezzo" else (1.1 if luoghi == "Arredato" else 1.25)

# --- IMMAGINE DINAMICA CHE CAMBIA LUOGHI ---
    if luoghi == "Al Grezzo":
        st.image("grezzo.jpg", caption="Esempio stanza Al Grezzo")
    elif luoghi == "Arredato":
        st.image("arredato.JPG", caption="Esempio Stanza Arredata")
    else:
        st.image("ingombrato.JPG", caption="Esempio Stanza ingombrata")

with col3:
    geometria = st.selectbox("Geometria", ["Ortogonale", "Storico / Irregolare"])
    molt_geom = 1.0 if geometria == "Ortogonale" else 1.4

# --- IMMAGINE DINAMICA CHE CAMBIA GEOMETRIA ---
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

# --- CALCOLO FINALE PREVENTIVO ---
totale_moltiplicatori_complessita = molt_spazi * molt_luoghi * molt_geom

# Calcolo Imponibile (Prezzo Base * Moltiplicatore Servizio * Moltiplicatori Complessità)
imponibile = prezzo_base * molt_servizio * totale_moltiplicatori_complessita

# Calcolo Tasse e Prezzo Finito
cassa = imponibile * 0.04  # Cassa al 4%
subtotale = imponibile + cassa
iva = subtotale * 0.22     # Iva al 22% calcolata su Imponibile + Cassa
prezzo_finito = subtotale + iva

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

matrice_tempi = {
    "SMART (Rilievo, elaborazione nuvola di punti)": {"Open Space": 3, "Standard": 3, "Frammentato": 3},
    "TECNICO (Smart + planimetrie CAD 2D di alta precisione)": {"Open Space": 5, "Standard": 7, "Frammentato": 7},
    "BIM (Smart + modellazione parametrica intelligente)": {"Open Space": 5, "Standard": 10, "Frammentato": 15},
    "VISUAL (Smart + Virtual Tour 360° immersivo)": {"Open Space": 5, "Standard": 5, "Frammentato": 5},
    "TECNICO + VISUAL": {"Open Space": 7, "Standard": 9, "Frammentato": 9},
    "BIM + VISUAL": {"Open Space": 8, "Standard": 13, "Frammentato": 18}
}

giorni_base = matrice_tempi[servizio][spazi]
giorni_stimati = int((giorni_base * molt_superficie_tempo) + 0.99)

# --- BOX RISULTATI IMPAGINATO ---
res_col1, res_col2 = st.columns(2)

with res_col1:
    st.subheader("💶 PREVENTIVO FINITO")
    st.markdown(f"### **{prezzo_finito:,.2f} €**")
    
with res_col2:
    st.subheader("⏳ TEMPI DI CONSEGNA")
    st.markdown(f"### **{giorni_stimati} giorni**")

# Aggiungo una riga in piccolo per mostrare la composizione del prezzo
st.caption(f"Imponibile: {imponibile:,.2f} € | Cassa (4%): {cassa:,.2f} € | IVA (22%): {iva:,.2f} €")
# Nota
st.caption("Il calcolo non include eventuali spese di trasferta con partenza da Noventa Vicentina se distanza superiore a 100km.")

# --- SEZIONE RICHIESTA SOPRALLUOGO (CON CALENDARIO E CAPTCHA) ---
st.divider()
st.subheader("📍 Richiedi un Sopralluogo")
st.write("Scegli una data, inserisci i dati dell'immobile e lasciaci i tuoi recapiti.")

import random
import datetime

# --- 1. SISTEMA DI PRENOTAZIONE (CALENDARIO AVANZATO) ---
st.markdown("#### 📅 Scegli Data e Ora")

# Il nuovo sistema usa un dizionario per definire l'occupazione: "Tutto il giorno", "Mattina", o "Pomeriggio"
date_occupate = {
    datetime.date(2026, 6, 15): "Mattina",
    datetime.date(2026, 6, 16): "Pomeriggio",
    datetime.date(2026, 6, 17): "Tutto il giorno",
    datetime.date(2026, 6, 18): "Pomeriggio",
    datetime.date(2026, 6, 19): "Pomeriggio",
    # Giornate bloccate interamente per le vacanze a Canazei di fine giugno
    datetime.date(2026, 6, 23): "Tutto il giorno",
    datetime.date(2026, 6, 24): "Tutto il giorno",
    datetime.date(2026, 6, 25): "Tutto il giorno",
    datetime.date(2026, 6, 26): "Tutto il giorno",
    datetime.date(2026, 6, 29): "Tutto il giorno",
    datetime.date(2026, 6, 30): "Tutto il giorno",
    datetime.date(2026, 7, 1): "Tutto il giorno",
    datetime.date(2026, 7, 2): "Tutto il giorno",
    datetime.date(2026, 7, 3): "Tutto il giorno",
    datetime.date(2026, 7, 6): "Tutto il giorno",
    datetime.date(2026, 7, 7): "Tutto il giorno",
    datetime.date(2026, 7, 8): "Tutto il giorno",
    datetime.date(2026, 7, 9): "Tutto il giorno",
    datetime.date(2026, 7, 10): "Tutto il giorno"
}

col_data, col_ora = st.columns(2)

with col_data:
    data_scelta = st.date_input("Giorno del sopralluogo:", min_value=datetime.date.today(), format="DD/MM/YYYY")
    
with col_ora:
    fascia_oraria = st.selectbox("Fascia oraria:", ["Mattina (09:00 - 12:00)", "Pomeriggio (15:00 - 18:00)"])

# Controllo disponibilità incrociando data, fascia oraria e weekend
data_disponibile = True

# 1. Controllo automatico Fine Settimana (5 = Sabato, 6 = Domenica)
if data_scelta.weekday() >= 5: 
    st.error("❌ I sopralluoghi non vengono effettuati nel fine settimana. Seleziona un giorno dal Lunedì al Venerdì.")
    data_disponibile = False

# 2. Controllo delle tue date specifiche occupate
elif data_scelta in date_occupate:
    stato_occupazione = date_occupate[data_scelta]
    
    if stato_occupazione == "Tutto il giorno":
        st.error("❌ Data completamente occupata. Seleziona un altro giorno.")
        data_disponibile = False
    elif stato_occupazione == "Mattina" and "Mattina" in fascia_oraria:
        st.error("❌ La mattina di questo giorno è già impegnata. Scegli il pomeriggio o un'altra data.")
        data_disponibile = False
    elif stato_occupazione == "Pomeriggio" and "Pomeriggio" in fascia_oraria:
        st.error("❌ Il pomeriggio di questo giorno è già impegnato. Scegli la mattina o un'altra data.")
        data_disponibile = False
    else:
        st.success("✅ Orario disponibile per questa data!")

# 3. Se non è weekend e non è nelle date occupate, via libera
else:
    st.success("✅ Data e orario disponibili!")
    
st.caption("Data e orario saranno confermate dopo l'invio della richiesta.")


# --- 2. DATI CLIENTE ---
st.markdown("#### 👤 I tuoi dati")
indirizzo = st.text_input("Indirizzo esatto dell'immobile da rilevare (Via, Civico, CAP, Città, Provincia):")
nome_cliente = st.text_input("Il tuo Nome e Cognome:")
contatto_cliente = st.text_input("Il tuo Telefono o Email per essere ricontattato:")

# --- 3. CAPTCHA ANTI-ROBOT ---
if 'captcha_a' not in st.session_state:
    st.session_state.captcha_a = random.randint(1, 9)
    st.session_state.captcha_b = random.randint(1, 9)

st.write(f"🤖 **Controllo Anti-Spam: quanto fa {st.session_state.captcha_a} + {st.session_state.captcha_b}?**")
risposta_captcha = st.text_input("Inserisci il risultato numerico per sbloccare l'invio:")
somma_corretta = str(st.session_state.captcha_a + st.session_state.captcha_b)

# --- 4. MOTORE DI INVIO EMAIL ---
if indirizzo and nome_cliente and contatto_cliente and risposta_captcha == somma_corretta and data_disponibile:
    if st.button("✉️ Invia Richiesta Sopralluogo", type="primary"):
        
        oggetto = f"Nuova Richiesta Sopralluogo - {nome_cliente}"
        corpo_email = f"""È stata generata una nuova richiesta di sopralluogo dal calcolatore web.

DATI CLIENTE:
- Nome/Azienda: {nome_cliente}
- Recapito: {contatto_cliente}

APPUNTAMENTO RICHIESTO:
- Data: {data_scelta.strftime('%d/%m/%Y')}
- Orario: {fascia_oraria}
- Indirizzo: {indirizzo}

RIEPILOGO PARAMETRI:
- Superficie: {superficie} mq
- Tipologia Servizio: {servizio}
- Complessità: Spazi {spazi}, Luoghi {luoghi}, Geometria {geometria}

- STIMA PREZZO: {preventivo_totale:,.2f} Euro
- TEMPI STIMATI: {giorni_stimati} giorni
"""
        try:
            import smtplib
            from email.mime.text import MIMEText

            msg = MIMEText(corpo_email)
            msg['Subject'] = oggetto
            msg['From'] = "studioandriolo@gmail.com"
            msg['To'] = "studioandriolo@gmail.com"

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login("studioandriolo@gmail.com", st.secrets["GMAIL_PASSWORD"])
            server.send_message(msg)
            server.quit()

            st.success("✅ Richiesta inviata con successo! Ti ricontatteremo al più presto per confermare l'appuntamento.")
            
            st.session_state.captcha_a = random.randint(1, 9)
            st.session_state.captcha_b = random.randint(1, 9)
            
        except Exception as e:
            st.error("⚠️ Si è verificato un errore nell'invio. Riprova più tardi.")
elif risposta_captcha != "" and risposta_captcha != somma_corretta:
    st.error("❌ Risultato matematico errato. Riprova.")
elif not data_disponibile:
    pass 
else:
    st.info("👆 Scegli una data disponibile, compila tutti i dati e risolvi il calcolo per inviare la richiesta.")
