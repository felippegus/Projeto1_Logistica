# Projeto 1: Logística Quantitativa Aplicada - Restaurante Gulla's

## 📋 Descrição

Este projeto apresenta uma análise completa da gestão de estoques do restaurante Gulla's, com foco no item "Frango Grelhado". A análise combina modelagem determinística (EOQ), simulação de Monte Carlo e análise de cenários para determinar a política de estoque ótima.

## 🎯 Objetivo

Desenvolver um sistema de apoio à decisão para a gestão de estoques de ingredientes críticos, utilizando modelos quantitativos para otimizar a política de reposição e minimizar custos logísticos.

## 📊 Dados

- **Período:** Março a Agosto de 2023
- **Item de Foco:** Frango Grelhado (produto mais vendido)
- **Demanda Média Semanal:** 68.86 unidades
- **Desvio Padrão:** 20.06 unidades/semana

## 🔧 Metodologia

### 1. Modelagem Determinística (EOQ)
- Cálculo do Lote Econômico de Compra (Q*)
- Determinação do Ponto de Reposição (ROP)
- Análise de custos de pedido e manutenção

### 2. Simulação de Monte Carlo
- 1000 replicações de 52 semanas
- Incorporação de incerteza na demanda
- Cálculo de nível de serviço e custos

### 3. Análise de Cenários
- Cenário 1: Política Base (Q=378, ROP=102)
- Cenário 2: Nível de Serviço 90%
- Cenário 3: Nível de Serviço 97.5%
- Cenário 4: Lote Reduzido (Q=250)
- Cenário 5: Lote Aumentado (Q=500)

## 📈 Resultados Principais

### Política Recomendada: Cenário 4 (Lote Reduzido)
- **Custo Total Anual:** R$ 1.627,29
- **Nível de Serviço:** 99,98%
- **Estoque Médio:** 161,50 unidades
- **Economia:** 11% em relação à política base

## 📁 Estrutura do Repositório

```
projeto-logistica-gullas/
├── README.md                          # Este arquivo
├── data/
│   ├── 1-2023 ATUALIZADA.xlsx       # Dados brutos de vendas
├── src/
│   ├── projeto_etapa2_monte_carlo.py # Simulação principal
│   ├── analise_cenarios_etapa2.py    # Análise de cenários
│   └── utils.py                      # Funções auxiliares
├── results/
│   ├── resultados_simulacao_etapa2.xlsx
│   ├── resumo_cenarios_etapa2.xlsx
│   ├── resultados_simulacao_etapa2.png
│   └── analise_cenarios_etapa2.png
├── notebooks/
│   └── analise_completa.ipynb        # Notebook interativo
├── docs/
│   └── Projeto_1_Completo_Final.pdf  # Relatório técnico
└── requirements.txt                  # Dependências Python
```

## 🚀 Como Usar

### Pré-requisitos
- Python 3.11+
- Pandas, NumPy, Matplotlib, Seaborn

### Instalação

```bash
# Clonar o repositório
git clone https://github.com/felippegsramos/projeto-logistica-gullas.git
cd projeto-logistica-gullas

# Instalar dependências
pip install -r requirements.txt
```

### Executar a Simulação

```bash
# Simulação principal
python src/projeto_etapa2_monte_carlo.py

# Análise de cenários
python src/analise_cenarios_etapa2.py
```

### Visualizar o Notebook

```bash
# Iniciar Jupyter
jupyter notebook notebooks/analise_completa.ipynb
```

## 📊 Visualizações

### Gráficos Gerados

1. **Distribuição de Custos:** Histograma do custo total anual
2. **Nível de Serviço:** Distribuição do nível de serviço alcançado
3. **Composição de Custos:** Gráfico de barras com pedido, manutenção e falta
4. **Estoque Médio:** Distribuição do estoque médio
5. **Box Plot:** Comparação de componentes de custo
6. **Trade-off:** Relação entre nível de serviço e custo total

## 🔗 Links Importantes

- **Notebook Interativo:** [Análise Completa](https://felippegsramos.github.io/projeto-logistica-gullas/notebook.html)
- **Dashboard Streamlit:** [Dashboard Interativo](https://felippegsramos-projeto-logistica-gullas.streamlit.app/)
- **Relatório Técnico:** [PDF Completo](docs/Projeto_1_Completo_Final.pdf)

## 📝 Decisão Recomendada

A análise recomenda a adoção da **Política de Estoque (Q=250, ROP=102)**, que apresenta:

- **Menor custo total:** R$ 1.627,29/ano
- **Nível de serviço excepcional:** 99,98%
- **Estoque reduzido:** 161,50 unidades (menos capital imobilizado)
- **Frequência de pedidos:** 13,7 pedidos/ano

Esta política minimiza os custos logísticos e praticamente elimina as faltas de estoque, garantindo a satisfação do cliente.

## 💡 Insights Principais

1. **Lote Reduzido é Ótimo:** Reduzir o lote de compra economiza 11% no custo total
2. **Trade-off Favorável:** Aumentar o nível de serviço custa apenas 5% a mais
3. **Impacto do Lote:** O tamanho do lote (Q) tem maior impacto que o ponto de reposição (ROP)
4. **Nível de Serviço Excepcional:** A política alcança 99,98%, praticamente eliminando faltas

## 📚 Referências

- Ballou, R. H. (2004). Business Logistics/Supply Chain Management
- Chopra, S., & Meindl, P. (2016). Supply Chain Management
- Heizer, J., & Render, B. (2014). Operations Management

## 👤 Autor

**Felippe G S Ramos**  
Engenharia de Produção - Universidade de Brasília  
Matrícula: 211027062

## 📄 Licença

Este projeto é fornecido para fins educacionais.

## 📧 Contato

Para dúvidas ou sugestões, entre em contato através do GitHub Issues.

---

**Última atualização:** 14 de Fevereiro de 2026
