import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- PARÂMETROS BASE ---

media_demanda_semanal = 68.86
desvio_padrao_demanda_semanal = 20.06
custo_pedido = 45.00
custo_item = 25.00
custo_falta = 18.00
taxa_manutencao_anual = 0.25
lead_time_semanas = 1
semanas_por_ano = 52

custo_manutencao_semanal = (custo_item * taxa_manutencao_anual) / semanas_por_ano
demanda_anual_media = media_demanda_semanal * semanas_por_ano

# --- FUNÇÃO DE SIMULAÇÃO (OTIMIZADA) ---

def simular_politica_estoque_rapido(Q, ROP, num_semanas, num_simulacoes, semente_base):
    np.random.seed(semente_base)
    
    resultados = []
    
    for sim in range(num_simulacoes):
        estoque_atual = Q + ROP
        custo_total = 0
        custo_pedidos = 0
        custo_manutencao = 0
        custo_falta = 0
        unidades_em_falta = 0
        pedidos_feitos = 0
        lead_time_restante = 0
        pedido_em_transito = False
        estoque_acumulado = 0
        
        for semana in range(num_semanas):
            # Chegada de pedido
            if pedido_em_transito:
                lead_time_restante -= 1
                if lead_time_restante <= 0:
                    estoque_atual += Q
                    pedido_em_transito = False
            
            # Demanda
            demanda = max(0, int(np.random.normal(media_demanda_semanal, desvio_padrao_demanda_semanal)))
            
            # Atender demanda
            if estoque_atual >= demanda:
                estoque_atual -= demanda
            else:
                unidades_em_falta += demanda - estoque_atual
                estoque_atual = 0
            
            # Custos
            custo_manutencao += estoque_atual * custo_manutencao_semanal
            custo_falta += (demanda - min(demanda, estoque_atual)) * custo_falta
            estoque_acumulado += estoque_atual
            
            # Novo pedido
            if not pedido_em_transito and estoque_atual <= ROP:
                custo_pedidos += custo_pedido
                pedidos_feitos += 1
                pedido_em_transito = True
                lead_time_restante = lead_time_semanas
        
        custo_total = custo_pedidos + custo_manutencao + custo_falta
        nivel_servico = 1 - (unidades_em_falta / (media_demanda_semanal * num_semanas))
        estoque_medio = estoque_acumulado / num_semanas
        
        resultados.append({
            "custo_total": custo_total,
            "custo_pedido": custo_pedidos,
            "custo_manutencao": custo_manutencao,
            "custo_falta": custo_falta,
            "nivel_servico": nivel_servico,
            "estoque_medio": estoque_medio,
            "pedidos_feitos": pedidos_feitos
        })
    
    return pd.DataFrame(resultados)

# --- ANÁLISE DE CENÁRIOS ---

# Cenário 1: Política Base (Q=378, ROP=102)
print("Executando Cenário 1: Política Base...")
Q_base = 378
ROP_base = 102
df_cenario1 = simular_politica_estoque_rapido(Q_base, ROP_base, 52, 500, 42)

# Cenário 2: Nível de Serviço Reduzido (z=1.28, 90%)
print("Executando Cenário 2: Nível de Serviço 90%...")
z_90 = 1.28
ROP_90 = int((media_demanda_semanal * lead_time_semanas) + (z_90 * desvio_padrao_demanda_semanal * np.sqrt(lead_time_semanas)))
df_cenario2 = simular_politica_estoque_rapido(Q_base, ROP_90, 52, 500, 42)

# Cenário 3: Nível de Serviço Elevado (z=1.96, 97.5%)
print("Executando Cenário 3: Nível de Serviço 97.5%...")
z_975 = 1.96
ROP_975 = int((media_demanda_semanal * lead_time_semanas) + (z_975 * desvio_padrao_demanda_semanal * np.sqrt(lead_time_semanas)))
df_cenario3 = simular_politica_estoque_rapido(Q_base, ROP_975, 52, 500, 42)

# Cenário 4: Lote Reduzido (Q=250)
print("Executando Cenário 4: Lote Reduzido...")
Q_reduzido = 250
df_cenario4 = simular_politica_estoque_rapido(Q_reduzido, ROP_base, 52, 500, 42)

# Cenário 5: Lote Aumentado (Q=500)
print("Executando Cenário 5: Lote Aumentado...")
Q_aumentado = 500
df_cenario5 = simular_politica_estoque_rapido(Q_aumentado, ROP_base, 52, 500, 42)

# --- CONSOLIDAÇÃO DOS RESULTADOS ---

cenarios = {
    "Cenário 1: Base (Q=378, ROP=102, SL=95%)": df_cenario1,
    "Cenário 2: SL 90% (Q=378, ROP=86)": df_cenario2,
    "Cenário 3: SL 97.5% (Q=378, ROP=118)": df_cenario3,
    "Cenário 4: Lote Reduzido (Q=250, ROP=102)": df_cenario4,
    "Cenário 5: Lote Aumentado (Q=500, ROP=102)": df_cenario5
}

# Resumo por cenário
resumo_cenarios = []
for nome, df in cenarios.items():
    resumo_cenarios.append({
        "Cenário": nome,
        "Custo Total Médio": df["custo_total"].mean(),
        "Custo Pedido Médio": df["custo_pedido"].mean(),
        "Custo Manutenção Médio": df["custo_manutencao"].mean(),
        "Custo Falta Médio": df["custo_falta"].mean(),
        "Nível de Serviço Médio": df["nivel_servico"].mean(),
        "Estoque Médio": df["estoque_medio"].mean(),
        "Pedidos Médios": df["pedidos_feitos"].mean()
    })

df_resumo = pd.DataFrame(resumo_cenarios)
df_resumo.to_excel("resumo_cenarios_etapa2.xlsx", index=False)

print("\nResumo dos Cenários:")
print(df_resumo.to_string())

# --- VISUALIZAÇÕES ---

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("Análise Comparativa de Cenários de Política de Estoque", fontsize=16)

# 1. Comparação de Custos Totais
cenario_nomes = [nome.split(":")[0] for nome in cenarios.keys()]
custos_medios = [cenarios[nome]["custo_total"].mean() for nome in cenarios.keys()]
axes[0, 0].bar(range(len(cenario_nomes)), custos_medios, color=["steelblue", "orange", "red", "green", "purple"])
axes[0, 0].set_xticks(range(len(cenario_nomes)))
axes[0, 0].set_xticklabels(cenario_nomes, rotation=45, ha='right')
axes[0, 0].set_title("Custo Total Médio por Cenário")
axes[0, 0].set_ylabel("Custo Total (R$)")

# 2. Comparação de Níveis de Serviço
niveis_servico = [cenarios[nome]["nivel_servico"].mean() for nome in cenarios.keys()]
axes[0, 1].bar(range(len(cenario_nomes)), niveis_servico, color=["steelblue", "orange", "red", "green", "purple"])
axes[0, 1].set_xticks(range(len(cenario_nomes)))
axes[0, 1].set_xticklabels(cenario_nomes, rotation=45, ha='right')
axes[0, 1].set_title("Nível de Serviço Médio por Cenário")
axes[0, 1].set_ylabel("Nível de Serviço")
axes[0, 1].set_ylim([0.98, 1.001])

# 3. Comparação de Estoque Médio
estoques_medios = [cenarios[nome]["estoque_medio"].mean() for nome in cenarios.keys()]
axes[1, 0].bar(range(len(cenario_nomes)), estoques_medios, color=["steelblue", "orange", "red", "green", "purple"])
axes[1, 0].set_xticks(range(len(cenario_nomes)))
axes[1, 0].set_xticklabels(cenario_nomes, rotation=45, ha='right')
axes[1, 0].set_title("Estoque Médio por Cenário")
axes[1, 0].set_ylabel("Estoque Médio (unidades)")

# 4. Trade-off Custo vs Nível de Serviço
axes[1, 1].scatter(niveis_servico, custos_medios, s=200, alpha=0.6, c=range(len(cenario_nomes)), cmap='viridis')
for i, nome in enumerate(cenario_nomes):
    axes[1, 1].annotate(nome, (niveis_servico[i], custos_medios[i]), fontsize=9, ha='center')
axes[1, 1].set_title("Trade-off: Nível de Serviço vs Custo Total")
axes[1, 1].set_xlabel("Nível de Serviço")
axes[1, 1].set_ylabel("Custo Total (R$)")
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("analise_cenarios_etapa2.png", dpi=150)
plt.show()

print("\nAnálise de cenários concluída. Resultados salvos em 'resumo_cenarios_etapa2.xlsx' e 'analise_cenarios_etapa2.png'.")
