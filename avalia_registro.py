import ants
import numpy as np
import pandas as pd
import os
from sklearn.metrics import mean_squared_error

# Diretório de entrada
arquivo_excel = './dataset_lotes.xlsx'
# Criando objeto ExcelFile
xls = pd.ExcelFile(arquivo_excel)
# Diretórios de entrada e saída
diretorio_fixas = './registro/fixas'
diretorio_registradas = './registro/ajustadas2'
# Criar uma lista para armazenar os dados
dados = []
n = 0

for planilha in xls.sheet_names:
    # Carregando a planilha Excel
    df = pd.read_excel(xls, sheet_name=planilha)
    # Iterando sobre as linhas da tabela
    for index, coluna in df.iterrows():
        id_defeituosos = os.path.join(diretorio_registradas, planilha, coluna['ID (Defeituosos)'] + '.nii.gz')
        id_saudaveis = os.path.join(diretorio_registradas, planilha, coluna['ID (Saudáveis)'] + '.nii.gz')
        id_fixa = os.path.join(diretorio_fixas, coluna['Registrada em:'] + '.nii.gz')
        # Carregando imagens com ANTs
        imagem_fixa = ants.image_read(id_fixa, dimension=3)
        imagem_registrada_def = ants.image_read(id_defeituosos, dimension=3)
        imagem_registrada_saud = ants.image_read(id_saudaveis, dimension=3)
        # Convertendo imagens em arrays
        dados_fixa = imagem_fixa.numpy()
        dados_registrada_def = imagem_registrada_def.numpy()
        dados_registrada_saud = imagem_registrada_saud.numpy()
        # Calculando Raiz do Erro Médio Quadrático Médio (RMSE)
        n += 1
        rmse_def = np.sqrt(mean_squared_error(dados_fixa.flatten(), dados_registrada_def.flatten()))
        print(f'Arquivo: {id_defeituosos}, numero: {n}, Raiz do Erro Médio Quadrático Médio (RMSE): {rmse_def}')
        rmse_saud = np.sqrt(mean_squared_error(dados_fixa.flatten(), dados_registrada_saud.flatten()))
        print(f'Arquivo: {id_saudaveis}, numero: {n}, Raiz do Erro Médio Quadrático Médio (RMSE): {rmse_saud}')
        dados.append([id_fixa, id_defeituosos, id_saudaveis, n, rmse_def, rmse_saud])

# Criando um tabela com os dados
df_resultado = pd.DataFrame(dados, columns=['Imagem Fixa', 'Imagem Registrada (D)', 'Imagem Registrada (S)', 'Número',
                                            'RMSE (D)', 'RMSE (S)'])
# Salvando o tabela em um arquivo Excel
arquivo_saida_excel = './resultado_registro2.xlsx'
df_resultado.to_excel(arquivo_saida_excel, index=False)
