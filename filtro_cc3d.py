import cc3d
import os
import numpy as np
import nrrd
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
entrada = "./dataset/zip2"
saida = "./dataset/nrrd2"
# Buscando NRRDs na entrada
nrrds = glob(os.path.join(entrada, '**/*.nrrd'), recursive=True)

for arq_nrrd in nrrds:
    print(f"Aplicando o filtro CC3D no arquivo: {arq_nrrd}")
    # Criando caminho de saída correspondente
    caminho_relativo = os.path.relpath(arq_nrrd, entrada)
    dir_saida = os.path.join(saida, caminho_relativo)
    # Garantindo que o diretório de saída exista
    os.makedirs(os.path.dirname(dir_saida), exist_ok=True)
    # Leitura da imagem médica nrrd
    data, header = nrrd.read(arq_nrrd)
    # Obtendo matriz de segmentação de componentes conectados 3D
    matriz_cc = cc3d.connected_components(data.astype('int32'))
    # Chamando função de isolamento de segundo maior componente conectado
    matriz_smcc = isola_smcc(matriz_cc)
    # Remove os demais componentes
    matriz_filtrada = (matriz_cc == matriz_smcc)
    matriz_filtrada = matriz_filtrada + 1 - 1
    print(f"Salvando imagem médica filtrada em: {dir_saida}")
    nrrd.write(dir_saida, matriz_filtrada, header)

print('Filtragem de ruído aplicada a todos os arquivos NRRDs encontrados no diretório de entrada!')
