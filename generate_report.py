import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
from datetime import datetime

print("🔄 Génération du rapport PDF en cours...")

# Configuration
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('husl')

# Chargement des données
df = pd.read_csv('Africa_climate_change.csv')
df['DATE'] = pd.to_datetime(df['DATE'].astype(str).str[:8], format='%Y%m%d', errors='coerce')
df['YEAR'] = df['DATE'].dt.year
df['PERIODE'] = df['YEAR'].apply(lambda x: 'Avant 2000' if x < 2000 else 'Après 2000')

# Calcul des augmentations
before_2000 = df[df['YEAR'] < 2000].groupby('COUNTRY')['TAVG'].mean()
after_2000 = df[df['YEAR'] >= 2000].groupby('COUNTRY')['TAVG'].mean()
increase = after_2000 - before_2000
increase_df = pd.DataFrame({
    'Pays': increase.index,
    'Avant 2000 (°F)': before_2000.values,
    'Après 2000 (°F)': after_2000.values,
    'Augmentation (°F)': increase.values
}).sort_values('Augmentation (°F)', ascending=False)

# Création du PDF
pdf_filename = f'Rapport_Climat_Afrique_{datetime.now().strftime("%Y%m%d")}.pdf'

with PdfPages(pdf_filename) as pdf:
    
    # PAGE 1 : Page de titre
    fig = plt.figure(figsize=(11, 8.5))
    fig.text(0.5, 0.7, '🌍 Analyse du Changement Climatique', 
             ha='center', fontsize=28, fontweight='bold', color='#2c3e50')
    fig.text(0.5, 0.6, 'en Afrique (1980-2023)', 
             ha='center', fontsize=24, fontweight='bold', color='#2c3e50')
    fig.text(0.5, 0.45, f'Tunisie • Cameroun • Sénégal • Égypte • Angola', 
             ha='center', fontsize=14, color='#7f8c8d')
    fig.text(0.5, 0.35, f'464,815 observations quotidiennes', 
             ha='center', fontsize=12, color='#95a5a6')
    fig.text(0.5, 0.3, f'Période : 1980 - 2023 (43 ans)', 
             ha='center', fontsize=12, color='#95a5a6')
    
    fig.text(0.5, 0.15, 'Cheikh Niang', ha='center', fontsize=14, fontweight='bold')
    fig.text(0.5, 0.12, 'Data Scientist Junior', ha='center', fontsize=12, color='#7f8c8d')
    fig.text(0.5, 0.09, 'cheikhniang159@gmail.com', ha='center', fontsize=10, color='#95a5a6')
    fig.text(0.5, 0.05, f'Rapport généré le {datetime.now().strftime("%d/%m/%Y")}', 
             ha='center', fontsize=9, color='#bdc3c7')
    
    plt.axis('off')
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # PAGE 2 : Résumé exécutif
    fig, ax = plt.subplots(figsize=(11, 8.5))
    ax.axis('off')
    
    summary_text = f"""
RÉSUMÉ EXÉCUTIF

Objectif
────────
Analyser l'évolution des températures en Afrique sur 43 ans pour identifier 
les tendances du réchauffement climatique.

Méthodologie
────────────
- Dataset : 464,815 observations quotidiennes (1980-2023)
- Pays : 5 pays africains (Tunisie, Cameroun, Sénégal, Égypte, Angola)
- Variables : Températures moyenne, maximale et minimale
- Analyse : Comparaison avant/après 2000

Résultats clés
──────────────
✓ Réchauffement généralisé : +1.51°F en moyenne
✓ Pays le plus touché : Cameroun (+2.63°F)
✓ Tendance croissante depuis les années 1990
✓ Accélération du réchauffement après 2010

Impact
──────
Le réchauffement climatique est VISIBLE et MESURABLE dans tous les pays 
analysés, avec des conséquences potentielles sur l'agriculture, la santé 
et le développement économique du continent africain.
    """
    
    ax.text(0.1, 0.95, summary_text, fontsize=11, verticalalignment='top', 
            fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='#ecf0f1', alpha=0.8))
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # PAGE 3 : Tableau des augmentations
    fig, ax = plt.subplots(figsize=(11, 8.5))
    ax.axis('off')
    
    ax.text(0.5, 0.95, 'AUGMENTATION DES TEMPÉRATURES PAR PAYS', 
            ha='center', fontsize=16, fontweight='bold', color='#c0392b')
    ax.text(0.5, 0.90, '(Comparaison Avant 2000 vs Après 2000)', 
            ha='center', fontsize=12, color='#7f8c8d')
    
    table_data = []
    table_data.append(['Rang', 'Pays', 'Avant 2000', 'Après 2000', 'Augmentation'])
    for idx, row in increase_df.iterrows():
        rank = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣'][list(increase_df.index).index(idx)]
        table_data.append([
            rank,
            row['Pays'],
            f"{row['Avant 2000 (°F)']:.2f}°F",
            f"{row['Après 2000 (°F)']:.2f}°F",
            f"+{row['Augmentation (°F)']:.2f}°F"
        ])
    
    table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                     bbox=[0.1, 0.4, 0.8, 0.4])
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5)
    
    for i in range(len(table_data)):
        for j in range(5):
            cell = table[(i, j)]
            if i == 0:
                cell.set_facecolor('#34495e')
                cell.set_text_props(weight='bold', color='white')
            else:
                cell.set_facecolor('#ecf0f1' if i % 2 == 0 else 'white')
    
    ax.text(0.5, 0.25, f'📊 Moyenne globale : +{increase_df["Augmentation (°F)"].mean():.2f}°F', 
            ha='center', fontsize=14, fontweight='bold', 
            bbox=dict(boxstyle='round', facecolor='#e74c3c', alpha=0.3))
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # PAGE 4 : Évolution temporelle
    temp_by_year = df.groupby(['YEAR', 'COUNTRY'])['TAVG'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(11, 8.5))
    for country in df['COUNTRY'].unique():
        data = temp_by_year[temp_by_year['COUNTRY'] == country]
        ax.plot(data['YEAR'], data['TAVG'], marker='o', label=country, linewidth=2, markersize=3)
    
    ax.set_title('Évolution de la Température Moyenne par Pays (1980-2023)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Année', fontsize=12, fontweight='bold')
    ax.set_ylabel('Température Moyenne (°F)', fontsize=12, fontweight='bold')
    ax.legend(loc='best', fontsize=10, frameon=True, shadow=True)
    ax.grid(True, alpha=0.3)
    ax.axvline(x=2000, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Année 2000')
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # PAGE 5 : Box plots comparatifs
    fig, axes = plt.subplots(1, 3, figsize=(14, 6))
    
    for idx, temp_col in enumerate(['TMAX', 'TAVG', 'TMIN']):
        sns.boxplot(data=df, x='PERIODE', y=temp_col, hue='COUNTRY', ax=axes[idx])
        axes[idx].set_title(f'Température {temp_col}', fontsize=12, fontweight='bold')
        axes[idx].set_xlabel('Période', fontsize=10)
        axes[idx].set_ylabel('Température (°F)', fontsize=10)
        if idx > 0:
            axes[idx].get_legend().remove()
    
    plt.suptitle('Comparaison des Températures : Avant vs Après 2000', 
                 fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # PAGE 6 : Distribution par pays
    fig, axes = plt.subplots(2, 3, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, country in enumerate(df['COUNTRY'].unique()):
        data = df[df['COUNTRY'] == country]['TAVG'].dropna()
        axes[idx].hist(data, bins=50, color='coral', edgecolor='black', alpha=0.7)
        axes[idx].set_title(f'{country}', fontsize=12, fontweight='bold')
        axes[idx].set_xlabel('Température (°F)', fontsize=9)
        axes[idx].set_ylabel('Fréquence', fontsize=9)
        axes[idx].axvline(data.mean(), color='red', linestyle='--', linewidth=2, 
                         label=f'Moy: {data.mean():.1f}°F')
        axes[idx].legend(fontsize=8)
    
    if len(df['COUNTRY'].unique()) < 6:
        axes[-1].axis('off')
    
    plt.suptitle('Distribution des Températures par Pays', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # PAGE 7 : Conclusions
    fig, ax = plt.subplots(figsize=(11, 8.5))
    ax.axis('off')
    
    conclusions_text = f"""
CONCLUSIONS ET RECOMMANDATIONS

Constats principaux
───────────────────
1. Réchauffement climatique généralisé
   → Tous les pays analysés montrent une augmentation significative
   → Augmentation moyenne : +{increase_df['Augmentation (°F)'].mean():.2f}°F

2. Pays le plus touché : {increase_df.iloc[0]['Pays']}
   → Augmentation de +{increase_df.iloc[0]['Augmentation (°F)']:.2f}°F
   → Zone tropicale particulièrement vulnérable

3. Accélération récente
   → Tendance croissante depuis les années 1990
   → Accélération marquée après 2010

4. Variabilité accrue
   → Augmentation des températures extrêmes (MAX/MIN)
   → Impact sur la stabilité climatique


Implications pour l'Afrique
────────────────────────────
⚠️ Agriculture : Risques pour les cultures et la sécurité alimentaire
⚠️ Santé : Augmentation des maladies liées à la chaleur
⚠️ Économie : Impact sur le développement et les infrastructures
⚠️ Environnement : Désertification et perte de biodiversité


Recommandations
───────────────
✓ Politiques d'adaptation climatique urgentes
✓ Investissement dans les énergies renouvelables
✓ Sensibilisation et éducation aux enjeux climatiques
✓ Coopération régionale pour la résilience climatique


Limites de l'étude
──────────────────
- Données de précipitations incomplètes (62% manquantes)
- Analyse limitée à 5 pays
- Période d'analyse : 1980-2023
    """
    
    ax.text(0.05, 0.95, conclusions_text, fontsize=10, verticalalignment='top', 
            fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='#ecf0f1', alpha=0.8))
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

print(f"✅ Rapport PDF généré : {pdf_filename}")
print(f"📄 Taille : {round(len(open(pdf_filename, 'rb').read()) / 1024 / 1024, 2)} MB")
