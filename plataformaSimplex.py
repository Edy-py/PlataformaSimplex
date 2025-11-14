from funcoes_simplex import *

# ==============================
# CONFIGURAÇÕES DA PÁGINA
# ==============================
st.set_page_config(page_title="Simplex Interativo (Primal / Dual)", page_icon="🧮", layout="wide")
st.title("🧮 Simplex Interativo — Primal & Dual")
st.markdown(
    "Resolva problemas de Programação Linear usando **Simplex Primal** ou **Dual Simplex**. "
    "Preencha os coeficientes e escolha o método."
)

st.markdown("---")

# ==============================
# UI: Entradas
# ==============================
st.sidebar.header("⚙️ Configurações do Problema")
metodo = st.sidebar.selectbox("Método:", ("Primal Simplex", "Dual Simplex"))
modo = st.sidebar.radio("Modo de otimização:", ("max", "min"))
num_vars = st.sidebar.number_input("Número de variáveis (x)", min_value=1, max_value=20, value=3)
num_rest = st.sidebar.number_input("Número de restrições", min_value=1, max_value=20, value=3)
st.sidebar.markdown("---")


st.markdown("## ⚙️ Entradas do Problema")

# Função objetivo
st.markdown("### Função Objetivo (Z):")
coef_c = []
cols = st.columns(num_vars)
for i in range(num_vars):
    coef_c.append(cols[i].number_input(f"Coef. de x{i+1}", value=1.0, key=f"c{i}"))

# Restrições
# {'≤' if mode == 'max' else '≥'}
st.markdown(f"### Restrições ({'≤' if modo == 'max' else '≥'}):")
A, b = [], []
for j in range(num_rest):
    cols = st.columns(num_vars + 1)
    linha = []
    for i in range(num_vars):
        linha.append(cols[i].number_input(f"A{j+1}{i+1}", value=1.0, key=f"a{j}{i}"))
    A.append(linha)
    b.append(cols[-1].number_input(f"b{j+1}", value=10.0, key=f"b{j}"))

# botão
if st.button("🚀 Resolver"):
    with st.spinner("Calculando..."):
        try:
            # valida forma da matriz
            A_np = np.array(A)
            if A_np.shape != (num_rest, num_vars):
                st.error("Dimensões de A incorretas.")
            else:
                if metodo == "Primal Simplex":
                    solve_simplex_step_by_step(coef_c, A, b, modo)
                else:
                    solve_dual_simplex_step_by_step(coef_c, A, b, modo)
                
        except Exception as e:
            st.error(f"Erro durante a resolução: {e}")

# Rodapé
st.markdown("<hr><center>Desenvolvido por <b>Edy</b> 🧠 with numpy & Streamlit</center>", unsafe_allow_html=True)
