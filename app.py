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
    layout="wide"
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
# FUNÇÕES
# =========================================================

def carregar_dados(arq, colunas):
    """Carrega um CSV ou cria um DataFrame vazio."""

    if os.path.exists(arq):
        try:
            df = pd.read_csv(arq)

            # Garante que todas as colunas necessárias existam
            for coluna in colunas:
                if coluna not in df.columns:
                    df[coluna] = None

            # Mantém somente as colunas utilizadas pelo sistema
            df = df[colunas]

            return df

        except Exception:
            st.warning(
                f"Não foi possível ler {arq}. "
                "Um novo arquivo será utilizado."
            )

    return pd.DataFrame(columns=colunas)


def salvar_dados(df, arq):
    """Salva o DataFrame no CSV."""

    df.to_csv(
        arq,
        index=False,
        encoding="utf-8-sig"
    )


def preparar_dados():
    """Converte os campos numéricos para números."""

    global df_estoque, df_vendas

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
    """Gera o próximo ID sem duplicar."""

    if df.empty:
        return 1

    valores = pd.to_numeric(
        df[coluna],
        errors="coerce"
    ).dropna()

    if valores.empty:
        return 1

    return int(valores.max()) + 1


# =========================================================
# CARREGAMENTO
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
# MENU LATERAL
# =========================================================

st.sidebar.title("⚡ SOTAM TECH")
st.sidebar.caption("Gestão de aparelhos e vendas")

menu = st.sidebar.radio(
    "Navegação",
    [
        "📊 Dashboard",
        "📦 Inventário",
        "💰 Vendas",
        "🎯 Metas"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

if menu == "📊 Dashboard":

    st.title("📊 Dashboard Executivo")
    st.caption("Visão geral da SOTAM TECH")

    # Quantidade de aparelhos disponíveis
    produtos_disponiveis = 0

    if not df_estoque.empty:
        produtos_disponiveis = len(
            df_estoque[
                df_estoque["Status"] == "Disponível para Venda"
            ]
        )

    # Faturamento
    faturamento = (
        df_vendas["Valor_Venda"].sum()
        if not df_vendas.empty
        else 0.0
    )

    # Lucro
    lucro_total = (
        df_vendas["Lucro"].sum()
        if not df_vendas.empty
        else 0.0
    )

    # Custo do estoque disponível
    custo_estoque = (
        df_estoque[
            df_estoque["Status"] == "Disponível para Venda"
        ]["Custo"].sum()
        if not df_estoque.empty
        else 0.0
    )

    # Ticket médio
    ticket_medio = (
        faturamento / len(df_vendas)
        if not df_vendas.empty
        else 0.0
    )

    # Margem
    margem = (
        (lucro_total / faturamento) * 100
        if faturamento > 0
        else 0.0
    )

    # CARDS
    c1, c2, c3 = st.columns(3)

    c1.metric(
        "📦 Produtos em Estoque",
        produtos_disponiveis
    )

    c2.metric(
        "💰 Total de Vendas",
        len(df_vendas)
    )

    c3.metric(
        "💵 Faturamento",
        f"R$ {faturamento:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "📈 Lucro Acumulado",
        f"R$ {lucro_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

    c5.metric(
        "🧾 Ticket Médio",
        f"R$ {ticket_medio:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

    c6.metric(
        "📊 Margem",
        f"{margem:.1f}%"
    )

    st.divider()

    # ESTOQUE
    st.subheader("📦 Resumo do Estoque")

    if df_estoque.empty:
        st.info("Nenhum aparelho cadastrado.")
    else:
        disponiveis = len(
            df_estoque[
                df_estoque["Status"] == "Disponível para Venda"
            ]
        )

        manutencao = len(
            df_estoque[
                df_estoque["Status"] == "Em Manutenção"
            ]
        )

        vendidos = len(
            df_estoque[
                df_estoque["Status"] == "Vendido"
            ]
        )

        a, b, c = st.columns(3)

        a.metric("Disponíveis", disponiveis)
        b.metric("Em manutenção", manutencao)
        c.metric("Vendidos", vendidos)

        st.write(
            f"Valor investido em estoque disponível: "
            f"**R$ {custo_estoque:,.2f}**".replace(",", "X").replace(".", ",").replace("X", ".")
        )


# =========================================================
# INVENTÁRIO
# =========================================================

elif menu == "📦 Inventário":

    st.title("📦 Gestão de Inventário")

    st.write("Cadastre os aparelhos que entram no estoque.")

    with st.form("form_est"):

        prod = st.text_input(
            "Nome do Aparelho / Modelo",
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
            "Custo Total R$",
            min_value=0.0,
            step=10.0
        )

        preco = st.number_input(
            "Preço de Venda R$",
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
            "➕ Cadastrar Aparelho"
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
                    f"'{prod}' cadastrado com sucesso!"
                )

                st.rerun()

    st.divider()

    st.subheader("📋 Estoque Atual")

    if df_estoque.empty:

        st.info(
            "Nenhum aparelho cadastrado no estoque."
        )

    else:

        # Cria uma cópia para exibição
        tabela = df_estoque.copy()

        tabela["Custo"] = tabela["Custo"].map(
            lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )

        tabela["Preco_Sugerido"] = tabela[
            "Preco_Sugerido"
        ].map(
            lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )

        st.dataframe(
            tabela,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# VENDAS
# =========================================================

elif menu == "💰 Vendas":

    st.title("💰 Registro de Vendas")

    # Somente aparelhos realmente disponíveis
    disponiveis = df_estoque[
        df_estoque["Status"] == "Disponível para Venda"
    ].copy()

    if disponiveis.empty:

        st.info(
            "Nenhum produto disponível em estoque para venda."
        )

    else:

        # Cria opções usando o ID
        opcoes = {}

        for _, linha in disponiveis.iterrows():

            texto = (
                f"#{int(linha['ID']):03d} - "
                f"{linha['Produto']} - "
                f"R$ {linha['Preco_Sugerido']:,.2f}"
            )

            opcoes[texto] = int(linha["ID"])

        with st.form("form_venda"):

            selecionado = st.selectbox(
                "Selecionar Aparelho",
                list(opcoes.keys())
            )

            id_aparelho = opcoes[selecionado]

            aparelho = df_estoque[
                df_estoque["ID"] == id_aparelho
            ].iloc[0]

            c_prod = float(
                aparelho["Custo"]
            )

            p_base = float(
                aparelho["Preco_Sugerido"]
            )

            st.write(
                f"**Preço sugerido:** "
                f"R$ {p_base:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            )

            pag = st.radio(
                "Forma de Pagamento",
                [
                    "À Vista",
                    "Parcelado"
                ]
            )

            val_fin = p_base
            parc = "1x"

            if pag == "Parcelado":

                n_p = st.slider(
                    "Quantidade de Parcelas",
                    min_value=2,
                    max_value=12,
                    value=3
                )

                juros = st.number_input(
                    "Juros ao mês (%)",
                    min_value=0.0,
                    value=2.0,
                    step=0.5
                )

                # Juros compostos
                val_fin = p_base * (
                    (1 + juros / 100) ** n_p
                )

                valor_parcela = val_fin / n_p

                parc = f"{n_p}x"

                st.info(
                    f"Total: R$ {val_fin:,.2f} | "
                    f"{n_p}x de R$ {valor_parcela:,.2f}"
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )

            lucro = val_fin - c_prod

            st.write(
                f"**Lucro estimado:** "
                f"R$ {lucro:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

            finalizar = st.form_submit_button(
                "✅ Finalizar Venda"
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

                # Marca SOMENTE o aparelho vendido
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

    st.subheader("📋 Histórico de Vendas")

    if df_vendas.empty:

        st.info(
            "Nenhuma venda registrada ainda."
        )

    else:

        tabela_vendas = df_vendas.copy()

        tabela_vendas["Valor_Venda"] = tabela_vendas[
            "Valor_Venda"
        ].map(
            lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )

        tabela_vendas["Lucro"] = tabela_vendas[
            "Lucro"
        ].map(
            lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )

        st.dataframe(
            tabela_vendas,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# METAS
# =========================================================

elif menu == "🎯 Metas":

    st.title("🎯 Metas Financeiras")

    meta = st.number_input(
        "Meta de Faturamento Mensal R$",
        min_value=0.0,
        value=5000.0,
        step=500.0
    )

    faturamento = (
        df_vendas["Valor_Venda"].sum()
        if not df_vendas.empty
        else 0.0
    )

    if meta > 0:

        progresso = min(
            faturamento / meta,
            1.0
        )

    else:

        progresso = 0.0

    st.progress(
        progresso
    )

    st.write(
        f"**Faturado:** "
        f"R$ {faturamento:,.2f} "
        f"de "
        f"R$ {meta:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

    faltante = max(
        meta - faturamento,
        0
    )

    if faltante > 0:

        st.warning(
            f"Faltam R$ {faltante:,.2f} "
            f"para atingir a meta."
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    else:

        st.success(
            "🎉 Meta atingida!"
        )
