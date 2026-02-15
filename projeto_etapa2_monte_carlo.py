import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- PARÂMETROS DO MODELO ---

# Parâmetros da Demanda (semanal)
media_demanda_semanal = 68.86
desvio_padrao_demanda_semanal = 20.06

# Parâmetros de Custo
custo_pedido = 45.00  # Custo fixo por pedido (K)
custo_item = 25.00  # Custo por unidade do item (c)
custo_falta = 18.00  # Custo por unidade em falta (p)
taxa_manutencao_anual = 0.25  # Taxa de custo de manutenção (i)

# Parâmetros de Tempo
lead_time_semanas = 1  # Lead time em semanas (L)
semanas_por_ano = 52

# Parâmetros da Simulação
num_simulacoes = 1000
num_semanas_simuladas = 52

# --- CÁLCULOS INTERMEDIÁRIOS ---

custo_manutencao_semanal = (custo_item * taxa_manutencao_anual) / semanas_por_ano
demanda_anual_media = media_demanda_semanal * semanas_por_ano

# --- POLÍTICA DE ESTOQUE (Q, ROP) ---

# Lote Econômico de Compra (EOQ)
Q_otimo = np.sqrt((2 * custo_pedido * demanda_anual_media) / (custo_item * taxa_manutencao_anual))
Q_otimo = int(Q_otimo)

# Nível de Serviço e Estoque de Segurança
nivel_servico_desejado = 0.95
z_score = 1.645  # Para 95% de nível de serviço

estoque_seguranca = z_score * desvio_padrao_demanda_semanal * np.sqrt(lead_time_semanas)
estoque_seguranca = int(estoque_seguranca)

# Ponto de Reposição (ROP)
ponto_reposicao = (media_demanda_semanal * lead_time_semanas) + estoque_seguranca
ponto_reposicao = int(ponto_reposicao)

# --- FUNÇÃO DE SIMULAÇÃO ---

def simular_politica_estoque(Q, ROP, num_semanas, semente):
    np.random.seed(semente)
    
    # Inicialização das variáveis
    estoque_inicial = Q + estoque_seguranca
    estoque_atual = estoque_inicial
    estoque_final_semana = []
    custo_total_periodo = 0
    custo_pedidos_total = 0
    custo_manutencao_total = 0
    custo_falta_total = 0
    unidades_em_falta_total = 0
    pedidos_feitos = 0
    semanas_com_falta = 0
    
    lead_time_restante = 0
    pedido_em_transito = False

    for semana in range(num_semanas):
        # 1. Chegada de pedido
        if pedido_em_transito:
            lead_time_restante -= 1
            if lead_time_restante <= 0:
                estoque_atual += Q
                pedido_em_transito = False

        # 2. Demanda da semana
        demanda_semana = int(np.random.normal(media_demanda_semanal, desvio_padrao_demanda_semanal))
        if demanda_semana < 0:
            demanda_semana = 0

        # 3. Atender demanda
        if estoque_atual >= demanda_semana:
            estoque_atual -= demanda_semana
            unidades_em_falta = 0
        else:
            unidades_em_falta = demanda_semana - estoque_atual
            estoque_atual = 0
            semanas_com_falta += 1

        # 4. Calcular custos da semana
        custo_manutencao_semana = estoque_atual * custo_manutencao_semanal
        custo_falta_semana = unidades_em_falta * custo_falta
        
        custo_manutencao_total += custo_manutencao_semana
        custo_falta_total += custo_falta_semana
        unidades_em_falta_total += unidades_em_falta

        # 5. Fazer novo pedido
        if not pedido_em_transito and estoque_atual <= ROP:
            custo_pedidos_total += custo_pedido
            pedidos_feitos += 1
            pedido_em_transito = True
            lead_time_restante = lead_time_semanas
            
        estoque_final_semana.append(estoque_atual)

    custo_total_periodo = custo_pedidos_total + custo_manutencao_total + custo_falta_total
    nivel_servico_demanda = 1 - (unidades_em_falta_total / (media_demanda_semanal * num_semanas))
    
    return {
        "custo_total": custo_total_periodo,
        "custo_pedido": custo_pedidos_total,
        "custo_manutencao": custo_manutencao_total,
        "custo_falta": custo_falta_total,
        "nivel_servico": nivel_servico_demanda,
        "estoque_medio": np.mean(estoque_final_semana)
    }

# --- EXECUÇÃO DA SIMULAÇÃO ---

resultados = []
for i in range(num_simulacoes):
    resultado_sim = simular_politica_estoque(Q_otimo, ponto_reposicao, num_semanas_simuladas, semente=i)
    resultados.append(resultado_sim)

df_resultados = pd.DataFrame(resultados)

# --- ANÁLISE E VISUALIZAÇÃO DOS RESULTADOS ---

# Resumo estatístico
resumo = df_resultados.describe()
print("Resumo Estatístico dos Resultados da Simulação:")
print(resumo)

# Salvar resultados em Excel
df_resultados.to_excel("resultados_simulacao_etapa2.xlsx", index=False)

# Gráficos
sns.set_style("whitegrid")
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle("Resultados da Simulação de Monte Carlo para a Política de Estoque (Q, ROP)", fontsize=16)

# 1. Distribuição do Custo Total
sns.histplot(df_resultados["custo_total"], kde=True, ax=axes[0, 0])
axes[0, 0].set_title("Distribuição do Custo Total Anual")
axes[0, 0].set_xlabel("Custo Total (R$)")
axes[0, 0].set_ylabel("Frequência")

# 2. Distribuição do Nível de Serviço
sns.histplot(df_resultados["nivel_servico"], kde=False, ax=axes[0, 1])
axes[0, 1].set_title("Distribuição do Nível de Serviço")
axes[0, 1].set_xlabel("Nível de Serviço")
axes[0, 1].set_ylabel("Frequência")

# 3. Composição Média de Custos
custos_medios = df_resultados[["custo_pedido", "custo_manutencao", "custo_falta"]].mean()
custos_medios.plot(kind='bar', ax=axes[0, 2], color=["steelblue", "darkorange", "red"])
axes[0, 2].set_title("Composição Média dos Custos")
axes[0, 2].set_ylabel("Custo (R$)")
axes[0, 2].tick_params(axis='x', rotation=0)

# 4. Distribuição do Estoque Médio
sns.histplot(df_resultados["estoque_medio"], kde=True, ax=axes[1, 0])
axes[1, 0].set_title("Distribuição do Estoque Médio")
axes[1, 0].set_xlabel("Estoque Médio (unidades)")
axes[1, 0].set_ylabel("Frequência")

# 5. Box Plot dos Componentes de Custo
sns.boxplot(data=df_resultados[["custo_pedido", "custo_manutencao", "custo_falta"]], ax=axes[1, 1])
axes[1, 1].set_title("Box Plot dos Componentes de Custo")
axes[1, 1].set_ylabel("Custo (R$)")

# Remover o sexto subplot (vazio)
fig.delaxes(axes[1, 2])

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("resultados_simulacao_etapa2.png")
plt.show()

print("\nSimulação concluída. Resultados salvos em 'resultados_simulacao_etapa2.xlsx' e 'resultados_simulacao_etapa2.png'.")
