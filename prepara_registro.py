import pandas as pd
import shutil
import os

# Diretório de entrada e saída
arquivo_excel = './registro.xlsx'
diretorio_saida = './dataset/registro/moveis'

# Criando objeto ExcelFile
xls = pd.ExcelFile(arquivo_excel)
i=0

for planilha in xls.sheet_names:
    # Carregar a planilha Excel
    df = pd.read_excel(xls, sheet_name=planilha)
    i+=1
    print(f"Lote {i}: {planilha} ")
    # Diretório de saída específico para a planilha atual
    diretorio_planilha = os.path.join(diretorio_saida, planilha)
    # Criar o diretório se não existir
    os.makedirs(diretorio_planilha, exist_ok=True)

    # Iterar sobre as linhas da planilha e copiar/renomear os arquivos
    for index, coluna in df.iterrows():
        numero_origem = str(coluna['N.O.']).zfill(3)
        nome_arquivo = numero_origem + '.nii.gz'
        diretorio_origem_defeituosos = str(coluna['Diretório Origem (Defeituosos)'])
        preid_defeituosos = str(coluna['Pré-ID (Defeituosos)'])
        diretorio_origem_saudaveis = str(coluna['Diretório Origem (Saudáveis)'])
        preid_saudaveis = str(coluna['Pré-ID (Saudáveis)'])

        origem_defeituosos = os.path.join(diretorio_origem_defeituosos, nome_arquivo)
        destino_defeituosos = os.path.join(diretorio_planilha, preid_defeituosos + '.nii.gz')

        # Verificar se o diretório de origem existe
        if os.path.exists(origem_defeituosos):
            shutil.copy(origem_defeituosos, destino_defeituosos)
            print(f"Copiado e renomeado: {destino_defeituosos}")
        else:
            print(f"Arquivo não encontrado: {origem_defeituosos}")

        origem_saudaveis = os.path.join(diretorio_origem_saudaveis, nome_arquivo)
        destino_saudaveis = os.path.join(diretorio_planilha, preid_saudaveis + '.nii.gz')

        # Verificar se o diretório de origem existe
        if os.path.exists(origem_saudaveis):
            shutil.copy(origem_saudaveis, destino_saudaveis)
            print(f"Copiado e renomeado: {destino_saudaveis}")
        else:
            print(f"Arquivo não encontrado: {destino_saudaveis}")

# Fechar o objeto ExcelFile após a conclusão
xls.close()

print("Preparando pasta de imagens fixas para o processo de registro")
diretorio_origem_fixas = 'C:/UNESP/dataset/niigz/mug500/fixas'
diretorio_destino_fixas = 'C:/UNESP/dataset/registro/fixas'
shutil.copytree(diretorio_origem_fixas, diretorio_destino_fixas)
print("Imagens fixas preparadas")
print("Preparando pasta de imagens moveis para o processo de registro")

print("Processo concluído.")
