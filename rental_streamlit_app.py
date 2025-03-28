import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.title("Analisi Redditività Affitti Brevi")

st.sidebar.header("Parametri")

# Parametri principali con valori predefiniti
price_range = st.sidebar.slider("Range di prezzo per notte (€)", 70, 150, (80, 100))
avg_nights_per_booking = st.sidebar.slider("Durata media prenotazione (notti)", 1, 7, 3)
owner_share = st.sidebar.slider("Quota al proprietario (%)", 0, 100, 50) / 100
owner_tax = st.sidebar.slider("Tasse pagate dal proprietario (%)", 0, 40, 21) / 100

# Costi fissi
cleaning_cost = st.sidebar.number_input("Costo pulizia (€)", min_value=0, value=15)
linen_cost = st.sidebar.number_input("Costo biancheria (€)", min_value=0, value=12)
self_cleaning = st.sidebar.checkbox("Svolgo le pulizie da solo", value=False)

# Parametri agente immobiliare
agent_share = st.sidebar.slider("Quota all'agente sul margine (%)", 0, 100, 50) / 100

# Parametri prenotazioni online
online_booking_percentage = st.sidebar.slider("Percentuale prenotazioni online (%)", 0, 100, 50) / 100
online_booking_commission = st.sidebar.slider("Commissione piattaforme online (%)", 0, 30, 17) / 100

# Parametri per il secondo grafico
fixed_price = st.sidebar.slider("Prezzo fisso per notte (€) per grafico occupazione", 
                               min_value=int(price_range[0]), 
                               max_value=int(price_range[1]), 
                               value=90)
num_apartments = st.sidebar.slider("Numero di appartamenti", 1, 10, 5)
max_nights = st.sidebar.slider("Massimo notti mensili per appartamento", 10, 31, 30)

# Funzione per calcolare il profitto per prenotazione
def calculate_profit_per_booking(price_per_night, self_cleaning_enabled=False):
    # Calcolo del fatturato totale per prenotazione
    total_revenue = price_per_night * avg_nights_per_booking
    
    # Divisione del fatturato
    business_revenue = total_revenue * (1 - owner_share)
    
    # Calcolo dei costi fissi effettivi
    effective_fixed_costs = linen_cost
    if not self_cleaning_enabled:
        effective_fixed_costs += cleaning_cost
    
    # Calcolo del margine dopo i costi fissi
    margin = business_revenue - effective_fixed_costs
    
    # Extra guadagno se faccio le pulizie io
    cleaning_income = cleaning_cost if self_cleaning_enabled else 0
    
    # Calcolo del profitto finale (dopo la divisione con l'agente)
    direct_booking_profit = margin * (1 - agent_share) + cleaning_income
    
    # Profitto per prenotazioni online (con commissione)
    online_booking_profit = direct_booking_profit * (1 - online_booking_commission)
    
    # Profitto medio ponderato
    weighted_profit = direct_booking_profit * (1 - online_booking_percentage) + \
                      online_booking_profit * online_booking_percentage
    
    return direct_booking_profit, online_booking_profit, weighted_profit

# Calcola e mostra i dati di esempio
if st.checkbox("Mostra dati di esempio", value=True):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Esempio singola prenotazione")
        example_price = fixed_price
        direct_profit, online_profit, weighted_profit = calculate_profit_per_booking(example_price, self_cleaning)
        
        data = {
            "Tipo": ["Diretta", "Online", "Media ponderata"],
            f"Profitto a {example_price}€/notte": [
                f"{direct_profit:.2f}€", 
                f"{online_profit:.2f}€", 
                f"{weighted_profit:.2f}€"
            ]
        }
        st.table(pd.DataFrame(data))
    
    with col2:
        st.subheader("Stima mensile")
        nights_example = 20
        bookings_example = nights_example / avg_nights_per_booking
        monthly_profit = weighted_profit * bookings_example * num_apartments
        
        st.metric(
            label=f"Profitto mensile con {nights_example} notti/appartamento", 
            value=f"{monthly_profit:.2f}€",
            delta=f"{monthly_profit/num_apartments:.2f}€ per appartamento"
        )

# Grafico 1: Profitto per prenotazione in funzione del prezzo per notte
st.header("Grafico 1: Profitto per prenotazione vs. Prezzo per notte")

night_prices = np.arange(price_range[0], price_range[1] + 1, 1)
direct_profits = []
online_profits = []
weighted_profits = []

for price in night_prices:
    direct_profit, online_profit, weighted_profit = calculate_profit_per_booking(price, self_cleaning)
    direct_profits.append(direct_profit)
    online_profits.append(online_profit)
    weighted_profits.append(weighted_profit)

fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(night_prices, direct_profits, 'b-', label='Prenotazioni dirette')
ax1.plot(night_prices, online_profits, 'r-', label='Prenotazioni online')
ax1.plot(night_prices, weighted_profits, 'g-', label='Media ponderata')
ax1.set_xlabel('Prezzo per notte (€)')
ax1.set_ylabel('Profitto per prenotazione (€)')
ax1.set_title('Profitto per prenotazione in funzione del prezzo per notte')
ax1.grid(True)
ax1.legend()
st.pyplot(fig1)

# Crea una tabella con i dati
profit_data = pd.DataFrame({
    'Prezzo/Notte (€)': night_prices,
    'Profitto Diretto (€)': np.round(direct_profits, 2),
    'Profitto Online (€)': np.round(online_profits, 2),
    'Profitto Medio (€)': np.round(weighted_profits, 2)
})

if st.checkbox("Mostra tabella dati profitto per prenotazione"):
    st.dataframe(profit_data)

# Grafico 2: Profitto mensile totale in funzione dell'occupazione mensile
st.header(f"Grafico 2: Profitto mensile totale per {num_apartments} appartamenti")

nights_range = np.arange(1, max_nights + 1, 1)
monthly_profits = []

for nights in nights_range:
    # Numero di prenotazioni mensili per appartamento
    bookings_per_apartment = nights / avg_nights_per_booking
    
    # Calcolo del profitto per singola prenotazione al prezzo fisso
    direct_profit, online_profit, weighted_profit = calculate_profit_per_booking(fixed_price, self_cleaning)
    
    # Profitto mensile totale per tutti gli appartamenti
    monthly_profit = weighted_profit * bookings_per_apartment * num_apartments
    monthly_profits.append(monthly_profit)

fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(nights_range, monthly_profits, 'b-')
ax2.set_xlabel('Notti di occupazione mensile per appartamento')
ax2.set_ylabel('Profitto mensile totale (€)')
ax2.set_title(f'Profitto mensile totale per {num_apartments} appartamenti (prezzo: {fixed_price}€/notte)')
ax2.grid(True)
st.pyplot(fig2)

# Tabella riepilogativa occupazione
occupancy_data = pd.DataFrame({
    'Notti/Mese': nights_range,
    'Prenotazioni/Mese': np.round(nights_range / avg_nights_per_booking, 2),
    'Profitto Totale (€)': np.round(monthly_profits, 2),
    'Profitto per Appartamento (€)': np.round(np.array(monthly_profits) / num_apartments, 2)
})

if st.checkbox("Mostra tabella dati profitto mensile"):
    st.dataframe(occupancy_data)

# Dettagli dei calcoli
if st.checkbox("Mostra dettagli calcoli"):
    st.subheader("Dettagli del modello di calcolo")
    
    st.markdown("""
    ### Formula di calcolo del profitto
    
    1. **Fatturato totale per prenotazione**:
       - `Prezzo per notte × Durata media prenotazione`
       
    2. **Quota spettante al business**:
       - `Fatturato totale × (1 - Quota proprietario)`
       
    3. **Costi fissi**:
       - Se svolgo le pulizie: `Costo biancheria`
       - Altrimenti: `Costo pulizia + Costo biancheria`
       
    4. **Margine dopo costi fissi**:
       - `Quota business - Costi fissi`
       
    5. **Profitto prenotazioni dirette**:
       - `Margine × (1 - Quota agente) + Guadagno pulizie`
       
    6. **Profitto prenotazioni online**:
       - `Profitto diretto × (1 - Commissione piattaforme)`
       
    7. **Profitto medio ponderato**:
       - `Profitto diretto × % prenotazioni dirette + Profitto online × % prenotazioni online`
    """)

st.sidebar.info("""
### Note
- Le tasse del proprietario (21%) sono già considerate nella sua quota
- Ogni prenotazione ha una durata media di 3 notti
- La commissione delle piattaforme online (17%) si applica solo alle prenotazioni provenienti da quei canali
""")