import random
import json

data = []
for i in range(10):
    categoria = {
        "nome": "Categoria {}".format(i + 1),
        "id": "cat-{}".format(i + 1),
        "itens": []
    }
    data.append(categoria)
    for j in range(random.randint(1, 10)):
        subcategoria = {
            "nome": "Subcategoria {}.{}".format(i + 1, j + 1),
            "id": "subcat-{}-{}".format(i + 1, j + 1),
            "itens": []
        }
        categoria['itens'].append(subcategoria)
        for k in range(random.randint(1, 20)):
            variavel = {
                "nome": "Variavel {}.{}.{}".format(i + 1, j + 1, k + 1),
                "id": "var-{}-{}-{}".format(i + 1, j + 1, k + 1),
                "itens": []
            }
            subcategoria['itens'].append(variavel)

json.dump({"menu": data}, open('data/variables.json', 'wb'), indent=2)