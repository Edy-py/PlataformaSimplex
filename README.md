# 🧮 PlataformaSimplex

Uma ferramenta web interativa para resolver problemas de Programação Linear (PL) passo a passo. Esta plataforma permite ao usuário inserir os coeficientes da função objetivo e das restrições, escolhendo entre os métodos **Primal Simplex** e **Dual Simplex** para encontrar a solução ótima.

A aplicação é construída em Python usando Streamlit para a interface de usuário e NumPy para os cálculos matemáticos.

---

## 🚀 Acessar a Aplicação (Deploy)

A plataforma está disponível publicamente e hospedada no Streamlit Cloud.

**Acesse aqui: [Plataforma Simplex](https://plataformasimplex-b6tyannbyswusrqgypdul3.streamlit.app/)**

---

## ✨ Funcionalidades Principais

* **Seleção de Método:** Permite ao usuário escolher entre "Primal Simplex", "Dual Simplex" e "Automático".
* **Modo de Otimização:** Suporta problemas de Maximização (`max`) e Minimização (`min`).
* **Entrada Dinâmica:** O usuário pode definir o número de variáveis e restrições que o problema possui.
* **Visualização Passo a Passo:** A principal funcionalidade. A plataforma não mostra apenas a resposta final, mas exibe cada "Quadro" (tableau) do Simplex em cada iteração, facilitando o aprendizado e a verificação.
* **Relatório Final:** Apresenta o valor ótimo da função objetivo (Z) e os valores finais das variáveis básicas.

## 🛠️ Tecnologias Utilizadas

* **Python**
* **Streamlit:** Para a criação da interface web interativa.
* **NumPy:** Para os cálculos matriciais e manipulação eficiente do tableau.
* **Pandas:** Para a formatação e exibição elegante dos quadros (tableaus).

## 🚀 Como Executar Localmente

Siga os passos abaixo para executar o projeto na sua máquina.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Edy-py/PlataformaSimplex.git](https://github.com/Edy-py/PlataformaSimplex.git)
    cd PlataformaSimplex
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    # Linux/macOS
    python3 -m venv .venv
    source .venv/bin/activate
    
    # Windows
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    (Recomenda-se criar um arquivo `requirements.txt` com `streamlit`, `numpy` e `pandas`)
    ```bash
    pip install streamlit numpy pandas
    ```

4.  **Execute a aplicação Streamlit:**
    ```bash
    streamlit run plataformaSimplex.py
    ```

5.  Acesse `http://localhost:8501` no seu navegador.

## 🐛 Contato e Relatório de Bugs

Encontrou um bug ou tem sugestões de melhoria? Existem duas formas principais de entrar em contato:

1.  **(Preferencial) Abrir uma Issue:** Para relatórios técnicos de bugs, por favor, abra uma **[Issue](https://github.com/Edy-py/PlataformaSimplex/issues)** neste repositório.
    * Ao relatar, inclua os valores de entrada, o método/modo e a mensagem de erro.

2.  **(Contato Profissional) E-mail:** Para outras questões, sugestões ou contato profissional, você pode me encontrar em:
    * **edilsonalvesprofissional@gmail.com**

## 🧠 Nota sobre o Desenvolvimento

> Uma parte significativa da interface de usuário (front-end) desta aplicação foi desenvolvida com o auxílio de ferramentas de Inteligência Artificial. Os componentes gerados pela IA foram então revisados, ajustados e integrados manualmente por mim (**Edy**) para garantir a funcionalidade correta e a conexão com os algoritmos de Simplex (back-end).

---
Desenvolvido por **Edy** 🧠
