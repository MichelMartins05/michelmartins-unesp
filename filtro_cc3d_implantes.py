import cc3d
import os
import numpy as np
import nibabel as nib
from glob import glob

def isola_smcc(matriz):
    # Reformatando a matriz 3D para uma array
    matriz2d = matriz.reshape((1, -1))
    array = matriz2d[0, :]
    # Obtendo segmentos da análise CC3D
    segmentos = np.unique(array)
    # Criando histograma
    hist, seg = np.histogram(array, bins=segmentos)
    # Convertendo histograma array np em lista python modo decrescente
    hist = np.ndarray.tolist(hist)
    hist_ = hist
    hist_ = np.array(hist_)
    hist.sort(reverse=True)
    # Exibe histograma
    # print('hist', hist)
    # Isolando segundo maior componente conectado
    idx = (hist_ == hist[1])
    idx = idx + 1 - 1
    idx_ = np.sum(idx * segmentos[0:len(idx)])
    return idx_

# Diretório de entrada e saída
entrada = "./dataset/posprocessamento/implantes_resultados"
saida = "./dataset/posprocessamento/implantes_filtrados"
# Buscando arquivos nifti na entrada
niis = glob(os.path.join(entrada, '**/*.nii.gz'), recursive=True)

for arq_nii in niis:
    print(f"Aplicando o filtro CC3D no arquivo: {arq_nii}")
    # Criando caminho de saída correspondente
    caminho_relativo = os.path.relpath(arq_nii, entrada)
    dir_saida = os.path.join(saida, caminho_relativo)
    # Garantindo que o diretório de saída exista
    os.makedirs(os.path.dirname(dir_saida), exist_ok=True)
    # Leitura da imagem médica nifti
    img = nib.load(arq_nii)
    data = img.get_fdata()
    # Obtendo matriz de segmentação de componentes conectados 3D
    matriz_cc = cc3d.connected_components(data.astype('int32'), connectivity=6)
    # Chamando função de isolamento de segundo maior componente conectado
    matriz_smcc = isola_smcc(matriz_cc)
    # Remove os demais componentes
    matriz_filtrada = (matriz_cc == matriz_smcc)
    matriz_filtrada = matriz_filtrada + 1 - 1

    # Salvando imagem médica filtrada
    img_filtrada = nib.Nifti1Image(matriz_filtrada.astype(np.uint8), img.affine)
    print(f"Salvando imagem médica filtrada em: {dir_saida}")
    nib.save(img_filtrada, dir_saida)


print('Filtragem de ruído aplicada a todos os arquivos NII.GZ encontrados no diretório de entrada!')
