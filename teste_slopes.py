import pandas as pd
import numpy as np

def enriquecer_relatorio_cambio(df):
    """
    Recebe um DataFrame com o histórico de operações.
    Colunas esperadas: ['data', 'volume_compra', 'volume_venda']
    """
    # 1. Preparação e Ordenação
    df['data'] = pd.to_datetime(df['data'])
    df = df.sort_values('data').reset_index(drop=True)
    
    df['ano'] = df['data'].dt.year
    df['mes'] = df['data'].dt.month
    
    # 2. Métricas Diárias e Proporções
    df['volume_total'] = df['volume_compra'] + df['volume_venda']
    # Evita divisão por zero caso não haja vendas no dia
    df['razao_compra_venda'] = df['volume_compra'] / df['volume_venda'].replace(0, np.nan)
    
    # 3. Métricas de Acumulado (MTD e YTD)
    df['mtd_total'] = df.groupby(['ano', 'mes'])['volume_total'].cumsum()
    df['ytd_total'] = df.groupby('ano')['volume_total'].cumsum()
    
    # 4. Médias Móveis (Tendência de curto prazo - 7 dias)
    df['mm_7d_total'] = df['volume_total'].rolling(window=7, min_periods=1).mean()
    
    return df

def calcular_coeficiente_tendencia(df):
    """
    Calcula o coeficiente angular (inclinação da reta) do YTD para cada ano.
    Mede a 'velocidade' ou aceleração do volume acumulado.
    """
    tendencias = {}
    
    for ano, grupo in df.groupby('ano'):
        # Eixo X: Dias transcorridos no ano
        x = np.arange(len(grupo))
        # Eixo Y: Volume acumulado no ano
        y = grupo['ytd_total'].values
        
        # Só calcula se houver mais de um dia de dado no ano
        if len(x) > 1:
            # np.polyfit(x, y, 1) retorna [coef_angular, intercepto] da reta de grau 1
            coef_angular, intercepto = np.polyfit(x, y, 1)
            tendencias[ano] = coef_angular
        else:
            tendencias[ano] = None
            
    return tendencias

# --- Exemplo de Uso ---
# Supondo que você carregou seus dados via pd.read_excel('seu_relatorio.xlsx')
# df_cambio = enriquecer_relatorio_cambio(seu_dataframe)
# tendencias_anuais = calcular_coeficiente_tendencia(df_cambio)
# print(tendencias_anuais) 
# Saída esperada: {2025: 150000.5, 2026: 185000.2} -> Indica que 2026 está acelerando mais rápido.


import pandas as pd
import numpy as np

def comparar_tendencia_ytd(df, data_referencia):
    """
    Compara o coeficiente angular do volume acumulado (YTD) do ano atual
    até a data de referência com o mesmo período do ano anterior.
    
    Colunas esperadas em df: ['data', 'ytd_total']
    data_referencia: string 'AAAA-MM-DD' ou objeto datetime
    """
    # 1. Converter e extrair os períodos de controlo
    df['data'] = pd.to_datetime(df['data'])
    data_ref = pd.to_datetime(data_referencia)
    
    ano_atual = data_ref.year
    ano_anterior = ano_atual - 1
    
    # Criar uma máscara de mês-dia (MM-DD) para fazer o corte simétrico
    df['mes_dia'] = df['data'].dt.strftime('%m-%d')
    limite_mes_dia = data_ref.strftime('%m-%d')
    
    # 2. Filtrar os dados para o intervalo correspondente em cada ano
    dados_atual = df[
        (df['data'].dt.year == ano_atual) & 
        (df['mes_dia'] <= limite_mes_dia)
    ].sort_values('data')
    
    dados_anterior = df[
        (df['data'].dt.year == ano_anterior) & 
        (df['mes_dia'] <= limite_mes_dia)
    ].sort_values('data')
    
    # Auxiliar para calcular o coeficiente angular
    def calcular_slope(sub_df):
        if len(sub_df) > 1:
            x = np.arange(len(sub_df))  # Dias corridos no período filtrado
            y = sub_df['ytd_total'].values
            coef_angular, _ = np.polyfit(x, y, 1)
            return coef_angular
        return None

    # 3. Calcular os coeficientes
    slope_atual = calcular_slope(dados_atual)
    slope_anterior = calcular_slope(dados_anterior)
    
    # 4. Estruturar o resultado da comparação
    resultado = {
        "periodo_ano_anterior": f"{ano_anterior}-01-01 até {ano_anterior}-{limite_mes_dia}",
        "coeficiente_ano_anterior": slope_anterior,
        "periodo_ano_atual": f"{ano_atual}-01-01 até {data_ref.strftime('%Y-%m-%d')}",
        "coeficiente_ano_atual": slope_atual,
        "aceleracao_vendas": "Maior" if (slope_atual and slope_anterior and slope_atual > slope_anterior) else "Menor ou Igual"
    }
    
    return resultado

# --- Exemplo de Teste e Uso ---
if __name__ == "__main__":
    # Criar um intervalo de datas fictício para teste (2025 e 2026)
    datas = pd.date_range(start="2025-01-01", end="2026-06-01", freq="D")
    
    # Criar volumes aleatórios simulando crescimento
    np.random.seed(42)
    volumes = np.random.randint(10000, 50000, size=len(datas))
    
    df_teste = pd.DataFrame({"data": datas, "volume_total": volumes})
    df_teste['ano'] = df_teste['data'].dt.year
    
    # Calcular o YTD acumulado por ano (essencial antes de rodar a função)
    df_teste['ytd_total'] = df_teste.groupby('ano')['volume_total'].cumsum()
    
    # Executar a comparação com a data pretendida
    data_alvo = "2026-05-29"
    relatorio_tendencia = comparar_tendencia_ytd(df_teste, data_referencia=data_alvo)
    
    # Mostrar resultados formatados
    print(f"Análise de Tendência YTD (Referência: {data_alvo})")
    print(f"Período Anterior: {relatorio_tendencia['periodo_ano_anterior']}")
    print(f"Coeficiente Angular 2025: {relatorio_tendencia['coeficiente_ano_anterior']:.2f}")
    print("-" * 50)
    print(f"Período Atual: {relatorio_tendencia['periodo_ano_atual']}")
    print(f"Coeficiente Angular 2026: {relatorio_tendencia['coeficiente_ano_atual']:.2f}")
    print("-" * 50)
    print(f"A taxa de crescimento em 2026 está: {relatorio_tendencia['aceleracao_vendas']}")
