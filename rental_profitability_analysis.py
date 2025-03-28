import numpy as np
import matplotlib.pyplot as plt

# Parametri iniziali
avg_nights_per_booking = 3
owner_share = 0.5  # 50% al proprietario
cleaning_cost = 15  # € per prenotazione
linen_cost = 12  # € per prenotazione
fixed_costs = cleaning_cost + linen_cost  # € per prenotazione
agent_share = 0.5  # 50% del margine al mio agente
online_booking_percentage = 0.5  # 50% delle prenotazioni tramite piattaforme online
online_booking_commission = 0.17  # 17% di commissione sulle prenotazioni online
owner_tax = 0.21  # 21% di tasse pagate dal proprietario

# Funzione per calcolare il profitto per prenotazione
def calculate_profit_per_booking(price_per_night):
    # Calcolo del fatturato totale per prenotazione
    total_revenue = price_per_night * avg_nights_per_booking
    
    # Divisione del fatturato
    business_revenue = total_revenue * (1 - owner_share)
    
    # Calcolo del margine dopo i costi fissi
    margin = business_revenue - fixed_costs
    
    # Calcolo del profitto finale (dopo la divisione con l'agente)
    direct_booking_profit = margin * (1 - agent_share)
    
    # Profitto per prenotazioni online (con commissione)
    online_booking_profit = direct_booking_profit * (1 - online_booking_commission)
    
    # Profitto medio ponderato
    weighted_profit = direct_booking_profit * (1 - online_booking_percentage) + \
                      online_booking_profit * online_booking_percentage
    
    return direct_booking_profit, online_booking_profit, weighted_profit

# Grafico 1: Profitto per prenotazione in funzione del prezzo per notte
night_prices = np.arange(80, 101, 1)  # Da 80€ a 100€
direct_profits = []
online_profits = []
weighted_profits = []

for price in night_prices:
    direct_profit, online_profit, weighted_profit = calculate_profit_per_booking(price)
    direct_profits.append(direct_profit)
    online_profits.append(online_profit)
    weighted_profits.append(weighted_profit)

plt.figure(figsize=(10, 6))
plt.plot(night_prices, direct_profits, 'b-', label='Prenotazioni dirette')
plt.plot(night_prices, online_profits, 'r-', label='Prenotazioni online (commissione 17%)')
plt.plot(night_prices, weighted_profits, 'g-', label='Media ponderata (50%/50%)')
plt.xlabel('Prezzo per notte (€)')
plt.ylabel('Profitto per prenotazione (€)')
plt.title('Profitto per prenotazione in funzione del prezzo per notte')
plt.grid(True)
plt.legend()
plt.savefig('profit_per_booking.png')
plt.close()

# Grafico 2: Profitto mensile totale in funzione dell'occupazione mensile
fixed_price = 90  # € per notte
nights_range = np.arange(5, 31, 1)  # Da 5 a 30 notti di occupazione mensile per appartamento

monthly_profits = []
num_apartments = 5

for nights in nights_range:
    # Numero di prenotazioni mensili per appartamento
    bookings_per_apartment = nights / avg_nights_per_booking
    
    # Calcolo del profitto per singola prenotazione al prezzo fisso
    direct_profit, online_profit, weighted_profit = calculate_profit_per_booking(fixed_price)
    
    # Profitto mensile totale per tutti gli appartamenti
    monthly_profit = weighted_profit * bookings_per_apartment * num_apartments
    monthly_profits.append(monthly_profit)

plt.figure(figsize=(10, 6))
plt.plot(nights_range, monthly_profits, 'b-')
plt.xlabel('Notti di occupazione mensile per appartamento')
plt.ylabel('Profitto mensile totale (€)')
plt.title(f'Profitto mensile totale per {num_apartments} appartamenti (prezzo: {fixed_price}€/notte)')
plt.grid(True)
plt.savefig('monthly_profit.png')
plt.close()

# Stampa di alcuni valori di esempio
print(f"Prezzo per notte: {fixed_price}€")
print(f"Profitto per prenotazione diretta: {calculate_profit_per_booking(fixed_price)[0]:.2f}€")
print(f"Profitto per prenotazione online: {calculate_profit_per_booking(fixed_price)[1]:.2f}€")
print(f"Profitto medio ponderato per prenotazione: {calculate_profit_per_booking(fixed_price)[2]:.2f}€")
print(f"Con 20 notti di occupazione mensile per appartamento:")
nights_example = 20
bookings_example = nights_example / avg_nights_per_booking
monthly_profit_example = calculate_profit_per_booking(fixed_price)[2] * bookings_example * num_apartments
print(f"Profitto mensile totale per {num_apartments} appartamenti: {monthly_profit_example:.2f}€")