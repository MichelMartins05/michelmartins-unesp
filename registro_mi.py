import ants

# Carregue as imagens registradas e a imagem de referência
imagem_fixa = ants.image_read("./teste/A0007.nii.gz")
imagem_resultado = ants.image_read("./teste/C0001.nii.gz")

# Calcule a Métrica de Similaridade Mútua (MI)
mi_metric = ants.image_mutual_information(imagem_fixa, imagem_resultado)

# Exiba o resultado
print(f"Métrica de Similaridade Mútua: {mi_metric}")
