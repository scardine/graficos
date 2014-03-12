#coding: utf-8
import json
import csv

datum = []
with open("variaveis.csv") as i:
    reader = csv.reader(i)
    head = reader.next()
    for line in reader:
        datum.append(dict(zip(head, line)))

r = []

eixos = u"""Contexto Socioeconômico
Educação Infantil - Creche
Educação Infantil - Pré-escola
Fundamental
Ensino Médio
Ensino Técnico
Educação de Jovens e Adultos""".split("\n")

print u"{} eixos".format(len(eixos))
for i, nome in enumerate(eixos):
    if nome not in eixos:
        continue
    print u"\teixo {}: {}".format(i+1, nome)
    eixo = {
        "nome": nome,
        "id": "eixo-{}".format(i+1),
        "collapsed": True,
        "itens": []
    }
    r.append(eixo)
    dimensoes = []
    # Primeira passada, dimensoes
    for line in datum:
        for k, v in line.items():
            if isinstance(v, unicode): continue
            try:
                line[k] = v.decode('utf-8')
            except UnicodeError:
                print k, v

        if line['eixo'] != eixo["nome"]:
            continue
        if line['dimensao'] in dimensoes:
            continue
        dimensoes.append(line['dimensao'])
    print u"\t\t{} dimensao(oes) para {}: {}".format(len(dimensoes), nome, ', '.join(dimensoes))

    # Segunda passada, variaveis
    for dim in dimensoes:
        dimensao = {
            "nome": dim,
            "id": "dim-{}-{}".format(i+1, len(dimensoes)),
            "collapsed": True,
            "itens": []
        }
        eixo["itens"].append(dimensao)

        for line in datum:
            if line['eixo'] != eixo["nome"]:
                continue
            if line['dimensao'] != dimensao["nome"]:
                continue
            variavel = {
                "nome": line['var_nome'],
                "id": line['var_cod'],
                "anos": [int(ano) for ano in line['var_periodo'].split(",")],
                "itens": [],
                "range": line['range'].split(","),
                "domain": json.loads(line['domain']),
                "scale": line['scale'],
                "features": line['features'].split(",")
            }
            dimensao["itens"].append(variavel)

        print u"\t\t\t{} variavel(eis) para {}->{}".format(
            len(dimensao["itens"]),
            nome,
            dimensao["nome"]
        )

with open("../data/variaveis.json", "wb") as o:
    o.write(json.dumps({"menu": r}, indent=2))

with open("../data/variaveis.min.json", "wb") as o:
    o.write(json.dumps({"menu": r}))
