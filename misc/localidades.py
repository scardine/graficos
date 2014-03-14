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

def eixo1_chart3(localidade):
    # Grafico de populacao em idade escolar
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1006).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1009).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1010).one(),
    ]

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
            "title": u"População em Idade Escolar",
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
            "legend": { "position": "bottom", "maxLines": 2}
        }
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": " ".join(var.var.var_nome.decode('iso-8859-1').split()[-4:]),
            "type": "number",
        })

    # Populacao: dados de 2000 a 2013
    for ano in range(2000, 2014):
        c = [{"v": str(ano)}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo1_chart5(localidade):
    # Grafico Participação dos Setores no Total do Valor Adicionado
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1495).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1496).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1497).one(),
    ]

    chart = {
        "type": "LineChart",
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
            "title": u"Participação dos setores no Total do Valor Adicionado",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Participação em %",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": "Ano"
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 2}
        }
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": var.var.var_nome.decode('iso-8859-1').split()[2],
            "type": "number",
        })

    # Dados de 2000 a 2011
    for ano in range(2000, 2012):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo1_chart6(localidade):
    # Grafico Participação dos Setores no Total dos Empregos Formais
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1045).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1046).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1047).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1475).one(),
    ]

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
            "title": u"Participação dos Setores no Total dos Empregos Formais",
            "isStacked": False,
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Participação em %",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": "Ano"
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 2}
        }
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": " ".join(var.var.var_nome.decode('iso-8859-1').split()[5:-5]),
            "type": "number",
        })

    # Dados de 2000 a 2012
    for ano in range(2000, 2013):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo1_chart7(localidade):
    # Grafico Indice Paulista de Responsabilisade Social, Por Dimensões
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=8).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=9).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=10).one(),
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
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Indice Paulista de Responsabilisade Social, Por Dimensões",
            "isStacked": False,
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Dimensão",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": "Ano"
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 2}
        }
    }

    anos = [2008, 2010]
    for ano in anos:
        chart['data']['cols'].append({
            "id": "p{}".format(ano),
            "label": str(ano),
            "type": "number",
        })

    for var in vars:
        label = var.var.var_nome.split()[-1]
        c = [{"v": label}]
        for ano in anos:
            coluna = "d_{}".format(ano)
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


for localidade in localidades:

    # Eixo 1
    charts = []
    charts.append(eixo1_chart1(localidade))
    charts.append(eixo1_chart2(localidade))
    charts.append(eixo1_chart3(localidade))
    charts.append(eixo1_chart5(localidade))
    charts.append(eixo1_chart6(localidade))
    charts.append(eixo1_chart7(localidade))

    with open('../data/charts/eixo-1-{}.json'.format(localidade['loc_cod']), 'wb') as o:
        o.write(json.dumps(charts, indent=2))


