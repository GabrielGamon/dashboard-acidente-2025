import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Segurança nas Rodovias Federais",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Segurança nas Rodovias Federais")

st.write("""
Este dashboard apresenta uma análise dos acidentes registrados
nas rodovias federais brasileiras em 2025, utilizando dados abertos
da Polícia Rodoviária Federal (PRF).

O objetivo é identificar quais estados registraram mais acidentes
e observar como a quantidade de ocorrências variou ao longo do ano.
""")

arquivo = st.file_uploader(
    "Envie o arquivo CSV da PRF",
    type=["csv"]
)

if arquivo is not None:

    df = pd.read_csv(
        arquivo,
        sep=";",
        encoding="latin1"
    )

    # -----------------------------
    # TRATAMENTO
    # -----------------------------

    df["data_inversa"] = pd.to_datetime(
        df["data_inversa"],
        errors="coerce"
    )

    df["mes"] = df["data_inversa"].dt.month

    meses = {
        1: "Jan",
        2: "Fev",
        3: "Mar",
        4: "Abr",
        5: "Mai",
        6: "Jun",
        7: "Jul",
        8: "Ago",
        9: "Set",
        10: "Out",
        11: "Nov",
        12: "Dez"
    }

    df["nome_mes"] = df["mes"].map(meses)

    # -----------------------------
    # INDICADORES
    # -----------------------------

    st.subheader("Resumo geral")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Acidentes registrados",
        f"{len(df):,}".replace(",", ".")
    )

    col2.metric(
        "Pessoas feridas",
        f"{int(df['feridos'].sum()):,}".replace(",", ".")
    )

    col3.metric(
        "Mortes registradas",
        f"{int(df['mortos'].sum()):,}".replace(",", ".")
    )

    # -----------------------------
    # GRÁFICO 1
    # -----------------------------

    acidentes_estado = (
        df.groupby("uf")
        .size()
        .reset_index(name="Quantidade de acidentes")
        .sort_values(
            "Quantidade de acidentes",
            ascending=False
        )
    )

    fig_estado = px.bar(
        acidentes_estado,
        x="uf",
        y="Quantidade de acidentes",
        title="Quantidade de Acidentes por Estado em 2025"
    )

    st.plotly_chart(
        fig_estado,
        use_container_width=True
    )

    maior_estado = acidentes_estado.iloc[0]

    st.markdown(f"""
    ### O que podemos observar?

    O gráfico compara a quantidade de acidentes registrados nas rodovias
    federais de cada estado durante 2025.

    O estado com maior quantidade de ocorrências foi **{maior_estado["uf"]}**,
    com **{maior_estado["Quantidade de acidentes"]} acidentes registrados**.

    Esses dados mostram a quantidade de ocorrências registradas, mas não são
    suficientes para afirmar que um estado seja mais perigoso do que outro.
    """)

    # -----------------------------
    # GRÁFICO 2
    # -----------------------------

    acidentes_mes = (
        df.groupby(["mes", "nome_mes"])
        .size()
        .reset_index(name="Quantidade de acidentes")
        .sort_values("mes")
    )

    fig_mes = px.line(
        acidentes_mes,
        x="nome_mes",
        y="Quantidade de acidentes",
        markers=True,
        title="Evolução Mensal dos Acidentes em 2025"
    )

    st.plotly_chart(
        fig_mes,
        use_container_width=True
    )

    maior_mes = acidentes_mes.loc[
        acidentes_mes["Quantidade de acidentes"].idxmax()
    ]

    st.markdown(f"""
    ### O que podemos observar?

    O gráfico mostra como a quantidade de acidentes variou ao longo
    dos meses de 2025.

    O mês com maior quantidade de ocorrências foi **{maior_mes["nome_mes"]}**,
    com **{maior_mes["Quantidade de acidentes"]} acidentes registrados**.

    É possível observar variações durante o ano, mas a base sozinha
    não permite determinar as causas dessas diferenças.
    """)

    # -----------------------------
    # VISUALIZAÇÃO DOS DADOS
    # -----------------------------

    st.subheader("Visualização dos dados")

    df_visual = df.copy()

    df_visual["data_inversa"] = df_visual["data_inversa"].dt.strftime("%d/%m/%Y")

    st.dataframe(
        df_visual[
            [
                "data_inversa",
                "uf",
                "municipio",
                "causa_acidente",
                "feridos",
                "mortos"
            ]
        ].head(10)
    )

    st.caption(
        "Fonte: Polícia Rodoviária Federal (PRF) — Dados Abertos."
    )