import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

print("🎨 Génération des visualisations pour GitHub et Portfolio...")

# Configuration
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')

# Chargement des données
df = pd.read_csv('Africa_climate_change.csv')
df['DATE'] = pd.to_datetime(df['DATE'].astype(str).str[:8], format='%Y%m%d', errors='coerce')
df['YEAR'] = df['DATE'].dt.year
df['PERIODE'] = df['YEAR'].apply(lambda x: 'Avant 2000' if x < 2000 else 'Après 2000')

# VIZ 1 : Évolution temporelle des températures (Plotly → PNG)
print("📊 1/5 - Évolution temporelle...")
temp_by_year = df.groupby(['YEAR', 'COUNTRY'])['TAVG'].mean().reset_index()

fig = px.line(temp_by_year, x='YEAR', y='TAVG', color='COUNTRY',
              title='🌡️ Évolution de la Température Moyenne par Pays (1980-2023)',
              labels={'TAVG': 'Température Moyenne (°F)', 'YEAR': 'Année', 'COUNTRY': 'Pays'},
              height=600, width=1200)
fig.update_layout(
    font=dict(size=14),
    title_font=dict(size=20, family='Arial Black'),
    hovermode='x unified',
    plot_bgcolor='white'
)
fig.write_image("viz_1_evolution_temperatures.png", width=1200, height=600, scale=2)

# VIZ 2 : Comparaison avant/après 2000 (Matplotlib)
print("📊 2/5 - Comparaison avant/après 2000...")
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for idx, temp_col in enumerate(['TMAX', 'TAVG', 'TMIN']):
    sns.boxplot(data=df, x='PERIODE', y=temp_col, hue='COUNTRY', ax=axes[idx], palette='husl')
    axes[idx].set_title(f'Température {temp_col.replace("T", "").upper()}', fontsize=16, fontweight='bold')
    axes[idx].set_xlabel('Période', fontsize=12, fontweight='bold')
    axes[idx].set_ylabel('Température (°F)', fontsize=12, fontweight='bold')
    axes[idx].grid(True, alpha=0.3)
    if idx > 0:
        axes[idx].get_legend().remove()
    else:
        axes[idx].legend(title='Pays', fontsize=10, title_fontsize=12)

plt.suptitle('📦 Comparaison des Températures : Avant 2000 vs Après 2000', 
             fontsize=18, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('viz_2_comparison_before_after.png', dpi=300, bbox_inches='tight')
plt.close()

# VIZ 3 : Heatmap température par année et pays
print("📊 3/5 - Heatmap...")
pivot = df.groupby(['YEAR', 'COUNTRY'])['TAVG'].mean().reset_index().pivot(index='YEAR', columns='COUNTRY', values='TAVG')

plt.figure(figsize=(14, 10))
sns.heatmap(pivot, cmap='YlOrRd', cbar_kws={'label': 'Température (°F)'}, linewidths=0.5, annot=False)
plt.title('🔥 Heatmap : Température Moyenne par Année et Pays (1980-2023)', 
          fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Pays', fontsize=14, fontweight='bold')
plt.ylabel('Année', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('viz_3_heatmap_temperatures.png', dpi=300, bbox_inches='tight')
plt.close()

# VIZ 4 : Distribution des températures par pays
print("📊 4/5 - Distribution par pays...")
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.flatten()

for idx, country in enumerate(df['COUNTRY'].unique()):
    data = df[df['COUNTRY'] == country]['TAVG'].dropna()
    axes[idx].hist(data, bins=50, color='coral', edgecolor='black', alpha=0.7)
    axes[idx].set_title(f'{country}', fontsize=14, fontweight='bold')
    axes[idx].set_xlabel('Température (°F)', fontsize=11)
    axes[idx].set_ylabel('Fréquence', fontsize=11)
    axes[idx].axvline(data.mean(), color='red', linestyle='--', linewidth=2, 
                     label=f'Moyenne: {data.mean():.1f}°F')
    axes[idx].legend(fontsize=10)
    axes[idx].grid(True, alpha=0.3)

if len(df['COUNTRY'].unique()) < 6:
    axes[-1].axis('off')

plt.suptitle('📊 Distribution des Températures par Pays (1980-2023)', 
             fontsize=18, fontweight='bold')
plt.tight_layout()
plt.savefig('viz_4_distribution_temperatures.png', dpi=300, bbox_inches='tight')
plt.close()

# VIZ 5 : Augmentation par pays (Bar chart)
print("📊 5/5 - Augmentation par pays...")
before_2000 = df[df['YEAR'] < 2000].groupby('COUNTRY')['TAVG'].mean()
after_2000 = df[df['YEAR'] >= 2000].groupby('COUNTRY')['TAVG'].mean()
increase = after_2000 - before_2000
increase_df = pd.DataFrame({
    'Pays': increase.index,
    'Augmentation (°F)': increase.values
}).sort_values('Augmentation (°F)', ascending=False)

fig, ax = plt.subplots(figsize=(12, 7))
colors = ['#e74c3c' if x == increase_df['Augmentation (°F)'].max() else '#3498db' 
          for x in increase_df['Augmentation (°F)']]
bars = ax.bar(increase_df['Pays'], increase_df['Augmentation (°F)'], color=colors, 
              edgecolor='black', linewidth=2, alpha=0.8)

# Ajouter valeurs sur les barres
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'+{height:.2f}°F',
            ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_title('🔥 Augmentation de Température par Pays (Avant vs Après 2000)', 
             fontsize=18, fontweight='bold', pad=20)
ax.set_xlabel('Pays', fontsize=14, fontweight='bold')
ax.set_ylabel('Augmentation de Température (°F)', fontsize=14, fontweight='bold')
ax.axhline(y=increase_df['Augmentation (°F)'].mean(), color='green', linestyle='--', 
           linewidth=2, label=f'Moyenne: +{increase_df["Augmentation (°F)"].mean():.2f}°F')
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('viz_5_augmentation_par_pays.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n✅ 5 visualisations générées avec succès !")
print("📁 Fichiers créés :")
print("   - viz_1_evolution_temperatures.png")
print("   - viz_2_comparison_before_after.png")
print("   - viz_3_heatmap_temperatures.png")
print("   - viz_4_distribution_temperatures.png")
print("   - viz_5_augmentation_par_pays.png")
