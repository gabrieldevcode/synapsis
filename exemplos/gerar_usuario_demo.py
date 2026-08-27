"""Cria um usuário de demonstração para experimentar o Synapsis sem cadastro.

O Synapsis guarda os dados de cada estudante em `usuarios/`, que é uma pasta
ignorada pelo git — logo, um repositório recém-clonado não tem nenhum conteúdo
para revisar e o ranking aparece vazio. Este script preenche essa lacuna:
monta um usuário fictício com quatro matérias já cadastradas, cada uma com uma
data de inclusão diferente, para que o ranking de prioridades tenha o que
ordenar logo no primeiro acesso.

Uso, a partir da raiz do repositório:

    python exemplos/gerar_usuario_demo.py

Depois, rode `python synapsis.py`, escolha "1. Login" e entre com:

    usuário: demo
    senha:   demo123

Os dados são inventados. Nenhuma informação real de estudante é distribuída
junto com o projeto.
"""

import datetime
import os

NOME = 'demo'
SENHA = 'demo123'
COEFICIENTE = 6.700  # equivalente a responder o questionário com notas medianas


# Cada entrada descreve uma matéria: quantas horas atrás ela foi cadastrada,
# a dificuldade calculada, o resumo, o quiz e os anexos.
#
# As horas variam de propósito (2h a 15 dias) para cobrir várias das faixas
# temporais que o ranking usa. Os caminhos de arquivo são fictícios: servem
# para mostrar o formato, não apontam para nada que exista.
ESTUDOS = [
    {
        'nome': 'Estruturas Condicionais',
        'horas_atras': 2,
        'dificuldade': 8.4,
        'resumo': (
            'if/elif/else, operadores de comparacao e encadeamento de condicoes. '
            'Cuidado com o uso de = no lugar de == dentro do if.'
        ),
        'quiz': [
            ['Qual operador compara igualdade em Python?', '=='],
            ['O bloco else e obrigatorio depois de um if?', 'nao'],
        ],
        'arquivos': ['materiais/computacao1/aula03_condicionais.pdf'],
        'videos': ['https://exemplo.invalido/aula-condicionais'],
    },
    {
        'nome': 'Laços de Repetição',
        'horas_atras': 20,
        'dificuldade': 6.1,
        'resumo': (
            'while roda enquanto a condicao for verdadeira; for percorre um '
            'iteravel. enumerate devolve indice e valor ao mesmo tempo.'
        ),
        'quiz': [
            ['Que funcao devolve indice e valor durante um for?', 'enumerate'],
            ['Qual comando interrompe um laco imediatamente?', 'break'],
        ],
        'arquivos': ['materiais/computacao1/aula05_lacos.pdf'],
        'videos': [],
    },
    {
        'nome': 'Manipulação de Arquivos',
        'horas_atras': 75,
        'dificuldade': 4.3,
        'resumo': (
            'open() com os modos r, w e a. O with fecha o arquivo sozinho, '
            'inclusive quando ocorre uma excecao no meio da escrita.'
        ),
        'quiz': [
            ['Qual modo de open apaga o conteudo anterior do arquivo?', 'w'],
            ['Qual metodo le todas as linhas e devolve uma lista?', 'readlines'],
        ],
        'arquivos': [],
        'videos': ['https://exemplo.invalido/aula-arquivos'],
    },
    {
        'nome': 'Recursividade',
        'horas_atras': 360,  # 15 dias — cai na última faixa temporal
        'dificuldade': 2.8,
        'resumo': (
            'Toda funcao recursiva precisa de um caso base, senao a pilha de '
            'chamadas estoura. Exemplo classico: fatorial e Fibonacci.'
        ),
        'quiz': [
            ['Como se chama a condicao que encerra a recursao?', 'caso base'],
            ['Que erro o Python levanta sem caso base?', 'RecursionError'],
        ],
        'arquivos': [],
        'videos': [],
    },
]


def escrever_estudo(pasta_estudos, estudo):
    """Grava um conteúdo no mesmo formato que `cadastrar_novo_conteudo` produz.

    O `open` é chamado sem `encoding=` de propósito. O Synapsis também não
    informa encoding ao gravar nem ao ler, então ambos usam o padrão da
    plataforma (cp1252 no Windows, UTF-8 no Linux). Fixar UTF-8 aqui faria os
    acentos chegarem embaralhados na tela do programa no Windows.
    """
    registro = datetime.datetime.now() - datetime.timedelta(hours=estudo['horas_atras'])
    horario = registro.strftime('%d/%m/%Y %H:%M')

    nome_arquivo = f"{estudo['nome'].replace(' ', '_')}.txt"
    caminho = os.path.join(pasta_estudos, nome_arquivo)

    with open(caminho, 'w') as f:
        f.write(f"Conteudo: {estudo['nome']}\n")
        f.write(f"Dificuldade: {estudo['dificuldade']}\n")
        f.write(f"Data de Inclusao: {horario}\n")
        f.write(f"Resumo: {estudo['resumo']}\n")
        f.write('-' * 20 + '\n')
        f.write('QUIZ:\n')
        for item in estudo['quiz']:
            f.write(f'{item}\n')
        f.write('-' * 20 + '\n')
        f.write('ARQUIVOS:\n')
        for arquivo in estudo['arquivos']:
            f.write(f'{arquivo}\n')
        f.write('-' * 20 + '\n')
        f.write('VIDEO-AULAS:\n')
        for video in estudo['videos']:
            f.write(f'{video}\n')

    return caminho


def main():
    pasta_usuario = os.path.join('usuarios', NOME)
    pasta_estudos = os.path.join(pasta_usuario, 'estudos')
    os.makedirs(pasta_estudos, exist_ok=True)

    caminho_pessoal = os.path.join(pasta_usuario, f'pessoal_{NOME}.txt')
    with open(caminho_pessoal, 'w') as f:
        f.write(f'{NOME}\n')
        f.write(f'{SENHA}\n')
        f.write(f'{COEFICIENTE:.3f}\n')
        f.write('0\n')

    print(f'Perfil criado:  {caminho_pessoal}')
    for estudo in ESTUDOS:
        print(f'Estudo criado:  {escrever_estudo(pasta_estudos, estudo)}')

    print()
    print(f'Pronto. Rode `python synapsis.py`, escolha "1. Login" e entre com')
    print(f'usuario "{NOME}" e senha "{SENHA}".')


if __name__ == '__main__':
    main()
