import pandas as pd
import numpy as np

# CSV'yi oku
df = pd.read_csv('data/eredivisie_midfielders_clustered.csv')

# Değiştirilmeyecek sütunlar
keep_cols = ['Player', 'Age', 'Pos', 'Squad', 'Nation', 'std_MP', 'std_Min', 'Cluster']

# Dönüştürülecek sütunları bul
transform_cols = [col for col in df.columns if col not in keep_cols]

print(f"Toplam {len(transform_cols)} sütun 0-100 arası puanlama sistemine dönüştürülecek...")
print(f"\nÖrnek sütunlar: {transform_cols[:5]}...")

# Her sütun için min-max scaling uygula (0-100 arası tam sayı)
for col in transform_cols:
    min_val = df[col].min()
    max_val = df[col].max()
    
    # Min-max scaling: (x - min) / (max - min) * 100
    if max_val != min_val:  # Sıfıra bölme hatası önleme
        df[col] = ((df[col] - min_val) / (max_val - min_val) * 100).round(0).astype(int)
    else:
        df[col] = 50  # Eğer tüm değerler aynıysa 50 ver
    
    print(f"{col}: [{min_val:.2f}, {max_val:.2f}] -> [0, 100]")

# Yeni CSV'ye kaydet
output_file = 'data/eredivisie_midfielders_scored.csv'
df.to_csv(output_file, index=False)

print(f"\n✓ Dönüşüm tamamlandı!")
print(f"✓ Yeni dosya kaydedildi: {output_file}")
print(f"\nÖrnek veriler (ilk 3 satır, ilk birkaç sütun):")
print(df[['Player', 'pass_Cmp%', 'pass_PrgDist', 'pass_KP', 'std_Gls', 'std_Ast', 'Cluster']].head(3))

