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






# validates the answers of the questionnaires that follow
def get_validated_answer(question):
    while True:
        try:
            print(question)
            answer = float(input('→ '))
            if 1 <= answer <= 10: # sets the limits
                return answer
            else:
                print('Enter a value between 1 and 10\n')

        except:
            print("Invalid input, type only numbers from 1 to 10\n")






# Defines the user's quality as a student
def performance_coefficient():

    header("Finding Your Pace")
    print()


    typewriter("The following questions are meant to personalize your \n" \
    "experience in Synapsis " \
    "and improve how you study  \n" \
    "with spaced repetition", 0.01)

    print()
    time.sleep(0.5)

    typewriter("The questions are personal and are not meant to embarrass you,\n" \
    "but to help your own growth!", 0.01)

    print()
    time.sleep(0.5)
    line()

    print('''
Answer every question on a scale from 1 to 10, where:

1: I don't relate to this at all / I'm very weak at this.

10: I relate to this completely / I'm excellent at this.

''')
    line()
    press_enter()
    clear_terminal()




    print(
        '''
1: I don't relate to this at all / I'm very weak at this.

10: I relate to this completely / I'm excellent at this.
'''
    )
    print()

# QUESTIONS


    p1 = get_validated_answer("On a scale from 1 to 10, how well can you keep a daily study routine, \neven on the days when you feel no motivation at all to study?")
    p2 = get_validated_answer("From 1 to 10, how persistent are you when you face complex content \nthat you don't understand on the first try?")
    p3 = get_validated_answer("From 1 to 10, how much do you use active study methods (such as solving exercises, \nexplaining the subject out loud or writing your own summaries) instead of just \nconsuming passively (only reading or watching video lessons)?")
    p4 = get_validated_answer("When studying a boring theoretical topic, from 1 to 10, how well can you picture \nhow it will help you solve real problems in your future career?")
    p5 = get_validated_answer("From 1 to 10, if the course material is poor or incomplete, how proactive are you in \nfinding the answer on your own in documentation, books or AI, without relying on a teacher?")

# ==============================================================================================================


    clear_terminal()
    header('Questionnaire Completed Successfully!!!')



# PERFORMANCE COEFFICIENT EQUATION


    weight1, weight2, weight3, weight4, weight5 = 0.1, 0.2, 0.3, 0.3 , 0.1
    quality = p1 * weight1 + p2 * weight2 + p3 * weight3 + p4 * weight4 + p5 * weight5

    typewriter(f"\nYour performance coefficient is {quality:.2f}")
    print('\n1 → low content absorption \n' \
    '10 → excellent understanding of the subjects')
    press_enter()

#==============================================================================================================

    return quality







# LOGIN AND SIGN-UP FUNCTIONS


def sign_up():
    users_folder = 'users' # created when the application starts
    header("User Sign-up")
    print()

    name = input("Username: ")
    print()
    password = input("Create a password: ")
    if password == '': # simple password check
        print(f"\n Your password cannot be empty")
        time.sleep(2)
        input('Press ENTER to go back to the menu')
        return

    print()
    line()

    user_path = os.path.join(users_folder, name) # path to this specific user's folder

    if os.path.exists(user_path): # checks, through the folder names, whether someone already has this username
        print("\nError: This username already exists.")
        print("Try a different name or log in.\n")
        line()
        input('Press ENTER to go back to the menu')
        return

    print()
    typewriter('Now we will set up your student profile')
    press_enter()

    questionnaire_result = performance_coefficient()

    try:
        os.makedirs(user_path)
        profile_file_path = os.path.join(user_path, f'profile_{name}.txt') # sign-up information saved in a txt file

        with open(profile_file_path, "w") as f:
            f.write(f'{name}\n')
            f.write(f'{password}\n')
            f.write(f'{questionnaire_result:.3f}\n')
            f.write('0\n') # total logins made

        clear_terminal()
        header("Sign-up completed successfully!")
        time.sleep(4)

    except OSError as e:
        print(f"\nError while creating the folder or file: {e}")
        print("Please try again.")
        time.sleep(3)

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        time.sleep(3)



def login():

    users_folder = 'users'
    header("Login")
    print()
    print("Name")
    name = input("→ ")

    #personal_info
    user_path = os.path.join(users_folder, name)
    profile_path = os.path.join(user_path, f'profile_{name}.txt')

    # checks whether the name matches any folder
    if not os.path.exists(user_path):
        typewriter("\nUser not found.", 0.03)
        typewriter("Check the username or sign up.", 0.03)
        time.sleep(1)
        input('Press ENTER to go back to the menu')
        return


    # Reads the correct password from the profile file
    correct_password = None
    try:
        with open(profile_path, 'r') as f:
            lines = f.readlines()
        correct_password = lines[1].strip() # the password is on line 2, so index 1


    except FileNotFoundError:
        print(f"\n File '{profile_path}' was not found.")
        print("Something went wrong during sign-up.")
        time.sleep(2)
        input('Press ENTER to go back to the menu')
        return

    except Exception as e:
        print(f"\n An error occurred while reading the profile: {e}")
        time.sleep(2)
        input('Press ENTER to go back to the menu')
        return


    # Password attempts
    max_attempts = 3
    # Limits how many times the password can be tried
    for current_attempt in range(1, max_attempts + 1):
        print()
        if current_attempt == 1:
            print("Password")
        else:
            print(f"(Attempt {current_attempt} of {max_attempts})")
            print('Password:')

        typed_password = input("→ ")

        if typed_password == correct_password:
            typewriter('\nLogin successful! Taking you to your study area...', 0.03)
            time.sleep(2)
            return name
        else:
            typewriter(f"\nYour password is incorrect. Try again:")

    print("\n[ERROR] Maximum number of attempts exceeded.")
    time.sleep(2)
    return










#   USER AREA


## HELPER FUNCTIONS

# Counts how many times the user has opened the application, to provide a better experience
def count_access(username):

    user_path = os.path.join('users', username, f'profile_{username}.txt')
    access_count_index = 3 # line of the user's profile file that holds the number of accesses

    try:
        try:
            with open(user_path, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print('Error finding the profile file')
            return


        current_accesses = int(lines[access_count_index].strip()) # converts from str to int

        new_access = current_accesses + 1 # adds 1 to the access count

        lines[access_count_index] = f'{new_access}\n' # updates the list

        with open(user_path, 'w') as f: # rewrites the profile file, now with +1 access
            f.writelines(lines)

        return new_access # returns the current number of accesses

    except Exception as e:
        print(f"Unexpected error while processing accesses for '{username}': {e}")
        return 1



# computes the difference between now and the moment the user registered the content
def delta_time(date, hour):

    start_datetime = datetime.datetime.strptime(f"{date} {hour}", "%d/%m/%Y %H:%M") # parses the time

    now = datetime.datetime.now()
    difference = now - start_datetime
    elapsed_hours = difference.total_seconds() / 3600.0

    return elapsed_hours # returns the total time














## THE FUNCTIONS THAT MAKE THE APPLICATION STAND OUT

# saves the desired content in an organized way
def register_content(username):
    header("New Study Entry")

    # repository for the studies
    studies_folder = os.path.join('users', username, 'studies')

    if not os.path.exists(studies_folder): # create it if missing
        os.makedirs(studies_folder)

    # content info
    content_name = input("Content/Subject name: ")
    reference_text = input("Description or summary of the content: ")

    # questionnaire to assess how well the user understands it
    print("\nAnswer everything on a scale from 1 to 10:")
    mastery = get_validated_answer("If you had to teach a class on this right now, how well would you do?")
    relevance = get_validated_answer("How essential is this subject to your current goals?")
    engagement = get_validated_answer("How much do you actually enjoy learning about this?")

    difficulty = ((mastery*0.5) + (relevance*0.3) + (engagement*0.2)) # assigned difficulty

    registration_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")



    # --- Register Quiz ---
    quiz_data = []
    print("\n--- Quick Quiz for future reviews ---")
    while True:
        option = input("Do you want to add a question to the quiz? (Y/N): ").upper()
        if option == 'Y':
            question = input("Question: ")
            answer = input("Correct answer: ")
            quiz_data.append([question, answer])
        elif option == 'N':
            break
        else:
            print("Invalid input! Type Y or N")

    # --- Local Files ---
    file_paths = []
    print("\n--- Attach Files from Your Computer ---")
    print('-> Add the relative paths of: slides, documents, images, etc..')
    while True:
        option = input("Do you want to save the path of a local file? (Y/N): ").upper()
        if option == 'Y':
            path = input("Paste the file path here: ").strip('"')
            file_paths.append(path)
        elif option == 'N':
            break
        else:
            print("Invalid input! Type Y or N")

    # --- Video Lessons ---
    links = []
    print("\n--- Save Video Lesson Links ---")
    while True:
        option = input("Do you want to save a video lesson link? (Y/N): ").upper()
        if option == 'Y':
            link = input("Paste the video link here: ")
            links.append(link)
        elif option == 'N':
            break
        else:
            print("Invalid input! Type Y or N")


    # --- Saving the File ---
    file_name = f"{content_name.replace(' ', '_')}.txt"
    final_path = os.path.join(studies_folder, file_name)


    # Saves the study info in the txt file
    try:
        with open(final_path, 'w') as f:

            f.write(f"Content: {content_name}\n")
            f.write(f"Difficulty: {difficulty}\n")
            f.write(f"Date Added: {registration_time}\n")
            f.write(f"Summary: {reference_text}\n")
            f.write("-" * 20 + "\n")
            f.write("QUIZ:\n")
            for item in quiz_data:
                f.write(f"{item}\n")
            f.write("-" * 20 + "\n")
            f.write("FILES:\n")
            for file in file_paths:
                f.write(f"{file}\n")
            f.write("-" * 20 + "\n")
            f.write('VIDEO LESSONS:\n')
            for video in links:
                f.write(f'{video}\n')


        line()
        typewriter("Content saved successfully!", 0.02)
        line()
        time.sleep(1)

    except Exception as e:
        print(f"Error while saving: {e}")
        press_enter()








# Uses the computed-priority algorithm to build the sorted list of reviews
def get_study_ranking(username, student_quality):

    studies_folder = os.path.join('users', username, 'studies')
    # Fetches all of the user's studies
    try:
        files = []
        full_list = os.listdir(studies_folder)

        for file in full_list:
            files.append(file)

    except Exception:
        return []


    # Extracting data from each study file
    ranked_list = []
    for study in files:
        study_full_path = os.path.join(studies_folder, study)

        with open(study_full_path, 'r') as f:
            data = f.readlines()
            content_name = data[0].strip().replace("Content: ", "")
            user_assigned_difficulty = float(data[1].strip().replace("Difficulty: ", ""))

            date_added = data[2].strip().replace('Date Added: ', '')
            day_hour = date_added.split(' ')
            day = day_hour[0]
            hour = day_hour[1]

            elapsed_time = delta_time(day, hour) # time difference function

            # For a better priority calculation, I defined a few time bands to tell whether little, some or a lot of time has passed
            if elapsed_time < 4:
                tv = 10.0
            elif 4 <= elapsed_time < 12:
                tv = 9.2
            elif 12 <= elapsed_time < 24:
                tv = 8.0
            elif 24 <= elapsed_time < 48:
                tv = 7.0
            elif 48 <= elapsed_time < 96:
                tv = 5.5
            elif 96 <= elapsed_time < 240:
                tv = 2.0
            else:
                tv = 0.5


            # The higher the result, the lower the need to review the content
            computed_priority = student_quality* 0.2 + user_assigned_difficulty * 0.5 + elapsed_time *0.5

            # Adds it to the list
            ranked_list.append([computed_priority, content_name])


    ranked_list.sort(key=lambda x: x[0])

    return ranked_list









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


    num_acessos = count_access(nome_usuario)
    
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


        ranking = get_study_ranking(nome_usuario, qualidade_aluno)
        
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
            register_content(nome_usuario)
            
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
            usuario_logado = login()
            
            if usuario_logado:
                menu_usuario(usuario_logado)

        elif escolha == "2":
            sign_up()
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