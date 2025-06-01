# Análise de Desempenho de Load Balancers

Explicaremos os gráficos gerados pelo código Python que processa o arquivo `logs_convertidos.csv`.

Claro! Aqui está uma versão mais organizada e clara da sua introdução:

---

## Introdução

Este script executa nove análises e gera diversos gráficos salvos na pasta `analises_desempenho`. Cada gráfico visa visualizar diferentes aspectos do desempenho dos load balancers (`loadbalance1` e `loadbalance2`) ao longo de três ciclos: 0, 1 e 2.

### Referência de Timestamps

As transições entre os componentes do sistema são representadas pelas diferenças entre os timestamps:

* **T1 → T2**: Envio do Source para o LoadBalancer
* **T2 → T3**: Envio do LoadBalancer para o Service
* **T3 → T4**: Processamento e resposta do Service
* **T4 → T1**: Retorno do Service para o Source

Onde:

* **T1**: Source
* **T2**: LoadBalancer
* **T3**: Service
* **T4**: Retorno do Service para o Source

---

## Análise 1: Distribuição de Tempos por Etapa (por LoadBalancer)

### 1. Gráficos de Linha por Ciclo (`grafico_linha_ciclo{ciclo}.png`)

- **Descrição**: Um gráfico de linha é gerado para cada ciclo (0, 1, 2), totalizando três arquivos: `grafico_linha_ciclo0.png`, `grafico_linha_ciclo1.png`, e `grafico_linha_ciclo2.png`.
- **Eixos**:
  - **X**: Etapas (`T1->T2`, `T2->T3`, `T3->T4`, `Tempo Total (T1->T4)`).
  - **Y**: Tempo médio (ms) para cada etapa.
- **Detalhes**:
  - Cada linha representa um load balancer (`loadbalance1` ou `loadbalance2`).
  - Há marcadores (pontos) em cada etapa para destacar os valores médios.
  - No Ciclo 0, por exemplo, há 10 requisições (5 por load balancer). O gráfico mostra que os tempos médios de `T3->T4` (etapa de resposta) são os mais longos (cerca de 3800 ms), enquanto `T1->T2` e `T2->T3` são muito rápidos (1–3 ms).
  - No Ciclo 2, observe que `loadbalance1` e `loadbalance2` têm picos de tempo total (devido a requisições com IDs 9 e 10, que atingem 33 segundos por atrasos no backend).
- **Objetivo**: Comparar o desempenho médio das etapas entre os load balancers em cada ciclo.

- ![grafico_linha_ciclo0.png](/graficos/analises_desempenho/grafico_linha_ciclo0.png).
- ![grafico_linha_ciclo1.png](/graficos/analises_desempenho/grafico_linha_ciclo1.png).
- ![grafico_linha_ciclo2.png](/graficos/analises_desempenho/grafico_linha_ciclo2.png).


### 2. Gráfico de Comparação entre Ciclos (`grafico_comparacao_ciclos_etapas.png`)

- **Descrição**: Um gráfico de linha comparando os tempos médios das etapas entre os ciclos.
- **Eixos**:
  - **X**: Etapas (`T1->T2`, `T2->T3`, `T3->T4`, `Tempo Total (T1->T4)`).
  - **Y**: Tempo médio (ms).
- **Detalhes**:
  - Cada linha representa um ciclo (0, 1, 2), com cores diferentes.
  - O Ciclo 2 tem tempos totais médios muito maiores (por causa das requisições com IDs 9 e 10, que chegam a 33 segundos).
  - Nos Ciclos 0 e 1, os tempos totais médios estão na faixa de 3800–4000 ms, enquanto no Ciclo 2 sobem para cerca de 8000 ms.
- **Objetivo**: Mostrar como o desempenho varia entre os ciclos, destacando que o Ciclo 2 teve um desempenho significativamente pior.
- ![grafico_comparacao_ciclos_etapas.png](/graficos/analises_desempenho/grafico_comparacao_ciclos_etapas.png).

### 3. Boxplots por Etapa (`boxplot_T1_T2_por_lb.png`, `boxplot_T2_T3_por_lb.png`, `boxplot_T3_T4_por_lb.png`)

- **Descrição**: Três boxplots, um para cada etapa (`T1->T2`, `T2->T3`, `T3->T4`), comparando a distribuição dos tempos entre os load balancers.
- **Eixos**:
  - **X**: LoadBalancer (`loadbalance1`, `loadbalance2`).
  - **Y**: Tempo (ms) da etapa correspondente.
- **Detalhes**:
  - Para `T1->T2` e `T2->T3`, os boxplots mostram tempos muito baixos (mediana em torno de 1–2 ms), com pouca variação e sem outliers significativos.
  - Para `T3->T4`, há maior dispersão, com tempos variando de 3000 a 8000 ms, e outliers no Ciclo 2 (33 segundos para IDs 9 e 10).
  - Não há diferença significativa entre `loadbalance1` e `loadbalance2` na maioria das etapas.
- **Objetivo**: Visualizar a dispersão e identificar outliers nos tempos de cada etapa por load balancer.
- ![boxplot_T1_T2_por_lb.png](/graficos/analises_desempenho/boxplot_T1_T2_por_lb.png).
- ![boxplot_T2_T3_por_lb.png](/graficos/analises_desempenho/boxplot_T2_T3_por_lb.png).
- ![boxplot_T3_T4_por_lb.png](/graficos/analises_desempenho/boxplot_T3_T4_por_lb.png).

## Análise 2: Requisições ao Longo do Tempo

### 4. Frequência de Requisições ao Longo do Tempo (`grafico_reqs_ao_longo_do_tempo.png`)

- **Descrição**: Um gráfico de linha mostrando a frequência de requisições por segundo, com base no timestamp `T1`.
- **Eixos**:
  - **X**: Tempo (convertido de `T1` para datetime, cobrindo o intervalo dos dados).
  - **Y**: Número de requisições por segundo.
- **Detalhes**:
  - O intervalo de tempo no CSV vai de `1748720829` a `1748720896` (cerca de 67 segundos).
  - Há picos de 1–2 requisições por segundo, já que as requisições estão espaçadas aproximadamente a cada segundo dentro de cada ciclo.
  - Nos primeiros 10 segundos (Ciclo 0), há 10 requisições, seguidas por 10 no Ciclo 1 (próximos 10 segundos), e 10 no Ciclo 2 (últimos 10 segundos), com algumas pequenas pausas entre os ciclos.
- **Objetivo**: Mostrar a taxa de chegada das requisições ao longo do tempo.
- ![grafico_reqs_ao_longo_do_tempo.png](/graficos/analises_desempenho/grafico_reqs_ao_longo_do_tempo.png).

### 5. Frequência de Requisições por Ciclo (`grafico_reqs_ao_longo_do_tempo_por_ciclo.png`)

- **Descrição**: Um gráfico de linha com uma curva para cada ciclo, mostrando a frequência de requisições por segundo.
- **Eixos**:
  - **X**: Tempo (datetime).
  - **Y**: Número de requisições por segundo.
- **Detalhes**:
  - Cada ciclo (0, 1, 2) tem sua própria linha.
  - O Ciclo 0 (primeiros 10 segundos) e o Ciclo 1 (10–20 segundos) mostram um padrão constante de 1 requisição por segundo.
  - O Ciclo 2 (últimos 10 segundos) também segue esse padrão, mas há uma pequena pausa entre os ciclos.
- **Objetivo**: Comparar a taxa de requisições entre os ciclos, destacando eventuais diferenças no ritmo.
- ![grafico_reqs_ao_longo_do_tempo_por_ciclo.png](/graficos/analises_desempenho/grafico_reqs_ao_longo_do_tempo_por_ciclo.png).

## Análise 3: Tempo Total por LoadBalancer e Ciclo

### 6. Tempo Total Médio por LoadBalancer e Ciclo (`barplot_tempo_total_lb_ciclo.png`)

- **Descrição**: Um gráfico de barras mostrando o tempo total médio (`T1->T4`) por load balancer, com barras separadas por ciclo.
- **Eixos**:
  - **X**: LoadBalancer (`loadbalance1`, `loadbalance2`).
  - **Y**: Tempo total médio (ms).
- **Detalhes**:
  - Cada load balancer tem três barras (uma para cada ciclo: 0, 1, 2).
  - Nos Ciclos 0 e 1, os tempos médios são semelhantes (cerca de 3800–4000 ms para ambos os load balancers).
  - No Ciclo 2, o tempo médio aumenta drasticamente (para cerca de 8000 ms), devido às requisições com IDs 9 e 10 (33 segundos).
  - As barras têm linhas de erro (desvio padrão), mostrando maior variabilidade no Ciclo 2.
- **Objetivo**: Comparar o desempenho médio entre os load balancers e ciclos, destacando o impacto do Ciclo 2.
- ![barplot_tempo_lb_ciclo.png](/graficos/analises_desempenho/barplot_tempo_total_lb_ciclo.png).

### 7. Distribuição do Tempo Total por LoadBalancer (`hist_tempo_total_por_lb_comparativo.png`)

- **Descrição**: Um histograma comparativo dos tempos totais, com curvas de densidade (KDE) sobrepostas.
- **Eixos**:
  - **X**: Tempo total (ms).
  - **Y**: Contagem de requisições.
- **Detalhes**:
  - Cada load balancer (`loadbalance1`, `loadbalance2`) tem uma distribuição com cores diferentes.
  - A maioria das requisições tem tempos totais entre 3000 e 5000 ms.
  - Há um pequeno pico em torno de 33.000 ms (33 segundos) para ambos os load balancers, correspondente às requisições do Ciclo 2 (IDs 9 e 10).
  - As curvas de densidade mostram que os tempos são semelhantes entre os load balancers.
- **Objetivo**: Mostrar a distribuição dos tempos totais e identificar valores atípicos (outliers).
- ![hist_tempo_total_por_lb_comparativo.png](/graficos/analises_desempenho/hist_tempo_total_por_lb_comparativo.png).

## Análise 4: Heatmap de Correlação entre Etapas

### 8. Heatmap de Correlação (`heatmap_correlacao_etapas.png`)

- **Descrição**: Um mapa de calor (heatmap) mostrando a correlação entre os tempos das etapas (`T1->T2`, `T2->T3`, `T3->T4`).
- **Eixos**:
  - **X e Y**: Etapas (`T1->T2`, `T2->T3`, `T3->T4`).
  - **Valores**: Coeficientes de correlação (de -1 a 1), com cores variando de azul (negativa) a vermelho (positiva).
- **Detalhes**:
  - Como `T1->T2` e `T2->T3` são muito rápidos e consistentes (1–3 ms), a correlação entre eles é baixa.
  - `T3->T4` varia muito (3000–33.000 ms), mas também não apresenta forte correlação com as etapas anteriores, já que os tempos são dominados por fatores externos (como o backend).
  - Os valores de correlação provavelmente estão próximos de 0, indicando pouca relação linear entre as etapas.
- **Objetivo**: Identificar se há dependências lineares entre os tempos das etapas (neste caso, parece não haver).
- ![heatmap_correlacao_etapas.png](/graficos/analises_desempenho/heatmap_correlacao_etapas.png).

## Análise 5: Quantidade de Requisições por LoadBalancer por Ciclo

### 9. Quantidade de Requisições (`barplot_reqs_lb_ciclo.png`)

- **Descrição**: Um gráfico de barras mostrando o número de requisições por load balancer em cada ciclo.
- **Eixos**:
  - **X**: Ciclo (0, 1, 2).
  - **Y**: Número de requisições.
- **Detalhes**:
  - Cada ciclo tem duas barras: uma para `loadbalance1` e outra para `loadbalance2`.
  - Ciclo 0: 5 requisições por load balancer (total 10).
  - Ciclo 1: 5 requisições por load balancer (total 10).
  - Ciclo 2: 5 requisições por load balancer (total 10).
  - As barras têm alturas iguais, indicando que a carga foi distribuída uniformemente entre os load balancers.
- **Objetivo**: Verificar se há desequilíbrio na distribuição de requisições entre os load balancers (neste caso, a distribuição é equilibrada).
- ![barplot_reqs_lb_ciclo.png](/graficos/analises_desempenho/barplot_reqs_lb_ciclo.png).

## Análise 6: Diferença de Tempo entre LoadBalancers em Cada Requisição

### 10. Histograma de Diferenças de Tempo (`hist_diferenca_tempo_lbs_por_id.png`)

- **Descrição**: Um histograma da diferença de tempo total (`loadbalance1 - loadbalance2`) para requisições com o mesmo `Ciclo` e `ID`. **Nota**: Este gráfico pode não ser gerado, pois os IDs não são consistentemente pareados entre os load balancers no CSV.
- **Eixos**:
  - **X**: Diferença de tempo (ms).
  - **Y**: Contagem de requisições (IDs).
- **Detalhes**:
  - No CSV, os IDs (1 a 10) não aparecem consistentemente para ambos os load balancers no mesmo ciclo. Por exemplo, no Ciclo 0, o ID 1 está em `loadbalance1`, mas não em `loadbalance2`.
  - O código verifica isso com `df_pivot_lb.dropna()` e, como não há IDs pareados completos, o gráfico não é gerado, e uma mensagem é exibida: *"Análise 6: Não foi possível calcular a diferença de tempo por ID pareado (nenhum ID comum completo ou dados insuficientes)."*
- **Objetivo**: Comparar o desempenho entre os load balancers para a mesma requisição (ID). Como os dados não permitem isso, a análise não é aplicável.
- ![hist_diferenca_tempo_lbs_por_id.png](/graficos/analises_desempenho/hist_diferenca_tempo_lbs_por_id.png).

## Análise 7: Histograma de Tempos Totais

### 11. Histograma de Tempos Totais (`hist_tempo_total_geral_por_lb.png`)

- **Descrição**: Um histograma empilhado dos tempos totais por load balancer, com curvas de densidade.
- **Eixos**:
  - **X**: Tempo total (ms).
  - **Y**: Contagem de requisições.
- **Detalhes**:
  - Similar ao histograma da Análise 3, mas com um estilo empilhado.
  - A maioria das requisições tem tempos entre 3000 e 5000 ms.
  - Há um pequeno pico em 33.000 ms (IDs 9 e 10 do Ciclo 2).
  - As distribuições de `loadbalance1` e `loadbalance2` são quase idênticas.
- **Objetivo**: Visualizar a distribuição geral dos tempos totais, destacando semelhanças entre os load balancers.
- ![hist_tempo_total_geral_por_lb.png](/graficos/analises_desempenho/hist_tempo_total_geral_por_lb.png).

## Análise 9: Diferença de Desempenho entre as Iterações (ID)

### 12. Desempenho por ID (`lineplot_tempo_total_por_id.png`)

- **Descrição**: Um gráfico de linha mostrando o tempo total por ID, com linhas separadas para cada load balancer.
- **Eixos**:
  - **X**: ID da requisição (1 a 10).
  - **Y**: Tempo total (ms).
- **Detalhes**:
  - Cada load balancer tem uma linha com marcadores.
  - Para a maioria dos IDs, os tempos estão entre 3000 e 5000 ms.
  - No Ciclo 2, os IDs 9 e 10 (para ambos os load balancers) disparam para 33.000 ms, criando picos visíveis.
  - O gráfico mostra que os tempos são consistentes dentro de cada ciclo, exceto pelos outliers no Ciclo 2.
- **Objetivo**: Analisar como o desempenho varia entre as requisições (IDs) e identificar padrões ou anomalias.
- ![lineplot_tempo_total_id.png](/graficos/analises_desempenho/lineplot_tempo_total_por_id.png).
## Resumo e Observações

### Padrões Gerais

- Os tempos das etapas `T1->T2` e `T2->T3` são muito baixos (1–3 ms), indicando que o processamento inicial é rápido.
- A etapa `T3->T4` domina o tempo total (3000–33.000 ms), sugerindo que o bottleneck está no backend ou na resposta do servidor.
- O Ciclo 2 tem desempenho significativamente pior devido a duas requisições (IDs 9 e 10) com tempos de 33 segundos.
- Não há diferença significativa entre `loadbalance1` e `loadbalance2` na maioria das métricas, indicando balanceamento adequado.

### Limitações

- A **Análise 6** não produz resultados úteis porque os IDs não estão pareados entre os load balancers.
- Alguns gráficos (como os histogramas) têm poucos dados (30 requisições), o que pode limitar a visualização de padrões.

Se você precisar de uma explicação mais detalhada sobre um gráfico específico ou quiser ajustar alguma análise (por exemplo, criar um gráfico diferente ou focar em um ciclo), posso ajudar!

## Análise dos Gráficos Fornecidos

Vou explicar cada um dos gráficos fornecidos com base em sua aparência e contexto. Os gráficos parecem ser parte de uma análise de desempenho de dois load balancers (`loadbalance1` e `loadbalance2`) ao longo de diferentes ciclos e etapas de processamento, com tempos medidos em milissegundos (ms) e timestamps em segundos.

### 1. Distribuição do Tempo Total por LoadBalancer

- **Descrição**: Um histograma empilhado que mostra a distribuição dos tempos totais (`T1->T4`) para cada load balancer.
- **Eixos**:
  - **X**: Tempo Total (ms), variando de 0 a 35.000 ms.
  - **Y**: Contagem de requisições.
- **Detalhes**:
  - A maioria das requisições (cerca de 8 para `loadbalance1` e 5 para `loadbalance2`) tem tempos totais entre 0 e 5000 ms.
  - Há um pico significativo em torno de 3500–4000 ms, indicando que esse é o tempo típico para a maioria das requisições.
  - Um outlier aparece em `loadbalance1` com cerca de 8 requisições atingindo aproximadamente 33.000 ms (33 segundos), sugerindo um atraso excepcional em algumas requisições.
  - `loadbalance2` não mostra esse outlier extremo, mas tem uma distribuição semelhante na faixa de 0–5000 ms.
- **Interpretação**: O desempenho geral é consistente entre os load balancers, mas `loadbalance1` experimentou algumas requisições com atrasos muito longos, possivelmente devido a problemas no backend.

### 2. Histograma de Tempos Totais por LoadBalancer

- **Descrição**: Um histograma empilhado com curvas de densidade, comparando os tempos totais de `loadbalance1` e `loadbalance2`.
- **Eixos**:
  - **X**: Tempo Total (ms), variando de 0 a 35.000 ms.
  - **Y**: Contagem de requisições.
- **Detalhes**:
  - Similar ao primeiro gráfico, com um pico entre 0 e 5000 ms (cerca de 6–12 requisições para `loadbalance1` e 4–6 para `loadbalance2`).
  - O outlier em `loadbalance1` aparece novamente em torno de 33.000 ms, com cerca de 2 requisições.
  - `loadbalance2` tem uma distribuição mais uniforme, com menos incidência de tempos extremos.
- **Interpretação**: Confirma a presença de outliers em `loadbalance1`, sugerindo que esse load balancer pode estar mais suscetível a atrasos ocasionais.

### 3. Desempenho (Tempo Total) por ID da Requisição

- **Descrição**: Um gráfico de dispersão com intervalos de confiança, mostrando o tempo total por ID de requisição para cada load balancer.
- **Eixos**:
  - **X**: ID da requisição (1 a 10).
  - **Y**: Tempo Total (ms), variando de 0 a 30.000 ms.
- **Detalhes**:
  - Os IDs 1 a 8 têm tempos totais consistentes entre 4000 e 6000 ms para ambos os load balancers, com sobreposição nos intervalos de confiança.
  - Nos IDs 9 e 10, há um salto drástico para cerca de 15.000–25.000 ms, com `loadbalance1` atingindo o pico mais alto (próximo de 25.000 ms) e `loadbalance2` um pouco abaixo (cerca de 15.000 ms).
- **Interpretação**: As requisições com IDs 9 e 10 indicam um problema específico (provavelmente no backend), com `loadbalance1` sendo mais afetado do que `loadbalance2`.

### 4. Heatmap de Correlação entre Tempos das Etapas

- **Descrição**: Um mapa de calor mostrando a correlação entre os tempos das etapas (`T1->T2`, `T2->T3`, `T3->T4`).
- **Eixos**:
  - **X e Y**: Etapas (`T1->T2`, `T2->T3`, `T3->T4`).
  - **Valores**: Coeficientes de correlação (de -1 a 1), com cores de azul (negativa) a vermelho (positiva).
- **Detalhes**:
  - `T1->T2` e `T2->T3` têm correlação de 0.06, indicando pouca relação linear.
  - `T2->T3` e `T3->T4` têm correlação de 0.16, sugerindo uma leve relação positiva.
  - `T1->T2` e `T3->T4` têm correlação negativa de -0.25, indicando que tempos mais longos na primeira etapa podem estar associados a tempos menores na última.
  - As correlações diagonais (`T1->T2` com `T1->T2`, `T2->T3` com `T2->T3`, `T3->T4` com `T3->T4`) são 1.00, como esperado (correlação de uma variável consigo mesma).
- **Interpretação**: Não há forte correlação entre as etapas, sugerindo que os tempos são influenciados por fatores independentes (como o backend em `T3->T4`).

### 5. Frequência de Requisições por Ciclo (por segundo)

- **Descrição**: Um gráfico de linha mostrando a frequência de requisições por segundo para cada ciclo.
- **Eixos**:
  - **X**: Tempo (T1), de 19:47:10 a 19:47:40.
  - **Y**: Número de requisições por segundo.
- **Detalhes**:
  - Cada ciclo (0, 1, 2) tem uma linha constante em torno de 1.0 requisição por segundo.
  - O Ciclo 0 cobre de 19:47:10 a 19:47:20, o Ciclo 1 de 19:47:20 a 19:47:30, e o Ciclo 2 de 19:47:30 a 19:47:40.
  - Há uma pequena variação (0.98–1.02), mas a frequência é estável.
- **Interpretação**: A taxa de chegada de requisições é consistente em todos os ciclos, com cerca de 1 requisição por segundo por ciclo.

## Resumo Geral

- **Desempenho Consistente**: A maioria das requisições tem tempos totais entre 3000 e 6000 ms, com `loadbalance1` e `loadbalance2` mostrando desempenho semelhante na maioria dos casos.
- **Outliers**: Requisições com IDs 9 e 10 (Ciclo 2) apresentam tempos extremos (15.000–25.000 ms), especialmente em `loadbalance1` (até 33.000 ms), indicando um problema específico (provavelmente no backend).
- **Distribuição**: Os histogramas mostram que os tempos totais são concentrados em faixas baixas, com poucos casos de atrasos significativos.
- **Correlação**: As etapas de processamento têm correlações fracas, sugerindo que os tempos são influenciados por fatores independentes.
- **Frequência**: A carga é distribuída uniformemente ao longo do tempo, com 1 requisição por segundo por ciclo.
