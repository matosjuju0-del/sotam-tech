import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="SOTAM TECH", page_icon="📱", layout="wide")

ESTOQUE_FILE = "estoque_sotam.csv"
VENDAS_FILE = "vendas_sotam.csv"

def carregar_dados(arq, cols):
        if os.path.exists(arq):
              return pd.read_csv(arq)
        return pd.DataFrame(columns=cols)

def salvar_dados(df, arq):
  df.to_csv(arq, index=False)

df_estoque = carregar_dados(ESTOQUE_FILE, ["ID", "Produto", "Categoria", "Custo", "Preco_Sugerido", "Status"])
df_vendas = carregar_dados(VENDAS_FILE, ["ID_Venda", "Produto", "Valor_Venda", "Lucro", "Parcelas", "Data"])

st.sidebar.title("⚡ SOTAM TECH")
menu = st.sidebar.radio("Navegação", ["📊 Dashboard", "📦 Inventário", "💰 Vendas", "🎯 Metas"])

if menu == "📊 Dashboard":
st.title("📊 Dashboard Executivo - SOTAM TECH")
c1, c2, c3 = st.columns(3)
c1.metric("Produtos em Estoque", len(df_estoque))
c2.metric("Total de Vendas", len(df_vendas))
c3.metric("Lucro Acumulado", f"R$ {df_vendas['Lucro'].sum() if not df_vendas.empty else 0.0:.2f}")

elif menu == "📦 Inventário":
st.title("📦 Gestão de Inventário")
with st.form("form_est"):
prod = st.text_input("Nome do Aparelho / Modelo")
cat = st.selectbox("Categoria", ["Smartphone", "Tablet", "Notebook", "Outros"])
custo = st.number_input("Custo Total R$", min_value=0.0)
preco = st.number_input("Preço de Venda R$", min_value=0.0)
status = st.selectbox("Status", ["Disponível para Venda", "Em Manutenção", "Vendido"])
if st.form_submit_button("Cadastrar") and prod:
novo = pd.DataFrame([[len(df_estoque)+1, prod, cat, custo, preco, status]], columns=df_estoque.columns)
df_estoque = pd.concat([df_estoque, novo], ignore_index=True)
salvar_dados(df_estoque, ESTOQUE_FILE)
st.success(f"'{prod}' cadastrado com sucesso!")
st.rerun()
st.dataframe(df_estoque, use_container_width=True)

elif menu == "💰 Vendas":
st.title("💰 Registo de Vendas")
disp = df_estoque[df_estoque["Status"] != "Vendido"]["Produto"].tolist() if not df_estoque.empty else []
if not disp:
st.info("Nenhum produto disponível em estoque para venda.")
else:
with st.form("form_venda"):
escolhido = st.selectbox("Selecionar Aparelho", disp)
c_prod = float(df_estoque.loc[df_estoque["Produto"] == escolhido, "Custo"].values[0])
p_base = float(df_estoque.loc[df_estoque["Produto"] == escolhido, "Preco_Sugerido"].values[0])
pag = st.radio("Pagamento", ["À Vista", "Parcelado"])
val_fin = p_base
parc = "1x"
if pag == "Parcelado":
n_p = st.slider("Parcelas", 2, 12, 3)
juros = st.number_input("Juros % a.m.", value=2.0)
val_fin = p_base * ((1 + (juros/100)) ** n_p)
parc = f"{n_p}x"
lucro = val_fin - c_prod
if st.form_submit_button("Finalizar Venda"):
nova_v = pd.DataFrame([[len(df_vendas)+1, escolhido, val_fin, lucro, parc, datetime.now().strftime("%Y-%m-%d %H:%M")]], columns=df_vendas.columns)
df_vendas = pd.concat([df_vendas, nova_v], ignore_index=True)
salvar_dados(df_vendas, VENDAS_FILE)
df_estoque.loc[df_estoque["Produto"] == escolhido, "Status"] = "Vendido"
salvar_dados(df_estoque, ESTOQUE_FILE)
st.success("Venda efetuada com sucesso!")
st.rerun()
st.dataframe(df_vendas, use_container_width=True)

elif menu == "🎯 Metas":
st.title("🎯 Metas Financeiras")
meta = st.number_input("Meta Mensal R$", value=5000.0)
fat = df_vendas["Valor_Venda"].sum() if not df_vendas.empty else 0.0
prog = min(fat / meta, 1.0) if meta > 0 else 0.0
st.progress(prog)
st.write(f"Faturado: R$ {fat:.2f} de R$ {meta:.2f} ({prog*100:.1f}%)")
