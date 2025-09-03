import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO
from fpdf import FPDF
from sklearn.preprocessing import MinMaxScaler

# ---------------------------
# ADIM 0: SABİT VERİ DOSYASI
# ---------------------------
df = pd.read_csv('../data/eredivisie_midfielders_clustered.csv')
df = df.dropna(how='all')  # Boş satırları temizle

# ---------------------------
# ADIM 0.5: SÜTUN AÇIKLAMALARI (Türkçe)
# ---------------------------
column_info = {
    "Player": "Oyuncu Adı",
    "Age": "Yaş",
    "Pos": "Pozisyon",
    "Squad": "Takım",
    "Nation": "Milliyet",
    "std_MP": "Maç Sayısı",
    "std_Min": "Oynama Süresi (dakika)",
    "pass_Cmp%": "Pas Başarı Yüzdesi",
    "pass_PrgDist": "İleriye Doğru Pas Mesafesi",
    "pass_KP": "Kilit Pas Sayısı",
    "pass_1/3": "Ceza Sahası İçine Pas",
    "pass_PPA": "Ceza Sahasına Pas Girişi",
    "pass_PrgP": "İleriye Pas Sayısı",
    "passt_TB": "Topa Basarak Pas",
    "passt_Sw": "Yan Pas / Switch",
    "passt_Crs": "Ortaya Pas / Cross",
    "gca_PassLive": "Canlı Paslardan Gol Katkısı",
    "gca_PassDead": "Ölü Toplardan Gol Katkısı",
    "poss_Carries": "Top Sürme",
    "poss_PrgDist": "İleri Taşıma Mesafesi",
    "poss_PrgC": "İleriye Taşıma Sayısı",
    "poss_1/3": "Ceza Sahasına Taşıma",
    "poss_CPA": "Ceza Sahasına Giriş",
    "gca_TO": "Top Kaybından Gol Katkısı",
    "gca_Sh": "Şutlardan Gol Katkısı",
    "gca_Fld": "Açık Oyundan Gol Katkısı",
    "def_Tkl": "Top Çalma",
    "def_TklW": "Başarılı Top Çalma",
    "def_Int": "Top Kesme",
    "def_Tkl+Int": "Top Çalma + Kesme",
    "def_Blocks": "Şut/Top Bloklama",
    "def_Pass": "Rakip Pasını Engelleme",
    "def_Def 3rd": "Defans Üçlüsünde Savunma",
    "def_Mid 3rd": "Orta Sahada Savunma",
    "def_Att 3rd": "Hücum Üçlüsünde Savunma",
    "misc_TklW": "Başarılı Top Çalma (Misc)",
    "misc_Recov": "Top Kazanma",
    "misc_Won": "Kazanılan Top",
    "misc_Lost": "Kaybedilen Top",
    "misc_Fls": "Fauller",
    "misc_Fld": "Faul Yapılan",
    "poss_Mis": "Kaybedilen Top / Misses",
    "poss_Dis": "Rakipten Top Alma",
    "def_Lost": "Kaybedilen Top Savunma",
    "std_Gls": "Gol Sayısı",
    "std_Ast": "Asist Sayısı",
    "std_xG": "Beklenen Gol (xG)",
    "std_xAG": "Beklenen Asist (xAG)",
    "std_PrgR": "İleri Pas",
    "shoot_Sh": "Şut Sayısı",
    "std_CrdY": "Sarı Kart",
    "std_CrdR": "Kırmızı Kart",
    "std_90s": "90 Dakika Başına Oynama",
    "pt_Min%": "Oynama Süresi Yüzdesi",
    "pt_Mn/MP": "Ortalama Dakika / Maç",
    "Cluster": "Oyuncu Kümesi"
}

with st.expander("📖 SÜTUN AÇIKLAMALARI"):
    for col, desc in column_info.items():
        st.write(f"**{col}**: {desc}")

# ---------------------------
# Cluster Profilleri (Gerçek Veri Analizine Dayalı)
# ---------------------------
cluster_profiles = {
    0: {
        "name": "Elite Yaratıcı Hücum Oyuncuları", 
        "description": """**GERÇEK VERİ ANALİZİ:**  
Bu cluster'da elit seviyedeki oyuncular bulunuyor. Kenneth Taylor (Ajax), Jakob Breum (Go Ahead Eagle), Leo Sauer (NAC Breda), Malik Tillman (PSV), Sem Steijn (Twente) gibi öne çıkan isimler.

**İSTATİSTİKLER:**  
Normalizeli skorlarda en yüksek gol ve asist değerleri görülüyor. Teknik kalite çok üstün seviyede.

**ÖZELLİKLER:**  
En yüksek yaratıcılık ve gol katkısı sağlayan oyuncular. Büyük kulüplerin genç yıldızları bu grupta yer alıyor.

**KONUMLAR:**  
Ofansif orta saha, 10 numara pozisyonu, yaratıcı merkez roller tercih ediliyor.

**SCOUT NOTU:**  
Transfer değeri en yüksek grup. Avrupa kulüplerinin yakından takip ettiği oyuncular.""",
        "detailed_stats": {
            "avg_goals": None, "avg_assists": None, "avg_xG": None, "avg_shots": None,
            "avg_age": None, "avg_minutes": None, "top_teams": ["Ajax", "PSV", "Go Ahead Eagle", "NAC Breda", "Twente"],
            "key_strengths": ["Gol", "Asist", "Yaratıcılık", "Şut", "xG"], 
            "playing_style": "Hücum odaklı yaratıcı, rakip defansını delme yeteneği, son pasta etkili"
        }
    },
    1: {
        "name": "Gelişim Aşamasındaki Oyuncular", 
        "description": """**GERÇEK VERİ ANALİZİ:**  
Bu cluster'da gelişim aşamasındaki oyuncular bulunuyor. (%54 - en büyük grup). Antoni Milambo (Feyenoord), Kian Fitz-Jim (Ajax), Jorg Schreuders (Groningen), Johan Hove (Groningen), Joshua Kitolano (Sparta R'dam) gibi gelişim aşamasındaki oyuncular.

**İSTATİSTİKLER:**  
Normalizeli skorlarda orta seviye pas başarısı görülüyor. Henüz gelişim aşamasında olan profiller.

**ÖZELLİKLER:**  
Temel pas yeteneği mevcut ancak henüz yaratıcı seviyede değil. Fiziksel gelişim devam ediyor, taktiksel anlayış öğrenme aşamasında.

**KONUMLAR:**  
Merkez orta saha, rotasyonlu roller, yedek başlangıç pozisyonları tercih ediliyor.

**SCOUT NOTU:**  
2-3 yıl içinde büyük gelişim gösterebilecek isimler. Düşük maliyetle alınabilir potansiyel yıldızlar.""",
        "detailed_stats": {
            "avg_pass_success": None, "avg_playing_time": None,             "avg_minutes": None, "avg_age": None,
            "top_teams": ["Groningen", "Utrecht", "Sparta R'dam", "Feyenoord", "Ajax"], "total_players": 26,
            "key_strengths": ["Rotasyon Uyumluluğu", "Temel Pas Yetisi", "Genç Yaş"],
            "playing_style": "Henüz gelişim aşamasında, temel yetenekleri var, ileride büyüme potansiyeli yüksek"
        }
    },
    2: {
        "name": "Defansif Motorlar", 
        "description": """**GERÇEK VERİ ANALİZİ:**  
Bu cluster'da defansif karakterli oyunculardan oluşuyor. Anouar El Azzouzi (Zwolle), Enric Llansana (Go Ahead Eagle), Paxten Aaronson (Utrecht), Dirk Proper (NEC Nijmegen), Espen van Ee (Heerenveen) gibi güvenilir profiller.

**İSTATİSTİKLER:**  
Normalizeli skorlarda en yüksek defansif değerler görülüyor. En fazla dakika oynayan grup olarak öne çıkıyor.

**ÖZELLİKLER:**  
Sürekli koşan, defansif görevleri aksatmayan, fiziksel mücadelede güçlü karakterde oyuncular.

**KONUMLAR:**  
Defensif orta saha, 6-8 numara, holding midfielder pozisyonları tercih ediliyor.

**SCOUT NOTU:**  
Takımın omurgası oyuncular. Lider karakterli, her maç %100 performans veren güvenilir isimler.""",
        "detailed_stats": {
            "avg_tackles": None, "avg_interceptions": None, "avg_recoveries": None,
            "avg_minutes": None, "avg_age": None, "total_players": 12,
            "top_teams": ["Go Ahead Eagle", "NEC Nijmegen", "Zwolle", "Utrecht", "Heerenveen"],
            "key_strengths": ["Savunma", "Top Kazanım", "Dayanıklılık"],
            "playing_style": "Destruktif orta saha, temizlik görevlisi, takım dengesi sağlayıcı"
        }
    }
}

# ---------------------------
# ADIM 1: SAYFA BAŞI BİLGİ
# ---------------------------
st.set_page_config(page_title="Oyuncu Analizi", layout="wide")
st.title("⚽ Eredivisie 24 Yaş Altı Ortasaha Oyuncuları Scouting Dashboard")


# Genel istatistikler
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Toplam Oyuncu", "48")
with col2:
    st.metric("🎯 Cluster Sayısı", "3")
st.markdown("### 🎯 Detaylı Cluster Profilleri")

for cid, prof in cluster_profiles.items():
    # Gerçek cluster verilerini hesapla
    cluster_data = df[df['Cluster'] == cid]
    real_player_count = len(cluster_data)
    
    with st.expander(f"🔍 **CLUSTER {cid}: {prof['name']}**"):
        st.markdown(prof['description'])
        
        # Gerçek verilerden dinamik istatistikler
        if len(cluster_data) > 0:
            real_avg_age = cluster_data['Age'].mean()
            real_avg_minutes = cluster_data['std_Min'].mean()
            
            # Her cluster için özel performans metrikleri
            if cid == 0:  # Elite Yaratıcı Hücum
                perf_metric_1 = cluster_data['std_Gls'].mean()
                perf_metric_2 = cluster_data['std_Ast'].mean()
                perf_label_1 = "Ortalama Gol"
                perf_label_2 = "Ortalama Asist"
            elif cid == 1:  # Gelişim Aşaması
                perf_metric_1 = cluster_data['pass_Cmp%'].mean()
                perf_metric_2 = cluster_data['pt_Min%'].mean()
                perf_label_1 = "Pas Başarı Skoru"
                perf_label_2 = "Oynama Oranı Skoru"
            elif cid == 2:  # Defansif Motor
                perf_metric_1 = cluster_data['def_Tkl'].mean()
                perf_metric_2 = cluster_data['misc_Recov'].mean()
                perf_label_1 = "Ortalama Top Çalma"
                perf_label_2 = "Top Kazanım"
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**📊 Temel İstatistikler**")
                st.metric("Ortalama Yaş", f"{real_avg_age:.1f}")
                st.metric("Ortalama Dakika", f"{real_avg_minutes:.0f}")
                    
            with col2:
                st.markdown("**⚽ Performans Metrikleri**")
                st.caption("*(Z-skor normalizasyonuna göre)*")
                st.metric(perf_label_1, f"{perf_metric_1:.2f}")
                st.metric(perf_label_2, f"{perf_metric_2:.2f}")
                    
            with col3:
                st.markdown("**🏆 En Çok Oyuncu Gönderen Takımlar**")
                top_teams = cluster_data['Squad'].value_counts().head(3)
                for team, count in top_teams.items():
                    st.write(f"• {team} ({count} oyuncu)")
        else:
            st.info("Bu cluster'da filtreleme sonrası oyuncu bulunmuyor.")
                        
        st.markdown(f"**🎮 Oyun Stili**: {prof['detailed_stats'].get('playing_style', 'Genel orta saha')}")
        
        if 'key_strengths' in prof['detailed_stats']:
            st.markdown(f"**💪 Ana Güçlü Yanları**: {', '.join(prof['detailed_stats']['key_strengths'])}")

# ---------------------------
# ADIM 2: FİLTRELER & OYUNCU ARAMA
# ---------------------------
st.subheader("📂 Filtreleme ve Oyuncu Arama")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    age_filter = st.slider("Yaş Aralığı", int(df["Age"].min()), int(df["Age"].max()), (18, 24))
with col2:
    pos_filter = st.multiselect("Pozisyon", sorted(df["Pos"].unique()), default=df["Pos"].unique())
with col3:
    squad_filter = st.multiselect("Takım", sorted(df["Squad"].unique()), default=df["Squad"].unique())
with col4:
    cluster_filter = st.multiselect("Cluster Seç", sorted(df["Cluster"].unique()), default=df["Cluster"].unique())
with col5:
    player_search = st.text_input("Oyuncu Ara (İsim)")

df_filtered = df[
    (df["Age"] >= age_filter[0]) &
    (df["Age"] <= age_filter[1]) &
    (df["Pos"].isin(pos_filter)) &
    (df["Squad"].isin(squad_filter)) &
    (df["Cluster"].isin(cluster_filter))
]

if player_search:
    df_filtered = df_filtered[df_filtered["Player"].str.contains(player_search, case=False, na=False)]

st.dataframe(df_filtered)


# ---------------------------
# ADIM 4: CLUSTER'A GÖRE EN İYİ 5 OYUNCU
# ---------------------------
st.header("🏆 Cluster'ın En İyi 5 Oyuncusu")

# Cluster profillerine uygun metrik setleri (Yeni 3 Cluster)
cluster_metrics_map = {
    0: ['std_Gls','std_Ast','std_xG','std_xAG','pass_KP','shoot_Sh','gca_PassLive'],      # Süper Yıldızlar: gol + asist + yaratıcılık + şut
    1: ['std_Min','pass_Cmp%','pt_Min%','misc_Won','std_MP'],                           # Gelişim Aşamasındaki: oynama süresi + temel pas + mücadele
    2: ['def_Tkl','def_TklW','def_Int','def_Blocks','misc_Recov','misc_TklW','poss_PrgDist'] # Çalışkan Motor: savunma + top kazanım + fiziksel güç
}

# Hesaplamayı mevcut filtrelere göre yapalım
df_rank = df_filtered.copy()

for cid, metrics in cluster_metrics_map.items():
    st.subheader(f"🏆 Cluster {cid}: {cluster_profiles[cid]['name']}")
    
    # Gerçek veri üzerinden cluster istatistikleri hesapla
    cluster_data = df_filtered[df_filtered['Cluster'] == cid]
    
    # En iyi 5 oyuncunun bireysel öne çıkan özelliklerini göster
    if len(cluster_data) > 0:
        st.markdown("**🌟 En İyi 5 Oyuncunun Öne Çıkan Özellikleri:**")
        
        # CSV'den doğrudan cluster bazlı en iyi oyuncuları belirle
        if cid == 0:  # Elite Yaratıcı Hücum
            # En yüksek gol+asist kombinasyonu
            cluster_data_sorted = cluster_data.copy()
            cluster_data_sorted['combined_score'] = cluster_data_sorted['std_Gls'] + cluster_data_sorted['std_Ast']
            top_5 = cluster_data_sorted.nlargest(5, 'combined_score')
            
            for idx, (_, player) in enumerate(top_5.iterrows(), 1):
                # Her oyuncuya özel yorum yap
                gol = player['std_Gls']
                asist = player['std_Ast']
                xg = player['std_xG']
                
                # Yorumları oluştur
                comment = ""
                if gol > 1.5 and asist > 1.0:
                    comment = "🔥 **Elite bitirici ve yaratıcı** - Hem gol atar hem de asist yapar"
                elif gol > 2.0:
                    comment = "⚽ **Süper golcü** - Takımın en güvenilir gol makinesi"
                elif asist > 1.5:
                    comment = "🎯 **Oyun kurucu** - Takım arkadaşlarını sürekli gole götürür"
                elif xg > 2.0:
                    comment = "📈 **Yüksek potansiyel** - İstatistiksel olarak çok etkili pozisyonlara girer"
                else:
                    comment = "✨ **Dengeli oyuncu** - Birçok alanda katkı sağlayan çok yönlü profil"
                    
                st.write(f"**{idx}. {player['Player']}**: {comment}")
                
        elif cid == 1:  # Gelişim Aşaması
            # En yüksek pas başarısı + oynama süresi
            cluster_data_sorted = cluster_data.copy()
            cluster_data_sorted['combined_score'] = cluster_data_sorted['pass_Cmp%'] + (cluster_data_sorted['std_Min'] / 1000)  # Normalize dakika
            top_5 = cluster_data_sorted.nlargest(5, 'combined_score')
            
            for idx, (_, player) in enumerate(top_5.iterrows(), 1):
                # Her oyuncuya özel yorum yap
                pas_success = player['pass_Cmp%']
                minutes = player['std_Min']
                play_ratio = player['pt_Min%']
                
                # Yorumları oluştur
                comment = ""
                if minutes > 2000 and pas_success > 0.5:
                    comment = "🌟 **Tecrübeli güvenilir** - Çok oynar ve pas kalitesi yüksek"
                elif minutes > 2000:
                    comment = "💪 **Çalışkan motor** - Takımda sürekli oynuyor, tecrübe kazanıyor"
                elif pas_success > 0.8:
                    comment = "🎯 **Teknik yetenek** - Pas kalitesi çok yüksek, güvenilir"
                elif play_ratio > 0.5:
                    comment = "📈 **Yükselen değer** - Antrenörün güvenini kazanmış, potansiyelli"
                else:
                    comment = "⭐ **Gelecek vaat ediyor** - Henüz ham ama gelişime açık profil"
                    
                st.write(f"**{idx}. {player['Player']}**: {comment}")
                
        elif cid == 2:  # Defansif Motor
            # En yüksek defansif katkı
            cluster_data_sorted = cluster_data.copy()
            cluster_data_sorted['combined_score'] = cluster_data_sorted['def_Tkl'] + cluster_data_sorted['misc_Recov']
            top_5 = cluster_data_sorted.nlargest(5, 'combined_score')
            
            for idx, (_, player) in enumerate(top_5.iterrows(), 1):
                # Her oyuncuya özel yorum yap
                tackles = player['def_Tkl']
                interceptions = player['def_Int']
                recoveries = player['misc_Recov']
                
                # Yorumları oluştur
                comment = ""
                if tackles > 2.5 and recoveries > 2.5:
                    comment = "🛡️ **Defansif duvar** - Hem agresif hem de akıllı savunma yapıyor"
                elif tackles > 3.0:
                    comment = "⚔️ **Agresif savaşçı** - Rakiplere nefes aldırmayan mücadele stili"
                elif recoveries > 3.0:
                    comment = "🧠 **Akıllı temizleyici** - Pozisyon alarak top kazanma ustası"
                elif interceptions > 2.0:
                    comment = "👁️ **Oyun okuyucu** - Rakip paslarını kesen zeki savunmacı"
                else:
                    comment = "💼 **Güvenilir işçi** - Sessiz ama etkili, takımın vazgeçilmezi"
                    
                st.write(f"**{idx}. {player['Player']}**: {comment}")
    
    st.caption(f"**Oyun Stili**: {cluster_profiles[cid]['detailed_stats'].get('playing_style', 'Genel orta saha oyuncuları')}")

    # Bu cluster seçili filtrede var mı?
    if cid not in df_rank["Cluster"].unique():
        st.info("Bu kümede filtreleme kriterlerine uyan oyuncu bulunamadı.")
        continue

    # Sadece mevcut olan metrikler
    available_metrics = [m for m in metrics if m in df_rank.columns]
    if not available_metrics:
        st.warning("Bu cluster için geçerli metrik bulunamadı.")
        continue

    # Normalizasyon
    scaler_rank = MinMaxScaler()
    scaled_vals = scaler_rank.fit_transform(df_rank[available_metrics])
    score = scaled_vals.mean(axis=1)  # Eşit ağırlık: istersen ağırlıklandırma ekleyebiliriz

    # Skor serisi
    df_rank[f"Cluster{cid}_Score"] = score

    # Bu cluster'daki en iyi 5
    top_players = df_rank[df_rank["Cluster"] == cid].nlargest(5, f"Cluster{cid}_Score")

    # Gösterilecek sütunlar
    show_cols = ["Player","Age","Pos","Squad",f"Cluster{cid}_Score"] + available_metrics
    renamed_cols = {col: column_info.get(col, col) for col in show_cols}

    st.dataframe(top_players[show_cols].rename(columns=renamed_cols))
# ---------------------------
# ADIM 3: RADAR + BENZER OYUNCU + CLUSTER PROFİLİ
# ---------------------------
st.subheader("📈 Profesyonel Radar Chart, Benzer Oyuncular ve Cluster Profili")

# İlk radar metrikleri
radar_metrics = ['std_MP','std_Min','std_90s','std_Gls','std_Ast','std_xG','std_xAG','misc_Fls','std_CrdY','std_CrdR']

player_select = st.multiselect("Oyuncu Seç (Birden fazla seçilebilir)", df_filtered["Player"].unique(), default=[], key="player_select")

def update_player_view(selected_players):
    if not selected_players:
        st.info("Lütfen analiz etmek istediğiniz oyuncu(lar)ı seçin.")
        return
        
    # Seçilen oyuncuların verilerini al
    selected_rows = df_filtered[df_filtered["Player"].isin(selected_players)]
    if selected_rows.empty:
        st.warning("Seçilen oyuncular filtreleme dışında kaldı.")
        return

    # Seçilen oyuncuların cluster bilgileri
    unique_clusters = selected_rows["Cluster"].unique()
    
    # Cluster bilgilerini göster
    for cluster_id in unique_clusters:
        players_in_cluster = selected_rows[selected_rows["Cluster"] == cluster_id]["Player"].tolist()
        st.write(f"**Cluster {cluster_id}: {cluster_profiles[cluster_id]['name']}** → {', '.join(players_in_cluster)}")
        st.caption(cluster_profiles[cluster_id]['description'])

    # ---------------------------
    # 1️⃣ Çoklu Oyuncu vs Cluster Radar
    # ---------------------------
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df_filtered[radar_metrics]), columns=radar_metrics, index=df_filtered.index)

    metrics_tr = [column_info[m] for m in radar_metrics]
    
    fig_radar = go.Figure()
    
    # Oyuncu renkleri
    player_colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880']
    
    # Her oyuncu için trace ekle
    for idx, player_name in enumerate(selected_players):
        player_row = selected_rows[selected_rows["Player"] == player_name]
        if not player_row.empty:
            player_scaled = df_scaled.loc[player_row.index[0]]
            color = player_colors[idx % len(player_colors)]
            # İlk değeri sona ekleyerek kapalı çokgen oluştur
            r_values = list(player_scaled.values) + [player_scaled.values[0]]
            theta_values = metrics_tr + [metrics_tr[0]]
            
            fig_radar.add_trace(go.Scatterpolar(
                r=r_values, 
                theta=theta_values, 
                fill='toself', 
                name=player_name, 
                line=dict(color=color, width=3)
            ))
    
    # Cluster ortalamalarını ekle
    cluster_colors = ['#F97316', '#EC4899', '#06B6D4']  # 3 cluster için: Turuncu, Pembe, Turkuaz
    for idx, cluster_id in enumerate(unique_clusters):
        cluster_mean_scaled = df_scaled[df_filtered["Cluster"] == cluster_id].mean()
        cluster_color = cluster_colors[cluster_id % len(cluster_colors)]
        # İlk değeri sona ekleyerek kapalı çokgen oluştur
        r_cluster_values = list(cluster_mean_scaled.values) + [cluster_mean_scaled.values[0]]
        theta_cluster_values = metrics_tr + [metrics_tr[0]]
        
        fig_radar.add_trace(go.Scatterpolar(
            r=r_cluster_values, 
            theta=theta_cluster_values, 
            fill='toself', 
            name=f"Cluster {cluster_id} Ortalaması", 
            line=dict(color=cluster_color, width=3, dash='dot'), 
            opacity=0.6,
            visible='legendonly'
        ))
    
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,1])),
        showlegend=True, 
        title="Seçilen Oyuncular vs Cluster Ortalamaları",
        template='plotly_dark', 
        title_font=dict(size=20), 
        legend=dict(font=dict(size=12))
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # ---------------------------
    # 2️⃣ Kategorilere Göre Radarlar
    # ---------------------------
    categories = {
        "Oynama Süresi / Katılım": ['std_MP','std_Min','std_90s','pt_Min%','pt_Mn/MP'],
        "Pas / Oyun Kurma": ['pass_Cmp%','pass_PrgDist','pass_KP','pass_1/3','pass_PPA','pass_PrgP','passt_TB','passt_Sw','passt_Crs','gca_PassLive','gca_PassDead','gca_TO'],
        "Top Taşıma / İleri Oyun": ['poss_Carries','poss_PrgDist','poss_PrgC','poss_1/3','poss_CPA','gca_Sh','gca_Fld'],
        "Şut / Gol Katkısı": ['std_Gls','std_Ast','std_xG','std_xAG','shoot_Sh'],
        "Defansif Aksiyonlar / Savunma": ['def_Tkl','def_TklW','def_Int','def_Tkl+Int','def_Blocks','def_Pass','def_Def 3rd','def_Mid 3rd','def_Att 3rd','misc_TklW','misc_Recov','misc_Won','def_Lost'],
        "Hatalar / Saha Disiplini": ['misc_Lost','misc_Fls','misc_Fld','std_CrdY','std_CrdR','poss_Mis','poss_Dis']
    }

    for category, cat_metrics in categories.items():
        st.subheader(category)
        cat_metrics_available = [m for m in cat_metrics if m in df_filtered.columns]
        cat_metrics_tr = [column_info[m] for m in cat_metrics_available]
        
        if not cat_metrics_tr:
            continue
            
        # Kategori için scaling
        cat_scaler = MinMaxScaler()
        df_cat_scaled = pd.DataFrame(
            cat_scaler.fit_transform(df_filtered[cat_metrics_available]),
            columns=cat_metrics_tr, 
            index=df_filtered.index
        )

        fig_cat = go.Figure()
        
        # Her oyuncu için trace ekle
        for idx, player_name in enumerate(selected_players):
            player_row = selected_rows[selected_rows["Player"] == player_name]
            if not player_row.empty:
                player_scaled_cat = df_cat_scaled.loc[player_row.index[0]]
                color = player_colors[idx % len(player_colors)]
                # İlk değeri sona ekleyerek kapalı çokgen oluştur
                r_cat_values = list(player_scaled_cat.values) + [player_scaled_cat.values[0]]
                theta_cat_values = cat_metrics_tr + [cat_metrics_tr[0]]
                
                fig_cat.add_trace(go.Scatterpolar(
                    r=r_cat_values, 
                    theta=theta_cat_values, 
                    fill='toself', 
                    name=player_name, 
                    line=dict(color=color, width=3)
                ))
        
        # Cluster ortalamalarını ekle
        for idx, cluster_id in enumerate(unique_clusters):
            cluster_mean_cat = df_cat_scaled[df_filtered["Cluster"] == cluster_id].mean()
            cluster_color = cluster_colors[cluster_id % len(cluster_colors)]
            # İlk değeri sona ekleyerek kapalı çokgen oluştur
            r_cat_cluster_values = list(cluster_mean_cat.values) + [cluster_mean_cat.values[0]]
            theta_cat_cluster_values = cat_metrics_tr + [cat_metrics_tr[0]]
            
            fig_cat.add_trace(go.Scatterpolar(
                r=r_cat_cluster_values, 
                theta=theta_cat_cluster_values, 
                fill='toself', 
                name=f"Cluster {cluster_id} Ortalaması", 
                line=dict(color=cluster_color, width=3, dash='dot'), 
                opacity=0.6,
                visible='legendonly'
            ))

        fig_cat.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0,1])),
            showlegend=True,
            template='plotly_dark',
            title=f"{category} - Seçilen Oyuncular vs Cluster Ortalamaları",
            title_font=dict(size=20),
            legend=dict(font=dict(size=12))
        )
        st.plotly_chart(fig_cat, use_container_width=True)

        

    # ---------------------------
    # 3️⃣ Benzer Oyuncular
    # ---------------------------
    st.subheader("🔍 Benzer Oyuncular")
    
    # Her seçilen oyuncu için benzer oyuncular bul
    for player_name in selected_players:
        player_row = selected_rows[selected_rows["Player"] == player_name]
        if not player_row.empty:
            df_metrics = df_filtered[radar_metrics].copy()
            selected_vector = player_row[radar_metrics].values.flatten()
            df_temp = df_filtered.copy()
            df_temp["Similarity"] = np.linalg.norm(df_metrics.values - selected_vector, axis=1)
            similar_players = df_temp[df_temp["Player"] != player_name].nsmallest(5, "Similarity")
            
            st.write(f"**{player_name}** oyuncusuna en benzer 5 oyuncu:")
            st.dataframe(similar_players[["Player","Pos","Squad","Age","Cluster"] + radar_metrics])

    # ---------------------------
    # 4️⃣ Tüm Cluster’ları Karşılaştırma
    # ---------------------------
    st.subheader("Tüm Cluster'ları Karşılaştırma")
    df_scaled_all = pd.DataFrame(MinMaxScaler().fit_transform(df_filtered[radar_metrics]),
                                 columns=radar_metrics, index=df_filtered.index)
    cluster_means_scaled = df_scaled_all.groupby(df_filtered["Cluster"]).mean()
    fig_all = go.Figure()
    colors = ['#F97316','#EC4899','#06B6D4']  # 3 cluster için: Turuncu, Pembe, Turkuaz
    for idx, (cid,row) in enumerate(cluster_means_scaled.iterrows()):
        # İlk değeri sona ekleyerek kapalı çokgen oluştur
        r_all_values = list(row.values) + [row.values[0]]
        theta_all_values = [column_info[m] for m in radar_metrics] + [column_info[radar_metrics[0]]]
        
        fig_all.add_trace(go.Scatterpolar(
            r=r_all_values,
            theta=theta_all_values,
            fill='toself',
            name=f"Cluster {cid}",
            line=dict(width=2,color=colors[idx%len(colors)]),
            opacity=0.7
        ))
    fig_all.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,1])),
        showlegend=True,
        title="Tüm Cluster'ların Karşılaştırması",
        template='plotly_dark'
    )
    st.plotly_chart(fig_all, use_container_width=True, key="all_clusters_radar")

    # ---------------------------
    # 5️⃣ PDF / Excel Rapor
    # ---------------------------
    st.subheader("💾 Rapor İndir")
    
    if len(selected_players) == 1:
        # Tek oyuncu için mevcut format
        player_name = selected_players[0]
        player_row = selected_rows[selected_rows["Player"] == player_name]
        df_metrics = df_filtered[radar_metrics].copy()
        selected_vector = player_row[radar_metrics].values.flatten()
        df_temp = df_filtered.copy()
        df_temp["Similarity"] = np.linalg.norm(df_metrics.values - selected_vector, axis=1)
        similar_players = df_temp[df_temp["Player"] != player_name].nsmallest(5, "Similarity")
        
        # Excel
        excel_buffer = BytesIO()
        similar_players.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)
        st.download_button(label=f"{player_name} - Benzer Oyuncuları Excel İndir",
                           data=excel_buffer,
                           file_name=f"{player_name}_similar_players.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"{player_name} - Benzer Oyuncular", ln=True)
        for idx, row in similar_players.iterrows():
            line = f"{row['Player']} | {row['Pos']} | {row['Squad']} | Cluster {row['Cluster']}"
            pdf.cell(200, 10, txt=line, ln=True)
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button(label=f"{player_name} - Benzer Oyuncuları PDF İndir",
                           data=pdf_output,
                           file_name=f"{player_name}_similar_players.pdf",
                           mime="application/pdf")
    
    elif len(selected_players) > 1:
        # Çoklu oyuncu için karşılaştırma raporu
        comparison_data = selected_rows[["Player","Pos","Squad","Age","Cluster"] + radar_metrics]
        
        # Excel
        excel_buffer = BytesIO()
        comparison_data.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)
        st.download_button(label="Seçilen Oyuncular Karşılaştırması - Excel İndir",
                           data=excel_buffer,
                           file_name=f"oyuncu_karsilastirmasi_{len(selected_players)}_oyuncu.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Oyuncu Karsilastirmasi - {len(selected_players)} Oyuncu", ln=True)
        pdf.ln(5)
        for idx, row in comparison_data.iterrows():
            line = f"{row['Player']} | {row['Pos']} | {row['Squad']} | Yas: {row['Age']} | Cluster: {row['Cluster']}"
            pdf.cell(200, 10, txt=line, ln=True)
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button(label="Seçilen Oyuncular Karşılaştırması - PDF İndir",
                           data=pdf_output,
                           file_name=f"oyuncu_karsilastirmasi_{len(selected_players)}_oyuncu.pdf",
                           mime="application/pdf")

update_player_view(player_select)



#streamlit run streamlit_app.py
