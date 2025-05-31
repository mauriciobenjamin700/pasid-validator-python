import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configurações gerais
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 7)

# Criar diretório para salvar gráficos se não existir
output_dir = "analises_desempenho"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Carregar CSV
try:
    # O CSV fornecido já tem cabeçalhos, então não usamos header=None
    df = pd.read_csv('logs_convertidos.csv')
except FileNotFoundError:
    print("Erro: Arquivo 'dados_recebidos.csv' não encontrado.")
    print("Crie um arquivo CSV com os dados ou ajuste o caminho.")
    exit()
except pd.errors.EmptyDataError:
    print("Erro: Arquivo 'dados_recebidos.csv' está vazio.")
    exit()
except Exception as e:
    print(f"Erro ao ler o CSV: {e}")
    exit()

# Renomear colunas para corresponder ao código original
# O CSV tem 'Timestamp 1', 'Timestamp 2', etc., que mapeamos para 'T1', 'T2', etc.
df = df.rename(columns={
    'Timestamp 1': 'T1',
    'Timestamp 2': 'T2',
    'Timestamp 3': 'T3',
    'Timestamp 4': 'T4'
})

# Verificar se todas as colunas esperadas estão presentes
expected_columns = ['Ciclo', 'Fonte', 'ID', 'T1', 'T2', 'T3', 'T4']
if not all(col in df.columns for col in expected_columns):
    print(f"Erro: O CSV deve conter as colunas {expected_columns}. Colunas encontradas: {list(df.columns)}")
    exit()

# Converter colunas de timestamp para numérico, caso não sejam
for col in ['T1', 'T2', 'T3', 'T4']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Remover linhas com timestamps inválidos que não puderam ser convertidos
df.dropna(subset=['T1', 'T2', 'T3', 'T4'], inplace=True)

if df.empty:
    print("DataFrame vazio após limpeza de dados. Verifique o conteúdo do CSV.")
    exit()

# Calcular tempos entre etapas em ms
df['T1->T2'] = (df['T2'] - df['T1']) * 1000
df['T2->T3'] = (df['T3'] - df['T2']) * 1000
df['T3->T4'] = (df['T4'] - df['T3']) * 1000
df['Tempo Total (T1->T4)'] = (df['T4'] - df['T1']) * 1000  # Tempo total

# Extrair nome do load balancer
df['LoadBalancer'] = df['Fonte'].apply(lambda x: str(x).split(':')[0])

print("Pré-processamento concluído. Iniciando análises...")
print("Exemplo de dados processados:")
print(df.head())

# --- ANÁLISE 1: Distribuição de tempos por etapa (por LoadBalancer) ---
print("\n--- ANÁLISE 1: Distribuição de tempos por etapa (por LoadBalancer) ---")

def plot_por_ciclo(ciclo_num, dataframe_local):
    df_ciclo = dataframe_local[dataframe_local['Ciclo'] == ciclo_num]
    if df_ciclo.empty:
        print(f"Nenhum dado encontrado para o Ciclo {ciclo_num} na Análise 1.")
        return

    # Média por LoadBalancer e Etapa
    media = df_ciclo.groupby('LoadBalancer')[['T1->T2', 'T2->T3', 'T3->T4', 'Tempo Total (T1->T4)']].mean().reset_index()
    media = pd.melt(media, id_vars='LoadBalancer', var_name='Etapa', value_name='Tempo Médio (ms)')

    # Gráfico de linha
    plt.figure()
    sns.lineplot(data=media, x='Etapa', y='Tempo Médio (ms)', hue='LoadBalancer', marker='o')
    plt.title(f'Desempenho Médio por Etapa - Ciclo {ciclo_num}')
    plt.ylabel('Tempo Médio (ms)')
    plt.xlabel('Etapa')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'grafico_linha_ciclo{ciclo_num}.png'))
    plt.close()  # Fechar a figura para liberar memória

# Gráficos de linha por ciclo
ciclos_unicos = df['Ciclo'].unique()
if len(ciclos_unicos) > 0:
    for ciclo_iter in ciclos_unicos:
        plot_por_ciclo(ciclo_iter, df)
else:
    print("Nenhum ciclo encontrado para a Análise 1.")

# Gráfico de Comparação entre ciclos (usando o tempo total e etapas)
media_ciclos_df = df.groupby('Ciclo')[['T1->T2', 'T2->T3', 'T3->T4', 'Tempo Total (T1->T4)']].mean().reset_index()
if not media_ciclos_df.empty:
    media_ciclos_melted = pd.melt(media_ciclos_df, id_vars='Ciclo', var_name='Etapa', value_name='Tempo Médio (ms)')

    plt.figure()
    sns.lineplot(data=media_ciclos_melted, x='Etapa', y='Tempo Médio (ms)', hue='Ciclo', marker='o', palette='tab10')
    plt.title('Comparação de Desempenho Médio entre Ciclos')
    plt.ylabel('Tempo Médio (ms)')
    plt.xlabel('Etapa')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'grafico_comparacao_ciclos_etapas.png'))
    plt.close()
else:
    print("Não há dados para gerar o gráfico de comparação entre ciclos.")

# Boxplots para ver a distribuição dos tempos das etapas
etapas_tempo = ['T1->T2', 'T2->T3', 'T3->T4']
for etapa in etapas_tempo:
    if etapa in df.columns:
        plt.figure()
        sns.boxplot(data=df, x='LoadBalancer', y=etapa)
        plt.title(f'Distribuição de Tempos ({etapa}) por LoadBalancer')
        plt.ylabel('Tempo (ms)')
        plt.xlabel('LoadBalancer')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'boxplot_{etapa.replace("->", "_")}_por_lb.png'))
        plt.close()
    else:
        print(f"Coluna {etapa} não encontrada para gerar boxplot.")

# --- ANÁLISE 2: Requisições ao longo do tempo ---
print("\n--- ANÁLISE 2: Requisições ao longo do tempo ---")
if 'T1' in df.columns:
    df['T1_datetime'] = pd.to_datetime(df['T1'], unit='s', errors='coerce')
    df.dropna(subset=['T1_datetime'], inplace=True)

    if not df.empty:
        plt.figure()
        df.set_index('T1_datetime').resample('1s').size().plot()
        plt.title('Frequência de Requisições ao Longo do Tempo (por segundo)')
        plt.xlabel('Tempo (T1)')
        plt.ylabel('Número de Requisições')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'grafico_reqs_ao_longo_do_tempo.png'))
        plt.close()

        # Agrupado por ciclo para ver diferenças de ritmo
        plt.figure()
        for ciclo_iter in ciclos_unicos:
            df_ciclo_tempo = df[df['Ciclo'] == ciclo_iter]
            if not df_ciclo_tempo.empty:
                df_ciclo_tempo.set_index('T1_datetime').resample('1s').size().plot(label=f'Ciclo {ciclo_iter}')
        if any((df['Ciclo'] == ciclo_iter).any() for ciclo_iter in ciclos_unicos):  # Linha corrigida
            plt.title('Frequência de Requisições por Ciclo (por segundo)')
            plt.xlabel('Tempo (T1)')
            plt.ylabel('Número de Requisições')
            plt.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, 'grafico_reqs_ao_longo_do_tempo_por_ciclo.png'))
            plt.close()
        else:
            print("Nenhum dado para plotar frequência de requisições por ciclo.")
    else:
        print("DataFrame vazio após conversão de T1 para datetime.")
else:
    print("Coluna 'T1' não encontrada para Análise 2.")
# --- ANÁLISE 3: Tempo total por LoadBalancer e Ciclo ---
print("\n--- ANÁLISE 3: Tempo total por LoadBalancer e Ciclo ---")
if 'Tempo Total (T1->T4)' in df.columns:
    plt.figure()
    sns.barplot(data=df, x='LoadBalancer', y='Tempo Total (T1->T4)', hue='Ciclo', estimator=pd.Series.mean, errorbar='sd')
    plt.title('Tempo Total Médio por LoadBalancer e Ciclo')
    plt.ylabel('Tempo Total Médio (ms)')
    plt.xlabel('LoadBalancer')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'barplot_tempo_total_lb_ciclo.png'))
    plt.close()

    plt.figure()
    sns.histplot(data=df, x='Tempo Total (T1->T4)', hue='LoadBalancer', multiple="dodge", shrink=.8, kde=True, palette='viridis')
    plt.title('Distribuição do Tempo Total por LoadBalancer')
    plt.xlabel('Tempo Total (ms)')
    plt.ylabel('Contagem')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'hist_tempo_total_por_lb_comparativo.png'))
    plt.close()
else:
    print("Coluna 'Tempo Total (T1->T4)' não encontrada para Análise 3.")

# --- ANÁLISE 4: Heatmap de correlação entre etapas ---
print("\n--- ANÁLISE 4: Heatmap de correlação entre etapas ---")
etapas_para_correlacao_cols = ['T1->T2', 'T2->T3', 'T3->T4']
if all(col in df.columns for col in etapas_para_correlacao_cols):
    etapas_para_correlacao_df = df[etapas_para_correlacao_cols]
    correlation_matrix = etapas_para_correlacao_df.corr()

    plt.figure()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Heatmap de Correlação entre Tempos das Etapas')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'heatmap_correlacao_etapas.png'))
    plt.close()
    print("Matriz de Correlação entre Etapas:")
    print(correlation_matrix)
else:
    print(f"Uma ou mais colunas {etapas_para_correlacao_cols} não encontradas para Análise 4.")

# --- ANÁLISE 5: Quantidade de requisições por LoadBalancer por ciclo ---
print("\n--- ANÁLISE 5: Quantidade de requisições por LoadBalancer por ciclo ---")
if 'Ciclo' in df.columns and 'LoadBalancer' in df.columns:
    reqs_lb_ciclo = df.groupby(['Ciclo', 'LoadBalancer']).size().unstack(fill_value=0)
    if not reqs_lb_ciclo.empty:
        reqs_lb_ciclo.plot(kind='bar', stacked=False)
        plt.title('Quantidade de Requisições por LoadBalancer e Ciclo')
        plt.xlabel('Ciclo')
        plt.ylabel('Número de Requisições')
        plt.xticks(rotation=0)
        plt.legend(title='LoadBalancer')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'barplot_reqs_lb_ciclo.png'))
        plt.close()
        print("Contagem de requisições por Ciclo e LoadBalancer:")
        print(reqs_lb_ciclo)
    else:
        print("Não há dados para Análise 5.")
else:
    print("Colunas 'Ciclo' ou 'LoadBalancer' não encontradas para Análise 5.")

# --- ANÁLISE 6: Diferença de tempo entre LoadBalancers em cada requisição ---
print("\n--- ANÁLISE 6: Diferença de tempo entre LoadBalancers em cada requisição ---")
if all(col in df.columns for col in ['Ciclo', 'ID', 'LoadBalancer', 'Tempo Total (T1->T4)']):
    try:
        df_pivot_lb = df.pivot_table(index=['Ciclo', 'ID'], columns='LoadBalancer', values='Tempo Total (T1->T4)')
        
        lb_names = df['LoadBalancer'].unique()
        if len(lb_names) == 2:
            lb1_name = lb_names[0]
            lb2_name = lb_names[1]
            
            if lb1_name in df_pivot_lb.columns and lb2_name in df_pivot_lb.columns:
                df_pivot_lb_completo = df_pivot_lb.dropna(subset=[lb1_name, lb2_name])

                if not df_pivot_lb_completo.empty:
                    df_pivot_lb_completo[f'Diferenca_Tempo ({lb1_name}-{lb2_name})'] = df_pivot_lb_completo[lb1_name] - df_pivot_lb_completo[lb2_name]

                    plt.figure()
                    sns.histplot(df_pivot_lb_completo[f'Diferenca_Tempo ({lb1_name}-{lb2_name})'], kde=True)
                    plt.title(f'Distribuição da Diferença de Tempo Total entre {lb1_name} e {lb2_name} por Requisição (ID)')
                    plt.xlabel(f'Diferença de Tempo ({lb1_name} - {lb2_name}) (ms)')
                    plt.ylabel('Contagem de Requisições (IDs)')
                    plt.tight_layout()
                    plt.savefig(os.path.join(output_dir, 'hist_diferenca_tempo_lbs_por_id.png'))
                    plt.close()
                    print(f"\nEstatísticas da Diferença de Tempo entre {lb1_name} e {lb2_name} (ms):")
                    print(df_pivot_lb_completo[f'Diferenca_Tempo ({lb1_name}-{lb2_name})'].describe())
                else:
                    print("Análise 6: Não foi possível calcular a diferença de tempo por ID pareado (nenhum ID comum completo ou dados insuficientes).")
            else:
                print(f"Análise 6: Colunas dos LoadBalancers {lb1_name} ou {lb2_name} não encontradas após pivotar.")
        elif len(lb_names) < 2:
            print(f"Análise 6: Menos de dois LoadBalancers ({lb_names}). Não é possível comparar.")
        else:
            print(f"Análise 6: Mais de dois LoadBalancers ({lb_names}). A comparação direta precisa ser ajustada.")
            print("DataFrame Pivotado (tempos por ID e LoadBalancer):")
            print(df_pivot_lb.head())

    except Exception as e:
        print(f"Erro ao tentar pivotar dados para Análise 6: {e}")
else:
    print("Colunas necessárias para Análise 6 não encontradas.")

# --- ANÁLISE 7: Histograma de tempos totais ---
print("\n--- ANÁLISE 7: Histograma de tempos totais ---")
if 'Tempo Total (T1->T4)' in df.columns:
    plt.figure()
    sns.histplot(data=df, x='Tempo Total (T1->T4)', hue='LoadBalancer', kde=True, multiple='stack')
    plt.title('Histograma de Tempos Totais por LoadBalancer')
    plt.xlabel('Tempo Total (ms)')
    plt.ylabel('Contagem')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'hist_tempo_total_geral_por_lb.png'))
    plt.close()
else:
    print("Coluna 'Tempo Total (T1->T4)' não encontrada para Análise 7.")

# --- ANÁLISE 8: Ranking de tempos totais por requisição ---
print("\n--- ANÁLISE 8: Ranking de tempos totais por requisição ---")
if 'Tempo Total (T1->T4)' in df.columns:
    df_sorted_fastest = df.sort_values('Tempo Total (T1->T4)').head()
    df_sorted_slowest = df.sort_values('Tempo Total (T1->T4)').tail()

    print("Requisições MAIS RÁPIDAS (Top 5):")
    print(df_sorted_fastest[['Ciclo', 'LoadBalancer', 'ID', 'Tempo Total (T1->T4)']])

    print("\nRequisições MAIS LENTAS (Top 5):")
    print(df_sorted_slowest[['Ciclo', 'LoadBalancer', 'ID', 'Tempo Total (T1->T4)']])
else:
    print("Coluna 'Tempo Total (T1->T4)' não encontrada para Análise 8.")

# --- ANÁLISE 9: Diferença de desempenho entre as iterações (ID) ---
print("\n--- ANÁLISE 9: Diferença de desempenho entre as iterações (ID) ---")
if all(col in df.columns for col in ['ID', 'Tempo Total (T1->T4)', 'LoadBalancer']):
    plt.figure(figsize=(15,7))
    try:
        if pd.api.types.is_numeric_dtype(df['ID']):
            sns.lineplot(data=df, x='ID', y='Tempo Total (T1->T4)', hue='LoadBalancer', marker='o', errorbar='sd')
            plt.title('Desempenho (Tempo Total) por ID da Requisição')
        else:
            df_sorted_id = df.copy()
            df_sorted_id['ID_str'] = df_sorted_id['ID'].astype(str)
            df_sorted_id = df_sorted_id.sort_values('ID_str')
            sns.lineplot(data=df_sorted_id, x='ID_str', y='Tempo Total (T1->T4)', hue='LoadBalancer', marker='.', errorbar='sd')
            plt.xlabel('ID da Requisição (como string)')
            plt.title('Desempenho (Tempo Total) por ID da Requisição (Tratado como Categórico)')
            plt.xticks(rotation=45, ha='right')
            
        plt.ylabel('Tempo Total (ms)')
        plt.legend(title='LoadBalancer')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'lineplot_tempo_total_por_id.png'))
        plt.close()
    except Exception as e:
        print(f"Não foi possível gerar o gráfico de linha por ID para Análise 9: {e}")
else:
    print("Colunas necessárias para Análise 9 não encontradas.")

print(f"\nTodas as análises foram concluídas. Gráficos salvos em: {os.path.abspath(output_dir)}")