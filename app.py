import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =========================================================
# CONFIGURAÇÃO
# =========================================================

st.set_page_config(
    page_title="SOTAM TECH",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

ESTOQUE_FILE = "estoque_sotam.csv"
VENDAS_FILE = "vendas_sotam.csv"

COLUNAS_ESTOQUE = [
    "ID",
    "Produto",
    "Categoria",
    "Custo",
    "Preco_Sugerido",
    "Status"
]

COLUNAS_VENDAS = [
    "ID_Venda",
    "Produto",
    "Valor_Venda",
    "Lucro",
    "Parcelas",
    "Data"
]


# =========================================================
# ESTILO VISUAL - SOTAM TECH
# =========================================================

st.markdown("""
<style>

    /* =========================
       FUNDO
       ========================= */

    .stApp {
        background: #f4f5f7;
        color: #171717;
    }

    [data-testid="stAppViewContainer"] {
        background: #f4f5f7;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }


    /* =========================
       ESCONDER ELEMENTOS PADRÃO
       ========================= */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e8e8e8;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    .sidebar-logo {
        background: #171717;
        color: white;
        border-radius: 16px;
        padding: 15px 16px;
        margin-bottom: 25px;
    }

    .sidebar-logo-title {
        font-size: 20px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    .sidebar-logo-sub {
        color: #aaaaaa;
        font-size: 11px;
        margin-top: 3px;
    }


    /* =========================
       TEXTOS
       ========================= */

    h1 {
        font-size: 32px !important;
        font-weight: 750 !important;
        letter-spacing: -1.2px !important;
    }

    h2 {
        font-size: 23px !important;
        font-weight: 700 !important;
    }

    h3 {
        font-size: 18px !important;
        font-weight: 700 !important;
    }


    /* =========================
       CARDS
       ========================= */

    .card {
        background: #ffffff;
        border: 1px solid #e9e9e9;
        border-radius: 20px;
        padding: 22px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.035);
        margin-bottom: 18px;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #e9e9e9;
        border-radius: 20px;
        padding: 21px;
        min-height: 130px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.035);
    }

    .metric-card-orange {
        background: linear-gradient(
            135deg,
            #ff7043,
            #f4511e
        );
        color: white;
        border-radius: 20px;
        padding: 21px;
        min-height: 130px;
        box-shadow: 0 8px 25px rgba(244,81,30,0.20);
    }

    .metric-title {
        font-size: 13px;
        color: #777777;
        font-weight: 500;
    }

    .metric-title-white {
        font-size: 13px;
        color: rgba(255,255,255,0.85);
        font-weight: 500;
    }

    .metric-value {
        font-size: 29px;
        font-weight: 750;
        margin-top: 13px;
        letter-spacing: -1px;
        color: #171717;
    }

    .metric-value-white {
        font-size: 29px;
        font-weight: 750;
        margin-top: 13px;
        letter-spacing: -1px;
        color: white;
    }

    .metric-description {
        font-size: 11px;
        color: #999999;
        margin-top: 7px;
    }

    .metric-description-white {
        font-size: 11px;
        color: rgba(255,255,255,0.8);
        margin-top: 7px;
    }


    /* =========================
       TÍTULO DO DASHBOARD
       ========================= */

    .welcome-title {
        font-size: 32px;
        font-weight: 750;
        letter-spacing: -1.2px;
        color: #171717;
    }

    .welcome-subtitle {
        color: #777777;
        font-size: 14px;
        margin-top: 5px;
        margin-bottom: 25px;
    }


    /* =========================
       BADGES
       ========================= */

    .badge-green {
        display: inline-block;
        background: #e9f8ef;
        color: #168344;
        border-radius: 20px;
        padding: 5px 10px;
        font-size: 11px;
        font-weight: 600;
    }

    .badge-orange {
        display: inline-block;
        background: #fff0e9;
        color: #e85b25;
        border-radius: 20px;
        padding: 5px 10px;
        font-size: 11px;
        font-weight: 600;
    }

    .badge-gray {
        display: inline-block;
        background: #f1f1f1;
        color: #777777;
        border-radius: 20px;
        padding: 5px 10px;
        font-size: 11px;
        font-weight: 600;
    }


    /* =========================
       BOTÕES
       ========================= */

    .stButton > button {
        border-radius: 12px;
        min-height: 42px;
        font-weight: 600;
        border: 1px solid #dedede;
        background: #ffffff;
    }

    .stButton > button:hover {
        border-color: #f4511e;
        color: #f4511e;
    }


    /* =========================
       INPUTS
       ========================= */

    input,
    textarea {
        border-radius: 12px !important;
    }

    div[data-baseweb="select"] > div {
        border-radius: 12px !important;
    }


    /* =========================
       TABELA
       ========================= */

    div[data-testid="stDataFrame"] {
        border: 1px solid #e9e9e9;
        border-radius: 16px;
        overflow: hidden;
    }


    /* =========================
       SEPARADORES
       ========================= */

    hr {
        border-color: #eeeeee;
    }


    /* =========================
       ATIVIDADES
       ========================= */

    .activity {
        background: #ffffff;
        border: 1px solid #eeeeee;
        border-radius: 14px;
        padding: 13px 16px;
        margin-bottom: 8px;
    }

    .activity-name {
        font-weight: 650;
        font-size: 14px;
    }

    .activity-date {
        color: #999999;
        font-size: 11px;
    }


    /* =========================
       BOX DE RESUMO
       ========================= */

    .summary-box {
        background: #ffffff;
        border: 1px solid #e9e9e9;
        border-radius: 20px;
        padding: 22px;
        min-height: 100%;
    }

    .summary-row {
        display: flex;
        justify-content: space-between;
        padding: 12px 0;
        border-bottom: 1px solid #f0f0f0;
        font-size: 13px;
    }

    .summary-label {
        color: #777777;
    }

    .summary-value {
        font-weight: 700;
        color: #171717;
    }


    /* =========================
       PROGRESSO
       ========================= */

    div[data-testid="stProgress"] > div > div {
        border-radius: 20px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# FUNÇÕES
# =========================================================

def carregar_dados(arq, colunas):

    if os.path.exists(arq):

        try:

            df = pd.read_csv(
                arq,
                encoding="utf-8-sig"
            )

            for coluna in colunas:

                if coluna not in df.columns:
                    df[coluna] = None

            return df[colunas]

        except Exception:

            st.warning(
                f"Não foi possível ler {arq}."
            )

    return pd.DataFrame(columns=colunas)


def salvar_dados(df, arq):

    df.to_csv(
        arq,
        index=False,
        encoding="utf-8-sig"
    )


def preparar_dados():

    if not df_estoque.empty:

        df_estoque["Custo"] = pd.to_numeric(
            df_estoque["Custo"],
            errors="coerce"
        ).fillna(0)

        df_estoque["Preco_Sugerido"] = pd.to_numeric(
            df_estoque["Preco_Sugerido"],
            errors="coerce"
        ).fillna(0)

        df_estoque["ID"] = pd.to_numeric(
            df_estoque["ID"],
            errors="coerce"
        ).fillna(0).astype(int)

    if not df_vendas.empty:

        df_vendas["Valor_Venda"] = pd.to_numeric(
            df_vendas["Valor_Venda"],
            errors="coerce"
        ).fillna(0)

        df_vendas["Lucro"] = pd.to_numeric(
            df_vendas["Lucro"],
            errors="coerce"
        ).fillna(0)

        df_vendas["ID_Venda"] = pd.to_numeric(
            df_vendas["ID_Venda"],
            errors="coerce"
        ).fillna(0).astype(int)


def proximo_id(df, coluna):

    if df.empty:
        return 1

    valores = pd.to_numeric(
        df[coluna],
        errors="coerce"
    ).dropna()

    if valores.empty:
        return 1

    return int(valores.max()) + 1


def moeda(valor):

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


# =========================================================
# CARREGAR DADOS
# =========================================================

df_estoque = carregar_dados(
    ESTOQUE_FILE,
    COLUNAS_ESTOQUE
)

df_vendas = carregar_dados(
    VENDAS_FILE,
    COLUNAS_VENDAS
)

preparar_dados()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("""
<div class="sidebar-logo">

    <div class="sidebar-logo-title">
        ⚡ SOTAM TECH
    </div>

    <div class="sidebar-logo-sub">
        Gestão inteligente
    </div>

</div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "MENU",
    [
        "📊 Dashboard",
        "📦 Inventário",
        "💰 Vendas",
        "🎯 Metas"
    ]
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "SOTAM TECH • Gestão"
)


# =========================================================
# DASHBOARD
# =========================================================

if menu == "📊 Dashboard":

    # -----------------------------------------------------
    # CÁLCULOS
    # -----------------------------------------------------

    if not df_estoque.empty:

        disponiveis = df_estoque[
            df_estoque["Status"] == "Disponível para Venda"
        ]

        manutencao = df_estoque[
            df_estoque["Status"] == "Em Manutenção"
        ]

    else:

        disponiveis = pd.DataFrame()
        manutencao = pd.DataFrame()

    produtos_disponiveis = len(disponiveis)
    produtos_manutencao = len(manutencao)

    total_vendas = len(df_vendas)

    faturamento = (
        df_vendas["Valor_Venda"].sum()
        if not df_vendas.empty
        else 0
    )

    lucro_total = (
        df_vendas["Lucro"].sum()
        if not df_vendas.empty
        else 0
    )

    ticket_medio = (
        faturamento / total_vendas
        if total_vendas > 0
        else 0
    )

    margem = (
        (lucro_total / faturamento) * 100
        if faturamento > 0
        else 0
    )

    # -----------------------------------------------------
    # CABEÇALHO
    # -----------------------------------------------------

    st.markdown(
        '<div class="welcome-title">Bom dia 👋</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="welcome-subtitle">'
        'Acompanhe o desempenho da SOTAM TECH e seus principais indicadores.'
        '</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # CARDS
    # -----------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(f"""
        <div class="metric-card">

            <div class="metric-title">
                📦 Produtos em estoque
            </div>

            <div class="metric-value">
                {produtos_disponiveis}
            </div>

            <div class="metric-description">
                aparelhos disponíveis
            </div>

        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown(f"""
        <div class="metric-card">

            <div class="metric-title">
                🧾 Total de vendas
            </div>

            <div class="metric-value">
                {total_vendas}
            </div>

            <div class="metric-description">
                vendas realizadas
            </div>

        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown(f"""
        <div class="metric-card-orange">

            <div class="metric-title-white">
                💰 Faturamento
            </div>

            <div class="metric-value-white">
                {moeda(faturamento)}
            </div>

            <div class="metric-description-white">
                receita acumulada
            </div>

        </div>
        """, unsafe_allow_html=True)

    with c4:

        st.markdown(f"""
        <div class="metric-card">

            <div class="metric-title">
                📈 Lucro acumulado
            </div>

            <div class="metric-value">
                {moeda(lucro_total)}
            </div>

            <div class="metric-description">
                margem de {margem:.1f}%
            </div>

        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # -----------------------------------------------------
    # SEGUNDA LINHA
    # -----------------------------------------------------

    esquerda, direita = st.columns([2, 1])

    with esquerda:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.subheader("📊 Faturamento")

        if not df_vendas.empty:

            vendas_grafico = df_vendas.copy()

            vendas_grafico["Data"] = pd.to_datetime(
                vendas_grafico["Data"],
                errors="coerce"
            )

            vendas_grafico = vendas_grafico.dropna(
                subset=["Data"]
            )

            if not vendas_grafico.empty:

                vendas_grafico["Mês"] = (
                    vendas_grafico["Data"]
                    .dt.strftime("%b")
                )

                mensal = (
                    vendas_grafico
                    .groupby(
                        "Mês",
                        sort=False
                    )["Valor_Venda"]
                    .sum()
                )

                st.bar_chart(
                    mensal,
                    height=280
                )

            else:

                st.info(
                    "Ainda não existem dados suficientes para o gráfico."
                )

        else:

            st.info(
                "As vendas aparecerão aqui conforme forem registradas."
            )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    with direita:

        st.markdown(f"""
        <div class="summary-box">

            <h3>Resumo financeiro</h3>

            <div class="summary-row">
                <span class="summary-label">
                    Faturamento
                </span>

                <span class="summary-value">
                    {moeda(faturamento)}
                </span>
            </div>

            <div class="summary-row">
                <span class="summary-label">
                    Lucro
                </span>

                <span class="summary-value">
                    {moeda(lucro_total)}
                </span>
            </div>

            <div class="summary-row">
                <span class="summary-label">
                    Ticket médio
                </span>

                <span class="summary-value">
                    {moeda(ticket_medio)}
                </span>
            </div>

            <div class="summary-row">
                <span class="summary-label">
                    Margem
                </span>

                <span class="summary-value">
                    {margem:.1f}%
                </span>
            </div>

            <div class="summary-row">
                <span class="summary-label">
                    Em manutenção
                </span>

                <span class="summary-value">
                    {produtos_manutencao}
                </span>
            </div>

        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # -----------------------------------------------------
    # ATIVIDADES RECENTES
    # -----------------------------------------------------

    st.subheader("Atividades recentes")

    if df_vendas.empty:

        st.markdown("""
        <div class="activity">

            <div class="activity-name">
                📱 Nenhuma venda registrada
            </div>

            <div class="activity-date">
                As vendas aparecerão aqui.
            </div>

        </div>
        """, unsafe_allow_html=True)

    else:

        recentes = df_vendas.tail(5).iloc[::-1]

        for _, venda in recentes.iterrows():

            st.markdown(f"""
            <div class="activity">

                <div class="activity-name">
                    📱 {venda["Produto"]}
                </div>

                <div class="activity-date">
                    Venda #{int(venda["ID_Venda"])}
                    &nbsp; • &nbsp;
                    {moeda(float(venda["Valor_Venda"]))}
                    &nbsp; • &nbsp;
                    {venda["Data"]}
                </div>

            </div>
            """, unsafe_allow_html=True)


# =========================================================
# INVENTÁRIO
# =========================================================

elif menu == "📦 Inventário":

    st.markdown(
        '<div class="welcome-title">Estoque</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="welcome-subtitle">'
        'Gerencie os aparelhos da SOTAM TECH.'
        '</div>',
        unsafe_allow_html=True
    )

    with st.form("form_est"):

        col1, col2 = st.columns(2)

        with col1:

            prod = st.text_input(
                "Nome do aparelho / modelo",
                placeholder="Ex: iPhone 11 64GB"
            )

            cat = st.selectbox(
                "Categoria",
                [
                    "Smartphone",
                    "Tablet",
                    "Notebook",
                    "Outros"
                ]
            )

            custo = st.number_input(
                "Custo total",
                min_value=0.0,
                step=10.0
            )

        with col2:

            preco = st.number_input(
                "Preço de venda",
                min_value=0.0,
                step=10.0
            )

            status = st.selectbox(
                "Status",
                [
                    "Disponível para Venda",
                    "Em Manutenção",
                    "Vendido"
                ]
            )

        cadastrar = st.form_submit_button(
            "➕ Cadastrar aparelho"
        )

        if cadastrar:

            if not prod.strip():

                st.error(
                    "Digite o nome do aparelho."
                )

            elif preco <= 0:

                st.error(
                    "Informe um preço de venda maior que zero."
                )

            else:

                novo_id = proximo_id(
                    df_estoque,
                    "ID"
                )

                novo = pd.DataFrame(
                    [[
                        novo_id,
                        prod.strip(),
                        cat,
                        custo,
                        preco,
                        status
                    ]],
                    columns=COLUNAS_ESTOQUE
                )

                df_estoque = pd.concat(
                    [
                        df_estoque,
                        novo
                    ],
                    ignore_index=True
                )

                salvar_dados(
                    df_estoque,
                    ESTOQUE_FILE
                )

                st.success(
                    f"{prod} cadastrado com sucesso!"
                )

                st.rerun()

    st.divider()

    st.subheader("📋 Estoque atual")

    if df_estoque.empty:

        st.info(
            "Nenhum aparelho cadastrado."
        )

    else:

        tabela = df_estoque.copy()

        tabela["Custo"] = tabela[
            "Custo"
        ].map(moeda)

        tabela["Preco_Sugerido"] = tabela[
            "Preco_Sugerido"
        ].map(moeda)

        st.dataframe(
            tabela,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# VENDAS
# =========================================================

elif menu == "💰 Vendas":

    st.markdown(
        '<div class="welcome-title">Vendas</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="welcome-subtitle">'
        'Registre vendas e acompanhe seus resultados.'
        '</div>',
        unsafe_allow_html=True
    )

    disponiveis = df_estoque[
        df_estoque["Status"] == "Disponível para Venda"
    ].copy()

    if disponiveis.empty:

        st.info(
            "Nenhum aparelho disponível para venda."
        )

    else:

        opcoes = {}

        for _, linha in disponiveis.iterrows():

            texto = (
                f"#{int(linha['ID']):03d} - "
                f"{linha['Produto']} - "
                f"{moeda(float(linha['Preco_Sugerido']))}"
            )

            opcoes[texto] = int(
                linha["ID"]
            )

        with st.form("form_venda"):

            selecionado = st.selectbox(
                "Selecionar aparelho",
                list(opcoes.keys())
            )

            id_aparelho = opcoes[
                selecionado
            ]

            aparelho = df_estoque[
                df_estoque["ID"] == id_aparelho
            ].iloc[0]

            c_prod = float(
                aparelho["Custo"]
            )

            p_base = float(
                aparelho["Preco_Sugerido"]
            )

            st.markdown(
                f"""
                <div class="card">

                    <b>{aparelho["Produto"]}</b>

                    <br><br>

                    Preço sugerido:
                    <strong>{moeda(p_base)}</strong>

                </div>
                """,
                unsafe_allow_html=True
            )

            pag = st.radio(
                "Pagamento",
                [
                    "À Vista",
                    "Parcelado"
                ],
                horizontal=True
            )

            val_fin = p_base
            parc = "1x"

            if pag == "Parcelado":

                n_p = st.slider(
                    "Parcelas",
                    2,
                    12,
                    3
                )

                juros = st.number_input(
                    "Juros ao mês (%)",
                    min_value=0.0,
                    value=2.0,
                    step=0.5
                )

                val_fin = p_base * (
                    (1 + juros / 100) ** n_p
                )

                valor_parcela = (
                    val_fin / n_p
                )

                parc = f"{n_p}x"

                st.info(
                    f"{n_p}x de {moeda(valor_parcela)} "
                    f"• Total: {moeda(val_fin)}"
                )

            lucro = val_fin - c_prod

            st.write(
                f"Lucro estimado: **{moeda(lucro)}**"
            )

            finalizar = st.form_submit_button(
                "✅ Finalizar venda"
            )

            if finalizar:

                novo_id_venda = proximo_id(
                    df_vendas,
                    "ID_Venda"
                )

                nova_venda = pd.DataFrame(
                    [[
                        novo_id_venda,
                        aparelho["Produto"],
                        val_fin,
                        lucro,
                        parc,
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M"
                        )
                    ]],
                    columns=COLUNAS_VENDAS
                )

                df_vendas = pd.concat(
                    [
                        df_vendas,
                        nova_venda
                    ],
                    ignore_index=True
                )

                salvar_dados(
                    df_vendas,
                    VENDAS_FILE
                )

                df_estoque.loc[
                    df_estoque["ID"] == id_aparelho,
                    "Status"
                ] = "Vendido"

                salvar_dados(
                    df_estoque,
                    ESTOQUE_FILE
                )

                st.success(
                    "🎉 Venda efetuada com sucesso!"
                )

                st.rerun()

    st.divider()

    st.subheader("📋 Histórico de vendas")

    if df_vendas.empty:

        st.info(
            "Nenhuma venda registrada."
        )

    else:

        tabela_vendas = df_vendas.copy()

        tabela_vendas["Valor_Venda"] = tabela_vendas[
            "Valor_Venda"
        ].map(moeda)

        tabela_vendas["Lucro"] = tabela_vendas[
            "Lucro"
        ].map(moeda)

        st.dataframe(
            tabela_vendas,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# METAS
# =========================================================

elif menu == "🎯 Metas":

    st.markdown(
        '<div class="welcome-title">Metas</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="welcome-subtitle">'
        'Acompanhe o progresso financeiro da SOTAM TECH.'
        '</div>',
        unsafe_allow_html=True
    )

    meta = st.number_input(
        "Meta de faturamento",
        min_value=0.0,
        value=5000.0,
        step=500.0
    )

    faturamento = (
        df_vendas["Valor_Venda"].sum()
        if not df_vendas.empty
        else 0
    )

    progresso = (
        min(faturamento / meta, 1.0)
        if meta > 0
        else 0
    )

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-title">
                🎯 Meta mensal
            </div>

            <div class="metric-value">
                {moeda(meta)}
            </div>

            <div class="metric-description">
                Faturado: {moeda(faturamento)}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(progresso)

    percentual = progresso * 100

    st.write(
        f"**{percentual:.1f}% da meta alcançada**"
    )

    faltante = max(
        meta - faturamento,
        0
    )

    if faltante > 0:

        st.warning(
            f"Faltam {moeda(faltante)} para atingir sua meta."
        )

    else:

        st.success(
            "🎉 Parabéns! A meta foi atingida."
        )
