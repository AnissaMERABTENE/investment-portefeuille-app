import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Titre de l'application
st.title("Application de Simulation d'Investissement Passif")

# Formulaire de saisie des paramètres
montant_initial = st.number_input("Montant Initial (€)", min_value=0, value=1000)
contributions = st.number_input("Contributions Mensuelles (€)", min_value=0, value=100)
duree = st.slider("Durée de l'investissement (années)", 1, 50, 10)
rendement_annuel = st.number_input("Rendement Annuel Moyen (%)", min_value=0.0, value=5.0)

# Calcul de la simulation d'investissement
if st.button("Simuler"):
    # Convertir les taux de pourcentage en décimal
    taux_rendement = rendement_annuel / 100
    mois = duree * 12
    
    # Créer une série de croissance avec NumPy
    montants = [montant_initial]
    for mois in range(1, mois + 1):
        dernier_montant = montants[-1]
        dernier_montant += contributions
        dernier_montant *= (1 + taux_rendement / 12)  # Rendement mensuel
        montants.append(dernier_montant)
    
    # Afficher les résultats avec Pandas
    df = pd.DataFrame({
        'Mois': np.arange(1, len(montants) + 1),
        'Valeur du Portefeuille (€)': montants
    })
    
    st.write("Voici l'évolution du portefeuille au fil du temps :")
    st.dataframe(df)
    
    # Visualiser les résultats avec Matplotlib
    fig, ax = plt.subplots()
    ax.plot(df['Mois'], df['Valeur du Portefeuille (€)'])
    ax.set_xlabel("Mois")
    ax.set_ylabel("Valeur du Portefeuille (€)")
    ax.set_title("Croissance du Portefeuille dans le Temps")
    st.pyplot(fig)

