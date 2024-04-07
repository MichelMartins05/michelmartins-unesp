import pandas as pd
import shutil
import os
import random
import nibabel as nib
import numpy as np

def subtracao_booleana(arquivo_saudaveis, arquivo_defeituosos, arquivo_saida):
    try:
        # Carregando imagens de entrada
        img_saudaveis = nib.load(arquivo_saudaveis)
        img_defeituosos = nib.load(arquivo_defeituosos)
        # Obtendo os dados das imagens
        data_saudaveis = img_saudaveis.get_fdata()
        data_defeituosos = img_defeituosos.get_fdata()
        # Subtração booleana
        resultado = np.logical_and(data_saudaveis, np.logical_not(data_defeituosos))
        # Salvando o resultado
        resultado_img = nib.Nifti1Image(resultado.astype(np.uint8), img_saudaveis.affine)
        nib.save(resultado_img, arquivo_saida)

        print(f"Subtração booleana concluída.")
    except Exception as e:
        print(f"Erro ao realizar a subtração booleana: {e}")

# Diretório de entrada e saída
arquivo_excel = './dataset_lotes.xlsx'
diretorio_registradas = './dataset/registro/saida'
diretorio_treinamento = './dataset/processamento/treinamento'
diretorio_validacao = './dataset/processamento/validacao'
diretorio_teste = './dataset/processamento/teste'

if not os.path.exists(diretorio_treinamento):
    os.makedirs(diretorio_treinamento)
if not os.path.exists(diretorio_validacao):
    os.makedirs(diretorio_validacao)
if not os.path.exists(diretorio_teste):
    os.makedirs(diretorio_teste)

# Criando objeto ExcelFile
xls = pd.ExcelFile(arquivo_excel)

for planilha in xls.sheet_names:
    # Carregando a planilha Excel
    df = pd.read_excel(xls, sheet_name=planilha)
    print(f"Lote {planilha}: ")

    # Criando uma lista de índices para aleatorização
    indices = list(range(len(df)))
    random.shuffle(indices)

    # Declarando índices de separação dos subconjuntos
    indice_treinamento = 24 #(24) por classe de região de defeito = 80% do conjunto de dados
    indice_validacao = 27 #(27-24=3) por classe de região de defeito = 15% do conjunto de dados
    indice_teste = 30 #(30-27=3) por classe de região de defeito = 15% do conjunto de dados

    # Iterando sobre os índices aleatorizados
    for index in indices:
        coluna = df.iloc[index]
        arq_defeituosos = os.path.join(diretorio_registradas, planilha, coluna['ID (Defeituosos)'] + '.nii.gz')
        arq_saudaveis = os.path.join(diretorio_registradas, planilha, coluna['ID (Saudáveis)'] + '.nii.gz')
        arq_implantes = os.path.join(diretorio_registradas, planilha, coluna['ID (Implantes)'] + '.nii.gz')

        # Separação dos subconjuntos e subtração booleana
        if os.path.exists(arq_defeituosos) and os.path.exists(arq_saudaveis):
            if index < indice_treinamento:  # treinamento
                destino_treinamento_defeituosos = os.path.join(diretorio_treinamento, 'defeituosos')
                destino_treinamento_saudaveis = os.path.join(diretorio_treinamento, 'saudaveis')
                destino_treinamento_implantes = os.path.join(diretorio_treinamento, 'implantes')
                os.makedirs(destino_treinamento_defeituosos, exist_ok=True)
                os.makedirs(destino_treinamento_saudaveis, exist_ok=True)
                os.makedirs(destino_treinamento_implantes, exist_ok=True)
                shutil.copy(arq_defeituosos, destino_treinamento_defeituosos)
                shutil.copy(arq_saudaveis, destino_treinamento_saudaveis)
                resultado_subtracao = os.path.join(destino_treinamento_implantes, coluna['ID (Implantes)'] + '.nii.gz')
                #subtracao_booleana(arq_saudaveis, arq_defeituosos, resultado_subtracao)
                print(
                    f"Trios separados para treinamento: {coluna['ID (Defeituosos)']} - {coluna['ID (Saudáveis)']} - {coluna['ID (Implantes)']}")
            elif indice_treinamento <= index < indice_validacao:  # validação
                destino_avaliacao_defeituosos = os.path.join(diretorio_validacao, 'defeituosos')
                destino_avaliacao_saudaveis = os.path.join(diretorio_validacao, 'saudaveis')
                destino_avaliacao_implantes = os.path.join(diretorio_validacao, 'implantes')
                os.makedirs(destino_avaliacao_defeituosos, exist_ok=True)
                os.makedirs(destino_avaliacao_saudaveis, exist_ok=True)
                os.makedirs(destino_avaliacao_implantes, exist_ok=True)
                shutil.copy(arq_defeituosos, destino_avaliacao_defeituosos)
                shutil.copy(arq_saudaveis, destino_avaliacao_saudaveis)
                resultado_subtracao = os.path.join(destino_avaliacao_implantes, coluna['ID (Implantes)'] + '.nii.gz')
                #subtracao_booleana(arq_saudaveis, arq_defeituosos, resultado_subtracao)
                print(
                    f"Trios separados para avaliação: {coluna['ID (Defeituosos)']} - {coluna['ID (Saudáveis)']} - {coluna['ID (Implantes)']}")
            else:  # teste
                destino_teste_defeituosos = os.path.join(diretorio_teste, 'defeituosos')
                destino_teste_saudaveis = os.path.join(diretorio_teste, 'saudaveis')
                destino_teste_implantes = os.path.join(diretorio_teste, 'implantes')
                os.makedirs(destino_teste_defeituosos, exist_ok=True)
                os.makedirs(destino_teste_saudaveis, exist_ok=True)
                os.makedirs(destino_teste_implantes, exist_ok=True)
                shutil.copy(arq_defeituosos, destino_teste_defeituosos)
                shutil.copy(arq_saudaveis, destino_teste_saudaveis)
                resultado_subtracao = os.path.join(destino_teste_implantes, coluna['ID (Implantes)'] + '.nii.gz')
                subtracao_booleana(arq_saudaveis, arq_defeituosos, resultado_subtracao)
                print(
                    f"Trios separados para teste: {coluna['ID (Defeituosos)']} - {coluna['ID (Saudáveis)']} - {coluna['ID (Implantes)']}")
        else:
            print(f"Arquivo não encontrado para o par: {coluna['ID (Defeituosos)']} - {coluna['ID (Saudáveis)']}")

# Fechando objeto ExcelFile
xls.close()
print("Processo concluído.")