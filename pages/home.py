import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf


# Fonction pour récupérer les données historiques d'un actif ////////// DATA
def recuperer_donnees(actif, periode="10y"):
    return yf.Ticker(actif).history(period=periode)
#//////////////////////////////////////////////////////////////////////




# Fonctions pour les calculs financiers /////////////////////////////
def volatilite(data):
    rendements = data['Close'].pct_change().dropna()
    return np.std(rendements) * np.sqrt(252)

def cagr(data):
    debut = data['Close'].iloc[0]
    fin = data['Close'].iloc[-1]
    n = len(data) / 252
    return (fin / debut) ** (1 / n) - 1

def rendement_total(data):
    debut = data['Close'].iloc[0]
    fin = data['Close'].iloc[-1]
    return (fin - debut) / debut

def ratio_sharpe(data, taux_sans_risque=0.02):
    rendements = data['Close'].pct_change().dropna()
    rendements_excedents = rendements - taux_sans_risque / 252
    return np.mean(rendements_excedents) / np.std(rendements) * np.sqrt(252)

# FIN ////////////////////////////////////////////////////////////////



# Interface utilisateur
st.title("Application de Simulation d'Investissement Passif")

# Fonction pour récupérer une liste d'actifs via yfinance
def get_assets(categorie):
    if categorie == "Actions":
        return [
            "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "ADBE", "PYPL",
            "INTC", "AMD", "CSCO", "ORCL", "IBM", "DIS", "V", "MA", "JNJ", "WMT",
            "PG", "HD", "BAC", "XOM", "CVX", "PFE", "KO", "PEP", "MRK", "T"
        ]
    elif categorie == "Obligations":
        return [
            "US10Y", "US30Y", "TLT", "IEF", "SHY", "BND", "AGG", "LQD", "HYG", "TIP",
            "ZROZ", "EDV", "VCSH", "MUB", "VMBS", "ITOT", "SCHZ", "BIV", "BNDX", "EMB",
            "VWOB", "SPSB", "BSV", "STIP", "FLRN", "ICVT", "IBND", "HYD", "XOVR", "SUB"
        ]
    elif categorie == "ETF":
        return [
            "SPY", "IVV", "VOO", "QQQ", "EEM", "IWM", "VTI", "VT", "XLK", "XLF",
            "XLV", "XLE", "XLY", "XLI", "XLP", "XLB", "XLU", "IYR", "VTV", "VUG",
            "SCHD", "VIG", "ARKK", "FDN", "SOXX", "XBI", "ITB", "REM", "HACK", "DIA"
        ]
    else:
        return []


# Formulaire
montant_initial = st.number_input("Montant Initial (€)", value=100000)
frequence = st.selectbox("Fréquence des Contributions", ["Mensuelles", "Trimestrielles", "Annuelles"])
contributions = st.number_input("Contributions en €", value=100)
duree = st.slider("Durée de l'investissement (années)", 1, 50, 10)
frais_annuel = st.number_input("Frais de gestion annuels (%)", value=1.0)
categories = ["Actions", "Obligations", "ETF"]
categorie = st.selectbox("Choisissez une catégorie d'actif", categories)
actifs = get_assets(categorie)
actif_choisi = st.selectbox("Choisissez un actif", actifs)

# Bouton pour générer le rapport
if st.button("Générer mon compte rendu"):
    # Récupération des données historiques
    data = recuperer_donnees(actif_choisi)

    # Calcul des ratios financiers
    vol = volatilite(data)
    taux_croissance = cagr(data)
    rend_total = rendement_total(data)
    sharpe = ratio_sharpe(data)


    # Préparation des données pour le tableau
    data['Annee'] = data.index.year
    data['Mois'] = data.index.month
    donnees_mois = data[data['Mois'].isin([1, 6, 12])].pivot_table(index='Mois', columns='Annee', values='Close')
    donnees_mois.loc['Moyenne'] = donnees_mois.mean()

    # Affichage du tableau
    st.subheader("Cours Moyens (Janvier, Juin, Décembre)")
    st.dataframe(donnees_mois.style.format("{:.2f}"))

    # Régression linéaire journalière
    data['Jours'] = (data.index - data.index[0]).days
    X = data['Jours'].values.reshape(-1, 1)
    y = data['Close'].values
    a, b = np.polyfit(X.flatten(), y, 1)
    predictions = a * X.flatten() + b


    st.subheader("Prédiction du cours Moyens ")

    # Graphique
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data.index, data['Close'], label="Cours journaliers", color="blue")
    ax.plot(data.index, predictions, label="Régression Linéaire", color="red", linestyle="--")
    ax.set_title("Cours et Tendance")
    ax.set_xlabel("Date")
    ax.set_ylabel("Prix")
    ax.legend()
    st.pyplot(fig)

     # Explication générale
    st.markdown(f"""
                ### Explication
                Le tableau ci-dessus montre les **cours moyens pour Janvier, Juin et Décembre** de chaque année sur les 10 dernières années.
                Une ligne supplémentaire affiche la **moyenne annuelle** pour chaque année.

                Le graphique ci-dessus montre l'évolution des **cours moyens annuels** de l'actif sur les 10 dernières années 
                (courbe bleue) ainsi qu'une prédiction linéaire des cours sur les 10 prochaines années (ligne rouge pointillée).

                L'**écart-type des résidus** indique la dispersion des valeurs réelles par rapport à 
                la ligne de tendance. Un écart-type faible suggère que le modèle est relativement précis pour représenter la 
                tendance générale de l'actif.
            """)

    # Affichage des ratios financiers
    st.subheader("|||||||||||||||||  LES CHIFFRE A RETENIR ||||||||||||||||||||")
    st.write(f"**Volatilité** : {vol:.2%}")
    st.write(f"**CAGR (Taux de croissance annuel composé)** : {taux_croissance:.2%}")
    st.write(f"**Rendement Total** : {rend_total:.2%}")
    st.write(f"**Ratio de Sharpe** : {sharpe:.2f}")