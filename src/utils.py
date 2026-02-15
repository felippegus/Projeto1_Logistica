#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de Funções Auxiliares - Projeto 1: Gestão de Estoques Gulla's

Este módulo contém funções reutilizáveis para cálculos, validações e 
processamento de dados relacionados à gestão de estoques.

Autor: Felippe G S Ramos
Data: 15 de Fevereiro de 2026
"""

import numpy as np
import pandas as pd
from scipy.stats import norm
from typing import Tuple, Dict, List, Union


# =====================================================
# FUNÇÕES DE CÁLCULO - MODELO EOQ
# =====================================================

def calcular_eoq(demanda_anual: float, custo_pedido: float, custo_manutencao: float) -> float:
    """
    Calcula o Lote Econômico de Compra (EOQ).
    
    Parâmetros:
    -----------
    demanda_anual : float
        Demanda anual em unidades
    custo_pedido : float
        Custo fixo por pedido (R$)
    custo_manutencao : float
        Custo anual de manutenção por unidade (R$)
    
    Retorna:
    --------
    float
        Quantidade ótima de pedido (Q*)
    
    Fórmula:
    --------
    Q* = sqrt(2 * D * K / h)
    """
    if custo_manutencao <= 0:
        raise ValueError("Custo de manutenção deve ser positivo")
    
    Q_star = np.sqrt((2 * demanda_anual * custo_pedido) / custo_manutencao)
    return Q_star


def calcular_custo_total_eoq(demanda_anual: float, Q: float, custo_pedido: float, 
                              custo_manutencao: float, custo_unitario: float) -> float:
    """
    Calcula o custo total anual usando o modelo EOQ.
    
    Parâmetros:
    -----------
    demanda_anual : float
        Demanda anual em unidades
    Q : float
        Quantidade de pedido
    custo_pedido : float
        Custo fixo por pedido (R$)
    custo_manutencao : float
        Custo anual de manutenção por unidade (R$)
    custo_unitario : float
        Custo unitário do item (R$)
    
    Retorna:
    --------
    float
        Custo total anual (R$)
    
    Fórmula:
    --------
    CT = (D/Q)*K + (Q/2)*h + D*c
    """
    custo_pedidos = (demanda_anual / Q) * custo_pedido
    custo_estoque = (Q / 2) * custo_manutencao
    custo_produto = demanda_anual * custo_unitario
    
    custo_total = custo_pedidos + custo_estoque + custo_produto
    return custo_total


def calcular_rop(demanda_media_lead_time: float, z_score: float, 
                 desvio_padrao_lead_time: float) -> float:
    """
    Calcula o Ponto de Reposição (ROP).
    
    Parâmetros:
    -----------
    demanda_media_lead_time : float
        Demanda média durante o lead time
    z_score : float
        Quantil da distribuição normal (ex: 1.645 para 95%)
    desvio_padrao_lead_time : float
        Desvio padrão da demanda durante lead time
    
    Retorna:
    --------
    float
        Ponto de reposição (ROP)
    
    Fórmula:
    --------
    ROP = μ_L + z * σ_L
    """
    ROP = demanda_media_lead_time + z_score * desvio_padrao_lead_time
    return ROP


def calcular_estoque_seguranca(z_score: float, desvio_padrao_lead_time: float) -> float:
    """
    Calcula o Estoque de Segurança.
    
    Parâmetros:
    -----------
    z_score : float
        Quantil da distribuição normal
    desvio_padrao_lead_time : float
        Desvio padrão da demanda durante lead time
    
    Retorna:
    --------
    float
        Estoque de segurança (unidades)
    
    Fórmula:
    --------
    SS = z * σ_L
    """
    SS = z_score * desvio_padrao_lead_time
    return SS


# =====================================================
# FUNÇÕES DE CÁLCULO - ESTATÍSTICAS
# =====================================================

def calcular_z_score(nivel_servico: float) -> float:
    """
    Calcula o z-score correspondente a um nível de serviço.
    
    Parâmetros:
    -----------
    nivel_servico : float
        Nível de serviço desejado (0-1, ex: 0.95 para 95%)
    
    Retorna:
    --------
    float
        Z-score correspondente
    
    Exemplo:
    --------
    >>> calcular_z_score(0.95)
    1.6448536269514722
    """
    if not 0 < nivel_servico < 1:
        raise ValueError("Nível de serviço deve estar entre 0 e 1")
    
    z = norm.ppf(nivel_servico)
    return z


def calcular_desvio_padrao_lead_time(desvio_padrao_demanda: float, lead_time: int) -> float:
    """
    Calcula o desvio padrão da demanda durante o lead time.
    
    Parâmetros:
    -----------
    desvio_padrao_demanda : float
        Desvio padrão da demanda por período
    lead_time : int
        Lead time em períodos
    
    Retorna:
    --------
    float
        Desvio padrão durante lead time
    
    Fórmula:
    --------
    σ_L = σ_d * sqrt(L)
    """
    sigma_L = desvio_padrao_demanda * np.sqrt(lead_time)
    return sigma_L


def calcular_demanda_media_lead_time(demanda_media: float, lead_time: int) -> float:
    """
    Calcula a demanda média durante o lead time.
    
    Parâmetros:
    -----------
    demanda_media : float
        Demanda média por período
    lead_time : int
        Lead time em períodos
    
    Retorna:
    --------
    float
        Demanda média durante lead time
    
    Fórmula:
    --------
    μ_L = μ_d * L
    """
    mu_L = demanda_media * lead_time
    return mu_L


def calcular_estatisticas_demanda(dados_demanda: List[float]) -> Dict[str, float]:
    """
    Calcula estatísticas descritivas da demanda.
    
    Parâmetros:
    -----------
    dados_demanda : List[float]
        Lista de valores de demanda
    
    Retorna:
    --------
    Dict[str, float]
        Dicionário com estatísticas (média, desvio padrão, mín, máx, CV)
    """
    dados = np.array(dados_demanda)
    
    stats = {
        'media': np.mean(dados),
        'desvio_padrao': np.std(dados, ddof=1),
        'minimo': np.min(dados),
        'maximo': np.max(dados),
        'mediana': np.median(dados),
        'q1': np.percentile(dados, 25),
        'q3': np.percentile(dados, 75),
    }
    
    # Coeficiente de Variação
    stats['coeficiente_variacao'] = stats['desvio_padrao'] / stats['media'] if stats['media'] != 0 else 0
    
    return stats


# =====================================================
# FUNÇÕES DE VALIDAÇÃO
# =====================================================

def validar_parametros_eoq(demanda_anual: float, custo_pedido: float, 
                            custo_manutencao: float) -> bool:
    """
    Valida os parâmetros do modelo EOQ.
    
    Parâmetros:
    -----------
    demanda_anual : float
        Demanda anual
    custo_pedido : float
        Custo de pedido
    custo_manutencao : float
        Custo de manutenção
    
    Retorna:
    --------
    bool
        True se todos os parâmetros são válidos
    """
    if demanda_anual <= 0:
        raise ValueError("Demanda anual deve ser positiva")
    if custo_pedido <= 0:
        raise ValueError("Custo de pedido deve ser positivo")
    if custo_manutencao <= 0:
        raise ValueError("Custo de manutenção deve ser positivo")
    
    return True


def validar_nivel_servico(nivel_servico: float) -> bool:
    """
    Valida se o nível de serviço está entre 0 e 1.
    """
    if not 0 < nivel_servico < 1:
        raise ValueError("Nível de serviço deve estar entre 0 e 1")
    return True


# =====================================================
# FUNÇÕES DE PROCESSAMENTO DE DADOS
# =====================================================

def agregar_demanda_semanal(df_vendas: pd.DataFrame, coluna_data: str, 
                             coluna_quantidade: str) -> pd.DataFrame:
    """
    Agrega dados de vendas diárias em demanda semanal.
    
    Parâmetros:
    -----------
    df_vendas : pd.DataFrame
        DataFrame com vendas diárias
    coluna_data : str
        Nome da coluna com datas
    coluna_quantidade : str
        Nome da coluna com quantidades
    
    Retorna:
    --------
    pd.DataFrame
        DataFrame com demanda semanal agregada
    """
    df = df_vendas.copy()
    df[coluna_data] = pd.to_datetime(df[coluna_data])
    
    # Agrupar por semana
    df_semanal = df.set_index(coluna_data).resample('W')[coluna_quantidade].sum()
    
    return df_semanal.reset_index()


def classificacao_abc(df_itens: pd.DataFrame, coluna_valor: str, 
                      limites: Tuple[float, float] = (0.8, 0.95)) -> pd.DataFrame:
    """
    Realiza classificação ABC dos itens.
    
    Parâmetros:
    -----------
    df_itens : pd.DataFrame
        DataFrame com itens e valores
    coluna_valor : str
        Nome da coluna com valores
    limites : Tuple[float, float]
        Limites para classes A e B (padrão: 80% e 95%)
    
    Retorna:
    --------
    pd.DataFrame
        DataFrame com classificação ABC
    """
    df = df_itens.copy()
    
    # Ordenar por valor decrescente
    df = df.sort_values(coluna_valor, ascending=False).reset_index(drop=True)
    
    # Calcular percentual acumulado
    total = df[coluna_valor].sum()
    df['percentual'] = df[coluna_valor] / total
    df['percentual_acumulado'] = df['percentual'].cumsum()
    
    # Classificar
    def classificar(row):
        if row['percentual_acumulado'] <= limites[0]:
            return 'A'
        elif row['percentual_acumulado'] <= limites[1]:
            return 'B'
        else:
            return 'C'
    
    df['classe'] = df.apply(classificar, axis=1)
    
    return df


# =====================================================
# FUNÇÕES DE FORMATAÇÃO
# =====================================================

def formatar_moeda(valor: float, moeda: str = 'R$') -> str:
    """
    Formata um valor como moeda.
    
    Parâmetros:
    -----------
    valor : float
        Valor a formatar
    moeda : str
        Símbolo da moeda
    
    Retorna:
    --------
    str
        Valor formatado
    """
    return f"{moeda} {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')


def formatar_percentual(valor: float, casas_decimais: int = 2) -> str:
    """
    Formata um valor como percentual.
    
    Parâmetros:
    -----------
    valor : float
        Valor entre 0 e 1
    casas_decimais : int
        Número de casas decimais
    
    Retorna:
    --------
    str
        Valor formatado como percentual
    """
    return f"{valor * 100:.{casas_decimais}f}%"


# =====================================================
# FUNÇÕES DE RELATÓRIO
# =====================================================

def gerar_resumo_politica(Q: float, ROP: float, demanda_anual: float, 
                          custo_pedido: float, custo_manutencao: float,
                          custo_unitario: float, nivel_servico: float) -> Dict:
    """
    Gera um resumo completo da política de estoque.
    
    Retorna:
    --------
    Dict
        Dicionário com resumo da política
    """
    custo_total = calcular_custo_total_eoq(demanda_anual, Q, custo_pedido, 
                                           custo_manutencao, custo_unitario)
    
    resumo = {
        'Q (Lote Econômico)': f"{Q:.2f} unidades",
        'ROP (Ponto de Reposição)': f"{ROP:.2f} unidades",
        'Estoque Médio': f"{Q/2:.2f} unidades",
        'Pedidos por Ano': f"{demanda_anual/Q:.2f}",
        'Custo Total Anual': formatar_moeda(custo_total),
        'Nível de Serviço': formatar_percentual(nivel_servico),
    }
    
    return resumo


if __name__ == "__main__":
    # Exemplo de uso
    print("=" * 50)
    print("MÓDULO DE FUNÇÕES AUXILIARES - GESTÃO DE ESTOQUES")
    print("=" * 50)
    
    # Parâmetros de exemplo
    demanda_anual = 3580.72
    custo_pedido = 45.00
    custo_unitario = 25.00
    taxa_manutencao = 0.25
    custo_manutencao = custo_unitario * taxa_manutencao
    
    # Calcular EOQ
    Q_star = calcular_eoq(demanda_anual, custo_pedido, custo_manutencao)
    print(f"\nLote Econômico (Q*): {Q_star:.2f} unidades")
    
    # Calcular custo total
    custo_total = calcular_custo_total_eoq(demanda_anual, Q_star, custo_pedido, 
                                           custo_manutencao, custo_unitario)
    print(f"Custo Total Anual: {formatar_moeda(custo_total)}")
    
    # Calcular ROP
    demanda_media = demanda_anual / 52
    desvio_padrao = 20.06
    lead_time = 1
    
    mu_L = calcular_demanda_media_lead_time(demanda_media, lead_time)
    sigma_L = calcular_desvio_padrao_lead_time(desvio_padrao, lead_time)
    z_score = calcular_z_score(0.95)
    ROP = calcular_rop(mu_L, z_score, sigma_L)
    
    print(f"Ponto de Reposição (ROP): {ROP:.2f} unidades")
    print(f"Estoque de Segurança: {calcular_estoque_seguranca(z_score, sigma_L):.2f} unidades")
    
    print("\n" + "=" * 50)
