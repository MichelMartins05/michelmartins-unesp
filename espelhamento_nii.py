import nibabel as nib
import os
from glob import glob

def espelhar_nii(dir_entrada, dir_saida):
    # Carregando imagem médica NIFTI
    imagem = nib.load(dir_entrada)
    # Espelhamento horizontal
    espelha_dados = imagem.get_fdata()[::-1, ::-1, :]
    # Nova imagem com espelhamento horizontal aplicado
    espelha_imagem = nib.Nifti1Image(espelha_dados, imagem.affine, imagem.header)
    # Salvando nova imagem
    nib.save(espelha_imagem, dir_saida)

entrada = 'C:/UNESP/dataset/backup/saudaveis_nii'  # Diretório de entrada
saida = 'C:/UNESP/dataset/backup/saudaveis_fix'  # Diretório de saída
niis = glob(os.path.join(entrada, '**/*.nii'), recursive=True)

for nii in niis:
    print(f"Espelhando horizontalmente o arquivo: {nii}")
    caminho_relativo = os.path.relpath(nii, entrada)
    nii_saida = os.path.join(saida, caminho_relativo)
    os.makedirs(os.path.dirname(nii_saida), exist_ok=True)
    espelhar_nii(nii, nii_saida)

print("Espelhamento concluído para todos os arquivo NIFTI encontrados no diretório de entrada.")