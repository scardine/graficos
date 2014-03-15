#coding: utf-8
import json
import csv
import sqlsoup
from ast import literal_eval
from scipy.stats.mstats import mquantiles

db = sqlsoup.SQLSoup('mysql://usu_simedu:usu_simedu@172.16.16.135/simeducacao')

datum = []
with open("variaveis.csv") as i:
    reader = csv.reader(i)
    head = reader.next()
    for line in reader:
        datum.append(dict(zip(head, line)))

r = []

eixos = u"""Educação Básica
Contexto Socioeconômico""".split("\n")


def get_domain(var_cod, ano):
    levels = {
        10: 'ra',
        70: 'mun',
        30: 'rm',
    }
    r = {}
    for level in levels:
        places = [l.loc_cod for l in db.tb_localidade.filter_by(loc_nivel=level)]
        domain = []
        for dado in db.tb_dados.filter_by(var_cod=var_cod).filter(db.tb_dados.loc_cod.in_(places)):
            val = getattr(dado, 'd_{}'.format(ano))
            if val.startswith('Grupo'):
                r[levels[level]] = [0,6]
                continue
            if val.strip() in ['', '-', 'N/A', 'N/D', 'NA', 'ND', '*', '?']:
                continue
            try:
                val = literal_eval(val.replace('.', '').replace(',', '.'))
            except (SyntaxError, ValueError):
                continue
            domain.append(val)
        r[levels[level]] = domain

    return r


def get_legend(domain):
    r = {}
    for k, v in domain.items():
        if v == [0, 6]:
            r[k] = ["Grupo {}".format(n) for n in range(1, 6)]
            continue

        quantiles = list(mquantiles(v, [0.2, 0.4, 0.6, 0.8]))
        legenda = ["até {}".format(quantiles[0])]
        for i in range(3):
            legenda.append('mais de {} até {}'.format(quantiles[i], quantiles[i+1]))
        legenda.append('mais de {}'.format(quantiles[-1]))
        r[k] = legenda

    return r


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
            var = db.tb_variavel.get(line['var_cod'])
            if not var:
                continue
            if line['eixo'] != eixo["nome"]:
                continue
            if line['dimensao'] != dimensao["nome"]:
                continue
            variable = {
                "nome": line['var_nome'],
                "id": var.var_cod,
                "anos": [int(ano) for ano in line['var_periodo'].split(",")],
                "itens": [],
                "range": line['range'].split(","),
                #"domain": json.loads(line['domain']),
                "scale": line['scale'],
                "features": line['features'].split(","),
                "fonte": line.get('fonte', '').split('|'),
            }
            variable['domain'] = get_domain(var.var_cod, variable['anos'][-1])
            variable["legenda"] = get_legend(variable['domain'])
            dimensao["itens"].append(variable)

        print u"\t\t\t{} variavel(eis) para {}->{}".format(
            len(dimensao["itens"]),
            nome,
            dimensao["nome"]
        )

with open("../data/variaveis.json", "wb") as o:
    o.write(json.dumps({"menu": r}, indent=2))

with open("../data/variaveis.min.json", "wb") as o:
    o.write(json.dumps({"menu": r}))
