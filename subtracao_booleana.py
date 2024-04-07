import os
import shutil
import numpy as np
import nibabel as nib


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

        print(f"Subtração booleana concluída para {arquivo_saudaveis} e {arquivo_defeituosos}.")
    except Exception as e:
        print(f"Erro ao realizar a subtração booleana: {e}")


def extrair_numero_serie(nome_arquivo):
    # Remove o sufixo "_completed" e extrai o número de série do nome do arquivo
    nome_arquivo = nome_arquivo.replace("_completed", "")
    partes = nome_arquivo.split('_')
    if len(partes) >= 4:
        return partes[0][1:]  # Exclui o primeiro caractere (S ou D) e retorna o número de série
    else:
        return None


#resultados = "./dataset/posprocessamento/resultados"
resultados = "./dataset/posprocessamento/sub_saud"
#entradas = "./dataset/processamento/teste/defeituosos"
entradas = "./dataset/processamento/teste/sub_def"
#implantes_resultados = "./dataset/posprocessamento/implantes_resultados"
implantes_resultados = "./dataset/posprocessamento/sub_res"
os.makedirs(resultados, exist_ok=True)
os.makedirs(entradas, exist_ok=True)
os.makedirs(implantes_resultados, exist_ok=True)

# Move os arquivos para a pasta principal (resultados) e renomeia-os
for pasta_atual, _, arquivos in os.walk(resultados):
    for arquivo in arquivos:
        caminho_arquivo = os.path.join(pasta_atual, arquivo)
        caminho_destino = os.path.join(resultados, arquivo)
        if caminho_arquivo != caminho_destino:  # Verifica se o arquivo já está no destino
            shutil.move(caminho_arquivo, resultados)
            print(f"Arquivo movido para {resultados}: {arquivo}")

        # Remove o primeiro caractere e o sufixo "_completed" dos arquivos na pasta 'resultados'
        numero_serie = extrair_numero_serie(arquivo)
        if numero_serie:
            novo_nome_arquivo = numero_serie + ".nii.gz"
            os.rename(os.path.join(resultados, arquivo), os.path.join(resultados, novo_nome_arquivo))

# Remove subpastas vazias
for pasta_atual, _, _ in os.walk(resultados, topdown=False):
    if not os.listdir(pasta_atual):  # Verifica se a subpasta está vazia
        os.rmdir(pasta_atual)  # Exclui a subpasta vazia

# Lista de arquivos em 'entradas'
arquivos_entradas = sorted(os.listdir(entradas))

# Subtração booleana entre os arquivos de 'resultados' e 'entradas'
for i, arquivo_resultado in enumerate(sorted(os.listdir(resultados))):
    if i < len(arquivos_entradas):
        caminho_resultado = os.path.join(resultados, arquivo_resultado)
        caminho_entrada = os.path.join(entradas, arquivos_entradas[i])
        caminho_implante = os.path.join(implantes_resultados, arquivo_resultado)

        subtracao_booleana(caminho_resultado, caminho_entrada, caminho_implante)
    else:
        print(f"Arquivo correspondente não encontrado para: {arquivo_resultado}")
