import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Profil Keuangan Pemda", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="LRA_Pemda7.xlsx",
        engine="openpyxl",
        sheet_name="Sheet3",
        skiprows=0,
        usecols="A:F",
        nrows=1570,
    )
    return df

df = get_data_from_excel()
    
# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
pemda = st.sidebar.selectbox(
    "Pilih Pemda:",
    options=df["Pemda"].unique()
)

tahun = st.sidebar.selectbox(
    "Pilih Tahun:",
    options=df["Tahun"].unique()
)

df_selection = df.query(
    "Pemda == @pemda & Tahun ==@tahun"
)

# ---- MAINPAGE ----
st.title(":bar_chart: Profil Keuangan Pemda")
st.markdown("##")

# TOP KPI's
total_pendapatan = int(df_selection["Pendapatan"].sum())
total_belanja = int(df_selection["Belanja"].sum())

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total Pendapatan:")
    st.subheader(f"IDR {total_pendapatan:,}")
    
with right_column:
    st.subheader("Total Belanja:")
    st.subheader(f"IDR {total_belanja:,}")
    
st.markdown("""---""")

# PENDAPATAN PER BULAN [BAR CHART]
pendapatan_per_bulan = df_selection.groupby(by=["Bulan"]).sum()[["Pendapatan"]]
fig_pendapatan_bulanan = px.bar(
    pendapatan_per_bulan,
    x=pendapatan_per_bulan.index,
    y="Pendapatan",
    title="<b>PENDAPATAN PER BULAN</b>",
    color_discrete_sequence=["#0083B8"] * len(pendapatan_per_bulan),
    template="plotly_white",
)
fig_pendapatan_bulanan.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

# BELANJA PER BULAN [BAR CHART]
belanja_per_bulan = df_selection.groupby(by=["Bulan"]).sum()[["Belanja"]]
fig_belanja_bulanan = px.bar(
    belanja_per_bulan,
    x=belanja_per_bulan.index,
    y="Belanja",
    title="<b>BELANJA PER BULAN</b>",
    color_discrete_sequence=["#0083B8"] * len(belanja_per_bulan),
    template="plotly_white",
)
fig_belanja_bulanan.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_pendapatan_bulanan, use_container_width=True)
right_column.plotly_chart(fig_belanja_bulanan, use_container_width=True)
