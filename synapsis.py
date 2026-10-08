import os
import time
import datetime
import ast



# LAYOUT AND DESIGN
def clear_terminal():
    if os.name == 'nt': 
        os.system('cls')
    else: 
        os.system('clear')


def line():
    print("═" * 60)


def header(text):
    clear_terminal()
    line()
    print(text.center(60))
    line()


def typewriter(text, delay=0.02):
    for character in text:
        print(character, end="", flush=True)
        time.sleep(delay)
    print()


def press_enter():
    input("\nPress ENTER to continue...")
    





# INTRODUCTION

# Creates the users folder when the program starts
def initialize_program():

    users_folder = 'users'

    if not os.path.exists(users_folder): # Checks whether it exists, creates it if not
        try:
            os.makedirs(users_folder) # create
        except OSError as e: # the machine may be blocking it
            print(f"Critical error while creating directory '{users_folder}': {e}")
            print("Please check the folder permissions and try again.")
            exit()





# Short explanation of the application
def show_intro():

    header("Welcome to SYNAPSIS")

    msg = ("""
    Our mission is to turn reviewing what you study
    into an intuitive, effective and smart routine.

    Synapsis uses spaced repetition to automatically
    schedule your reviews at the right moment.

    Let's beat disorganization together.
    """)
    
    typewriter(msg)
    line()
    press_enter()






# verifica as respostas dos futuros questionários
def obter_resposta_verificada(pergunta):
    while True:
        try:
            print(pergunta)
            resposta = float(input('→ '))
            if 1 <= resposta <= 10: # define os limites
                return resposta
            else:
                print('Digite um valor entre 1 e 10\n')
                
        except:
            print("Entrada Invalida, digite apenas numeros de 1 a 10\n")






# Define a qualidade como aluno do usuário
def coeficiente_rendimento():

    header("Definindo o seu Ritmo")
    print()


    typewriter("As seguintes perguntas tem por objetivo personalizar a sua \n" \
    "experiencia no Synapsis " \
    "e melhorar seu desempenho no estudo  \n" \
    "por repetições espaçadas", 0.01)

    print()
    time.sleep(0.5)

    typewriter("As perguntas são pessoais e não tem por objetivo constranger,\n" \
    "e sim ajudar no seu próprio desenvolvimento!", 0.01)

    print()
    time.sleep(0.5)
    line()

    print('''
Responda todas as perguntas em uma escala de 1 a 10, sendo:
          
1: Não me identifico nem um pouco / Sou muito fraco nisso.

10: Me identifico completamente / Sou excelente nisso.
                 
''')
    line()
    press_enter()
    clear_terminal()




    print(
        '''
1: Não me identifico nem um pouco / Sou muito fraco nisso.

10: Me identifico completamente / Sou excelente nisso.
'''
    )
    print()

# ESPAÇO PARA PERGUNTAS
    

    p1 = obter_resposta_verificada("Em uma escala de 1 a 10, o quanto você consegue manter uma rotina de estudos diária, \nmesmo naqueles dias em que você não sente nenhuma motivação para estudar?")
    p2 = obter_resposta_verificada("De 1 a 10, qual é o seu nível de persistência quando se depara com um conteúdo \ncomplexo que você não entende na primeira tentativa?")
    p3 = obter_resposta_verificada("De 1 a 10, o quanto você utiliza métodos ativos de estudo (como fazer exercícios, \nexplicar a matéria em voz alta ou criar seus próprios resumos) em vez de apenas \nconsumir passivamente (apenas ler ou assistir vídeo-aula)")  
    p4 = obter_resposta_verificada("Ao estudar um tema teórico chato, de 1 a 10, qual é a sua capacidade de visualizar \ncomo aquilo será útil para resolver problemas reais na sua futura carreira?")
    p5 = obter_resposta_verificada("De 1 a 10, se o material do curso for ruim ou incompleto, quão proativo você é para \nbuscar a resposta sozinho em documentações, livros ou I.A, sem depender de um professor?")

# ==============================================================================================================


    clear_terminal()
    header('Questionario Preenchido com Sucesso!!!')



# ESPAÇO PARA EQUAÇÃO DO COEFICIENTE DE RENDIMENTO


    peso1, peso2, peso3, peso4, peso5 = 0.1, 0.2, 0.3, 0.3 , 0.1
    qualidade = p1 * peso1 + p2 * peso2 + p3 * peso3 + p4 * peso4 + p5 * peso5

    typewriter(f"\nSeu coeficiente de rendimento é {qualidade:.2f}")
    print('\n1 → baixa absorção de conteúdos \n' \
    '10 → excelente compreensão das matérias')
    press_enter()

#==============================================================================================================

    return qualidade







# FUNÇÕES DE LOGIN E CADASTRO


def processo_cadastro():
    pasta_usuarios = 'users' # criada no inicio da aplicação
    header("Cadastro de Usuário")
    print()

    nome = input("Nome de usuário: ")
    print()
    senha = input("Crie uma senha: ")
    if senha == '': # verificacao simples de senha
        print(f"\n Sua senha não pode ser vazia")
        time.sleep(2)
        input('Pressione ENTER para voltar ao menu')
        return

    print()
    line()

    caminho_usuario = os.path.join(pasta_usuarios, nome) # caminho da pasta do usuario especifico

    if os.path.exists(caminho_usuario): # verifica se já existe alguém com o mesmo nome de usuario por meio do nome das pastas
        print("\nErro: Este nome de usuário já existe.")
        print("Tente um nome diferente ou faça login.\n")
        line()
        input('Pressione ENTER para voltar ao menu')
        return

    print()
    typewriter('Agora iremos definir o seu perfil de estudante')
    press_enter()

    resultado_questionario = coeficiente_rendimento() 

    try:
        os.makedirs(caminho_usuario)
        caminho_arquivo_pessoal = os.path.join(caminho_usuario, f'profile_{nome}.txt') # informações de cadastro salvas em um arquivo txt

        with open(caminho_arquivo_pessoal, "w") as f:
            f.write(f'{nome}\n')
            f.write(f'{senha}\n')
            f.write(f'{resultado_questionario:.3f}\n')
            f.write('0\n') # logins totais feitos

        clear_terminal()
        header("Cadastro realizado com sucesso!")
        time.sleep(4)

    except OSError as e:
        print(f"\nErro ao criar a pasta ou arquivo: {e}")
        print("Tente novamente.")
        time.sleep(3)

    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")
        time.sleep(3)



def processo_login():

    pasta_usuarios = 'users'
    header("Login")
    print()
    print("Nome")
    nome = input("→ ")

    #info_pessoais
    caminho_usuario = os.path.join(pasta_usuarios, nome) 
    caminho_pessoal = os.path.join(caminho_usuario, f'profile_{nome}.txt')

    # verifica se o nome corresponde a alguma pasta
    if not os.path.exists(caminho_usuario):
        typewriter("\nUsuário não encontrado.", 0.03)
        typewriter("Verifique o nome de usuário ou cadastre-se.", 0.03)
        time.sleep(1)
        input('Pressione ENTER para voltar ao menu')
        return
    

    # Busca a senha correta no arquivo pessoal
    senha_correta = None
    try:
        with open(caminho_pessoal, 'r') as f:
            linhas = f.readlines()
        senha_correta = linhas[1].strip() # a senha corresponde a line 2, logo indice 1


    except FileNotFoundError:
        print(f"\n Arquivo '{caminho_pessoal}' não foi encontrado.")
        print("Erro no processo de cadastro.")
        time.sleep(2)
        input('Pressione ENTER para voltar ao menu')
        return

    except Exception as e:
        print(f"\n Ocorreu um erro ao ler o perfil: {e}")
        time.sleep(2)
        input('Pressione ENTER para voltar ao menu')
        return


    # Tentativas de Senha
    max_tentativas = 3
    # Faz a verificação limitada de tentativas
    for tentativa_atual in range(1, max_tentativas + 1):
        print()
        if tentativa_atual == 1:
            print("Senha")
        else:
            print(f"(Tentativa {tentativa_atual} de {max_tentativas})")
            print('Senha:')

        senha_digitada = input("→ ")

        if senha_digitada == senha_correta:
            typewriter('\nLogin bem-sucedido! Você será direcionado para a aba de usuários...', 0.03)
            time.sleep(2)
            return nome
        else:
            typewriter(f"\nSua senha esta incorreta. Tente novamente:")

    print("\n[ERRO] Número máximo de tentativas excedido.")
    time.sleep(2)
    return










#   ÁREA DO USUÁRIO


## FUNÇÕES AUXILIARES

# Contabiliza quantas vezes o usuario acessou a aplicação, com a finalidade de promover melhor experiencia
def contador_acessos(nome_usuario):

    caminho_user = os.path.join('users', nome_usuario, f'profile_{nome_usuario}.txt')
    indice_qtd_acessos = 3 # referencia ao local do arquivo pessoal do usuario que corresponde a quantidade de acessos

    try:
        try:
            with open(caminho_user, 'r') as f:
                linhas = f.readlines()
        except FileNotFoundError:
            print('Erro ao encontrar arquivo pessoal')
            return

        
        acessos_atuais = int(linhas[indice_qtd_acessos].strip()) # transforma de str para int

        novo_acesso = acessos_atuais + 1 # adiciona 1 a variavel de acessos

        linhas[indice_qtd_acessos] = f'{novo_acesso}\n' # modifica a lista

        with open(caminho_user, 'w') as f: # reescreve o documento pessoal, porém com  +1 acesso
            f.writelines(linhas)
            
        return novo_acesso # retorna a qtd atual de acessos
            
    except Exception as e:
        print(f"Erro inesperado ao processar acessos para '{nome_usuario}': {e}")
        return 1



# faz a diferença entre a hora atual e aquela que o usario cadastrou o conteudo
def delta_time(data, hora):

    data_hora_inicial = datetime.datetime.strptime(f"{data} {hora}", "%d/%m/%Y %H:%M") # formata a hora

    agora = datetime.datetime.now()
    diferenca = agora - data_hora_inicial
    horas_decorridas = diferenca.total_seconds() / 3600.0

    return horas_decorridas # retorna o tempo total














## FUNÇÕES QUE FAZEM O DIFERENCIAL DA APLICAÇÃO

# deixa salvo de forma organizada o conteudo desejado
def cadastrar_novo_conteudo(nome_usuario):
    header("Novo Cadastro de Estudo")
    
    # repositório para os estudos 
    pasta_estudos = os.path.join('users', nome_usuario, 'studies')

    if not os.path.exists(pasta_estudos): # se não tiver cria
        os.makedirs(pasta_estudos)
    
    # infos conteudo
    nome_conteudo = input("Nome do Conteúdo/Matéria: ")
    texto_referencia = input("Descrição ou Resumo do conteúdo: ")
    
    # questionario para avaliar a compreensão do usario
    print("\nResponda tudo em uma escala de 1 a 10:")
    dominio = obter_resposta_verificada("Se voce precisasse dar uma aula sobre isso agora, quão bem voce se sairia?")
    relevancia = obter_resposta_verificada("O quanto esse assunto é fundamental para seus objetivos atuais?")
    engajamento = obter_resposta_verificada("O quanto você realmente gosta de aprender sobre isso?")
    
    dificuldade = ((dominio*0.5) + (relevancia*0.3) + (engajamento*0.2)) # dificuldade atribuida

    horario_registro = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    


    # --- Cadastrar Quiz ---
    quiz_dados = []
    print("\n--- Criação de Quiz Rápido para revisões futuras ---")
    while True:
        opcao = input("Deseja adicionar uma pergunta ao quiz? (S/N): ").upper()
        if opcao == 'S':
            pergunta = input("Pergunta: ")
            resposta = input("Resposta correta: ")
            quiz_dados.append([pergunta, resposta])
        elif opcao == 'N':
            break
        else:
            print("Entrada inválida! Digite S ou N")

    # --- Arquivos Locais ---
    caminhos_arquivos = []
    print("\n--- Anexar Arquivos do Computador ---")
    print('-> Adicone os caminhos relativos de: Apresentações, documentos, imagens, etc..')
    while True:
        opcao = input("Deseja salvar o caminho de um arquivo local? (S/N): ").upper()
        if opcao == 'S':
            caminho = input("Cole o caminho do arquivo aqui: ").strip('"')
            caminhos_arquivos.append(caminho)
        elif opcao == 'N':
            break
        else:
            print("Entrada inválida! Digite S ou N")

    # --- Video-Aulas ---
    links = []
    print("\n--- Salvar links de Videoaulas ---")
    while True:
        opcao = input("Deseja salvar o link de alguma video-aula? (S/N): ").upper()
        if opcao == 'S':
            link = input("Cole o link do video aqui: ")
            links.append(link)
        elif opcao == 'N':
            break
        else:
            print("Entrada inválida! Digite S ou N")


    # --- Salvando o Arquivo ---
    nome_arquivo = f"{nome_conteudo.replace(' ', '_')}.txt"
    caminho_final = os.path.join(pasta_estudos, nome_arquivo)
    

    # Salva no arquivo txt as infos do estudo
    try:
        with open(caminho_final, 'w') as f:

            f.write(f"Content: {nome_conteudo}\n")
            f.write(f"Difficulty: {dificuldade}\n")
            f.write(f"Date Added: {horario_registro}\n")
            f.write(f"Summary: {texto_referencia}\n")
            f.write("-" * 20 + "\n")
            f.write("QUIZ:\n")
            for item in quiz_dados:
                f.write(f"{item}\n")
            f.write("-" * 20 + "\n")
            f.write("FILES:\n")
            for arq in caminhos_arquivos:
                f.write(f"{arq}\n")
            f.write("-" * 20 + "\n")
            f.write('VIDEO LESSONS:\n')
            for video in links:
                f.write(f'{video}\n')


        line()                
        typewriter("Conteúdo salvo com sucesso!", 0.02)
        line
        time.sleep(1)

    except Exception as e:
        print(f"Erro ao salvar: {e}")
        press_enter()








# Por meio do algoritmo de definição de prioridade calculada, se define ordena uma lista para fazer as revisões
def obter_ranking_estudos(nome_usuario, qualidade_aluno):

    pasta_estudos = os.path.join('users', nome_usuario, 'studies')
    # Busca todos os estudos do usuario
    try:
        arquivos = []
        lista_completa = os.listdir(pasta_estudos)

        for arquivo in lista_completa:
            arquivos.append(arquivo)

    except Exception:
        return []


    # Extraindo dados do arquivo de estudo específico
    lista_rankeada = []
    for estudo in arquivos:
        caminho_completo_estudo = os.path.join(pasta_estudos, estudo)
        
        with open(caminho_completo_estudo, 'r') as f:
            dados = f.readlines()
            nome_conteudo = dados[0].strip().replace("Content: ", "")
            dificuldade_atribuida_usuario = float(dados[1].strip().replace("Difficulty: ", ""))

            data_inclusao = dados[2].strip().replace('Date Added: ', '')
            dia_hora = data_inclusao.split(' ')
            dia = dia_hora[0]
            hora = dia_hora[1]

            tempo_decorrido = delta_time(dia, hora) # função para diferença de tempo

            # Para um melhor calculo de prioridades, defini algumas faixas temporais para identificar se falta pouco, médio ou muito tempo
            if tempo_decorrido < 4:
                vt = 10.0
            elif 4 <= tempo_decorrido < 12:
                vt = 9.2
            elif 12 <= tempo_decorrido < 24:
                vt = 8.0
            elif 24 <= tempo_decorrido < 48:
                vt = 7.0 
            elif 48 <= tempo_decorrido < 96:
                vt = 5.5
            elif 96 <= tempo_decorrido < 240:
                vt = 2.0
            else:
                vt = 0.5
                                
            
            # Quanto maior o resultado menor a nescessidade de rever o conteudo
            prioridade_calculada = qualidade_aluno* 0.2 + dificuldade_atribuida_usuario * 0.5 + tempo_decorrido *0.5

            # Adiciona a lista
            lista_rankeada.append([prioridade_calculada, nome_conteudo]) 
    

    lista_rankeada.sort(key=lambda x: x[0])

    return lista_rankeada









# método de revisar aquilo que voce já cadastrou de forma eficaz
def revisar_conteudo(nome_usuario):

    pasta_estudos = os.path.join('users', nome_usuario, 'studies')
    if not os.path.exists(pasta_estudos):
        print("Nenhum estudo cadastrado ainda.")
        time.sleep(1)
        return

    arquivos = []
    

    lista_completa = os.listdir(pasta_estudos)

    for arquivo in lista_completa:
        if arquivo.endswith('.txt'):
            arquivos.append(arquivo)

    if not arquivos:
        print("Nenhum estudo cadastrado ainda.")
        time.sleep(1)
        return

    header("Revisar Conteúdo")
    print("Escolha o conteúdo para revisar:")

    for i, arq in enumerate(arquivos): # melhor maneira de percorrer uma lista sabendo seu indice
        print(f"{i+1}. {arq.replace('.txt','').replace('_',' ')}")

    print()
    print("Digite 0 para voltar")

    # verificação do valor
    try:
        line()
        escolha = int(input("Opção: "))
        line()
    except ValueError:
        print("Entrada inválida.")
        time.sleep(1)
        return
    if escolha == 0:
        return
    if escolha < 1 or escolha > len(arquivos):
        print("Opção inválida.")
        time.sleep(1)
        return

    # guarda qual é o arquivo desejado
    arquivo_escolhido = arquivos[escolha-1]
    caminho = os.path.join(pasta_estudos, arquivo_escolhido)
    try:
        with open(caminho, 'r') as f:
            linhas = f.readlines()
    except Exception as e:
        print(f"Erro ao abrir o arquivo: {e}")
        time.sleep(1)
        return

    # mostra resumo
    resumo = ""
    quiz = []
    arquivos_locais = []
    videos = []
    leitura_quiz = False
    leitura_arquivos = False
    leitura_videos = False


    for ln in linhas:
        # pular linhas de separador
        if ln.strip().startswith("-"):
            continue

        if ln.startswith("Summary:"):
            resumo = ln.replace("Summary:", "").strip()
            leitura_quiz = leitura_arquivos = leitura_videos = False

        elif ln.strip() == "QUIZ:":
            leitura_quiz = True
            leitura_arquivos = leitura_videos = False
            continue

        elif ln.strip() == "FILES:":
            leitura_arquivos = True
            leitura_quiz = leitura_videos = False
            continue

        elif ln.strip() == "VIDEO LESSONS:":
            leitura_quiz = leitura_arquivos = False
            leitura_videos = True
            continue

        if leitura_quiz and ln:
            try:
                # Transforma a string "['P', 'R']" em uma lista real ['P', 'R']
                dados_linha = ast.literal_eval(ln)
                if isinstance(dados_linha, list):
                    quiz.append(dados_linha)
            except:
                # Se a line não for uma lista válida, ignora
                continue
        elif leitura_arquivos:
            arquivos_locais.append(ln.strip())
        elif leitura_videos:
            videos.append(ln.strip())

    header(f"Revisando: {arquivo_escolhido.replace('.txt','')}")
    print("Summary:")
    print(resumo)
    print()
    if arquivos_locais:
        print('Voce pode copiar os caminhos relativos abaixo, colocar em seu explorador de arquivos e visualizar conteudos da matéria')
        print("Arquivos anexados:")
        for arq in arquivos_locais:
            print(f" - {arq}")
    if videos:
        print("Vídeos relacionados ao conteudo:")
        for v in videos:
            print(f" - {v}")
    line()
    press_enter()


    # Fazer o quiz se existir
    if not quiz:
        print("Nenhum quiz cadastrado para este conteúdo.")
        press_enter()
        return

    header("Quiz de Revisão")
    acertos = 0
    for i, (pergunta, resposta_correta) in enumerate(quiz, start=1):
        print(f"Pergunta {i}: {pergunta}")
        resposta_usuario = input("Resposta: ").strip()
        if resposta_usuario.lower() == str(resposta_correta).strip().lower():
            print("Correto!")
            acertos += 1
        else:
            print(f"Errado. Resposta correta: {resposta_correta}")
        line()
        time.sleep(0.8)

    total = len(quiz)
    print(f"Você acertou {acertos} de {total} ({(acertos/total)*100:.1f}%).")
    press_enter()




def listar_editar_deletar(nome_usuario):

    pasta_estudos = os.path.join('users', nome_usuario, 'studies')
    if not os.path.exists(pasta_estudos):
        print("Nenhum estudo cadastrado ainda.")
        time.sleep(1)
        return

    while True:
        header("Seus Estudos - Listar / Editar / Deletar")
        arquivos = []    
        todos_os_itens = os.listdir(pasta_estudos)
        for item in todos_os_itens:
            arquivos.append(item)


        if not arquivos:
            print("Nenhum estudo cadastrado ainda.")
            press_enter()
            return

        for i, arq in enumerate(arquivos):
            print(f"{i+1}. {arq.replace('.txt','').replace('_',' ')}")
        print("0. Voltar")
        try:
            escolha = int(input("Escolha um item para ver/editar/deletar (número): "))
        except ValueError:
            print("Entrada inválida.")
            time.sleep(1)
            continue

        if escolha == 0:
            return
        if escolha < 1 or escolha > len(arquivos):
            print("Opção inválida.")
            time.sleep(1)
            continue

        arquivo_selecionado = arquivos[escolha-1]
        caminho = os.path.join(pasta_estudos, arquivo_selecionado)
        # mostrar opções
        header(f"Conteúdo: {arquivo_selecionado.replace('.txt','')}")
        print("1. Visualizar conteúdo")
        print("2. Editar resumo")
        print("3. Renomear conteúdo")
        print("4. Deletar conteúdo")
        print("0. Voltar")
        op = input("Opção: ")

        if op == '1':
            try:
                with open(caminho, 'r') as f:
                    print(f.read())
            except Exception as e:
                print(f"Erro ao abrir o arquivo: {e}")
            press_enter()

        elif op == '2':
            # editar resumo (line que começa com 'Resumo:')
            try:
                with open(caminho, 'r') as f:
                    linhas = f.readlines()
                for idx, l in enumerate(linhas):
                    if l.startswith("Summary:"):
                        print("Resumo atual:")
                        print(l.replace("Summary:", "").strip())
                        novo = input("Novo resumo (deixe vazio para manter): ")
                        if novo.strip() != "":
                            linhas[idx] = f"Summary: {novo}\n"
                        break
                with open(caminho, 'w') as f:
                    f.writelines(linhas)
                print("Resumo atualizado com sucesso.")
            except Exception as e:
                print(f"Erro ao editar: {e}")
            press_enter()

        elif op == '3':
            novo_nome = input("Digite o novo nome do conteúdo (apenas o nome, sem extensão): ").strip()
            if novo_nome == "":
                print("Nome inválido.")
                time.sleep(1)
            else:
                novo_arquivo = f"{novo_nome.replace(' ', '_')}.txt"
                novo_caminho = os.path.join(pasta_estudos, novo_arquivo)
                try:
                    os.rename(caminho, novo_caminho)
                    print("Renomeado com sucesso.")
                except Exception as e:
                    print(f"Erro ao renomear: {e}")
                time.sleep(1)

        elif op == '4':
            confirmacao = input(f"Tem certeza que deseja apagar '{arquivo_selecionado}'? (DIGITE 'SIM'): ")
            if confirmacao == 'SIM':
                try:
                    os.remove(caminho)
                    print("Conteúdo deletado com sucesso.")
                except Exception as e:
                    print(f"Erro ao deletar: {e}")
            else:
                print("Operação cancelada.")
            time.sleep(1)

        elif op == '0':
            continue
        else:
            print("Opção inválida.")
            time.sleep(1)





# UNIÃO DAS FUNÇÕES AUXILIARES PARA FORMAR O MENU DO USUARIO


def menu_usuario(nome_usuario):


    pasta_estudos = os.path.join('users', nome_usuario, 'studies')
    if not os.path.exists(pasta_estudos):
        os.makedirs(pasta_estudos)


    caminho_pessoal = os.path.join('users', nome_usuario, f'profile_{nome_usuario}.txt')
    with open(caminho_pessoal, 'r') as f:
        dados_pessoais = f.readlines()
        qualidade_aluno = float(dados_pessoais[2].strip())


    num_acessos = contador_acessos(nome_usuario)
    
    clear_terminal()
    line()
    if num_acessos == 1:
        typewriter(f"Olá {nome_usuario}! Seja muito bem-vindo(a) à sua área de estudos!", 0.03)
        typewriter("Preparei tudo para o seu primeiro acesso.", 0.03)


    else:
        typewriter(f"Bem-vindo de volta, {nome_usuario}!", 0.03)
        print(f"Acessos totais: {num_acessos}")
    line()
    time.sleep(1)




    while True:

        todos_arquivos = os.listdir(pasta_estudos)
        qtd_estudos = 0
        for arquivo in todos_arquivos:
            if arquivo.endswith('.txt'):
                qtd_estudos = qtd_estudos + 1


        ranking = obter_ranking_estudos(nome_usuario, qualidade_aluno)
        
        header(f"Olá {nome_usuario}")
        print(f"Estudos Cadastrados: {qtd_estudos}".center(60))
        print(f"Acessos: {num_acessos}".center(60))
        line()
        print("Ranking de Prioridades:")
        if ranking:
            print(f"{'PRIORIDADE':<12} | {'CONTEÚDO':<30}")
            print("-" * 60)
            for i, item in enumerate(ranking): 
                # Acessa os elementos dentro do 'item'
                score = item[0]
                nome = item[1]
                print(f"{i +1: <12} | {nome:<30}")





        else:
            print("Nenhum conteúdo para rankear ainda.")
        
        line()

        # Menu
        print("1. Cadastrar novo conteúdo")
        print("2. Revisar Conteúdo")
        print("3. Listar conteúdos (Visualizar / Editar / Deletar)")
        print("4. Sair")
        line()
        
        escolha = input("Escolha: ")
        
        if escolha == '1':
            cadastrar_novo_conteudo(nome_usuario)
            
        elif escolha == '2':
            revisar_conteudo(nome_usuario)            
            
        elif escolha == '3':
            listar_editar_deletar(nome_usuario)

        elif escolha == '4':
            return

        else:
            print("Opção inválida. Tente novamente.")
            time.sleep(1)






def main():

    initialize_program()
    show_intro()
    habilitado = ''
    while habilitado != True:
        header("Menu Principal")
        print("1. Login")
        print("2. Cadastrar-se")
        print("3. Sair")
        line()
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == "1":
            usuario_logado = processo_login()
            
            if usuario_logado:
                menu_usuario(usuario_logado)

        elif escolha == "2":
            processo_cadastro()
        elif escolha == "3":
            clear_terminal()
            print("Obrigado por usar o Gerenciador de Estudos.")
            print("Até logo!")
            break 
        else:
            print("\nOpção inválida. Por favor, tente novamente.")
            time.sleep(1) 




if __name__ == "__main__":
    main()