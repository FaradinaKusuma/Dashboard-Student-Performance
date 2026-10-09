import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# KONFIGURASI HALAMAN
# ============================================================

st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("StudentsPerformance.csv")


df = load_data()


# ============================================================
# JUDUL UTAMA
# ============================================================

st.title("🎓 Student Performance Analytics Dashboard")

st.markdown(
    "Aplikasi interaktif untuk menganalisis performa akademik "
    "siswa berdasarkan faktor demografi dan latar belakang."
)


# ============================================================
# SIDEBAR - FILTER DATA
# ============================================================

st.sidebar.header("⚙️ Filter Data")


gender = st.sidebar.multiselect(
    "Jenis Kelamin:",
    options=df["gender"].unique(),
    default=df["gender"].unique()
)


race = st.sidebar.multiselect(
    "Kelompok Ras/Etnis:",
    options=df["race/ethnicity"].unique(),
    default=df["race/ethnicity"].unique()
)


parent_edu = st.sidebar.multiselect(
    "Pendidikan Orang Tua:",
    options=df["parental level of education"].unique(),
    default=df["parental level of education"].unique()
)


test_prep = st.sidebar.multiselect(
    "Persiapan Ujian:",
    options=df["test preparation course"].unique(),
    default=df["test preparation course"].unique()
)


# ============================================================
# FILTER DATA
# ============================================================

df_filtered = df[
    (df["gender"].isin(gender))
    & (df["race/ethnicity"].isin(race))
    & (df["parental level of education"].isin(parent_edu))
    & (df["test preparation course"].isin(test_prep))
].copy()


# ============================================================
# HITUNG RATA-RATA NILAI
# ============================================================

if not df_filtered.empty:

    df_filtered["average score"] = df_filtered[
        [
            "math score",
            "reading score",
            "writing score"
        ]
    ].mean(axis=1)

else:

    df_filtered["average score"] = pd.Series(
        dtype="float64"
    )


# ============================================================
# METRICS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)


with col1:
    st.metric(
        "Total Siswa",
        len(df_filtered)
    )


with col2:
    st.metric(
        "Rata-rata Math",
        f"{df_filtered['math score'].mean():.1f}"
        if not df_filtered.empty
        else "0"
    )


with col3:
    st.metric(
        "Rata-rata Reading",
        f"{df_filtered['reading score'].mean():.1f}"
        if not df_filtered.empty
        else "0"
    )


with col4:
    st.metric(
        "Rata-rata Writing",
        f"{df_filtered['writing score'].mean():.1f}"
        if not df_filtered.empty
        else "0"
    )


with col5:
    st.metric(
        "Rata-rata Overall",
        f"{df_filtered['average score'].mean():.1f}"
        if not df_filtered.empty
        else "0"
    )


st.markdown("---")


# ============================================================
# TAB VISUALISASI
# ============================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Distribusi & Korelasi",
        "📈 Perbandingan Demografi",
        "📄 Data Tabular"
    ]
)


# ============================================================
# TAB 1 - DISTRIBUSI & KORELASI
# ============================================================

with tab1:

    st.subheader(
        "Distribusi Nilai & Korelasi Antar Pelajaran"
    )

    col_a, col_b = st.columns(2)


    # --------------------------------------------------------
    # GRAFIK DISTRIBUSI
    # --------------------------------------------------------

    with col_a:

        score_type = st.selectbox(
            "Pilih Mata Pelajaran:",
            [
                "math score",
                "reading score",
                "writing score",
                "average score"
            ]
        )


        if not df_filtered.empty:

            fig_hist = px.histogram(
                df_filtered,
                x=score_type,
                color="gender",
                marginal="box",
                nbins=30,
                title=(
                    f"Distribusi {score_type.title()} "
                    "berdasarkan Gender"
                ),
                barmode="overlay"
            )

            st.plotly_chart(
                fig_hist,
                use_container_width=True
            )

        else:

            st.warning(
                "Tidak ada data yang sesuai dengan filter."
            )


    # --------------------------------------------------------
    # GRAFIK SCATTER / KORELASI
    # --------------------------------------------------------

    with col_b:

        if not df_filtered.empty:

            fig_scatter = px.scatter(
                df_filtered,
                x="reading score",
                y="writing score",
                color="math score",
                hover_data=[
                    "gender",
                    "parental level of education"
                ],
                title=(
                    "Korelasi Reading vs Writing Score "
                    "(Warna = Math Score)"
                )
            )

            st.plotly_chart(
                fig_scatter,
                use_container_width=True
            )

        else:

            st.warning(
                "Tidak ada data untuk ditampilkan."
            )


# ============================================================
# TAB 2 - PERBANDINGAN DEMOGRAFI
# ============================================================

with tab2:

    st.subheader(
        "Perbandingan Nilai Rata-rata berdasarkan Kategori"
    )


    group_col = st.selectbox(
        "Kelompokkan Berdasarkan:",
        [
            "gender",
            "race/ethnicity",
            "parental level of education",
            "lunch",
            "test preparation course"
        ]
    )


    if not df_filtered.empty:

        df_grouped = (
            df_filtered
            .groupby(group_col)[
                [
                    "math score",
                    "reading score",
                    "writing score"
                ]
            ]
            .mean()
            .reset_index()
        )


        fig_bar = px.bar(
            df_grouped,
            x=group_col,
            y=[
                "math score",
                "reading score",
                "writing score"
            ],
            barmode="group",
            title=(
                f"Rata-rata Nilai berdasarkan "
                f"{group_col.title()}"
            )
        )


        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )

    else:

        st.warning(
            "Tidak ada data yang sesuai dengan filter."
        )


# ============================================================
# TAB 3 - DATA TABULAR
# ============================================================

with tab3:

    st.subheader("Data Siswa Tersaring")


    st.dataframe(
        df_filtered,
        use_container_width=True
    )


    st.caption(
        f"Menampilkan {len(df_filtered)} "
        f"dari {len(df)} total baris data."
    )