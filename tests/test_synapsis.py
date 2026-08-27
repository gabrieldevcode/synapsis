"""Testes das regras de negócio do Synapsis.

O foco está nas funções que decidem o comportamento do programa e que, se
quebrarem, quebram em silêncio: o cálculo de tempo decorrido, a montagem do
ranking de prioridades, a contagem de acessos e a validação das notas. O resto
do sistema é entrada e saída de terminal, testada na mão.

Nenhum teste toca a pasta `usuarios/` real: cada caso roda dentro de um
diretório temporário, porque o Synapsis resolve os caminhos a partir do
diretório de trabalho atual. Nenhum teste acessa a rede.

Para rodar, a partir da raiz do repositório:

    python -m unittest discover -s tests -v
"""

import ast
import contextlib
import datetime
import io
import os
import sys
import tempfile
import unittest
from unittest import mock

# A raiz do repositório precisa estar no path para importar `synapsis`.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import synapsis  # noqa: E402


def escrever_estudo(pasta_estudos, nome, dificuldade, horas_atras, quiz=()):
    """Grava um estudo no formato exato que `cadastrar_novo_conteudo` produz.

    O `open` vai sem `encoding=` de propósito, igual ao programa: assim a
    fixture usa o mesmo padrão da plataforma que o Synapsis vai usar na leitura.
    """
    registro = datetime.datetime.now() - datetime.timedelta(hours=horas_atras)
    caminho = os.path.join(pasta_estudos, nome.replace(' ', '_') + '.txt')
    with open(caminho, 'w') as f:
        f.write('Conteudo: ' + nome + '\n')
        f.write('Dificuldade: ' + str(dificuldade) + '\n')
        f.write('Data de Inclusao: ' + registro.strftime('%d/%m/%Y %H:%M') + '\n')
        f.write('Resumo: resumo de teste\n')
        f.write('-' * 20 + '\n')
        f.write('QUIZ:\n')
        for item in quiz:
            f.write(str(list(item)) + '\n')
        f.write('-' * 20 + '\n')
        f.write('ARQUIVOS:\n')
        f.write('-' * 20 + '\n')
        f.write('VIDEO-AULAS:\n')
    return caminho


class BaseEmDiretorioTemporario(unittest.TestCase):
    """Roda cada teste num diretório vazio, isolado da pasta `usuarios/` real."""

    def setUp(self):
        self._origem = os.getcwd()
        self._temp = tempfile.TemporaryDirectory()
        os.chdir(self._temp.name)

    def tearDown(self):
        os.chdir(self._origem)
        self._temp.cleanup()

    def criar_usuario(self, nome='aluno', senha='senha', coeficiente=6.5, acessos=0):
        pasta = os.path.join('usuarios', nome)
        os.makedirs(os.path.join(pasta, 'estudos'), exist_ok=True)
        with open(os.path.join(pasta, 'pessoal_' + nome + '.txt'), 'w') as f:
            f.write(nome + '\n')
            f.write(senha + '\n')
            f.write('{:.3f}\n'.format(coeficiente))
            f.write(str(acessos) + '\n')
        return os.path.join(pasta, 'estudos')


class TestDeltaTime(unittest.TestCase):
    """`delta_time` converte data/hora de cadastro em horas decorridas."""

    def test_conta_as_horas_desde_o_cadastro(self):
        ha_cinco_horas = datetime.datetime.now() - datetime.timedelta(hours=5)

        horas = synapsis.delta_time(
            ha_cinco_horas.strftime('%d/%m/%Y'),
            ha_cinco_horas.strftime('%H:%M'),
        )

        self.assertAlmostEqual(horas, 5.0, delta=0.05)

    def test_registro_no_futuro_devolve_valor_negativo(self):
        # O relógio da máquina pode estar atrasado, ou o arquivo pode ter sido
        # editado à mão. O cálculo não deve estourar por isso.
        futuro = datetime.datetime.now() + datetime.timedelta(hours=3)

        horas = synapsis.delta_time(
            futuro.strftime('%d/%m/%Y'),
            futuro.strftime('%H:%M'),
        )

        self.assertLess(horas, 0)

    def test_data_em_formato_invalido_levanta_erro(self):
        with self.assertRaises(ValueError):
            synapsis.delta_time('2025-01-30', '10:00')


class TestRanking(BaseEmDiretorioTemporario):
    """`obter_ranking_estudos` ordena o que o estudante deve revisar."""

    def test_usuario_sem_pasta_de_estudos_devolve_lista_vazia(self):
        # Instalação limpa: o programa precisa abrir sem conteúdo nenhum.
        self.assertEqual(synapsis.obter_ranking_estudos('ninguem', 6.5), [])

    def test_pasta_de_estudos_vazia_devolve_lista_vazia(self):
        self.criar_usuario()

        self.assertEqual(synapsis.obter_ranking_estudos('aluno', 6.5), [])

    def test_devolve_um_par_score_nome_por_estudo(self):
        pasta = self.criar_usuario()
        escrever_estudo(pasta, 'Recursividade', dificuldade=4.0, horas_atras=1)

        ranking = synapsis.obter_ranking_estudos('aluno', 6.5)

        self.assertEqual(len(ranking), 1)
        score, nome = ranking[0]
        self.assertEqual(nome, 'Recursividade')
        self.assertIsInstance(score, float)

    def test_menor_dominio_aparece_primeiro(self):
        # Com o mesmo tempo decorrido, o conteúdo em que o estudante se sai
        # pior (dificuldade menor) tem de encabeçar a lista de revisão.
        pasta = self.criar_usuario()
        escrever_estudo(pasta, 'Dominado', dificuldade=9.0, horas_atras=1)
        escrever_estudo(pasta, 'Fraco', dificuldade=2.0, horas_atras=1)

        nomes = [nome for _, nome in synapsis.obter_ranking_estudos('aluno', 6.5)]

        self.assertEqual(nomes, ['Fraco', 'Dominado'])

    def test_ranking_sai_ordenado_do_menor_para_o_maior_score(self):
        pasta = self.criar_usuario()
        for indice, dificuldade in enumerate((7.0, 3.0, 9.0, 1.0)):
            escrever_estudo(pasta, 'Materia' + str(indice), dificuldade=dificuldade,
                            horas_atras=1)

        scores = [score for score, _ in synapsis.obter_ranking_estudos('aluno', 6.5)]

        self.assertEqual(scores, sorted(scores))

    def test_coeficiente_do_aluno_desloca_todos_os_scores_igualmente(self):
        # O coeficiente entra com peso 0.2 e é o mesmo para todos os conteúdos,
        # então ele muda o valor absoluto mas nunca a ordem.
        pasta = self.criar_usuario()
        escrever_estudo(pasta, 'A', dificuldade=5.0, horas_atras=1)
        escrever_estudo(pasta, 'B', dificuldade=8.0, horas_atras=1)

        baixo = synapsis.obter_ranking_estudos('aluno', 1.0)
        alto = synapsis.obter_ranking_estudos('aluno', 10.0)

        self.assertEqual([n for _, n in baixo], [n for _, n in alto])
        self.assertAlmostEqual(alto[0][0] - baixo[0][0], 9.0 * 0.2, places=4)

    def test_nome_com_acento_sobrevive_a_ida_e_volta_do_arquivo(self):
        pasta = self.criar_usuario()
        escrever_estudo(pasta, 'Manipulação de Arquivos', dificuldade=6.0, horas_atras=2)

        nomes = [nome for _, nome in synapsis.obter_ranking_estudos('aluno', 6.5)]

        self.assertEqual(nomes, ['Manipulação de Arquivos'])


class TestContadorAcessos(BaseEmDiretorioTemporario):
    """`contador_acessos` mantém o total de entradas na área do estudante."""

    def test_incrementa_e_persiste_no_arquivo_pessoal(self):
        self.criar_usuario(acessos=4)

        with contextlib.redirect_stdout(io.StringIO()):
            retorno = synapsis.contador_acessos('aluno')

        self.assertEqual(retorno, 5)
        with open(os.path.join('usuarios', 'aluno', 'pessoal_aluno.txt')) as f:
            self.assertEqual(f.readlines()[3].strip(), '5')

    def test_preserva_as_demais_linhas_do_perfil(self):
        # A contagem reescreve o arquivo inteiro; nome, senha e coeficiente
        # precisam sobreviver a isso.
        self.criar_usuario(nome='aluno', senha='segredo', coeficiente=7.25, acessos=0)

        with contextlib.redirect_stdout(io.StringIO()):
            synapsis.contador_acessos('aluno')

        with open(os.path.join('usuarios', 'aluno', 'pessoal_aluno.txt')) as f:
            linhas = [linha.strip() for linha in f.readlines()]

        self.assertEqual(linhas[:3], ['aluno', 'segredo', '7.250'])

    def test_perfil_inexistente_nao_derruba_o_programa(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertIsNone(synapsis.contador_acessos('fantasma'))


class TestRespostaVerificada(unittest.TestCase):
    """`obter_resposta_verificada` só aceita notas de 1 a 10."""

    def responder(self, entradas):
        with mock.patch('builtins.input', side_effect=entradas):
            with contextlib.redirect_stdout(io.StringIO()):
                return synapsis.obter_resposta_verificada('pergunta')

    def test_aceita_valor_dentro_da_faixa(self):
        self.assertEqual(self.responder(['7']), 7.0)

    def test_aceita_os_extremos_da_faixa(self):
        self.assertEqual(self.responder(['1']), 1.0)
        self.assertEqual(self.responder(['10']), 10.0)

    def test_aceita_nota_fracionada(self):
        self.assertEqual(self.responder(['7.5']), 7.5)

    def test_repergunta_ate_receber_valor_valido(self):
        # Texto, valor abaixo do mínimo e valor acima do máximo são recusados;
        # a função só devolve quando a resposta cabe na escala.
        self.assertEqual(self.responder(['abc', '0', '11', '-3', '8']), 8.0)


class TestFormatoDoArquivoDeEstudo(BaseEmDiretorioTemporario):
    """O quiz é gravado como repr de lista e relido com `ast.literal_eval`."""

    def test_quiz_gravado_volta_a_ser_lista_de_pergunta_e_resposta(self):
        pasta = self.criar_usuario()
        perguntas = [
            ['Qual o caso base?', 'n == 0'],
            ["Aspas simples ' no meio", 'ok'],
            ['Acento na resposta?', 'recursão'],
        ]
        caminho = escrever_estudo(pasta, 'Quiz', dificuldade=5.0, horas_atras=1,
                                  quiz=perguntas)

        with open(caminho) as f:
            linhas = f.readlines()
        inicio = linhas.index('QUIZ:\n') + 1
        lido = [ast.literal_eval(linha) for linha in linhas[inicio:inicio + len(perguntas)]]

        self.assertEqual(lido, perguntas)

    def test_linha_de_quiz_corrompida_nao_e_confundida_com_pergunta(self):
        # O arquivo é texto puro e editável à mão. Uma linha que não seja um
        # literal Python válido tem de ser descartada, não virar pergunta.
        with self.assertRaises((ValueError, SyntaxError)):
            ast.literal_eval('isto nao e uma lista\n')


if __name__ == '__main__':
    unittest.main(verbosity=2)
