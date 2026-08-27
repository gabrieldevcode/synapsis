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

    cabecalho("Definindo o seu Ritmo")
    print()


    delay_texto("As seguintes perguntas tem por objetivo personalizar a sua \n" \
    "experiencia no Synapsis " \
    "e melhorar seu desempenho no estudo  \n" \
    "por repetições espaçadas", 0.01)

    print()
    time.sleep(0.5)

    delay_texto("As perguntas são pessoais e não tem por objetivo constranger,\n" \
    "e sim ajudar no seu próprio desenvolvimento!", 0.01)

    print()
    time.sleep(0.5)
    linha()

    print('''
Responda todas as perguntas em uma escala de 1 a 10, sendo:
          
1: Não me identifico nem um pouco / Sou muito fraco nisso.

10: Me identifico completamente / Sou excelente nisso.
                 
''')
    linha()
    enter_para_pular()
    limpar_terminal()




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


    limpar_terminal()
    cabecalho('Questionario Preenchido com Sucesso!!!')



# ESPAÇO PARA EQUAÇÃO DO COEFICIENTE DE RENDIMENTO


    peso1, peso2, peso3, peso4, peso5 = 0.1, 0.2, 0.3, 0.3 , 0.1
    qualidade = p1 * peso1 + p2 * peso2 + p3 * peso3 + p4 * peso4 + p5 * peso5

    delay_texto(f"\nSeu coeficiente de rendimento é {qualidade:.2f}")
    print('\n1 → baixa absorção de conteúdos \n' \
    '10 → excelente compreensão das matérias')
    enter_para_pular()

#==============================================================================================================

    return qualidade







# FUNÇÕES DE LOGIN E CADASTRO


def processo_cadastro():
    pasta_usuarios = 'usuarios' # criada no inicio da aplicação
    cabecalho("Cadastro de Usuário")
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
    linha()

    caminho_usuario = os.path.join(pasta_usuarios, nome) # caminho da pasta do usuario especifico

    if os.path.exists(caminho_usuario): # verifica se já existe alguém com o mesmo nome de usuario por meio do nome das pastas
        print("\nErro: Este nome de usuário já existe.")
        print("Tente um nome diferente ou faça login.\n")
        linha()
        input('Pressione ENTER para voltar ao menu')
        return

    print()
    delay_texto('Agora iremos definir o seu perfil de estudante')
    enter_para_pular()

    resultado_questionario = coeficiente_rendimento() 

    try:
        os.makedirs(caminho_usuario)
        caminho_arquivo_pessoal = os.path.join(caminho_usuario, f'pessoal_{nome}.txt') # informações de cadastro salvas em um arquivo txt

        with open(caminho_arquivo_pessoal, "w") as f:
            f.write(f'{nome}\n')
            f.write(f'{senha}\n')
            f.write(f'{resultado_questionario:.3f}\n')
            f.write('0\n') # logins totais feitos

        limpar_terminal()
        cabecalho("Cadastro realizado com sucesso!")
        time.sleep(4)

    except OSError as e:
        print(f"\nErro ao criar a pasta ou arquivo: {e}")
        print("Tente novamente.")
        time.sleep(3)

    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")
        time.sleep(3)



def processo_login():

    pasta_usuarios = 'usuarios'
    cabecalho("Login")
    print()
    print("Nome")
    nome = input("→ ")

    #info_pessoais
    caminho_usuario = os.path.join(pasta_usuarios, nome) 
    caminho_pessoal = os.path.join(caminho_usuario, f'pessoal_{nome}.txt')

    # verifica se o nome corresponde a alguma pasta
    if not os.path.exists(caminho_usuario):
        delay_texto("\nUsuário não encontrado.", 0.03)
        delay_texto("Verifique o nome de usuário ou cadastre-se.", 0.03)
        time.sleep(1)
        input('Pressione ENTER para voltar ao menu')
        return
    

    # Busca a senha correta no arquivo pessoal
    senha_correta = None
    try:
        with open(caminho_pessoal, 'r') as f:
            linhas = f.readlines()
        senha_correta = linhas[1].strip() # a senha corresponde a linha 2, logo indice 1


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
            delay_texto('\nLogin bem-sucedido! Você será direcionado para a aba de usuários...', 0.03)
            time.sleep(2)
            return nome
        else:
            delay_texto(f"\nSua senha esta incorreta. Tente novamente:")

    print("\n[ERRO] Número máximo de tentativas excedido.")
    time.sleep(2)
    return










#   ÁREA DO USUÁRIO


## FUNÇÕES AUXILIARES

# Contabiliza quantas vezes o usuario acessou a aplicação, com a finalidade de promover melhor experiencia
def contador_acessos(nome_usuario):

    caminho_user = os.path.join('usuarios', nome_usuario, f'pessoal_{nome_usuario}.txt')
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
    cabecalho("Novo Cadastro de Estudo")
    
    # repositório para os estudos 
    pasta_estudos = os.path.join('usuarios', nome_usuario, 'estudos')

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

            f.write(f"Conteudo: {nome_conteudo}\n")
            f.write(f"Dificuldade: {dificuldade}\n")
            f.write(f"Data de Inclusao: {horario_registro}\n")
            f.write(f"Resumo: {texto_referencia}\n")
            f.write("-" * 20 + "\n")
            f.write("QUIZ:\n")
            for item in quiz_dados:
                f.write(f"{item}\n")
            f.write("-" * 20 + "\n")
            f.write("ARQUIVOS:\n")
            for arq in caminhos_arquivos:
                f.write(f"{arq}\n")
            f.write("-" * 20 + "\n")
            f.write('VIDEO-AULAS:\n')
            for video in links:
                f.write(f'{video}\n')


        linha()                
        delay_texto("Conteúdo salvo com sucesso!", 0.02)
        linha
        time.sleep(1)

    except Exception as e:
        print(f"Erro ao salvar: {e}")
        enter_para_pular()








# Por meio do algoritmo de definição de prioridade calculada, se define ordena uma lista para fazer as revisões
def obter_ranking_estudos(nome_usuario, qualidade_aluno):

    pasta_estudos = os.path.join('usuarios', nome_usuario, 'estudos')
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
            nome_conteudo = dados[0].strip().replace("Conteudo: ", "")
            dificuldade_atribuida_usuario = float(dados[1].strip().replace("Dificuldade: ", ""))

            data_inclusao = dados[2].strip().replace('Data de Inclusao: ', '')
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

    pasta_estudos = os.path.join('usuarios', nome_usuario, 'estudos')
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

    cabecalho("Revisar Conteúdo")
    print("Escolha o conteúdo para revisar:")

    for i, arq in enumerate(arquivos): # melhor maneira de percorrer uma lista sabendo seu indice
        print(f"{i+1}. {arq.replace('.txt','').replace('_',' ')}")

    print()
    print("Digite 0 para voltar")

    # verificação do valor
    try:
        linha()
        escolha = int(input("Opção: "))
        linha()
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

        if ln.startswith("Resumo:"):
            resumo = ln.replace("Resumo:", "").strip()
            leitura_quiz = leitura_arquivos = leitura_videos = False

        elif ln.strip() == "QUIZ:":
            leitura_quiz = True
            leitura_arquivos = leitura_videos = False
            continue

        elif ln.strip() == "ARQUIVOS:":
            leitura_arquivos = True
            leitura_quiz = leitura_videos = False
            continue

        elif ln.strip() == "VIDEO-AULAS:":
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
                # Se a linha não for uma lista válida, ignora
                continue
        elif leitura_arquivos:
            arquivos_locais.append(ln.strip())
        elif leitura_videos:
            videos.append(ln.strip())

    cabecalho(f"Revisando: {arquivo_escolhido.replace('.txt','')}")
    print("Resumo:")
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
    linha()
    enter_para_pular()


    # Fazer o quiz se existir
    if not quiz:
        print("Nenhum quiz cadastrado para este conteúdo.")
        enter_para_pular()
        return

    cabecalho("Quiz de Revisão")
    acertos = 0
    for i, (pergunta, resposta_correta) in enumerate(quiz, start=1):
        print(f"Pergunta {i}: {pergunta}")
        resposta_usuario = input("Resposta: ").strip()
        if resposta_usuario.lower() == str(resposta_correta).strip().lower():
            print("Correto!")
            acertos += 1
        else:
            print(f"Errado. Resposta correta: {resposta_correta}")
        linha()
        time.sleep(0.8)

    total = len(quiz)
    print(f"Você acertou {acertos} de {total} ({(acertos/total)*100:.1f}%).")
    enter_para_pular()



