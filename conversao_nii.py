import SimpleITK as sitk
import os
from glob import glob

def convert_nrrd_to_nii(dir_entrada, dir_saida):
    # Leitura do NRRD
    imagem = sitk.ReadImage(dir_entrada)
    # Obtendo informações do NRRD
    origem = imagem.GetOrigin()
    espacamento = imagem.GetSpacing()
    direcao = imagem.GetDirection()
    # Escrevendo NRRD como NIFTI
    sitk.WriteImage(imagem, dir_saida)
    # Carregando arquivo NIFTI
    nova_imagem = sitk.ReadImage(dir_saida)
    # Atualizando informações
    nova_imagem.SetOrigin(origem)
    nova_imagem.SetSpacing(espacamento)
    nova_imagem.SetDirection(direcao)
    # Escrevendo NIFTI com informações atualizadas
    sitk.WriteImage(nova_imagem, dir_saida)

# Diretórios de entrada e saída
entrada = './dataset/nrrd2/'
saida = './dataset/nii2/'
# Buscando NRRDs na entrada
nrrds = glob(os.path.join(entrada, '**/*.nrrd'), recursive=True)

for nrrd in nrrds:
    print(f"Convertendo o arquivo: {nrrd}")
    # Criando caminho de saída correspondente
    caminho_relativo = os.path.relpath(nrrd, entrada)
    nii_saida = os.path.join(saida, os.path.dirname(caminho_relativo), os.path.basename(nrrd)[:-5] + '.nii')
    # Garantindo que o diretório de saída exista
    os.makedirs(os.path.dirname(nii_saida), exist_ok=True)
    # Chamando função de conversão
    convert_nrrd_to_nii(nrrd, nii_saida)

print('Conversão NIFTI aplicada a todos os arquivos NRRDs encontrados no diretório de entrada!')