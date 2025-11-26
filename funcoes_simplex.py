import numpy as np
import pandas as pd
import streamlit as st

# Constante para o "Grande M"
M_CONST = 1.0e5 

def _build_tableau(c, A_ub, b_ub):
    """
    Constrói o tableau inicial padrão para o método Simplex (Primal ou Dual).

    Esta função prepara a matriz para problemas que já estão na forma padrão
    (restrições de desigualdade <=), adicionando apenas variáveis de folga.

    :param c: Coeficientes da função objetivo.
    :type c: list or np.ndarray
    :param A_ub: Matriz de coeficientes das restrições (lado esquerdo).
    :type A_ub: list or np.ndarray
    :param b_ub: Vetor de termos independentes das restrições (lado direito).
    :type b_ub: list or np.ndarray
    :return: Uma tupla contendo o tableau inicial (numpy array), a lista de nomes das colunas e a lista das variáveis básicas iniciais.
    :rtype: tuple(np.ndarray, list, list)
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

def _build_big_m_tableau(c, A, b, tipos, mode='max'):
    """
    Constrói o tableau inicial para o Método Big M, lidando com restrições mistas (<=, >=, =).

    Adiciona automaticamente variáveis de folga (s) e variáveis artificiais (a)
    conforme necessário para cada tipo de restrição. Também aplica a penalidade M
    na função objetivo para as variáveis artificiais.

    :param c: Coeficientes da função objetivo.
    :type c: list or np.ndarray
    :param A: Matriz de coeficientes das restrições.
    :type A: list or np.ndarray
    :param b: Termos independentes das restrições.
    :type b: list or np.ndarray
    :param tipos: Lista de strings indicando o tipo de cada restrição ('<=', '>=', '=').
    :type tipos: list[str]
    :param mode: Modo de otimização ('max' ou 'min'). O padrão é 'max'.
    :type mode: str
    :return: Tableau montado, lista completa de nomes das colunas e lista de variáveis básicas iniciais.
    :rtype: tuple(np.ndarray, list, list)
    """
    num_vars = len(c)
    num_rest = len(A)
    
    # 1. Listas separadas para garantir a ordem correta
    x_names = [f'x{i+1}' for i in range(num_vars)]
    s_names = [] 
    a_names = [] 
    
    A_matrix = np.array(A, dtype=float)
    slack_cols = [] 
    artif_cols = []
    
    base_vars = [None] * num_rest 

    # 2. Preenchimento das listas
    for i, tipo in enumerate(tipos):
        if tipo == '≤':
            col = np.zeros(num_rest)
            col[i] = 1.0
            slack_cols.append(col)
            name = f's{len(slack_cols)}'
            s_names.append(name)
            base_vars[i] = name
            
        elif tipo == '≥':
            col_s = np.zeros(num_rest)
            col_s[i] = -1.0
            slack_cols.append(col_s)
            name_s = f's{len(slack_cols)}'
            s_names.append(name_s)
            
            col_a = np.zeros(num_rest)
            col_a[i] = 1.0
            artif_cols.append(col_a)
            name_a = f'a{len(artif_cols)}'
            a_names.append(name_a)
            base_vars[i] = name_a
            
        elif tipo == '=':
            col_a = np.zeros(num_rest)
            col_a[i] = 1.0
            artif_cols.append(col_a)
            name_a = f'a{len(artif_cols)}'
            a_names.append(name_a)
            base_vars[i] = name_a

    # 3. Montagem da Matriz
    constraint_matrix = A_matrix
    if slack_cols:
        constraint_matrix = np.hstack([constraint_matrix, np.column_stack(slack_cols)])
    if artif_cols:
        constraint_matrix = np.hstack([constraint_matrix, np.column_stack(artif_cols)])
        
    # 4. Montagem da Lista de Nomes
    col_names = x_names + s_names + a_names
    
    total_cols = len(col_names) + 2 
    tableau = np.zeros((num_rest + 1, total_cols))
    
    tableau[1:, :len(col_names)] = constraint_matrix
    tableau[1:, -1] = b
    
    tableau[0, :num_vars] = -np.array(c, dtype=float)
    tableau[0, -2] = 1 
    
    full_col_names = col_names + ['Z', 'RHS']
    
    # Ajuste Big M na Função Objetivo
    indices_artificiais = [idx for idx, nome in enumerate(full_col_names) if nome.startswith('a')]
    
    for idx_col_artif in indices_artificiais:
        rows_with_1 = np.where(tableau[1:, idx_col_artif] == 1)[0]
        if len(rows_with_1) > 0:
            row_idx = rows_with_1[0] + 1
            if mode == 'max':
                tableau[0, :] -= M_CONST * tableau[row_idx, :]
            else: # min
                tableau[0, :] += M_CONST * tableau[row_idx, :]
                
    tableau[0, -2] = 1 

    return tableau, full_col_names, base_vars

def show_tableau_streamlit(tableau, columns, base_vars, title="Quadro", iteration=None, ratios=None):
    """
    Exibe o tableau atual na interface do Streamlit formatado como um DataFrame pandas.

    Formata os valores para ocultar a magnitude do 'Big M' (exibindo como '1.0M' em vez de 100000)
    e adiciona a coluna de Razão se fornecida.

    :param tableau: A matriz numérica do tableau atual.
    :type tableau: np.ndarray
    :param columns: Lista com os nomes das colunas.
    :type columns: list[str]
    :param base_vars: Lista com os nomes das variáveis que estão na base atualmente.
    :type base_vars: list[str]
    :param title: Título descritivo para a tabela.
    :type title: str
    :param iteration: Número da iteração atual (opcional).
    :type iteration: int or None
    :param ratios: Array com os valores calculados do teste da razão (opcional).
    :type ratios: np.ndarray or None
    """
    st.markdown(f"#### {title} {'(' + str(iteration) + ')' if iteration else ''}")
    df = pd.DataFrame(tableau, columns=columns)
    df.insert(0, 'Base', ['Z'] + base_vars)
    
    def format_val(x):
        if abs(x) >= M_CONST / 100: 
            return f"{x/M_CONST:.1f}M"
        return f"{x:.2f}"

    df_display = df.copy()
    for col in df.columns:
        if col != 'Base' and col != 'Razão':
             df_display[col] = df[col].apply(format_val)

    if ratios is not None:
        df_display['Razão'] = ['-'] + [f'{r:.2f}' if np.isfinite(r) else '-' for r in ratios]
        
    st.dataframe(df_display, use_container_width=True)

def solve_simplex_step_by_step(c, A_ub, b_ub, mode='max'):
    """
    Executa o algoritmo Simplex Primal passo a passo.

    Indicado para problemas na forma padrão (RHS >= 0).

    :param c: Coeficientes da função objetivo.
    :type c: list
    :param A_ub: Coeficientes das restrições (lado esquerdo).
    :type A_ub: list
    :param b_ub: Termos independentes (lado direito).
    :type b_ub: list
    :param mode: 'max' ou 'min'.
    :type mode: str
    """
    tableau, columns, base_vars = _build_tableau(c, A_ub, b_ub)
    # Passamos 'c' para saber quantas variáveis exibir no final
    _run_simplex_loop(tableau, columns, base_vars, mode, method_name="Primal Simplex", c_original=c)

def solve_dual_simplex_step_by_step(c, A_ub, b_ub, mode='max'):
    """
    Executa o algoritmo Dual Simplex passo a passo.

    Indicado quando a solução é "otimal" (Z satisfaz condição de parada) mas infactível (RHS < 0).

    :param c: Coeficientes da função objetivo.
    :type c: list
    :param A_ub: Coeficientes das restrições.
    :type A_ub: list
    :param b_ub: Termos independentes.
    :type b_ub: list
    :param mode: 'max' ou 'min'.
    :type mode: str
    """
    tableau, columns, base_vars = _build_tableau(c, A_ub, b_ub)
    iteration = 1
    
    while np.any(tableau[1:, -1] < -1e-9): # Tolerância pequena
        pivot_row = np.argmin(tableau[1:, -1]) + 1
        pivot_row_values = tableau[pivot_row, :-2]
        z_row_values = tableau[0, :-2]
        ratios_dual = np.full(len(pivot_row_values), np.inf)
        
        for i in range(len(pivot_row_values)):
            if pivot_row_values[i] < 0:
                ratios_dual[i] = np.abs(z_row_values[i] / pivot_row_values[i])
        
        if np.all(ratios_dual == np.inf):
            st.error("❌ Problema infactível.")
            return

        pivot_col = np.argmin(ratios_dual)
        entering_var, leaving_var = columns[pivot_col], base_vars[pivot_row - 1]
        
        show_tableau_streamlit(tableau, columns, base_vars, title="Dual Quadro", iteration=iteration)
        st.markdown(f"**Dual:** Sai `{leaving_var}` → Entra `{entering_var}`")
        
        base_vars[pivot_row - 1] = entering_var
        _pivot(tableau, pivot_row, pivot_col)
        iteration += 1

    st.success("✅ Solução Dual encontrada!")
    _show_final_result(tableau, columns, base_vars, mode, c)

def solve_big_m_step_by_step(c, A, b, tipos, mode='max'):
    """
    Executa o Método Big M passo a passo.

    Utilizado para problemas com restrições mistas ou igualdades que exigem variáveis artificiais.

    :param c: Coeficientes da função objetivo.
    :type c: list
    :param A: Coeficientes das restrições.
    :type A: list
    :param b: Termos independentes.
    :type b: list
    :param tipos: Lista de tipos das restrições ('<=', '>=', '=').
    :type tipos: list[str]
    :param mode: 'max' ou 'min'.
    :type mode: str
    """
    st.info(f"⚙️ Inicializando **Método Big M** (M = {M_CONST:.0f})...")
    tableau, columns, base_vars = _build_big_m_tableau(c, A, b, tipos, mode)
    
    # Passamos 'c' para o display final
    _run_simplex_loop(tableau, columns, base_vars, mode, method_name="Big M", c_original=c)
    
    # Validação Final: Variáveis Artificiais
    final_base = base_vars
    artificiais_na_base = [var for var in final_base if var.startswith('a')]
    
    tem_artificial_positiva = False
    for artif in artificiais_na_base:
        row_idx = final_base.index(artif) + 1
        val = tableau[row_idx, -1]
        if val > 1e-5: 
            tem_artificial_positiva = True
    
    if tem_artificial_positiva:
        st.error("❌ **Solução Infactível:** Variáveis artificiais permanecem positivas. O problema não tem solução real.")
    else:
        st.success("✅ Solução Ótima Real encontrada (Artificiais zeradas)!")

def _run_simplex_loop(tableau, columns, base_vars, mode, method_name="Simplex", c_original=None):
    """
    Loop principal genérico do algoritmo Simplex (Primal).

    Itera sobre o tableau até encontrar a solução ótima ou ilimitada, exibindo cada passo no Streamlit.

    :param tableau: Matriz do tableau inicial.
    :type tableau: np.ndarray
    :param columns: Nomes das colunas.
    :type columns: list[str]
    :param base_vars: Nomes das variáveis básicas iniciais.
    :type base_vars: list[str]
    :param mode: 'max' ou 'min'.
    :type mode: str
    :param method_name: Nome do método para exibição nos títulos (ex: "Big M").
    :type method_name: str
    :param c_original: Coeficientes originais para formatação do resultado final.
    :type c_original: list or None
    """
    iteration = 1
    while True:
        linha_z = tableau[0, :-2]
        
        # Critério de parada
        if mode == 'max':
            if np.all(linha_z >= -1e-5):
                break
            pivot_col = np.argmin(linha_z)
        elif mode == 'min':
            if np.all(linha_z <= 1e-5):
                break
            pivot_col = np.argmax(linha_z)

        # Razão
        col = tableau[1:, pivot_col]
        rhs = tableau[1:, -1]
        
        with np.errstate(divide='ignore'):
            ratios = np.where(col > 1e-9, rhs / col, np.inf)

        if np.all(ratios == np.inf):
            st.error("⚠️ Solução ilimitada.")
            return

        pivot_row = np.argmin(ratios) + 1
        entering_var, leaving_var = columns[pivot_col], base_vars[pivot_row - 1]

        show_tableau_streamlit(tableau, columns, base_vars, title=f"Quadro {method_name}", iteration=iteration, ratios=ratios)
        
        base_vars[pivot_row - 1] = entering_var
        _pivot(tableau, pivot_row, pivot_col)
        iteration += 1

    _show_final_result(tableau, columns, base_vars, mode, c_original)

def _pivot(tableau, pivot_row, pivot_col):
    """
    Realiza a operação de pivoteamento Gaussiano no tableau.

    Altera o tableau in-place, tornando a coluna pivô um vetor unitário.

    :param tableau: Matriz do tableau a ser modificada.
    :type tableau: np.ndarray
    :param pivot_row: Índice da linha do elemento pivô.
    :type pivot_row: int
    :param pivot_col: Índice da coluna do elemento pivô.
    :type pivot_col: int
    """
    pivot_element = tableau[pivot_row, pivot_col]
    tableau[pivot_row] /= pivot_element
    for i in range(tableau.shape[0]):
        if i != pivot_row:
            tableau[i] -= tableau[i, pivot_col] * tableau[pivot_row]

def _show_final_result(tableau, columns, base_vars, mode, c_original):
    """
    Exibe o resultado final formatado com métricas e valores das variáveis de decisão.

    :param tableau: Tableau final otimizado.
    :type tableau: np.ndarray
    :param columns: Lista de nomes das colunas.
    :type columns: list[str]
    :param base_vars: Variáveis que terminaram na base.
    :type base_vars: list[str]
    :param mode: 'max' ou 'min'.
    :type mode: str
    :param c_original: Lista de coeficientes originais para determinar o número de variáveis de decisão.
    :type c_original: list or None
    """
    final_z_value = tableau[0, -1]
    
    st.markdown("### 🏁 Solução Final")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Z ótimo", value=f"{final_z_value:.2f}")
    with col2:
        st.metric(label="Modo", value="Maximização" if mode == 'max' else "Minimização")

    st.markdown("### 📈 Variáveis de Decisão:")

    # Define número de variáveis originais para exibir
    if c_original is not None:
        total_vars = len(c_original)
    else:
        # Fallback: conta colunas que começam com 'x'
        total_vars = sum(1 for c in columns if c.startswith('x'))

    num_cols = min(max(2, total_vars // 3 + 1), 5)  # entre 2 e 5 colunas
    cols = st.columns(num_cols)

    for i in range(total_vars):
        var_name = f'x{i+1}'
        valor = "0.00"
        
        if var_name in base_vars:
            # Pega o valor da coluna RHS (-1) na linha correspondente à variável básica
            idx_linha = base_vars.index(var_name) + 1
            valor_float = tableau[idx_linha, -1]
            valor = f"{valor_float:.2f}"
        
        with cols[i % num_cols]:
            st.metric(label=var_name, value=valor)

def solve_automatico(c, A, b, tipos, mode='max'):
    """
    Analisa o problema e roteia automaticamente para o algoritmo mais adequado (Primal, Dual ou Big M).

    1. Se houver igualdades ('='), roteia para Big M.
    2. Tenta converter restrições '>=' para '<=' multiplicando por -1.
    3. Analisa a factibilidade Primal (b >= 0) e Dual (otimalidade de Z).
    4. Escolhe entre Primal Simplex, Dual Simplex ou Big M.

    :param c: Coeficientes da função objetivo.
    :type c: list
    :param A: Coeficientes das restrições.
    :type A: list
    :param b: Termos independentes.
    :type b: list
    :param tipos: Lista de tipos das restrições.
    :type tipos: list[str]
    :param mode: 'max' ou 'min'.
    :type mode: str
    """
    c_np = np.array(c, dtype=float)
    A_np = np.array(A, dtype=float)
    b_np = np.array(b, dtype=float)

    if "=" in tipos:
        st.warning("⚠️ Igualdades detectadas: Usando **Método Big M**.")
        solve_big_m_step_by_step(c, A, b, tipos, mode)
        return

    A_norm = A_np.copy()
    b_norm = b_np.copy()
    tipos_convertidos = False
    
    for i, tipo in enumerate(tipos):
        if tipo == "≥":
            A_norm[i] = -A_norm[i]
            b_norm[i] = -b_norm[i]
            tipos_convertidos = True
            
    primal_factivel = np.all(b_norm >= 0)
    
    z_row = -c_np if mode == 'max' else c_np
    dual_factivel = np.all(z_row >= 0) if mode == 'max' else np.all(z_row <= 0)

    if primal_factivel and not tipos_convertidos:
        st.success("✅ Problema Padrão. Usando **Primal Simplex**.")
        solve_simplex_step_by_step(c, A_norm.tolist(), b_norm.tolist(), mode)
        
    elif not primal_factivel and dual_factivel:
        st.success("✅ RHS Negativo e Z Ótimo. Usando **Dual Simplex**.")
        solve_dual_simplex_step_by_step(c, A_norm.tolist(), b_norm.tolist(), mode)
        
    else:
        st.warning("🔄 Problema Misto. Usando **Método Big M**.")
        solve_big_m_step_by_step(c, A, b, tipos, mode)