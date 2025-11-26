# 🧮 PlataformaSimplex

Uma ferramenta web interativa e educativa para resolver problemas de Programação Linear (PL). Projetada para estudantes e profissionais, a plataforma resolve desde problemas simples até casos complexos com restrições mistas, mostrando todo o passo a passo do algoritmo.

---

## 🚀 Acesse Agora

A aplicação está rodando na nuvem e pronta para uso. Não é necessário instalar nada!

### 👉 [Clique aqui para acessar a Plataforma Simplex](https://plataformasimplex-b6tyannbyswusrqgypdul3.streamlit.app/)

---

## 📖 Guia de Uso

A plataforma foi desenhada para ser intuitiva. Siga os passos abaixo para resolver seu problema:

### 1. Configuração Inicial (Barra Lateral)
No menu à esquerda, defina as bases do seu problema:
* **Método:**
    * **Automático:** A opção mais poderosa. O sistema analisa suas restrições e escolhe sozinho entre *Primal*, *Dual* ou *Big M*. Permite usar $\le$, $\ge$ e $=$.
    * **Primal Simplex:** Para problemas na forma padrão (apenas restrições $\le$ e RHS positivo).
    * **Dual Simplex:** Para problemas onde a solução inicial é "otimista" mas infactível (ex: restrições $\ge$ convertidas).
* **Modo de Otimização:** Escolha se deseja **Maximizar** (lucro, produção) ou **Minimizar** (custo, tempo).
* **Dimensões:** Defina quantas **variáveis de decisão** ($x$) e quantas **restrições** o problema possui.

### 2. Inserindo os Dados
Após configurar, preencha os campos que aparecem na tela principal:

* **Função Objetivo (Z):** Digite os coeficientes que acompanham cada variável na função que você quer otimizar.
* **Restrições:**
    * Se estiver no **Modo Automático**, você verá uma caixa de seleção para cada linha. Você pode misturar restrições do tipo Menor ou Igual ($\le$), Maior ou Igual ($\ge$) e Igualdade ($=$).
    * Digite os coeficientes das variáveis e o termo independente (RHS - *Right Hand Side*).

### 3. Interpretando os Resultados
Ao clicar em **"🚀 Resolver"**, a mágica acontece:

* **Passo a Passo:** A plataforma exibe cada quadro (*tableau*) gerado pelo algoritmo. Você pode ver quem entra na base, quem sai e como os valores mudam a cada iteração.
* **Diagnóstico Automático:** O sistema avisa qual método foi escolhido (ex: *"Igualdades detectadas: Usando Método Big M"*).
* **Quadro Final:** Um resumo elegante mostrando:
    * O valor ótimo de **Z**.
    * Os valores finais das variáveis de decisão ($x_1, x_2, ...$).
    * Variáveis de folga ou excesso resultantes.

---

## ✨ Funcionalidades Detalhadas

A Plataforma Simplex é completa e suporta:

### 🤖 Modo Automático Inteligente
Não sabe qual método usar? O modo automático analisa a estrutura matemática do seu problema:
1.  Verifica se há igualdades ou restrições de "maior que".
2.  Normaliza o problema.
3.  Decide se usa **Primal**, **Dual** ou o **Método Big M** (Grande M).

### 📐 Método Big M (Grande M)
Implementação robusta para lidar com problemas difíceis que não possuem uma solução inicial óbvia (como aqueles com restrições $=$ ou $\ge$). O sistema adiciona automaticamente variáveis artificiais e aplica penalidades para encontrar a solução real.

### 🔄 Dual Simplex
Capaz de resolver problemas onde a função objetivo satisfaz a condição de otimalidade, mas as restrições são violadas (RHS negativo). Essencial para análises de sensibilidade e problemas de minimização convertidos.

### 📊 Visualização Didática
Perfeito para estudantes! Diferente de solucionadores "caixa preta" (como o Excel Solver), aqui você vê a matemática acontecendo quadro a quadro.

---

## 🛠️ Tecnologias

* **Front-end:** Streamlit (Interface limpa e responsiva).
* **Back-end:** Python puro.
* **Matemática:** NumPy (Álgebra linear e manipulação de matrizes) e Pandas (Estruturação dos quadros).

---

## 🐛 Contato e Suporte

Encontrou um bug nos cálculos ou tem uma sugestão?

1.  **(Preferencial) GitHub Issues:** Abra uma **[Issue](https://github.com/Edy-py/PlataformaSimplex/issues)** detalhando o problema (inclua os valores usados).
2.  **(E-mail):** Para contato profissional: **edilsonalvesprofissional@gmail.com**

## 🧠 Nota sobre o Desenvolvimento

> Uma parte significativa da interface de usuário (front-end) desta aplicação foi desenvolvida com o auxílio de ferramentas de Inteligência Artificial. Os componentes gerados pela IA foram rigorosamente revisados, ajustados e a lógica matemática (back-end) foi integrada e validada manualmente por mim (**Edy**) para garantir precisão nos resultados.

---
Desenvolvido por **Edy** 🧠
