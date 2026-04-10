# Centro de Distribuição com Fila de Pedidos
**Checkpoint 1 – FIAP – Engenharia de Software – Dynamic Programming**  
Enunciado A – RA com final PAR

---

## Descrição

Simulação de um centro de distribuição logístico que lê pedidos de um arquivo CSV, os organiza por nível de urgência e os processa em ordem de prioridade. Pedidos com pagamento pendente são automaticamente bloqueados.

---

## Estrutura do Projeto

```
Projeto
    |- centroDistribuicao.py              #Código principal
    |- dataset.csv                        #Dataset de entrada
    |- grafico                            #Será gerado com a aplicação do código
    |- read.me
```

---

## Como Executar

### 1. Instale as dependências
```bash
pip install pandas matplotlib
```

### 2. Coloque o arquivo CSV na mesma pasta do script
O arquivo deve se chamar `input_par.csv` e seguir o formato:
```
pedido_id,cidade_destino,produto,categoria,quantidade,valor_unitario,urgencia,tempo_estimado_horas,modal,status_pagamento
```

### 3. Execute o código
```bash
python centro_distribuicao.py
```

---

## O que o script faz (passo a passo)
- Etapa 1 - Lê o CSV e converte cada linha em tupla imutável.
    --> Estrutura usada: tupla.

- Etapa 2 - Cria dicionário mapeando urgência → número.
    --> Estrutura usada: dicionário.

- Etapa 3 - Ordena a lista de tuplas por urgência→número.
    --> Estrutura usada: lista + `.sort()`.

- Etapa 4 - Move os pedidos ordenados para a fila.
    --> Estrutura usada: deque.

- Etapa 5 - Verifica status de pagamento de cada pedido. 
    --> Estrutura usada: dicionário.

- Etapa 6 - Calcula valor total recursivamente.
    --> Estrutura usada: recursão.

- Etapa 7 - Processa a fila (despacha ou bloqueia). 
    --> Estrutura usada: deque + `.popleft()`.

- Etapa 8 - Consolida resultados em tabela.
    --> Estrutura usada: DataFrame.

- Etapa 9 - Gera gráficos de análise.
    --> Estrutura usada: matplotlib.

---

## Por que não usar `.sort()` direto no DataFrame?

O erro `AttributeError: 'DataFrame' object has no attribute 'sort'` acontece porque DataFrame do pandas **não tem** o método `.sort()` — ele usa `.sort_values()`. 

Nesta solução, convertemos o DataFrame em **lista de tuplas** antes de ordenar, o que:
- Resolve o problema central;
- Permite usar `.sort()` com `key=lambda` corretamente.

---

## Estruturas de Dados Utilizadas

- Tupla:
    --> Usada em cada pedido, pois cada pedido representa um dado que não pode ser mudado durante o processamento.
- Lista:
    --> Usada no armazenamento e ordenação, pois possibilida realizar ordenação por urgência utilizando o `.sort()`.
- Dicionário:
    --> Usado no mapeamento de urgência e status, pois permite acesso O(1) por chave.
- Deque:
    --> Usado na fila de processamento, pois permite o uso do `popleft()` em O(1).
- DataFrame:
    --> Usado na consolidação e análise final, pois permite a análise tabular com pandas.
---

## Complexidade (Big O)

- Operação 1: Ordenação (`.sort()`) 
    --> Complexidade: O(n log n)
- Operação 2: Inserção na deque 
    --> Complexidade: O(1)
- Operação 3: Retirada da deque (`popleft`)  
    --> Complexidade: O(1)
- Operação 4: Consulta no dicionário  
    --> Complexidade: O(1)
- Operação 5: Cálculo de valor total (recursão)  
    --> Complexidade: O(n)

---

## Requisitos

- Python 3.8+
- pandas
- matplotlib
