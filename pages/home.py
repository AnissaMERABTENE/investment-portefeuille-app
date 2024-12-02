import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# Fonction pour récupérer une liste d'actifs via yfinance
def get_assets(category):
    if category == "Actions":
        # Liste de 30 actions populaires
        ticker_list = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "ADBE", "PYPL",
            "INTC", "AMD", "CSCO", "ORCL", "IBM", "DIS", "V", "MA", "JNJ", "WMT",
            "PG", "HD", "BAC", "XOM", "CVX", "PFE", "KO", "PEP", "MRK", "T"
        ]
    elif category == "Obligations":
        # Liste de 30 obligations populaires ou représentatives
        ticker_list = [
            "US10Y", "US30Y", "TLT", "IEF", "SHY", "BND", "AGG", "LQD", "HYG", "TIP",
            "ZROZ", "EDV", "VCSH", "MUB", "VMBS", "ITOT", "SCHZ", "BIV", "BNDX", "EMB",
            "VWOB", "SPSB", "BSV", "STIP", "FLRN", "ICVT", "IBND", "HYD", "XOVR", "SUB"
        ]
    elif category == "ETF":
        # Liste de 30 ETF populaires
        ticker_list = [
            "SPY", "IVV", "VOO", "QQQ", "EEM", "IWM", "VTI", "VT", "XLK", "XLF",
            "XLV", "XLE", "XLY", "XLI", "XLP", "XLB", "XLU", "IYR", "VTV", "VUG",
            "SCHD", "VIG", "ARKK", "FDN", "SOXX", "XBI", "ITB", "REM", "HACK", "DIA"
        ]
    else:
        ticker_list = []
    return ticker_list

# Titre de l'application
st.title("Application de Simulation d'Investissement Passif")

# Formulaire de saisie des paramètres
montant_initial = st.number_input("Montant Initial (€)", min_value=0, value=1000000000000)

# Fréquence des contributions
frequence = st.selectbox("Fréquence des Contributions", ["Mensuelles", "Trimestrielles", "Annuelles"])

# Montant des contributions
contributions = st.number_input("Contributions en € ", min_value=0, value=100)

# Durée de l'investissement
duree = st.slider("Durée de l'investissement (années)", 1, 50, 10)

# Frais de gestion annuels
frais_annuel = st.number_input("Frais de gestion annuels (%)", min_value=0.0, value=5.0)

# Catégorie d'actif
categories = ["Actions", "Obligations", "ETF"]
categorie_actif = st.selectbox("Choisissez une catégorie d'actif", categories)

# Récupérer les actifs de la catégorie sélectionnée
actifs = get_assets(categorie_actif)

# Sélection de l'actif spécifique
if actifs:
    actif_choisi = st.selectbox(f"Choisissez un actif ({categorie_actif})", actifs)
    st.write(f"Vous avez choisi : {categorie_actif} - {actif_choisi}")
else:
    st.warning("Aucun actif disponible pour cette catégorie.")

# Fonction pour récupérer les données historiques d'un actif
def get_historical_data(ticker, period="5y"):
    data = yf.Ticker(ticker).history(period=period)
    return data

# Fonction pour calculer la volatilité
def calculate_volatility(data):
    returns = data['Close'].pct_change().dropna()
    return np.std(returns) * np.sqrt(252)  # Annualisée

# Fonction pour calculer le CAGR
def calculate_cagr(data):
    initial_value = data['Close'].iloc[0]
    final_value = data['Close'].iloc[-1]
    n = len(data) / 252  # Convertir les jours de marché en années
    return (final_value / initial_value) ** (1 / n) - 1

# Fonction pour calculer le rendement total
def calculate_total_return(data):
    initial_value = data['Close'].iloc[0]
    final_value = data['Close'].iloc[-1]
    return (final_value - initial_value) / initial_value

# Fonction pour calculer le ratio de Sharpe
def calculate_sharpe_ratio(data, risk_free_rate=0.02):
    returns = data['Close'].pct_change().dropna()
    excess_returns = returns - risk_free_rate / 252
    sharpe_ratio = np.mean(excess_returns) / np.std(returns) * np.sqrt(252)
    return sharpe_ratio

# Bouton pour soumettre les calculs
if st.button("Calculer les ratios financiers"):
    if actifs:
        st.write(f"Calcul des ratios pour : {actif_choisi}")
        data = get_historical_data(actif_choisi)

        # Vérification que des données ont bien été récupérées
        if data.empty:
            st.warning("Impossible de récupérer les données pour cet actif. Essayez un autre actif.")
        else:
            # Calcul des ratios
            volatility = calculate_volatility(data)
            cagr = calculate_cagr(data)
            total_return = calculate_total_return(data)
            sharpe_ratio = calculate_sharpe_ratio(data)

            # Affichage des résultats
            st.subheader("Résultats des ratios financiers")
            st.write(f"**Ratio de Sharpe** : {sharpe_ratio:.2f} \n"
                     f"➡️ Ce ratio mesure la performance ajustée au risque. Plus il est élevé, mieux c'est.")
            st.write(f"**Volatilité** : {volatility:.2%} \n"
                     f"➡️ La volatilité représente l'ampleur des fluctuations des rendements.")
            st.write(f"**CAGR (Taux de croissance annuel composé)** : {cagr:.2%} \n"
                     f"➡️ Cela montre la croissance annuelle moyenne du portefeuille.")
            st.write(f"**Rendement total** : {total_return:.2%} \n"
                     f"➡️ Le rendement total mesure l'évolution globale de la valeur du portefeuille.")
    else:
        st.warning("Veuillez sélectionner un actif pour effectuer les calculs.")



# ATTENTION A REVOIR // il faut comprendre et surtout modifier un peut mais sa fonctionne 
# Prochaine etape, fait les courbe ( plus compliquer )