# Simular um centro de distribuicao com file de pedidos.
# priorizando pedidos por urgencia e organizar saidas logisticas

import pandas as pd;
import matplotlib.pyplot as plt;
import matplotlib.patches as mtpp;
from collections import deque;
from datetime import datetime;

df = pd.read_csv ('datasetPar.csv')

'''Converte cada linha do dataset em uma tupla'''
pedidos = [tuple(row) for row in df.intertuples(index=False, name=None)]

''' Define nivel de urgencia do pedido.'''
urgeNivel = {
    'baixa': 1,
    'media': 2,
    'alta': 3
} 

'''Deselvolve ordem do mais urgente para o menos urgente.'''
pedidos.sort(key=lambda pedido: urgeNivel[pedido[6]], reverse=True)
print('\n' '-' * 20)
print('Pedidos ordenados por nível de urgencia: \n')
for i in pedidos:
    print(f'ID {i[0]:02d} | {i[2]:<8} - {i[1]:<4} | Urgência: {i[6]:<6} | {i[8]}')

'''Transfere as listas ordenadas para um deque.'''
filaSaida = deque()
for pedido in pedidos:
    filaSaida.append(pedido)
print(f'\n Total de pedidos na fila de saída: {len(filaSaida)}')

'''Controla o estado de cada pedido durante o processo.'''
pedidoStatus = {}
for pedido in pedidos:
    '''Bloqueia aqueles pedidos que constam o pagamento como pendente.'''
    if pedido[9] == "pendente":
        pedidoStatus[pedido[0]] = 'bloqueado'
    else:
        pedidoStatus[pedido[0]] = 'aguardando'

'''Calcula o valor total da carga.'''
def calculaValorTotal (pedidos, indice = 0):
    '''
    Calcula o valor total de todos os pedidos recursivamente.
    Valor = quantidade (pos 4) * valorUnitario (pos 5).
    '''
    if indice >= len(pedidos):
        return 0
    valorPedidos = pedidos [indice][4] * pedidos [indice][5]
    return valorPedidos + calculaValorTotal(pedidos, indice + 1)

valorTotal = calculaValorTotal(pedidos)
print(f'Valor total da carga: R$ {valorTotal:.2f}')

''' Simula o centro de distribuicao despachando pedidos.'''
pedidosProcessados = []
pedidosBloqueados = []

print('\n' + '-' * 20)
print('Processando fila de saída')

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

'''Consolida todos os pedidos, incluindo os despachados e os bloqueados, em um DataFrame para analise e geracao de graficos.'''
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

todos = pedidosProcessados + pedidosBloqueados
df = pd.DataFrame(todos, columns=colunas)

'''Adiciona colunas calculadas.'''
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

'''Define configuracoes dos graficos.'''
cores = {'alta':'#e74c3c', 'media':'#f39c12', 'baixa':'#2ecc71'}
fig, axes = plt.subplots(1,3, figsize = (16,5))
fig.subtitle('Centro de Distribuicao - Analise de Pedidos', fontsize = 14, fontweight='bold')

'''Configura grafico numero 1 - urgencias (grafico de pizza).'''
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

'''Configura grafico numero 2 - valor total por pedido (grafico de barras coloridas por urgencia).'''
coresBarras = [cores[u] for u in df['urgencia']]
axes[1].bar(df['produto'], df['valor_total'], color=coresBarras, edgecolor='white')
axes[1].set_title('Valor total por pedido (R$)')
axes[1].set_xlabel('Produto')
axes[1].set_ylabel('Valor (R$)')
patches = [mtpp.Patch(color=v, label=k) for k, v in cores.items()]
axes[1].legend(handles=patches, title='Urgencia')

'''Coonfigura grafico numero 3 - quantidade por modal'''
modal_qtd = df.groupby("modal")["quantidade"].sum()
axes[2].bar(modal_qtd.index, modal_qtd.values, color=['#3498db', '#9b59b6'], edgecolor='white')
axes[2].set_title('Quantidade total por modal')
axes[2].set_xlabel('Modal')
axes[2].set_ylabel('Quantidade (unidades)')
 
plt.tight_layout()
plt.savefig('grafico_centro_distribuicao.png', dpi=150, bbox_inches='tight')
plt.show()
print("\nGráfico salvo como 'grafico_centro_distribuicao.png'")