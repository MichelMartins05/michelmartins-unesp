import pandas as pd
import os
import subprocess

# Diretório de entrada
arquivo_excel = './dataset_lotes.xlsx'
# Criando objeto ExcelFile
xls = pd.ExcelFile(arquivo_excel)
# Diretórios de entrada e saída
diretorio_registradas = './registro/saida'
i = 0

for planilha in xls.sheet_names:
    # Carregando a planilha Excel
    df = pd.read_excel(xls, sheet_name=planilha)
    i += 1
    print(f"Lote {i}: {planilha} ")
    # Iterando sobre as linhas da tabela
    for index, coluna in df.iterrows():
        # Construir o caminho para os arquivos movéis considerando o diretório da planilha
        id_defeituosos = os.path.join(diretorio_registradas, planilha, coluna['ID (Defeituosos)'] + '.nii.gz')
        id_saudaveis = os.path.join(diretorio_registradas, planilha, coluna['ID (Saudáveis)'] + '.nii.gz')
        id_def_alinhado = os.path.join(diretorio_registradas, planilha, coluna['ID (Defeituosos)'] + '.nii.gz')

        if not (os.path.exists(id_defeituosos) and os.path.exists(id_saudaveis)):
            continue

        # Comando antsRegistrationSyNQuick.sh
        comando = [
            'antsRegistrationSyNQuick.sh',
            '-d', '3',
            '-f', id_saudaveis,
            '-m', id_defeituosos,
            '-o', id_def_alinhado,
            '-n', '8',
            '-p', 'f',
            '-t', 'a'
        ]
        # Executar o comando
        subprocess.run(comando)
        print(f"Removendo arquivo .mat {id_def_alinhado}0GenericAffine.mat.")
        os.remove(id_def_alinhado + '0GenericAffine.mat')

print("Alinhamentos concluídos.")
