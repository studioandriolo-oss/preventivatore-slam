import streamlit as st
import random

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
luogo = st.text_input("Indirizzo e città dove effettuare il rilievo") 
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
    "TECNICO (Smart + planimetrie CAD 2D)",
    "BIM (Smart + modellazione parametrica)",
    "VISUAL (Smart + Virtual Tour 360° immersivo)",
    "TECNICO + VISUAL",
    "BIM + VISUAL"
])

# Assegnazione del moltiplicatore fisso per ogni servizio
dati_servizi = {
    "SMART (Rilievo, elaborazione nuvola di punti)": 1.0,
    "TECNICO (Smart + planimetrie CAD 2D)": 2,
    "BIM (Smart + modellazione parametrica)": 3,
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
    luoghi = st.selectbox("Tipologia Luoghi", ["Al Grezzo", "Arredato", "Ingombrato/Tanti Riflessi"])
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

st.divider()

# --- MOTORE CALCOLO TEMPI DI CONSEGNA ---
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
    "TECNICO (Smart + planimetrie CAD 2D)": {"Open Space": 5, "Standard": 7, "Frammentato": 7},
    "BIM (Smart + modellazione parametrica)": {"Open Space": 5, "Standard": 10, "Frammentato": 15},
    "VISUAL (Smart + Virtual Tour 360° immersivo)": {"Open Space": 5, "Standard": 5, "Frammentato": 5},
    "TECNICO + VISUAL": {"Open Space": 7, "Standard": 9, "Frammentato": 9},
    "BIM + VISUAL": {"Open Space": 8, "Standard": 13, "Frammentato": 18}
}

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

# --- SEZIONE INVIO RICHIESTA ---
st.divider()
st.subheader("📍 Richiedi Sopralluogo")
st.write("Inserisci i dati dell'immobile e i tuoi recapiti per inviare la richiesta all'architetto.")

# --- 1. DATI CLIENTE ---
indirizzo = st.text_input("Indirizzo esatto dell'immobile da rilevare (Via, Civico, CAP, Città, Provincia):")
nome_cliente = st.text_input("Il tuo Nome e Cognome / Azienda:")
codice_fiscale = st.text_input("Il tuo Codice Fiscale / P.IVA:")
col_tel, col_mail = st.columns(2)
with col_tel:
    telefono_cliente = st.text_input("Il tuo Telefono per essere ricontattato:")
with col_mail:
    email_cliente = st.text_input("La tua Email:")

# --- 2. CAPTCHA ANTI-ROBOT ---
if 'captcha_a' not in st.session_state:
    st.session_state.captcha_a = random.randint(1, 9)
    st.session_state.captcha_b = random.randint(1, 9)

st.write(f"🤖 **Controllo Anti-Spam: quanto fa {st.session_state.captcha_a} + {st.session_state.captcha_b}?**")
risposta_captcha = st.text_input("Inserisci il risultato numerico per sbloccare l'invio:")
somma_corretta = str(st.session_state.captcha_a + st.session_state.captcha_b)

# --- 3. MOTORE DI INVIO EMAIL ---
privacy_accettata = st.checkbox("Accetto il trattamento dei dati personali per la gestione della richiesta di preventivo.")

if indirizzo and nome_cliente and telefono_cliente and email_cliente and risposta_captcha == somma_corretta:
    if st.button("✉️ Invia Richiesta all'Architetto", type="primary"):
        
        oggetto = f"Nuova Richiesta Sopralluogo - {nome_cliente}"
        corpo_email = f"""È stata generata una nuova richiesta di preventivo/sopralluogo dal calcolatore web.

DATI CLIENTE:
- Nome/Azienda: {nome_cliente}
- CF/P.IVA: {codice_fiscale}
- Recapiti: {telefono_cliente} | {email_cliente}
- Indirizzo Immobile: {indirizzo}

RIEPILOGO PARAMETRI:
- Luogo: {luogo}
- Superficie: {superficie} mq
- Tipologia Servizio: {servizio}
- Complessità: Spazi {spazi}, Luoghi {luoghi}, Geometria {geometria}

STIMA CALCOLATA:
- Prezzo Finito: {prezzo_finito:,.2f} Euro
- Tempi Stimati: {giorni_stimati} giorni
"""
        try:
            import smtplib
            from email.mime.text import MIMEText

            msg = MIMEText(corpo_email)
            msg['Subject'] = oggetto
            msg['From'] = "studioandriolo@gmail.com"
            msg['To'] = "studioandriolo@gmail.com"
            msg['Reply-To'] = email_cliente

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login("studioandriolo@gmail.com", st.secrets["GMAIL_PASSWORD"])
            server.send_message(msg)
            server.quit()

            st.success("✅ Richiesta inviata con successo! Ti ricontatteremo al più presto.")
            
            # Rigenera i numeri del captcha dopo l'invio
            st.session_state.captcha_a = random.randint(1, 9)
            st.session_state.captcha_b = random.randint(1, 9)
            
        except Exception as e:
            st.error("⚠️ Si è verificato un errore nell'invio. Riprova più tardi.")
elif risposta_captcha != "" and risposta_captcha != somma_corretta:
    st.error("❌ Risultato matematico errato. Riprova.")
else:
    st.info("👆 Compila tutti i campi richiesti, accetta la privacy e risolvi il calcolo per inviare la richiesta.")
