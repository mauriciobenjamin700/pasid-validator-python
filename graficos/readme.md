# Análise de Desempenho de Load Balancers

Explicaremos os gráficos gerados pelo código Python que processa o arquivo `logs_convertidos.csv`.

## Introdução

Este script executa nove análises e gera diversos gráficos salvos na pasta `analises_desempenho`. Cada gráfico visa visualizar diferentes aspectos do desempenho dos load balancers (`loadbalance1` e `loadbalance2`) ao longo de três ciclos: 0, 1 e 2.

### Referência de Timestamps

As transições entre os componentes do sistema são representadas pelas diferenças entre os timestamps:

- **T1 → T2**: Envio do Source para o LoadBalancer
- **T2 → T3**: Envio do LoadBalancer para o Service
- **T3 → T4**: Processamento e resposta do Service
- **T4 → T1**: Retorno do Service para o Source

Onde:

- **T1**: Source
- **T2**: LoadBalancer
- **T3**: Service
- **T4**: Retorno do Service para o Source

---

## Análise 1: Distribuição de Tempos por Etapa (por LoadBalancer)

### 1. Tempo Médio de Resposta vs Taxa de Chegada por CFC (`mrt_por_cfc.png`)

- **Descrição**: Um gráfico de linha que compara o tempo médio de resposta em função da taxa de chegada para diferentes valores de CFC (Credit Flow Control), uma métrica que regula o fluxo de dados no sistema.
- **Eixos**:
  - **X**: Taxa de Chegada (pacotes/segundo), variando de 200 a 1000 pacotes/s.
  - **Y**: Tempo Médio de Resposta (segundos), variando de aproximadamente 2.0 a 2.4 segundos.
- **Detalhes**:
  - Cada linha representa um valor de CFC: 0 (azul), 1 (verde), e 2 (vermelho).
  - Para CFC = 0, o tempo médio de resposta é o mais alto, começando em ~2.25 segundos e aumentando para ~2.4 segundos à medida que a taxa de chegada cresce, indicando menor eficiência sob alta carga, o que pode ser correlacionado ao desempenho do Ciclo 0.
  - Para CFC = 1, o tempo médio de resposta é intermediário, começando em ~2.1 segundos e subindo gradualmente para ~2.15 segundos, refletindo um desempenho mediano, semelhante ao observado no Ciclo 1.
  - Para CFC = 2, o tempo médio de resposta é o mais baixo e mais estável, começando em 2.0 segundos e caindo ligeiramente para ~1.95 segundos, indicando o melhor desempenho mesmo com taxas de chegada mais altas, alinhado com o Ciclo 2.
- **Objetivo**: Avaliar como diferentes configurações de CFC impactam o tempo médio de resposta sob várias taxas de chegada, sugerindo que um valor mais alto de CFC (como 2) otimiza o desempenho dos load balancers, especialmente em cenários de alta demanda.
- ![mrt_por_cfc.png](/graficos/analises_desempenho/mrt_por_cfc.png)

### 2. Gráficos de Linha por Ciclo (`grafico_linha_ciclo{ciclo}.png`)

- **Descrição**: Um gráfico de linha é gerado para cada ciclo (0, 1, 2), totalizando três arquivos: `grafico_linha_ciclo0.png`, `grafico_linha_ciclo1.png`, e `grafico_linha_ciclo2.png`.
- **Eixos**:
  - **X**: Etapas (`T1->T2`, `T2->T3`, `T3->T4`, `Tempo Total (T1->T4)`).
  - **Y**: Tempo médio (ms) para cada etapa.
- **Detalhes**:
  - Cada linha representa um load balancer (`loadbalance1` ou `loadbalance2`).
  - Há marcadores (pontos) em cada etapa para destacar os valores médios.
  - No Ciclo 0, os tempos médios totais são os mais longos (cerca de 3000 ms), refletindo o pior desempenho, com `T3->T4` dominando o tempo (aproximadamente 2980 ms), enquanto `T1->T2` e `T2->T3` são rápidos (1–3 ms).
  - No Ciclo 1, os tempos totais médios são intermediários (cerca de 1500 ms), com `T3->T4` contribuindo com cerca de 1480 ms, indicando um desempenho mediano.
  - No Ciclo 2, os tempos totais médios são os menores (cerca de 1000 ms), com `T3->T4` em torno de 980 ms, destacando o melhor desempenho.
- **Objetivo**: Comparar o desempenho médio das etapas entre os load balancers em cada ciclo.
- ![grafico_linha_ciclo0.png](/graficos/analises_desempenho/grafico_linha_ciclo0.png)
- ![grafico_linha_ciclo1.png](/graficos/analises_desempenho/grafico_linha_ciclo1.png)
- ![grafico_linha_ciclo2.png](/graficos/analises_desempenho/grafico_linha_ciclo2.png)

### 3. Gráfico de Comparação entre Ciclos (`grafico_comparacao_ciclos_etapas.png`)

- **Descrição**: Um gráfico de linha comparando os tempos médios das etapas entre os ciclos.
- **Eixos**:
  - **X**: Etapas (`T1->T2`, `T2->T3`, `T3->T4`, `Tempo Total (T1->T4)`).
  - **Y**: Tempo médio (ms).
- **Detalhes**:
  - Cada linha representa um ciclo (0, 1, 2), com cores diferentes.
  - O Ciclo 0 apresenta o maior tempo total médio (cerca de 3000 ms), refletindo o pior desempenho.
  - O Ciclo 1 mostra um tempo total médio intermediário (cerca de 1500 ms), indicando um desempenho mediano.
  - O Ciclo 2 exibe o menor tempo total médio (cerca de 1000 ms), destacando o melhor desempenho.
  - As etapas `T1->T2` e `T2->T3` permanecem consistentes e rápidas (1–3 ms) em todos os ciclos, com a diferença principal no processamento `T3->T4`.
- **Objetivo**: Mostrar como o desempenho varia entre os ciclos, com o Ciclo 2 como o mais eficiente, seguido pelo Ciclo 1 e pelo Ciclo 0 como o menos eficiente.
- ![grafico_comparacao_ciclos_etapas.png](/graficos/analises_desempenho/grafico_comparacao_ciclos_etapas.png)

---

## Considerações Finais

Os gráficos gerados fornecem uma visão detalhada do desempenho dos load balancers em diferentes ciclos e configurações de CFC. O Ciclo 2 demonstra o melhor desempenho geral (tempo total médio ~1000 ms), enquanto o Ciclo 0 apresenta o pior (tempo total médio ~3000 ms), e o Ciclo 1 fica em uma posição intermediária (tempo total médio ~1500 ms). Além disso, o uso de CFC = 2 melhora significativamente a resposta do sistema sob altas taxas de chegada, sugerindo que ajustes nesse parâmetro podem ser benéficos para otimizar o desempenho. Esta análise reflete os dados processados até 10:14 PM -03, segunda-feira, 02/06/2025.
