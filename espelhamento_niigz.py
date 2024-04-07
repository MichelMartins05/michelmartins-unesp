import os
import nibabel as nib
import numpy as np
from glob import glob


def espelhar_niigz(dir_entrada, dir_saida):
    # Carregue a imagem médica 3D
    imagem = nib.load(dir_entrada)
    # Obtenha os dados da imagem
    dados = imagem.get_fdata()[::-1, ::-1, :]
    # Espelhamento horizontal
    espelha_dados = np.fliplr(dados)
    # Nova imagem com espelhamento horizontal aplicado
    espelha_imagem = nib.Nifti1Image(espelha_dados, imagem.affine, imagem.header)
    # Salvando nova imagem espelhada
    nib.save(espelha_imagem, dir_saida)

# Diretórios de entrada e saída
entrada = "C:/UNESP/dataset/niigz/espelhados"
saida = "C:/UNESP/dataset/niigz/espelhados"
# Buscando NII.GZs na entrada
niigzs = glob(os.path.join(entrada, '**/*.nii.gz'), recursive=True)

for niigz in niigzs:
    print(f"Espelhando horizontalmente o arquivo {niigz}")
    # Criando caminho de saída correspondente
    caminho_relativo = os.path.relpath(niigz, entrada)
    niigz_saida = os.path.join(saida, caminho_relativo)
    # Garantindo que o diretório de saída exista
    os.makedirs(os.path.dirname(niigz_saida), exist_ok=True)
    # Chamando função de espelhamento horizontal
    espelhar_niigz(niigz, niigz_saida)

print("Espelhamento concluído para todos os arquivo nii.gz encontrados no diretório de entrada.")

