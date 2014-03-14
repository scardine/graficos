#coding:utf-8
import csv
import json
from unidecode import unidecode
import sqlsoup

db = sqlsoup.SQLSoup('mysql://usu_simedu:usu_simedu@127.0.0.1:3307/simeducacao')
db.tb_dados.relate('var', db.tb_variavel, primaryjoin=db.tb_dados.var_cod==db.tb_variavel.var_cod, foreign_keys=[db.tb_dados.var_cod])

with open("localidades.tsv") as i:
    reader = csv.reader(i, delimiter='\t')
    head = reader.next()
    localidades = []
    for linha in reader:
        data = dict(zip(head, linha))
        for k, v in data.items():
            if k in ['loc_cod', 'loc_pai', 'loc_nivel', 'loc_cod_ibge']:
                data[k] = int(v)
        localidade = {}
        for k, v in data.items():
            if k != 'loc_pai_old':
                localidade[k] = data[k]
        localidade['nome'] = unidecode(data['loc_nome'].decode('utf-8'))
        localidades.append(localidade)

with open("../data/localidades.json", "wb") as o:
    o.write(json.dumps({"lista": localidades}))


def get_var(f):
    if not f:
        v = 0
    elif f.startswith('Grupo '):
        v = int(f[6])
    else:
        v = f.replace('.', '').replace(',', '.')
        try:
            float(v)
        except ValueError:
            v = 0
    return v


def eixo1_chart1(localidade):
    # Grafico de populacao masculina/feminina
    masc = db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=57).one()
    fem = db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=56).one()

    vars = [masc, fem]
    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:350px; width:425px;",
        "data": {
            "cols": [
              {
                "id": "valor",
                "label": "Valor",
                "type": "number",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"População Masculina/Feminina",
            "isStacked": "true",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"População",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": "Ano"
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "top", "maxLines": 1 }
        }
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": var.var.var_nome.decode('iso-8859-1'),
            "type": "number",
        })

    # Populacao: dados de 2000 a 2020
    for ano in range(2000, 2021):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo1_chart2(localidade):
    # Taxa geometrica de crescimento da populacao
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=157).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2000).one()
    ]

    chart = {
        "type": "BarChart",
        "cssStyle": "height:350px; width:425px;",
        "data": {
            "cols": [
              {
                "id": "var",
                "label": "Variavel",
                "type": "string",
              },
              {
                "id": "valor",
                "label": "Valor",
                "type": "number",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Taxa Geometrica de Crescimento Anual da População",
            "isStacked": "true",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Taxa de Crescimento",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": "variavel"
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "none"}
        }
    }

    #for var in vars:
    #    chart['data']['cols'].append({
    #        "id": "v{}".format(var.var_cod),
    #        "label": var.var.var_nome.decode('iso-8859-1'),
    #        "type": "number",
    #    })

    # Somente 2010?
    for var in vars:
        label = var.var.var_nome.split()[-1]
        ano = label.split("/")[-1]
        c = [{"v": label}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart

for localidade in localidades:
    charts = []
    charts.append(eixo1_chart1(localidade))
    charts.append(eixo1_chart2(localidade))

    with open('../data/charts/eixo-1-{}.json'.format(localidade['loc_cod']), 'wb') as o:
        o.write(json.dumps(charts, indent=2))


