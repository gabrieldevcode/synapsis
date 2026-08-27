# Synapsis

Gerenciador de estudos por repetição espaçada que roda inteiro no terminal, em
Python puro, sem instalar nada além do próprio Python.

O Synapsis guarda o que você estudou, mede o quanto você domina cada assunto e
usa isso para montar uma fila de revisão — em vez de deixar a decisão do "o que
eu reviso hoje?" para a sua memória, que é justamente a parte que está falhando.

Este é o projeto de conclusão da disciplina de **Computação 1**.

> **Privacidade:** a pasta `usuarios/`, onde ficam os perfis e todos os
> conteúdos cadastrados, **não** faz parte deste repositório — está no
> `.gitignore`. Um clone novo vem sem nenhum dado de estudante. Para ver o
> programa funcionando com conteúdo, existe um gerador de usuário fictício,
> descrito em [Uso rápido](#-uso-rápido).

![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![Licença](https://img.shields.io/badge/licença-MIT-green)
![Dependências](https://img.shields.io/badge/dependências-nenhuma-lightgrey)

---

## Índice

- [O problema](#-o-problema)
- [Como funciona, em uma passada](#-como-funciona-em-uma-passada)
- [Instalação](#-instalação)
- [Uso rápido](#-uso-rápido)
- [O perfil do estudante](#-o-perfil-do-estudante)
- [Cadastrando um conteúdo](#-cadastrando-um-conteúdo)
- [O ranking de prioridades](#-o-ranking-de-prioridades)
- [A revisão e o quiz](#-a-revisão-e-o-quiz)
- [Formato dos arquivos](#-formato-dos-arquivos)
- [Rede de segurança](#-rede-de-segurança)
- [Arquitetura](#-arquitetura)
- [Privacidade e segurança](#-privacidade-e-segurança)
- [Testes](#-testes)
- [Limites conhecidos](#-limites-conhecidos)
- [Licença](#-licença)

---

## 🎯 O problema

Quem estuda várias matérias ao mesmo tempo acumula três problemas que não são de
conteúdo, e sim de organização.

**O material se espalha.** O PDF da aula está em `Downloads`, o vídeo está num
link perdido no histórico, o resumo está num caderno e a lista de exercícios
está no e-mail. Na hora de revisar, metade do tempo vai embora só reunindo as
peças — e essa fricção é motivo suficiente para não revisar.

**A escolha do que revisar é péssima.** Deixado por conta própria, o estudante
revisa o que é confortável: a matéria que ele já entende, porque revisar aquilo
dá a sensação boa de estar indo bem. O conteúdo que ele não domina é justamente
o que ele evita, e é justamente o que precisaria de revisão.

**O esquecimento não avisa.** A queda de retenção é silenciosa. Não existe
notificação de "você esqueceu Recursividade"; você só descobre na prova.

O Synapsis ataca os três. Cada conteúdo cadastrado carrega, num único arquivo, o
resumo, os caminhos dos materiais, os links das videoaulas e um quiz que o
próprio estudante escreveu enquanto o assunto ainda estava fresco. E, em vez de
mostrar essa lista em ordem alfabética ou de cadastro, o programa a ordena por
uma prioridade calculada a partir de três coisas: o quanto o estudante domina
aquele assunto, há quanto tempo ele viu aquilo, e o perfil geral dele como
estudante.

Ou seja: a fila de revisão é montada pelo programa, não pela vontade do dia.

---

## 🔭 Como funciona, em uma passada

```
                         python synapsis.py
                                 │
                      inicializar_programa()  ──► cria usuarios/ se não existir
                                 │
                       mostrar_introducao()
                                 │
                              main()  ─── Menu Principal ───┐
                                 │                          │
                ┌────────────────┴────────────────┐         │
                ▼                                 ▼         │
       processo_cadastro()               processo_login()   │
                │                                 │         │
     coeficiente_rendimento()             até 3 tentativas  │
     5 perguntas ponderadas → CR                  │         │
                │                                 │         │
                └──► usuarios/<nome>/pessoal_<nome>.txt     │
                                 │                          │
                                 └──► menu_usuario(nome) ◄──┘
                                            │
                                  contador_acessos()   ──► +1 no perfil
                                            │
                                  obter_ranking_estudos()
                                       │         │
                              delta_time()   dificuldade gravada
                                       └────┬────┘
                                            ▼
                              fila ordenada por prioridade
                                            │
         ┌──────────────────────────────────┼──────────────────────────────┐
         ▼                                  ▼                              ▼
 cadastrar_novo_conteudo()        revisar_conteudo()          listar_editar_deletar()
         │                                  │                              │
  3 notas + quiz +              resumo, anexos, links            visualizar / editar
  anexos + links                 e quiz corrigido                resumo / renomear /
         │                                                            deletar
         ▼
 usuarios/<nome>/estudos/<Conteudo>.txt
```

Não há banco de dados, servidor nem rede. O estado inteiro do programa são
arquivos `.txt` dentro de `usuarios/`.

---

## 📦 Instalação

**Requisito único:** Python 3.6 ou superior. Nenhuma biblioteca externa — o
programa usa só `os`, `time`, `datetime` e `ast`, todos da biblioteca padrão.

```bash
git clone https://github.com/gabrieldevcode/synapsis.git
cd synapsis
python synapsis.py
```

Em algumas distribuições Linux e no macOS o comando é `python3`:

```bash
python3 synapsis.py
```

O programa cria a pasta `usuarios/` sozinho no primeiro acesso. Se ele não
conseguir (permissão negada na pasta), avisa e encerra em vez de continuar num
estado quebrado.

### Sobre o terminal

A interface desenha molduras com o caractere `═` (U+2550). Terminais modernos
(Windows Terminal, VS Code, GNOME Terminal, iTerm2) mostram isso sem ajuste. No
`cmd.exe` antigo, se aparecerem caracteres estranhos no lugar das linhas:

```bat
chcp 65001
```

---

## 🚀 Uso rápido

Um clone novo não tem nenhum estudante cadastrado, então o ranking abre vazio.
Para ver o programa com conteúdo já dentro, gere um usuário de demonstração:

```bash
python exemplos/gerar_usuario_demo.py
```

Ele cria o estudante `demo` (senha `demo123`) com quatro matérias de Computação 1
cadastradas em datas diferentes, para que o ranking tenha o que ordenar. Os
dados são inventados.

Depois é só rodar o programa, escolher **1. Login** e entrar com `demo` /
`demo123`:

```
════════════════════════════════════════════════════════════
                          Olá demo
════════════════════════════════════════════════════════════
                   Estudos Cadastrados: 4
                         Acessos: 2
════════════════════════════════════════════════════════════
Ranking de Prioridades:
PRIORIDADE   | CONTEÚDO
------------------------------------------------------------
1            | Estruturas Condicionais
2            | Laços de Repetição
3            | Manipulação de Arquivos
4            | Recursividade
════════════════════════════════════════════════════════════
1. Cadastrar novo conteúdo
2. Revisar Conteúdo
3. Listar conteúdos (Visualizar / Editar / Deletar)
4. Sair
════════════════════════════════════════════════════════════
Escolha:
```

Para apagar a demonstração, basta remover a pasta: `rm -rf usuarios/demo`
(ou `rmdir /s usuarios\demo` no `cmd.exe`).

---

## 📊 O perfil do estudante

No cadastro, antes de qualquer conteúdo, o programa aplica um questionário de
cinco perguntas, todas em escala de 1 a 10. O resultado é o **coeficiente de
rendimento (CR)** do estudante, gravado no perfil e usado depois no ranking.

Os pesos **não são iguais**, e essa é uma escolha de projeto, não um descuido:

| # | O que a pergunta mede | Peso |
|---|---|---|
| 1 | Constância na rotina, mesmo sem motivação | 0.10 |
| 2 | Persistência diante de conteúdo complexo | 0.20 |
| 3 | Uso de **métodos ativos** (exercícios, explicar em voz alta, resumir) | **0.30** |
| 4 | Capacidade de **conectar teoria a aplicação prática** | **0.30** |
| 5 | Proatividade para buscar respostas sozinho | 0.10 |

As perguntas 3 e 4 pesam três vezes mais que a primeira porque são as que mais
se correlacionam com retenção real. Estudo ativo fixa mais que leitura passiva, e
quem consegue enxergar para que serve um conteúdo abstrato ancora ele em algo
que não se apaga junto com a memória de curto prazo. Constância importa, mas
constância aplicada a um método ruim rende pouco.

```
CR = p1×0.10 + p2×0.20 + p3×0.30 + p4×0.30 + p5×0.10
```

Como os pesos somam 1.0, o CR fica sempre na mesma escala das respostas: de 1
(baixa absorção) a 10 (excelente compreensão).

---

## ✍️ Cadastrando um conteúdo

Ao cadastrar, o programa pede nome e resumo e faz três perguntas de 1 a 10:

| Pergunta | Variável | Peso |
|---|---|---|
| "Se você precisasse dar uma aula sobre isso agora, quão bem você se sairia?" | domínio | 0.5 |
| "O quanto esse assunto é fundamental para seus objetivos atuais?" | relevância | 0.3 |
| "O quanto você realmente gosta de aprender sobre isso?" | engajamento | 0.2 |

```
dificuldade = domínio×0.5 + relevância×0.3 + engajamento×0.2
```

Repare no sentido do número: **quanto maior, mais confortável você está com o
assunto**. Um valor alto significa que você daria a aula, o tema é relevante e
você gosta dele — logo, precisa de menos revisão. Um valor baixo é o sinal de
alerta. O ranking usa isso diretamente.

Em seguida, três laços opcionais, cada um repetindo enquanto você responder `S`:

1. **Quiz** — pares de pergunta e resposta escritos por você, agora, enquanto o
   assunto está fresco. É o material da revisão futura.
2. **Arquivos locais** — caminhos de PDFs, slides, imagens. O programa guarda o
   caminho, nunca copia o arquivo.
3. **Videoaulas** — links.

Tudo vai para um único `.txt` dentro de `usuarios/<você>/estudos/`.

---

## 🏆 O ranking de prioridades

É o núcleo do programa. Toda vez que a área do estudante é desenhada, o Synapsis
lê todos os conteúdos cadastrados, calcula uma prioridade para cada um e ordena.

Para cada conteúdo, `delta_time()` converte a data de cadastro em horas
decorridas, e então:

```
prioridade = CR×0.2 + dificuldade×0.5 + horas_decorridas×0.5
```

A lista é ordenada de forma **crescente**, e a posição 1 é a primeira a revisar.
Como a `dificuldade` cresce com o seu domínio, o conteúdo em que você se sai pior
produz o menor score e sobe para o topo da fila — que é exatamente o
comportamento desejado, e o que o teste
`test_menor_dominio_aparece_primeiro` trava.

O CR entra com peso 0.2 e é o mesmo para todos os conteúdos do estudante, então
ele desloca todos os scores juntos sem nunca mudar a ordem entre eles. Ele existe
para calibrar a escala do estudante, não para reordenar a fila.

### As faixas temporais

O programa também classifica o tempo decorrido em sete faixas, com um valor
associado a cada uma:

| Tempo desde o cadastro | Valor da faixa |
|---|---|
| menos de 4 h | 10.0 |
| 4 h a 12 h | 9.2 |
| 12 h a 24 h | 8.0 |
| 24 h a 48 h | 7.0 |
| 48 h a 96 h | 5.5 |
| 96 h a 240 h | 2.0 |
| mais de 240 h (10 dias) | 0.5 |

O desenho é o de uma curva de esquecimento: o valor cai rápido nas primeiras
horas e desaba depois de dez dias. **Essas faixas estão calculadas mas ainda não
entram no cálculo do score** — hoje quem entra na fórmula é o número bruto de
horas. Está descrito em [Limites conhecidos](#-limites-conhecidos), junto com a
consequência prática disso.

---

## 🔁 A revisão e o quiz

A opção **2. Revisar Conteúdo** abre um conteúdo, mostra o resumo e reúne os
materiais num lugar só:

```
             Revisando: Estruturas_Condicionais
════════════════════════════════════════════════════════════
Resumo:
if/elif/else, operadores de comparacao e encadeamento de condicoes. Cuidado
com o uso de = no lugar de == dentro do if.

Voce pode copiar os caminhos relativos abaixo, colocar em seu explorador de
arquivos e visualizar conteudos da matéria
Arquivos anexados:
 - materiais/computacao1/aula03_condicionais.pdf
Vídeos relacionados ao conteudo:
 - https://exemplo.invalido/aula-condicionais
════════════════════════════════════════════════════════════
```

Depois vem o quiz que você mesmo escreveu no cadastro, corrigido pergunta a
pergunta:

```
                      Quiz de Revisão
════════════════════════════════════════════════════════════
Pergunta 1: Qual operador compara igualdade em Python?
Resposta: ==
Correto!
════════════════════════════════════════════════════════════
Pergunta 2: O bloco else e obrigatorio depois de um if?
Resposta: sim
Errado. Resposta correta: nao
════════════════════════════════════════════════════════════
Você acertou 1 de 2 (50.0%).
```

A comparação ignora maiúsculas/minúsculas e espaços nas pontas, mas exige o
texto certo — não há tolerância a sinônimos.

---

## 📄 Formato dos arquivos

Todo o estado do programa é texto legível. Dá para abrir, ler e corrigir com
qualquer editor.

### `usuarios/<nome>/pessoal_<nome>.txt`

Quatro linhas, sempre nesta ordem, lidas por índice:

```
demo
demo123
6.700
2
```

| Linha | Conteúdo |
|---|---|
| 1 | nome de usuário |
| 2 | senha (texto puro — veja [Limites conhecidos](#-limites-conhecidos)) |
| 3 | coeficiente de rendimento, 3 casas decimais |
| 4 | total de acessos à área do estudante |

### `usuarios/<nome>/estudos/<Conteudo>.txt`

Cabeçalho de quatro linhas fixas, seguido de três seções nomeadas e separadas
por uma linha de hífens. Cada seção tem tamanho variável:

```
Conteudo: Estruturas Condicionais
Dificuldade: 8.4
Data de Inclusao: 27/08/2026 13:51
Resumo: if/elif/else, operadores de comparacao e encadeamento de condicoes.
--------------------
QUIZ:
['Qual operador compara igualdade em Python?', '==']
['O bloco else e obrigatorio depois de um if?', 'nao']
--------------------
ARQUIVOS:
materiais/computacao1/aula03_condicionais.pdf
--------------------
VIDEO-AULAS:
https://exemplo.invalido/aula-condicionais
```

A data segue `%d/%m/%Y %H:%M` — é o formato que `delta_time()` espera, e alterar
isso à mão quebra o ranking daquele conteúdo. Cada linha do quiz é a
representação Python de uma lista `[pergunta, resposta]`, relida com
`ast.literal_eval` (veja [Arquitetura](#-arquitetura)).

---

## 🛡️ Rede de segurança

O que o programa valida e recusa, em vez de aceitar e quebrar depois:

| Situação | O que acontece |
|---|---|
| Nota fora da escala de 1 a 10 | Repergunta até receber um valor válido |
| Texto onde se espera um número | Repergunta, sem estourar exceção |
| Senha vazia no cadastro | Recusa e volta ao menu |
| Nome de usuário já existente | Recusa e sugere login |
| Login com usuário inexistente | Avisa e volta ao menu |
| Senha errada | Até 3 tentativas, depois volta ao menu |
| Opção de menu inválida | Avisa e redesenha o menu |
| Resposta que não seja `S` ou `N` | Repergunta |
| Escolher item fora da lista | Avisa e volta |
| Deletar um conteúdo | Exige digitar `SIM`, em maiúsculas, por extenso |
| Arquivo de perfil ausente ou corrompido | Mensagem de erro, sem derrubar o programa |
| Linha de quiz malformada no `.txt` | É ignorada; a revisão continua |
| Sem permissão para criar `usuarios/` | Avisa e encerra, em vez de seguir quebrado |

---

## 🏗️ Arquitetura

Um único módulo, `synapsis.py`, organizado em blocos por responsabilidade.

| Função | Papel |
|---|---|
| `limpar_terminal`, `linha`, `cabecalho`, `delay_texto`, `enter_para_pular` | Camada de apresentação: tudo que desenha na tela passa por aqui |
| `inicializar_programa` | Garante a pasta `usuarios/` antes de qualquer coisa |
| `mostrar_introducao` | Tela de abertura |
| `obter_resposta_verificada` | Porta de entrada única para toda nota de 1 a 10 |
| `coeficiente_rendimento` | Aplica o questionário e devolve o CR |
| `processo_cadastro` / `processo_login` | Criam e autenticam o estudante |
| `contador_acessos` | Incrementa e persiste o total de acessos |
| `delta_time` | Converte data de cadastro em horas decorridas |
| `cadastrar_novo_conteudo` | Coleta notas, quiz, anexos e links; grava o `.txt` |
| `obter_ranking_estudos` | Lê todos os conteúdos e devolve a fila ordenada |
| `revisar_conteudo` | Faz o parse do `.txt`, exibe o material e aplica o quiz |
| `listar_editar_deletar` | Visualizar, editar resumo, renomear e apagar |
| `menu_usuario` | Área do estudante: junta ranking e menu |
| `main` | Menu principal e laço da aplicação |

### Decisões de projeto

**Persistência em texto puro, sem banco e sem dependências.** A pasta é o banco:
cada estudante é um diretório, cada conteúdo é um arquivo. Isso custa
concorrência, índice e consulta — não dá para perguntar "todos os conteúdos com
dificuldade abaixo de 4" sem varrer tudo, e é por isso que `obter_ranking_estudos`
relê a pasta inteira a cada desenho de tela. Em troca, o programa roda em
qualquer máquina com Python e nada mais, o estado inteiro é inspecionável com um
editor de texto, e um arquivo corrompido derruba um conteúdo em vez do sistema.
Para o volume real de um estudante — dezenas de conteúdos, não milhões — a
varredura completa é irrelevante e a legibilidade vale mais.

**`ast.literal_eval` em vez de `eval` para reler o quiz.** O quiz é gravado como
a representação Python de uma lista e precisa voltar a ser lista na leitura.
`eval` faria isso em uma linha — e executaria como código qualquer coisa que
estivesse naquele arquivo. Como o formato é texto puro que o próprio README
convida a editar, isso seria transformar uma anotação de estudo em vetor de
execução. `literal_eval` só aceita literais: uma linha adulterada vira erro, não
comando. E o erro é capturado, então a linha é descartada e a revisão segue.

**O parser da revisão é uma máquina de estados por seção.** As três seções
(`QUIZ:`, `ARQUIVOS:`, `VIDEO-AULAS:`) têm tamanho variável, então ler por número
de linha quebraria assim que alguém adicionasse uma pergunta. `revisar_conteudo`
percorre o arquivo mantendo o registro de qual seção está aberta, e cada linha é
interpretada conforme esse contexto. Linhas de separador são puladas e linhas
que não encaixam são ignoradas em silêncio — o arquivo é editável à mão, então o
parser é tolerante por necessidade, não por descuido.

**Anexos são referências, nunca cópias.** O programa guarda o caminho do PDF ou
do slide, e nunca copia, move ou abre o arquivo. O estudante continua dono da
organização das próprias pastas, o Synapsis não duplica gigabytes de material, e
não existe caminho de código em que ele possa corromper um arquivo que não seja
dele. O preço é que mover o material quebra a referência — um preço aceitável
diante da alternativa de um programa de estudos mexendo nos seus arquivos.

---

## 🔒 Privacidade e segurança

A pasta `usuarios/` está no `.gitignore` e nunca deve ser versionada. Ela contém
nome, senha e todo o material de estudo de cada pessoa cadastrada.

**As senhas são gravadas em texto puro.** Isto é um projeto acadêmico de
Computação 1, e armazenamento seguro de credenciais (hash com sal, algo como
`bcrypt` ou `argon2`) está fora do escopo da disciplina. A consequência prática é
direta: **não use aqui uma senha que você use em qualquer outro lugar.** Qualquer
pessoa com acesso à pasta lê a senha abrindo um `.txt`.

Pelo mesmo motivo, o login serve para separar perfis num computador compartilhado
— não é um controle de acesso. Não há criptografia, e apagar a pasta do usuário
apaga tudo dele.

---

## 🧪 Testes

A suíte cobre as regras que quebram em silêncio: cálculo de tempo decorrido,
montagem e ordenação do ranking, contagem de acessos, validação das notas e o
formato de ida e volta do arquivo de estudo.

```bash
python -m unittest discover -s tests -v
```

```
Ran 19 tests in 0.397s

OK
```

Todo teste roda dentro de um diretório temporário — a suíte **não toca a pasta
`usuarios/` real** e não acessa a rede. Como o Synapsis resolve os caminhos a
partir do diretório de trabalho, cada caso faz `chdir` para um `tempdir` no
`setUp` e volta no `tearDown`.

Para testar o programa à mão sem sujar seus dados, use o usuário `demo` do
gerador de exemplo e apague a pasta depois.

---

## ⚠️ Limites conhecidos

**Senha em texto puro.** Descrito em
[Privacidade e segurança](#-privacidade-e-segurança). É a limitação mais séria e
a única com consequência fora do programa.

**As faixas temporais não entram no score.** `obter_ranking_estudos` calcula a
faixa de tempo (a tabela em [O ranking](#-o-ranking-de-prioridades)) mas usa o
número bruto de horas na fórmula. Como esse termo cresce sem limite, um conteúdo
cadastrado há 15 dias soma `360×0.5 = 180` pontos e vai parar no fim da fila —
quando deveria estar no começo, que é exatamente para o que as faixas foram
desenhadas. Na prática, hoje o ranking prioriza bem por domínio e mal por tempo.
Trocar `horas_decorridas` pelo valor da faixa na fórmula é a correção.

**Renomear um conteúdo não atualiza o nome interno.** A opção 3 renomeia o
arquivo, mas a linha `Conteudo:` dentro dele continua com o nome antigo. O
resultado é que a listagem mostra o nome novo e o ranking continua mostrando o
antigo. Corrigir o texto da primeira linha do `.txt` resolve.

**Nomes de conteúdo viram nomes de arquivo.** Espaços viram `_`, mas caracteres
que o sistema operacional proíbe (`\ / : * ? " < > |`) fazem a gravação falhar
com uma mensagem de erro. Cadastrar dois conteúdos com o mesmo nome sobrescreve
o primeiro, sem aviso.

**O encoding não é declarado.** Leitura e escrita usam o padrão da plataforma
(cp1252 no Windows, UTF-8 na maioria dos Linux). Uma pasta `usuarios/` criada no
Windows e lida no Linux embaralha os acentos, e rodar com `PYTHONUTF8=1` sobre
dados antigos causa `UnicodeDecodeError`. Passar `encoding='utf-8'` em todos os
`open()` resolveria, ao custo de migrar os arquivos já existentes.

**O score é calculado mas não é exibido.** A tela mostra só a posição na fila,
não o valor da prioridade.

**O quiz não pode ser editado depois de criado.** A opção 3 do menu permite
alterar resumo e nome; para mudar uma pergunta é preciso editar o `.txt` à mão.

**Não há exclusão de usuário pelo programa.** Apagar a pasta do estudante é a
única forma.

---

## 📜 Licença

[MIT](LICENSE) — Gabriel Robalinho.
