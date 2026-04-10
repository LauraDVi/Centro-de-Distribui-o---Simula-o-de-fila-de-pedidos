"""
Centro de Distribuição - Simulação de fila de pedidos
Equipe: 
    Laura Dantas - 564064
    Raphael Aaron - 564067
    Felipe Catto - 562106
    Kimberly Kristina - 564080
Data: 09/04/2026
Descrição:
    Simula o processamento de pedidos de um centro de distribuição logístico.
    Os pedidos são priorizados por nível de urgência e organizados em uma fila
    de saída. Pedidos com pagamento pendente são bloqueados antes do despacho.
    Ao final, são gerados gráficos analíticos sobre o estado da operação.
"""

import pandas as pd;
import matplotlib.pyplot as plt;
import matplotlib.patches as mtpp;
from collections import deque;
from datetime import datetime;

df = pd.read_csv ('datasetPar.csv')

# Converte cada linha do Dataframe em uma tupla para garantir
# que os dados de cada pedido não sejam alterados durante o prossamento.
pedidos = [tuple(row) for row in df.itertuples(index=False, name=None)]

# Mapeia os níveis de urgência para valores numéricos,
#permitindo ordenação comparativa entre os pedidos.
urgeNivel = {
    'baixa': 1,
    'media': 2,
    'alta': 3
} 

# Ordena os pedidos do mais urgente para o menos urgente (ordem decrescente),
# garantindo que pedidos críticos sejam processados primeiro — O(n log n).
pedidos.sort(key=lambda pedido: urgeNivel[pedido[6]], reverse=True)
print('\n' + '-' * 20)
print('Pedidos ordenados por nível de urgencia: \n')
for i in pedidos:
    print(f'ID {i[0]:02d} | {i[2]:<8} - {i[1]:<4} | Urgência: {i[6]:<6} | {i[8]}')

# Usa deque para a fila de saída pois oferece remoção O(1) pela esquerda,
# mais eficiente do que listas comuns, que realizam essa operação em O(n).
filaSaida = deque()
for pedido in pedidos:
    filaSaida.append(pedido)
print(f'\n Total de pedidos na fila de saída: {len(filaSaida)}')

# Dicionário que rastreia o estado atual de cada pedido.
# Pedidos com pagamento pendente são marcados como 'bloqueado'
# para impedir seu despacho até que a situação seja regularizada.
pedidoStatus = {}
for pedido in pedidos:
    '''Bloqueia aqueles pedidos que constam o pagamento como pendente.'''
    if pedido[9] == "pendente":
        pedidoStatus[pedido[0]] = 'bloqueado'
    else:
        pedidoStatus[pedido[0]] = 'aguardando'

def calculaValorTotal (pedidos, indice = 0):
    """
    Calcula recursivamente o valor total de todos os pedidos.
 
    A cada chamada, soma o valor do pedido na posição atual
    (quantidade * valorUnitário) com o resultado da chamada
    seguinte, até percorrer toda a lista.
 
    Args:
        pedidos (list): Lista de tuplas com os dados dos pedidos.
        indice (int): Índice atual da recursão (começa em 0).
 
    Returns:
        float: Soma acumulada do valor total de todos os pedidos.
    """
    if indice >= len(pedidos):
        return 0
    valorPedidos = pedidos [indice][4] * pedidos [indice][5]
    return valorPedidos + calculaValorTotal(pedidos, indice + 1)

valorTotal = calculaValorTotal(pedidos)
print(f'Valor total da carga: R$ {valorTotal:.2f}')

pedidosProcessados = []
pedidosBloqueados = []

print('\n' + '-' * 20)
print('Processando fila de saída')

# Consome a fila de saída da esquerda para a direita, respeitando a prioridade
# definida na etapa de ordenação. Pedidos bloqueados são separados para controle.
while filaSaida:
    pedidoAtual = filaSaida.popleft()
    pedidoId = pedidoAtual[0]

    if pedidoStatus[pedidoId] == 'bloqueado':
        print(f'Bloqueado: ID {pedidoId:02d} | {pedidoAtual[2]:<8} | Pagamento pendente')
        pedidosBloqueados.append(pedidoAtual)
    else:
        pedidoStatus[pedidoId] = 'despachado'
        print(f'Despachado: ID {pedidoId:02d} | {pedidoAtual[2]:<8} | Urgência: {pedidoAtual[6]:<6} | Modal: {pedidoAtual[8]}')
        pedidosProcessados.append(pedidoAtual)

# Define os nomes das colunas na mesma ordem em que os campos aparecem nas tuplas.
colunas = [
    'pedido_id',
    'cidade_destino',
    'produto',
    'categoria',
    'quantidade',
    'valor_unitario',
    'urgencia',
    'tempo_estimado_horas',
    'modal',
    'status_pagamento'
]

# Junta pedidos despachados e bloqueados em um único DataFrame para análise.
todos = pedidosProcessados + pedidosBloqueados
df = pd.DataFrame(todos, columns=colunas)

# Colunas calculadas adicionadas para facilitar análise e geração de gráficos.
df['status_despacho'] = df['pedido_id'].map(pedidoStatus)
df['valor_total'] = df['quantidade'] * df['valor_unitario']
df['prioridade_num'] = df['urgencia'].map(urgeNivel)

print('\n' + '-' * 20)
print('Relatorio final - DataFrame')
print(df[['pedido_id','produto','cidade_destino','urgencia','modal','valor_total','status_despacho']].to_string(index=False))

print('\n Estatisticas: \n')
print(
    f'Total despachado: {len(pedidosProcessados)}','\n'
    f'Total bloqueado: {len(pedidosBloqueados)}','\n'
    f'Valor total: {df['valor_total'].sum():.2f}','\n'
    f'Valor medio: {df['valor_total'].mean():.2f}', '\n'
    f'Modal rodoviario: {len(df[df['modal']=='rodoviario'])} pedidos','\n'
    f'Modal ferroviario: {len(df[df['modal']=='ferroviario'])} pedidos'
)

# Paleta de cores associada a cada nível de urgência, usada nos três gráficos.
cores = {'alta':'#e74c3c', 'media':'#f39c12', 'baixa':'#2ecc71'}

fig, axes = plt.subplots(1,3, figsize = (16,5))
fig.suptitle('Centro de Distribuicao - Analise de Pedidos', fontsize = 14, fontweight='bold')

# Gráfico 1 — Distribuição percentual por nível de urgência (pizza).
contagem = df['urgencia'].value_counts()
coresPizza = [cores[u] for u in contagem.index]

axes[0].pie(
    contagem.values, 
    labels=contagem.index, 
    colors=coresPizza,
    autopct='%1.0f%%',
    startangle=90
    )
axes[0].set_title('Distribuicao por Urgencia')

# Gráfico 2 — Valor total por pedido colorido por nível de urgência (barras).
coresBarras = [cores[u] for u in df['urgencia']]
axes[1].bar(df['produto'], df['valor_total'], color=coresBarras, edgecolor='white')
axes[1].set_title('Valor total por pedido (R$)')
axes[1].set_xlabel('Produto')
axes[1].set_ylabel('Valor (R$)')
patches = [mtpp.Patch(color=v, label=k) for k, v in cores.items()]
axes[1].legend(handles=patches, title='Urgencia')

# Gráfico 3 — Quantidade total de unidades agrupada por modal de transporte (barras).
modal_qtd = df.groupby("modal")["quantidade"].sum()
axes[2].bar(modal_qtd.index, modal_qtd.values, color=['#3498db', '#9b59b6'], edgecolor='white')
axes[2].set_title('Quantidade total por modal')
axes[2].set_xlabel('Modal')
axes[2].set_ylabel('Quantidade (unidades)')
 
plt.tight_layout()
plt.savefig('grafico_centro_distribuicao.png', dpi=150, bbox_inches='tight')
plt.show()
print("\nGráfico salvo como 'grafico_centro_distribuicao.png'")