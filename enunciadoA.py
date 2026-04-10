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
