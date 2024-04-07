import os
import medpy
import medpy.metric
import numpy as np
import seg_metrics.seg_metrics as sg
import SimpleITK as sitk
import time
import pandas as pd

# Diretórios de entrada
gdth_dir = "./resultados/implantes_referencias/"
pred_dir = "./resultados/implantes_resultados/"

# Listar todos os arquivos nii.gz nos diretórios
gdth_files = [os.path.join(gdth_dir, f) for f in os.listdir(gdth_dir) if f.endswith('.nii.gz')]
pred_files = [os.path.join(pred_dir, f) for f in os.listdir(pred_dir) if f.endswith('.nii.gz')]

# Inicializar listas para armazenar os resultados
file_pred = []
file_gdth = []
hd_values = []
dice_values = []

# Iterar sobre os pares de arquivos gdth e pred
for gdth_fpath, pred_fpath in zip(gdth_files, pred_files):
    # Ler imagens e convertê-las em arrays numpy
    gdth_img = sitk.ReadImage(gdth_fpath)
    gdth_np = sitk.GetArrayFromImage(gdth_img)

    pred_img = sitk.ReadImage(pred_fpath)
    pred_np = sitk.GetArrayFromImage(pred_img)

    spacing = np.array(list((pred_img.GetSpacing())))

    gdth_np = gdth_np[::2, ::2, ::2]
    pred_np = pred_np[::2, ::2, ::2]

    gdth_labels = np.unique(gdth_np)

    # Calcular métricas
    labels = [1]
    metrics = sg.write_metrics(labels=labels,
                                gdth_img=gdth_np,
                                pred_img=pred_np,
                                spacing=spacing,
                                metrics=['hd', 'dice'])

    # Obter os valores das métricas
    hd_value = metrics[0]['hd']
    dice_value = metrics[0]['dice']

    # Armazenar informações dos arquivos e métricas
    file_pred.append(os.path.basename(pred_fpath))
    file_gdth.append(os.path.basename(gdth_fpath))
    hd_values.append(hd_value[0])  # Apenas o valor numérico
    dice_values.append(dice_value[0])  # Apenas o valor numérico

# Criar DataFrame
df = pd.DataFrame({'Nome do arquivo (pred)': file_pred,
                   'Nome do arquivo (gdth)': file_gdth,
                   'HD': hd_values,
                   'DICE': dice_values})

# Salvar DataFrame em arquivo Excel
excel_file = 'resultado_metricas.xlsx'
df.to_excel(excel_file, index=False)

print(f"Tabela Excel criada e salva em {excel_file}")
