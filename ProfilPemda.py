import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Dashboard Profil Pemda", layout="wide")

# ---- READ EXCEL ----
df = pd.read_excel(
        io="LRA_Pemda5.xlsx",
        engine="openpyxl",
        sheet_name="Sheet3",
        skiprows=0,
        usecols="A:F",
        nrows=157,
)

# ---- SIDEBAR ----
st.sidebar.header("Pilih Disini:")
pemda = st.sidebar.selectbox(
    "Pilih Pemerintah Daerah:",
    options=df["Pemda"].unique(),
)
tahun = st.sidebar.selectbox(
    "Pilih Tahun:",
    options=df["Tahun"].unique(),
)

df_selection = df.query(
    "Pemda == @pemda & Tahun ==@tahun"
)

# ---- MAINPAGE ----
st.title(":bar_chart: Dashboard Profil Keuangan Pemda se-Provinsi Jambi")
st.markdown("##")

# TOP KPI's
total_pendapatan = int(df_selection["Pendapatan"].sum())
total_belanja = int(df_selection["Belanja Daerah"].sum())

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total Belanja:")
    st.subheader(f"Rp {total_belanja:,}")

with right_column:
    st.subheader("Total Pendapatan:")
    st.subheader(f"Rp {total_pendapatan:,}")
    
st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
pendapatan_per_bulan = df_selection.groupby(by=["Bulan"]).sum()[["Pendapatan"]]
fig_pendapatan_pemda = px.bar(
    pendapatan_per_bulan,
    x=pendapatan_per_bulan.index,
    y="Pendapatan",
    title="<b>Pendapatan per Bulan</b>",
    color_discrete_sequence=["#0083B8"] * len(pendapatan_per_bulan),
    template="plotly_white",
)

# SALES BY HOUR [BAR CHART]
belanja_per_bulan = df_selection.groupby(by=["Bulan"]).sum()[["Belanja Daerah"]]
fig_belanja_pemda = px.bar(
    belanja_per_bulan,
    x=belanja_per_bulan.index,
    y="Belanja Daerah",
    title="<b>Belanja per Bulan</b>",
    color_discrete_sequence=["#0083B8"] * len(belanja_per_bulan),
    template="plotly_white",
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_belanja_pemda, use_container_width=True)
right_column.plotly_chart(fig_pendapatan_pemda, use_container_width=True)

st.markdown("""---""")

st.dataframe(df_selection)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)