from funcoes_simplex import *

# ==============================
# CONFIGURAÇÕES DA PÁGINA
# ==============================
st.set_page_config(page_title="Simplex Interativo (Primal / Dual / Big M)", page_icon="🧮", layout="wide")
st.title("🧮 Simplex Interativo — Primal, Dual & Big M")
st.markdown(
    "Resolva problemas de Programação Linear de qualquer tipo. "
    "O modo **Automático** identifica a melhor estratégia (incluindo Big M para igualdades)."
)

st.markdown("---")

# ==============================
# UI: Entradas (Sidebar)
# ==============================
st.sidebar.header("⚙️ Configurações do Problema")

# Seletor de Método com a nova opção Automático
metodo = st.sidebar.selectbox(
    "Método:", 
    ("Automático", "Primal Simplex", "Dual Simplex")
)

modo = st.sidebar.radio("Modo de otimização:", ("max", "min"))
num_vars = st.sidebar.number_input("Número de variáveis (x)", min_value=1, max_value=20, value=2)
num_rest = st.sidebar.number_input("Número de restrições", min_value=1, max_value=20, value=2)
st.sidebar.markdown("---")


st.markdown("## ⚙️ Entradas do Problema")

# ==============================
# Função Objetivo
# ==============================
st.markdown("### Função Objetivo (Z):")
coef_c = []
cols = st.columns(num_vars)
for i in range(num_vars):
    coef_c.append(cols[i].number_input(f"Coef. de x{i+1}", value=1.0, key=f"c{i}"))

# ==============================
# Restrições (Lógica Condicional)
# ==============================
st.markdown("### Restrições:")
A, b = [], []
tipos_rest = [] # Lista para guardar os tipos (≤, ≥, =)

if metodo == "Automático":
    st.info("💡 No Modo Automático, você pode misturar restrições de diferentes tipos.")
    
    for j in range(num_rest):
        # Cria colunas: Uma para cada variável + 1 para o Símbolo + 1 para o Valor b
        # A proporção das colunas pode ser ajustada, mas o padrão do Streamlit funciona bem
        cols = st.columns(num_vars + 2) 
        linha = []
        
        # 1. Inputs dos Coeficientes das Variáveis (A)
        for i in range(num_vars):
            val = cols[i].number_input(f"x{i+1} (R{j+1})", value=1.0, key=f"a{j}{i}", label_visibility="visible")
            linha.append(val)
        A.append(linha)
        
        # 2. Selectbox para o Tipo de Desigualdade/Igualdade
        # key=f"tipo{j}" garante que cada linha tenha seu próprio seletor
        tipo = cols[num_vars].selectbox(
            "Tipo", 
            options=["≤", "≥", "="], 
            key=f"tipo{j}", 
            label_visibility="visible"
        )
        tipos_rest.append(tipo)
        
        # 3. Input do Lado Direito (b)
        val_b = cols[-1].number_input(f"RHS (b{j+1})", value=10.0, key=f"b{j}", label_visibility="visible")
        b.append(val_b)

else:
    # Modos Manuais (Primal ou Dual) - Interface Simplificada (Tudo ≤)
    st.warning(f"⚠️ Modo Manual ({metodo}): O sistema assume que todas as restrições são do tipo '≤'.")
    
    for j in range(num_rest):
        cols = st.columns(num_vars + 1)
        linha = []
        for i in range(num_vars):
            linha.append(cols[i].number_input(f"A{j+1}{i+1}", value=1.0, key=f"a{j}{i}"))
        A.append(linha)
        
        # Define padrão como '≤' para manter compatibilidade
        tipos_rest.append("≤")
        
        b.append(cols[-1].number_input(f"b{j+1}", value=10.0, key=f"b{j}"))

# ==============================
# Botão de Ação
# ==============================
st.markdown("---")
if st.button("🚀 Resolver", use_container_width=True):
    with st.spinner("Processando..."):
        try:
            # Validação básica de dimensões
            A_np = np.array(A)
            if A_np.shape != (num_rest, num_vars):
                st.error("Erro nas dimensões da matriz A.")
            else:
                # Roteamento para as funções do backend
                if metodo == "Automático":
                    solve_automatico(coef_c, A, b, tipos_rest, modo)
                elif metodo == "Primal Simplex":
                    solve_simplex_step_by_step(coef_c, A, b, modo)
                elif metodo == "Dual Simplex":
                    solve_dual_simplex_step_by_step(coef_c, A, b, modo)
                
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")

# Rodapé
st.markdown("<br><hr><center>Desenvolvido por <b>Edy</b> 🧠</center>", unsafe_allow_html=True)