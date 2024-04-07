import ants
import numpy as np
from sklearn.metrics import mean_squared_error


dir_teste = './ensaio/'
extensao = '.nii.gz'
tipos_registros = ['FRA', 'DRA', 'FRAS', 'FRAB', 'FRS', 'FRB']
testes = [1,2,3,4,5,6]

for tipo_registro in tipos_registros:
    for teste in testes:
        if teste == 1:
            nome_fixa = 'A0007'
        if teste == 2:
            nome_fixa = 'A0048'
        if teste == 3:
            nome_fixa = 'A0117'
        if teste == 4:
            nome_fixa = 'A0324'
        if teste == 5:
            nome_fixa = 'A0422'
        if teste == 6:
            nome_fixa = 'A0497'

        nome_registrada = f'TESTE{teste}{tipo_registro}'

        imagem_fixa = ants.image_read(dir_teste + nome_fixa + extensao, dimension=3)
        imagem_registrada = ants.image_read(dir_teste + nome_registrada + extensao, dimension=3)

        # Obter os dados da imagem
        dados_fixa = imagem_fixa.numpy()
        dados_registrada = imagem_registrada.numpy()

        # Calcular o RMSE usando scikit-learn
        rmse = np.sqrt(mean_squared_error(dados_fixa.flatten(), dados_registrada.flatten()))
        print(f'Tipo de Registro: {tipo_registro}, Teste: {teste}, Erro Médio Quadrático (RMSE): {rmse}')