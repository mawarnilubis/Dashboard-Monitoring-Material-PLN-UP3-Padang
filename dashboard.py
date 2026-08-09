"""
DASHBOARD MONITORING MATERIAL GUDANG - PLN UP3
Gabungan: Material Masuk SP2B | Material Return | Material Keluar
Dibangun dengan Streamlit + Plotly (Tanpa Sidebar Filter)
Cara menjalankan:
streamlit run dashboard.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="PLN UP3 | Dashboard Monitoring Material Gudang",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Konfigurasi Spreadsheet (Sheet ID sama, GID berbeda tiap modul)
SHEET_ID = "107fOUVlUVh0VdUZp1tHZzL5B6-QcPIdarmMTAGOdzcg"
GID_MASUK = "347674201"
GID_RETURN = "2024563293"
GID_KELUAR = "2083300164"
URL_MASUK = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID_MASUK}"
URL_RETURN = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID_RETURN}"
URL_KELUAR = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID_KELUAR}"

# 2. CUSTOM CSS - CORPORATE THEME (PLN)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: linear-gradient(180deg, #f4f6fb 0%, #eef1f8 100%);
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ---------- HERO BANNER UTAMA ---------- */
    .hero-banner {
        background: linear-gradient(115deg, #062250 0%, #0b2f66 38%, #12428c 68%, #1a5bb8 100%);
        padding: 34px 40px;
        border-radius: 18px;
        margin-bottom: 18px;
        box-shadow: 0 12px 30px rgba(11, 36, 71, 0.30);
        position: relative;
        overflow: hidden;
        border-bottom: 6px solid #ffcc00;
    }
    .hero-banner::before {
        content: "";
        position: absolute;
        top: 0; right: 0; bottom: 0;
        width: 42%;
        background: linear-gradient(115deg, rgba(255,204,0,0) 0%, rgba(255,204,0,0.16) 55%, rgba(255,204,0,0.32) 100%);
        clip-path: polygon(35% 0, 100% 0, 100% 100%, 0% 100%);
        pointer-events: none;
    }
    .hero-title {
        color: #ffffff;
        font-size: 32px;
        font-weight: 800;
        margin: 0;
        letter-spacing: 0.3px;
        display: flex;
        align-items: center;
        gap: 12px;
        text-shadow: 0 2px 6px rgba(0,0,0,0.35);
        position: relative;
        z-index: 2;
    }
    .hero-subtitle {
        color: #eaf1fc;
        font-size: 15px;
        font-weight: 400;
        margin-top: 8px;
        max-width: 760px;
        line-height: 1.6;
        text-shadow: 0 1px 4px rgba(0,0,0,0.25);
        position: relative;
        z-index: 2;
    }
    .hero-badge {
        display: inline-block;
        background: #ffcc00;
        color: #062250;
        font-weight: 800;
        font-size: 12px;
        padding: 6px 16px;
        border-radius: 20px;
        margin-top: 16px;
        margin-right: 8px;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 12px rgba(255, 204, 0, 0.35);
        position: relative;
        z-index: 2;
    }

    /* ---------- SUB-HEADER TIAP TAB MODUL ---------- */
    .module-header {
        display: flex;
        align-items: center;
        gap: 12px;
        background: #ffffff;
        border-radius: 14px;
        padding: 16px 22px;
        margin: 6px 0 20px 0;
        box-shadow: 0 4px 14px rgba(20, 40, 80, 0.06);
        border-left: 6px solid #1a5bb8;
    }
    .module-header .icon {
        font-size: 28px;
    }
    .module-header .title {
        font-size: 19px;
        font-weight: 800;
        color: #0b2447;
        margin: 0;
    }
    .module-header .desc {
        font-size: 13px;
        color: #6b7280;
        margin: 2px 0 0 0;
    }

    /* ---------- KPI CARDS ---------- */
    .kpi-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 22px 24px;
        box-shadow: 0 6px 18px rgba(20, 40, 80, 0.08);
        border-left: 6px solid #ffcc00;
        transition: transform 0.2s ease;
        height: 100%;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
    }
    .kpi-card.blue { border-left-color: #1e5fa8; }
    .kpi-card.red { border-left-color: #e63946; }
    .kpi-label {
        font-size: 13px;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 30px;
        font-weight: 800;
        color: #0b2447;
        margin: 0;
    }
    .kpi-icon {
        font-size: 26px;
        margin-bottom: 8px;
    }

    /* ---------- SECTION & CHART ---------- */
    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #0b2447;
        margin-top: 10px;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-desc {
        font-size: 13px;
        color: #6b7280;
        margin-bottom: 16px;
    }
    .chart-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 18px 22px 6px 22px;
        box-shadow: 0 6px 18px rgba(20, 40, 80, 0.07);
        margin-bottom: 22px;
    }
    hr {
        border: none;
        border-top: 1px solid #e2e6ee;
        margin: 22px 0;
    }

    /* ---------- TABS STYLING ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: #ffffff;
        padding: 8px;
        border-radius: 14px;
        box-shadow: 0 4px 14px rgba(20, 40, 80, 0.06);
    }
    .stTabs [data-baseweb="tab"] {
        height: 46px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 14px;
        color: #0b2447;
        padding: 0 18px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(115deg, #12428c 0%, #1a5bb8 100%) !important;
        color: #ffffff !important;
    }
</style>""", unsafe_allow_html=True)

# 3. FUNGSI LOAD & PREP DATA
@st.cache_data(ttl=600)
def load_data_masuk(url: str) -> pd.DataFrame:
    """Load & preprocessing untuk data Material Masuk SP2B (logika asli dipertahankan)."""
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    df.rename(columns={df.columns[0]: 'WAKTU'}, inplace=True)

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    df.replace(["#N/A", "nan", "None"], np.nan, inplace=True)

    if "JUMLAH" in df.columns:
        df["JUMLAH"] = df["JUMLAH"].astype(str).str.replace(",", ".", regex=False)
        df["JUMLAH"] = pd.to_numeric(df["JUMLAH"], errors="coerce")

    df.dropna(how="all", inplace=True)
    if "NAMA MATERIAL" in df.columns:
        df = df[df["NAMA MATERIAL"].notna()]
    df = df[df["WAKTU"].notna()]

    for col in df.columns:
        if col == "JUMLAH":
            df[col] = df[col].fillna(0)
        else:
            df[col] = df[col].fillna("-")

    df.reset_index(drop=True, inplace=True)

    df["WAKTU_DT"] = pd.to_datetime(df["WAKTU"], format="%d/%m/%Y", errors="coerce")
    if df["WAKTU_DT"].notna().sum() == 0:
        df["WAKTU_DT"] = pd.to_datetime(df["WAKTU"], errors="coerce")

    if "VENDOR PENGANTAR / PENGADAAN" not in df.columns:
        vendor_cols = [c for c in df.columns if "VENDOR" in c or "PENGANTAR" in c]
        if vendor_cols:
            df["VENDOR PENGANTAR / PENGADAAN"] = df[vendor_cols[0]]
        else:
            df["VENDOR PENGANTAR / PENGADAAN"] = "TIDAK DIKETAHUI"

    return df

@st.cache_data(ttl=600)
def load_data_return(url: str) -> pd.DataFrame:
    """Load & preprocessing untuk data Material Return (logika asli dipertahankan)."""
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    df.rename(columns={df.columns[0]: 'WAKTU'}, inplace=True)

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    df.replace(["#N/A", "nan", "None"], np.nan, inplace=True)

    if "JUMLAH" in df.columns:
        df["JUMLAH"] = df["JUMLAH"].astype(str).str.replace(",", ".", regex=False)
        df["JUMLAH"] = pd.to_numeric(df["JUMLAH"], errors="coerce")

    df.dropna(how="all", inplace=True)
    if "NAMA MATERIAL" in df.columns:
        df = df[df["NAMA MATERIAL"].notna()]
    df = df[df["WAKTU"].notna()]

    for col in df.columns:
        if col == "JUMLAH":
            df[col] = df[col].fillna(0)
        else:
            df[col] = df[col].fillna("-")

    df.reset_index(drop=True, inplace=True)

    df["WAKTU_DT"] = pd.to_datetime(df["WAKTU"], format="%d/%m/%Y", errors="coerce")
    if df["WAKTU_DT"].notna().sum() == 0:
        df["WAKTU_DT"] = pd.to_datetime(df["WAKTU"], errors="coerce")

    return df

@st.cache_data(ttl=600)
def load_data_keluar(url: str) -> pd.DataFrame:
    """Load & preprocessing untuk data Material Keluar (logika asli dipertahankan)."""
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()

    # 1. Cleaning string spasi liar
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # 2. Penanganan Missing Values / Null String
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    df.replace(["#N/A", "nan", "None"], np.nan, inplace=True)

    # 3. Konversi Kolom JUMLAH
    if "JUMLAH" in df.columns:
        df["JUMLAH"] = df["JUMLAH"].astype(str).str.replace(",", ".", regex=False)
        df["JUMLAH"] = pd.to_numeric(df["JUMLAH"], errors="coerce")

    # 4. Filter Baris Utama Kosong
    df.dropna(how="all", inplace=True)
    if "NAMA MATERIAL" in df.columns:
        df = df[df["NAMA MATERIAL"].notna()]
    if "WAKTU" in df.columns:
        df = df[df["WAKTU"].notna()]

    # 5. Imputasi Default Value
    for col in df.columns:
        if col == "JUMLAH":
            df[col] = df[col].fillna(0)
        else:
            df[col] = df[col].fillna("-")

    # 6. Pembersihan Tahun & Datetime Parsing
    if "WAKTU" in df.columns:
        df["WAKTU"] = df["WAKTU"].astype(str).str.replace("2005", "2025", regex=False)
        df["WAKTU_DT"] = pd.to_datetime(df["WAKTU"], format="%d/%m/%Y", errors="coerce")
        if df["WAKTU_DT"].notna().sum() == 0:
            df["WAKTU_DT"] = pd.to_datetime(df["WAKTU"], errors="coerce")

    # CATATAN: drop_duplicates() TIDAK DIGUNAKAN
    # agar transaksi bernilai sama persis tidak terhapus.
    df.reset_index(drop=True, inplace=True)

    return df

def build_bar_chart(series: pd.Series, hover_label: str, hover_unit: str = "") -> go.Figure:
    """Fungsi bantu untuk membangun bar chart horizontal Top 10 (styling identik di semua modul)."""
    fig_max = float(series.values.max()) if len(series) > 0 else 1.0

    fig = go.Figure(go.Bar(
        x=series.values,
        y=series.index,
        orientation="h",
        marker=dict(
            color=series.values,
            colorscale=[[0, "#ffcc00"], [1, "#1e5fa8"]],
        ),
        text=series.values,
        textposition="outside",
        cliponaxis=False,
        hovertemplate=f"<b>%{{y}}</b><br>{hover_label}: %{{x}}{hover_unit}<extra></extra>",
    ))

    fig.update_layout(
        height=480,
        margin=dict(l=30, r=100, t=20, b=60),
        xaxis_title=dict(text=hover_label, font=dict(color="#0b2447", size=13), standoff=15),
        yaxis_title="",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Poppins, sans-serif", color="#0b2447", size=13),
        xaxis=dict(
            showgrid=True, gridcolor="#eef1f8",
            tickfont=dict(color="#0b2447", size=12),
            range=[0, fig_max * 1.25],
        ),
        yaxis=dict(
            tickfont=dict(color="#0b2447", size=12, weight="bold"),
            automargin=True,
        ),
        uniformtext_minsize=11,
        uniformtext_mode="show",
    )
    fig.update_traces(textfont=dict(color="#0b2447", size=12))
    return fig

def kpi_card(col, icon: str, label: str, value, variant: str = ""):
    css_class = f"kpi-card {variant}".strip()
    with col:
        st.markdown(f"""
        <div class="{css_class}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <p class="kpi-value">{value:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)

# 4. HERO HEADER UTAMA
st.markdown("""
<div class="hero-banner">
    <p class="hero-title">⚡ Dashboard Monitoring Material Gudang</p>
    <p class="hero-subtitle">
        Pusat pemantauan arus material gudang PLN UP3 secara real-time — mencakup material masuk (SP2B),
        material return, dan material keluar. Mendukung evaluasi rantai pasok, manajemen vendor,
        dan pengambilan keputusan berbasis data.
    </p>
    <span class="hero-badge">PLN UP3</span>
    <span class="hero-badge">MONITORING MATERIAL GUDANG</span>
</div>
""", unsafe_allow_html=True)

# 5. NAVIGASI TAB ANTAR MODUL (Urutan diubah: Material Keluar, Material Masuk, Material Return)
tab_keluar, tab_masuk, tab_return = st.tabs([
    "📤  Material Keluar",
    "📥  Material Masuk (SP2B)",
    "🔄  Material Return",
])

# TAB 1 — MATERIAL KELUAR
with tab_keluar:
    try:
        with st.spinner("🔄 Mengambil data Material Keluar dari Google Sheets..."):
            df_keluar = load_data_keluar(URL_KELUAR)
    except Exception as e:
        st.error(f"⚠️ Gagal mengambil data Material Keluar: {e}")
        df_keluar = pd.DataFrame()

    st.markdown("""
    <div class="module-header">
        <div class="icon">📤</div>
        <div>
            <p class="title">Monitoring Material Keluar</p>
            <p class="desc">Tingkat konsumsi, frekuensi pengeluaran, dan item material paling kritis di gudang</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if df_keluar.empty:
        st.warning("Tidak ada data pengeluaran material yang tersedia.")
    else:
        total_transaksi_keluar = len(df_keluar)
        total_volume_keluar = df_keluar["JUMLAH"].sum() if "JUMLAH" in df_keluar.columns else 0
        jumlah_item_material = df_keluar["NAMA MATERIAL"].nunique() if "NAMA MATERIAL" in df_keluar.columns else 0

        c1, c2, c3 = st.columns(3)
        kpi_card(c1, "📤", "Total Transaksi Keluar", total_transaksi_keluar)
        kpi_card(c2, "📦", "Total Volume Keluar", total_volume_keluar, "blue")
        kpi_card(c3, "🏷️", "Variasi Jenis Material", jumlah_item_material, "red")

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown('<p class="section-title">🏆 Top 10 Material yang Paling Sering Dikeluarkan</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-desc">Peringkat 10 jenis material gudang dengan frekuensi transaksi pengambilan terbanyak</p>', unsafe_allow_html=True)

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        top10_material = (
            df_keluar["NAMA MATERIAL"]
            .value_counts()
            .head(10)
            .sort_values(ascending=True)
        )
        fig_keluar = build_bar_chart(top10_material, "Frekuensi Pengeluaran", " kali")
        st.plotly_chart(fig_keluar, use_container_width=True, theme=None, key="chart_keluar")
        st.markdown('</div>', unsafe_allow_html=True)

# TAB 2 — MATERIAL MASUK SP2B
with tab_masuk:
    try:
        with st.spinner("🔄 Mengambil data Material Masuk dari Google Sheets..."):
            df_masuk = load_data_masuk(URL_MASUK)
    except Exception as e:
        st.error(f"⚠️ Gagal mengambil data Material Masuk: {e}")
        df_masuk = pd.DataFrame()

    st.markdown("""
    <div class="module-header">
        <div class="icon">📥</div>
        <div>
            <p class="title">Monitoring Material Masuk SP2B</p>
            <p class="desc">Frekuensi pasokan, volume, dan pemetaan vendor pengantar material gudang</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if df_masuk.empty:
        st.warning("Tidak ada data yang tersedia pada spreadsheet Material Masuk.")
    else:
        total_transaksi = len(df_masuk)
        total_material_masuk = df_masuk["JUMLAH"].sum() if "JUMLAH" in df_masuk.columns else 0
        jumlah_vendor = df_masuk["VENDOR PENGANTAR / PENGADAAN"].nunique()

        c1, c2, c3 = st.columns(3)
        kpi_card(c1, "📦", "Total Transaksi Masuk", total_transaksi)
        kpi_card(c2, "📥", "Total Volume Masuk", total_material_masuk, "blue")
        kpi_card(c3, "🏢", "Jumlah Vendor / Pengantar", jumlah_vendor, "red")

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown('<p class="section-title">🏆 Top 10 Vendor / Pengantar Material Paling Dominan</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-desc">Peringkat 10 vendor atau unit pengantar material masuk teraktif berdasarkan frekuensi pengiriman</p>', unsafe_allow_html=True)

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        top10_vendors = (
            df_masuk["VENDOR PENGANTAR / PENGADAAN"]
            .value_counts()
            .head(10)
            .sort_values(ascending=True)
        )
        fig_masuk = build_bar_chart(top10_vendors, "Frekuensi Pengiriman")
        st.plotly_chart(fig_masuk, use_container_width=True, theme=None, key="chart_masuk")
        st.markdown('</div>', unsafe_allow_html=True)

# TAB 3 — MATERIAL RETURN
with tab_return:
    try:
        with st.spinner("🔄 Mengambil data Material Return dari Google Sheets..."):
            df_return = load_data_return(URL_RETURN)
    except Exception as e:
        st.error(f"⚠️ Gagal mengambil data Material Return: {e}")
        df_return = pd.DataFrame()

    st.markdown("""
    <div class="module-header">
        <div class="icon">🔄</div>
        <div>
            <p class="title">Monitoring Material Return</p>
            <p class="desc">Analisis frekuensi pengembalian (return) material gudang</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if df_return.empty:
        st.warning("Tidak ada data yang tersedia pada spreadsheet Material Return.")
    else:
        total_transaksi_return = len(df_return)
        total_volume_return = df_return["JUMLAH"].sum() if "JUMLAH" in df_return.columns else 0
        total_jenis_material = df_return["NAMA MATERIAL"].nunique() if "NAMA MATERIAL" in df_return.columns else 0

        c1, c2, c3 = st.columns(3)
        kpi_card(c1, "🔄", "Total Transaksi Return", total_transaksi_return)
        kpi_card(c2, "📉", "Total Volume Return", total_volume_return, "blue")
        kpi_card(c3, "🏷️", "Variasi Jenis Material", total_jenis_material, "red")

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown('<p class="section-title">🔄 Top 10 Material yang Paling Sering Return</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-desc">Peringkat 10 material gudang dengan frekuensi pengembalian (return) tertinggi</p>', unsafe_allow_html=True)

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        top10_material_return = (
            df_return["NAMA MATERIAL"]
            .value_counts()
            .head(10)
            .sort_values(ascending=True)
        )
        fig_return = build_bar_chart(top10_material_return, "Frekuensi Return")
        st.plotly_chart(fig_return, use_container_width=True, theme=None, key="chart_return")
        st.markdown('</div>', unsafe_allow_html=True)