import pandas as pd
import os
import subprocess

# Diretório de entrada
arquivo_excel = './registro.xlsx'
# Criando objeto ExcelFile
xls = pd.ExcelFile(arquivo_excel)
# Diretórios de entrada e saída
diretorio_moveis = './registro/moveis'
diretorio_fixas = './registro/fixas'
diretorio_saida = './registro/saida'
i = 0

for planilha in xls.sheet_names:
    # Carregando a planilha Excel
    df = pd.read_excel(xls, sheet_name=planilha)
    i += 1
    print(f"Lote {i}: {planilha} ")
    # Diretório de saída específico para a planilha atual
    diretorio_planilha = os.path.join(diretorio_saida, planilha)
    # Criar o diretório se não existir
    os.makedirs(diretorio_planilha, exist_ok=True)

    # Iterar sobre as linhas da tabela
    for index, coluna in df.iterrows():
        # Construir o caminho para os arquivos movéis considerando o diretório da planilha
        movel_defeituosos = os.path.join(diretorio_moveis, planilha, coluna['Pré-ID (Defeituosos)'] + '.nii.gz')
        movel_saudaveis = os.path.join(diretorio_moveis, planilha, coluna['Pré-ID (Saudáveis)'] + '.nii.gz')
        fixa = os.path.join(diretorio_fixas, coluna['Registrada em:'] + '.nii.gz')
        id_defeituosos = os.path.join(diretorio_planilha, coluna['ID (Defeituosos)'] + '.nii.gz')
        id_saudaveis = os.path.join(diretorio_planilha, coluna['ID (Saudáveis)'] + '.nii.gz')

        if os.path.exists(id_defeituosos) and os.path.exists(id_saudaveis):
            print(f"Arquivos já existem para a linha {index + 1} da planilha {planilha}.")
            continue

        # Comando antsRegistrationSyNQuick.sh
        comando = [
            'antsRegistrationSyNQuick.sh',
            '-d', '3',
            '-f', fixa,
            '-m', movel_defeituosos,
            '-o', id_defeituosos,
            '-n', '8',
            '-p', 'f',
            '-t', 'a'
        ]
        # Executar o comando
        subprocess.run(comando)
        print(f"Removendo arquivo .mat {id_defeituosos}0GenericAffine.mat.")
        os.remove(id_defeituosos + '0GenericAffine.mat')

        # Comando antsRegistrationSyNQuick.sh
        comando = [
            'antsRegistrationSyNQuick.sh',
            '-d', '3',
            '-f', fixa,
            '-m', movel_saudaveis,
            '-o', id_saudaveis,
            '-n', '8',
            '-p', 'f',
            '-t', 'a'
        ]
        # Executar o comando
        subprocess.run(comando)
        print(f"Removendo arquivo .mat {id_saudaveis}0GenericAffine.mat.")
        os.remove(id_saudaveis + '0GenericAffine.mat')

print("Registros concluídos.")
