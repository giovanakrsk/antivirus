import os
import sys


def verificar_antivirus_extensao(diretorio):
    extensoes_perigosas = [".exe", ".bat"]

    for pasta_atual, subpastas, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            nome_arquivo, extensao = os.path.splitext(arquivo)
            if extensao in extensoes_perigosas:
                caminho_completo = os.path.join(pasta_atual, arquivo)
                print(f"Arquivo suspeito encontrado: {caminho_completo}")


def verificar_antivirus(diretorio, arquivos_perigosos):
    resultado = []
    for pasta_atual, subpastas, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            if arquivo in arquivos_perigosos:
                caminho_completo = os.path.join(pasta_atual, arquivo)
                resultado.append([arquivo, caminho_completo])
    return resultado


def coletar_referencia(destino=None):
    if destino is None:
        caminho_absoluto = os.path.dirname(__file__)
        pasta_relativa = os.path.join(caminho_absoluto, "ArquivosReferencia")
    else:
        pasta_relativa = destino

    arquivos_perigosos = []

    for pasta_atual, subpastas, arquivos in os.walk(pasta_relativa):
        for arquivo in arquivos:
            arquivos_perigosos += [arquivo]

    return arquivos_perigosos


def create_report(arquivos_perigosos, resultado, removidos):
    with open("Report.txt", "w") as report_file:
        report_file.write(
            """!!!   Relatorio do Ameacas  !!!

McAfreeze Antivirus - Mantenha seu computador sempre frio!

_________________________________
Os arquivos de referencia foram:

"""
        )

        for line in arquivos_perigosos:
            report_file.write(line + "\n")

        report_file.write(
            "\n\n_______ Arquivos encontrados _____________________________________________________________________________________________________________________\n"
        )
        report_file.write(
            "       Arquivo                                                     Endereco\n"
        )
        report_file.write(
            "__________________________________________________________________________________________________________________________________________________\n"
        )
        row_format = "{:<50} {:<50}"
        for line in resultado:
            report_file.write(row_format.format(line[0], line[1]) + "\n")

        report_file.write(
            "\n\n_______ Arquivos removidos _______________________________________________________________________________________________________________________\n"
        )
        for line in removidos:
            report_file.write(row_format.format(line[1][0], line[1][1]) + "\n")


def remover_arquivo(caminho_completo):
    try:
        os.remove(caminho_completo)
        print(f"Arquivo removido: {caminho_completo}")
        return True
    except OSError as e:
        print(f"Falha ao remover o arquivo {caminho_completo}: {e}")
        return False


def find(lst, a):
    for i, x in enumerate(lst):
        if x[0] == a:
            return i
    return -1


def loop_de_interacao(resultado):
    remover = list(enumerate(resultado))
    removidos = []
    while True:
        print("Foram encontrados os seguintes arquivos perigosos:")
        for item in remover:
            row_format = "{:<5} {:<50} {:<50}"
            print(row_format.format(item[0], item[1][0], item[1][1]))

        want_to_remove = input("Voce gostaria de remover algum arquivo? (y/N) ")

        if want_to_remove in ["y", "Y"]:
            remove_number = input("Qual gostaria de remover? ")
            try:
                remove_number = int(remove_number)

                if remove_number in [x[0] for x in remover]:
                    if remover_arquivo(
                        [x[1][1] for x in remover if x[0] == remove_number][0]
                    ):
                        removidos += [remover.pop(find(remover, remove_number))]
                else:
                    print("Por favor, insira uma resposta valida")
            except ValueError:
                print("Por favor, insira uma resposta valida")

        else:
            break
    return removidos


if len(sys.argv) != 2:
    print("Argumentos invalidos!")
    exit()

if not os.path.isdir(sys.argv[1]):
    print("Não é uma pasta valida!")
    exit()

arquivos_perigosos = coletar_referencia()

test_path = sys.argv[1]

resultado = verificar_antivirus(test_path, arquivos_perigosos)

removidos = loop_de_interacao(resultado)

create_report(arquivos_perigosos, resultado, removidos)
