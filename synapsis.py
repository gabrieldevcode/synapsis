import os
import time
import datetime
import ast



# ORGANIZAÇÃO E DESIGN
def limpar_terminal():
    if os.name == 'nt': 
        os.system('cls')
    else: 
        os.system('clear')


def linha():
    print("═" * 60)


def cabecalho(texto):
    limpar_terminal()
    linha()
    print(texto.center(60))
    linha()


def delay_texto(texto, delay=0.02):
    for caracter in texto:
        print(caracter, end="", flush=True)
        time.sleep(delay)
    print()


def enter_para_pular():
    input("\nPressione ENTER para continuar...")
    





# INTRODUÇÃO

# Utilizada para criar a pasta dos usuarios ao inicializar o programa
def inicializar_programa():

    pasta_usuarios = 'usuarios'

    if not os.path.exists(pasta_usuarios): # Verifica se existe, se não cria
        try:
            os.makedirs(pasta_usuarios) # cria
        except OSError as e: # possivel bloqueio da maquina
            print(f"Erro crítico ao criar diretório '{pasta_usuarios}': {e}")
            print("Por favor, verifique as permissões da pasta e tente novamente.")
            exit()





# Explicacao breve da aplicacao 
def mostrar_introducao():

    cabecalho("Bem-vindo ao SYNAPSIS")

    msg = ("""
    Nossa missão é transformar a revisão de conteúdos
    em uma rotina intuitiva, eficaz e inteligente.
           
    O Synapsis usa repetição espaçada para agendar
    automaticamente as suas revisões no momento ideal.

    Vamos combater a desorganização juntos.
    """)
    
    delay_texto(msg)
    linha()
    enter_para_pular()






