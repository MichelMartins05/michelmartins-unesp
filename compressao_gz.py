import os
import gzip
import shutil
from glob import glob

entrada = './dataset/posprocessamento/implantes_manual'
saida = './dataset/posprocessamento/implantes_manual'

niis = glob(os.path.join(entrada, '**/*.nii'), recursive=True)

# Estrutura de repetição entre cada arquivo
for nii_entrada in niis:
    # Obtendo caminho do diretório
    print(f"Comprimindo arquivo: {nii_entrada}")

    if os.path.isfile(nii_entrada):
        # Configura arquivo de saída de compressão gzip
        caminho_relativo = os.path.relpath(nii_entrada, entrada)
        nii_saida = os.path.join(saida, caminho_relativo)

        # Garante que o diretório de saída exista
        os.makedirs(os.path.dirname(nii_saida), exist_ok=True)

        # Configura arquivo como entrada de compressão gzip
        with open(nii_entrada, 'rb') as f_in:
            with gzip.open(nii_saida + '.gz', 'wb') as f_out:
                # Armazena arquivo comprimido
                f_out.write(f_in.read())

            print(f'Arquivo comprimido: {nii_saida + ".gz"}')

print('Compressão GZ aplicada a todos os arquivos NIFTI encontrados no diretório de entrada!')
