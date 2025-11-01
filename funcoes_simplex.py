import numpy as np
import pandas as pd
import streamlit as st


def _build_tableau(c, A_ub, b_ub):
    """
    Cria o tableau padrão (igual para primal e dual).
    
    param c: Coeficientes da função objetivo
    param A_ub: Coeficientes das restrições (≤)
    param b_ub: Termos independentes das restrições
    return: tableau, nomes das colunas, variáveis básicas iniciais
    """

    c, A_ub, b_ub = map(np.array, (c, A_ub, b_ub))
    num_constraints, num_vars = A_ub.shape
    tableau = np.zeros((num_constraints + 1, num_vars + num_constraints + 2))
    tableau[0, :num_vars] = -c
    tableau[0, -2] = 1
    tableau[1:, :num_vars] = A_ub
    tableau[1:, num_vars:num_vars + num_constraints] = np.eye(num_constraints)
    tableau[1:, -1] = b_ub
    columns = [f'x{i+1}' for i in range(num_vars)] + [f'f{i+1}' for i in range(num_constraints)] + ['Z', 'RHS']
    base_vars = [f'f{i+1}' for i in range(num_constraints)]
    return tableau, columns, base_vars


def show_tableau_streamlit(tableau, columns, base_vars, title="Quadro", iteration=None, ratios=None):
    """
    Exibe o tableau no Streamlit.
    
    param tableau: Matriz do tableau
    param columns: Nomes das colunas
    param base_vars: Variáveis básicas atuais
    param title: Título do quadro
    param iteration: Número da iteração (opcional)
    param ratios: Razões calculadas (opcional)
    """

    st.markdown(f"#### {title} {'(' + str(iteration) + ')' if iteration else ''}")
    df = pd.DataFrame(tableau, columns=columns)
    df.insert(0, 'Base', ['Z'] + base_vars)
    if ratios is not None:
        df['Razão'] = ['-'] + [f'{r:.2f}' if np.isfinite(r) else '-' for r in ratios]
    st.dataframe(df, use_container_width=True)


def solve_simplex_step_by_step(c, A_ub, b_ub, mode='max'):
    """
    Simplex Primal (passo a passo). Exibe cada quadro no Streamlit.

    param c: Coeficientes da função objetivo
    param A_ub: Coeficientes das restrições (≤)
    param b_ub: Termos independentes das restrições
    param mode: 'max' para maximização, 'min' para minimização
    """

    tableau, columns, base_vars = _build_tableau(c, A_ub, b_ub)
    num_constraints = len(base_vars)
    iteration = 1

    while True:
        linha_z = tableau[0, :-2]
        if mode == 'max':
            if np.all(linha_z >= 0):
                break
            pivot_col = np.argmin(linha_z)
        elif mode == 'min':
            if np.all(linha_z <= 0):
                break
            pivot_col = np.argmax(linha_z)
        else:
            st.error("Erro: modo deve ser 'max' ou 'min'.")
            return

        col = tableau[1:, pivot_col]
        rhs = tableau[1:, -1]
        ratios = np.where(col > 0, rhs / col, np.inf)

        if np.all(ratios == np.inf):
            st.error("⚠️ Solução ilimitada (nenhuma razão válida).")
            return

        pivot_row = np.argmin(ratios) + 1
        entering_var, leaving_var = columns[pivot_col], base_vars[pivot_row - 1]

        show_tableau_streamlit(tableau, columns, base_vars, title="📋 Quadro", iteration=iteration, ratios=ratios)

        st.markdown(
            f"### 🔁 Iteração {iteration}\n"
            f"**Decisão:** Entra na base :blue[`{entering_var}`] → Sai da base :red[`{leaving_var}`]"
        )

        base_vars[pivot_row - 1] = entering_var

        # pivoteamento
        pivot_element = tableau[pivot_row, pivot_col]
        tableau[pivot_row] /= pivot_element
        for i in range(tableau.shape[0]):
            if i != pivot_row:
                tableau[i] -= tableau[i, pivot_col] * tableau[pivot_row]

        iteration += 1

    st.success("✅ Solução ótima (Primal) encontrada!")
    show_tableau_streamlit(tableau, columns, base_vars, title="📊 Quadro Final (Solução Ótima)")

    final_z_value = tableau[0, -1]
    st.markdown("### 🏁 Solução Final (Primal)")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Z ótimo", value=f"{final_z_value:.2f}")
    with col2:
        st.metric(label="Modo", value="Maximização" if mode == 'max' else "Minimização")

    st.markdown("### 📈 Variáveis básicas:")


    total_vars = len(c)
    num_cols = min(max(2, total_vars // 3 + 1), 5)  # entre 2 e 5 colunas
    cols = st.columns(num_cols)

    for i in range(total_vars):
        var_name = f'x{i+1}'
        valor = "0.00"
        if var_name in base_vars:
            valor = f"{tableau[base_vars.index(var_name) + 1, -1]:.2f}"

        with cols[i % num_cols]:
            st.metric(label=var_name, value=valor)
                

def solve_dual_simplex_step_by_step(c, A_ub, b_ub, mode='max'):
    """
    Dual Simplex (passo a passo). Exibe cada quadro no Streamlit.
    Útil quando Z está "ótima" mas RHS possui negativos (infactível).

    param c: Coeficientes da função objetivo
    param A_ub: Coeficientes das restrições (≤)
    param b_ub: Termos independentes das restrições
    param mode: 'max' para maximização, 'min' para minimização
    """
    tableau, columns, base_vars = _build_tableau(c, A_ub, b_ub)
    num_constraints = len(base_vars)
    iteration = 1

    # loop enquanto houver RHS negativo (infactibilidade)
    while np.any(tableau[1:, -1] < 0):
        # encontra linha pivô: RHS mais negativo
        pivot_row = np.argmin(tableau[1:, -1]) + 1
        pivot_row_values = tableau[pivot_row, :-2]
        z_row_values = tableau[0, :-2]

        # calcula razões dual: só para elementos negativos na linha pivô
        ratios_dual = np.full(len(pivot_row_values), np.inf)
        for i in range(len(pivot_row_values)):
            if pivot_row_values[i] < 0:
                # razão = |Z_i / pivot_row_i|
                ratios_dual[i] = np.abs(z_row_values[i] / pivot_row_values[i])

        if np.all(ratios_dual == np.inf):
            st.error("❌ Problema infactível: nenhum candidato de entrada (nenhum valor negativo na linha pivô).")
            return

        pivot_col = np.argmin(ratios_dual)
        entering_var = columns[pivot_col]
        leaving_var = base_vars[pivot_row - 1]

        show_tableau_streamlit(tableau, columns, base_vars, title="📋 Quadro DUAL", iteration=iteration)
        st.markdown(
            f"### 🔁 Iteração DUAL {iteration}\n"
            f"**Decisão DUAL:** Sai da base :red[`{leaving_var}`] (RHS mais negativo) → Entra na base :blue[`{entering_var}`]"
        )

        base_vars[pivot_row - 1] = entering_var

        # pivoteamento (mesma rotina)
        pivot_element = tableau[pivot_row, pivot_col]
        tableau[pivot_row] /= pivot_element
        for i in range(tableau.shape[0]):
            if i != pivot_row:
                tableau[i] -= tableau[i, pivot_col] * tableau[pivot_row]

        iteration += 1

    st.success("✅ Solução ótima e factível (Dual) encontrada!")
    show_tableau_streamlit(tableau, columns, base_vars, title="📊 Quadro Final (Solução Ótima e Factível)")

    final_z_value = tableau[0, -1]
    st.markdown("### 🏁 Solução Final (Dual)")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Z ótimo", value=f"{final_z_value:.2f}")
    with col2:
        st.metric(label="Modo", value="Maximização" if mode == 'max' else "Minimização")


    st.markdown("### 📈 Variáveis básicas:")

# calcula número de colunas de forma flexível
    total_vars = len(c)
    num_cols = min(max(2, total_vars // 3 + 1), 5)  # entre 2 e 5 colunas
    cols = st.columns(num_cols)

    for i in range(total_vars):
        var_name = f'x{i+1}'
        valor = "0.00"
        if var_name in base_vars:
            valor = f"{tableau[base_vars.index(var_name) + 1, -1]:.2f}"

        with cols[i % num_cols]:
            st.metric(label=var_name, value=valor)

