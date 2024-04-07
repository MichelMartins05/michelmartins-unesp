import nibabel as nib
import numpy as np
import os
import pandas as pd

def hausdorff_distance(nii1_data, nii2_data):

    print("Verificando resolução das imagens médicas.")
    if nii1_data.shape != nii2_data.shape:
        return "ERRO: As imagens médicas precisam ter a mesma resolução"


    shape = nii1_data.shape
    hd = 0

    # Calculando distância de Hausdorff
    # Varredura em cada voxel
    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in range(shape[2]):
                # Registrando posições dos voxels
                v1 = nii1_data[i, j, k]
                v2 = nii2_data[i, j, k]

                # Atualizando valor da distancia máxima encontrada
                if v1 != v2:
                    hd = max(hd, abs(v1 - v2))
    return hd


def dice_similarity_coefficient(nii1_data, nii2_data):
    print("Verificando resolução das imagens médicas.")
    if nii1_data.shape != nii2_data.shape:
        return "ERRO: As imagens médicas precisam ter a mesma resolução"

    # Calculando coeficiente de similaridade de Dice
    overlap = np.sum((nii1_data > 0) & (nii2_data > 0))
    dice = 2 * overlap / (np.sum(nii1_data > 0) + np.sum(nii2_data > 0))
    return dice


def calculate_metrics(gt_path, inf_path):

    # Lista de arquivos de referência
    gt_files = [f for f in os.listdir(gt_path) if f.endswith('.nii.gz')]

    # Lista de arquivos de inferência
    inf_files = [f for f in os.listdir(inf_path) if f.endswith('.nii.gz')]

    # Vetor memória
    results = []

    # Varredura entre os pares
    for i, gt_file in enumerate(gt_files):
        inf_file = inf_files[i]
        # Carregando arquivos NIFTI
        gt_nii = nib.load(os.path.join(gt_path, gt_file))
        inf_nii = nib.load(os.path.join(inf_path, inf_file))

        print(f"Implante de Referência:  {gt_file}, Implante de Inferência: {inf_file}.")

        # Criando máscaras binárias
        gt_data = gt_nii.get_fdata()
        inf_data = inf_nii.get_fdata()

        print("Calculando Distância de Hausdorff.")
        hd = hausdorff_distance(gt_data, inf_data)
        print("Calculando Coeficiente de Similaridade de Dice.")
        dice = dice_similarity_coefficient(gt_data, inf_data)

        print("Armazenando resultados.")
        results.append((gt_file, inf_file, hd, dice))

    print("Criando tabela de dados.")
    df = pd.DataFrame(results, columns=['Implante de Referencia', 'Implante de Inferência', 'Distância de Hausdorff', 'Coeficiente de Similaridade de Dice'])

    print("Exportando tabela de dados Excel")
    df.to_excel('results.xlsx', index=False)

    return 0


gt_path = './gt/'
inf_path = './inf/'
calculate_metrics(gt_path, inf_path)
