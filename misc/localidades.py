#coding:utf-8
import csv
import json
from unidecode import unidecode
import sqlsoup

try:
    db = sqlsoup.SQLSoup('mysql://usu_simedu:usu_simedu@172.16.16.135:3306/simeducacao')
    db.execute('show tables')
except:
    db = sqlsoup.SQLSoup('mysql://usu_simedu:usu_simedu@127.0.0.1:3307/simeducacao')

db.tb_dados.relate('var', db.tb_variavel, primaryjoin=db.tb_dados.var_cod==db.tb_variavel.var_cod, foreign_keys=[db.tb_dados.var_cod])
db.tb_variavel.relate('fntrel', db.tb_rel_var_fnt, primaryjoin=db.tb_variavel.var_cod==db.tb_rel_var_fnt.var_cod, foreign_keys=[db.tb_rel_var_fnt.var_cod])
db.tb_rel_var_fnt.relate('fnt', db.tb_fonte, primaryjoin=db.tb_rel_var_fnt.fnt_cod==db.tb_fonte.fnt_cod, foreign_keys=[db.tb_rel_var_fnt.fnt_cod])

altura = 440
largura = 570


def get_fontes(dados):
    fontes = []
    for dado in dados:
        for rel in dado.var.fntrel:
            fontes.append(rel.fnt.fnt_nome.decode('iso-8859-1'))
    return sorted(set(fontes))


with open("localidades.tsv") as i:
    reader = csv.reader(i, delimiter='\t')
    head = reader.next()
    localidades = []
    for linha in reader:
        data = dict(zip(head, linha))
        for k, v in data.items():
            if k in ['loc_cod', 'loc_pai', 'loc_nivel', 'loc_cod_ibge']:
                data[k] = int(v)
        if data['loc_nivel'] == 0:
            data['loc_nivel'] == 99
        localidade = {}
        for k, v in data.items():
            if k != 'loc_pai_old':
                localidade[k] = data[k]
        localidade['nome'] = unidecode(data['loc_nome'].decode('utf-8'))
        localidades.append(localidade)

with open("../data/localidades.json", "wb") as o:
    o.write(json.dumps({"lista": localidades}))

fontes = {}
with open("variaveis.csv") as i:
    reader = csv.reader(i)
    head = reader.next()
    for line in reader:
        dado = dict(zip(head, line))
        fontes[int(dado['var_cod'])] = dado['fontes']


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


######## EIXO 0 - 1 - 2 Pre-Escola | Creche | Fundamental - Sergio/LUIZA #########
########## EIXO 0 ###############

def eixo0_chart1(localidade):
    # Grafico Matrículas em Pré-escola, por Rede de Atendimento 2009
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=c).one()
        for c in [2061,160,2059,2230]
    ]

    chart = {
        "type": "PieChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "label": "Variavel",
                "type": "string",
              },
              {
                "label": "Valor",
                "type": "number",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Matrículas em Pré-escola, por Rede de Atendimento\n2009",
            "legend": { "position": "bottom", "maxLines": len(vars)}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        label = " " .join(var.var.var_nome.decode('iso-8859-1').split()[6:])
        c = [{"v": label}]
        coluna = "d_2009"
        f = getattr(var, coluna)
        v = get_var(f)
        c.append({"v": float(v), "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo0_chart2(localidade):
    # Grafico Matrículas em Pré-escola, por Rede de Atendimento 2012
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=c).one()
        for c in [2061,160,2059,2230]
    ]

    chart = {
        "type": "PieChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "label": "Variavel",
                "type": "string",
              },
              {
                "label": "Valor",
                "type": "number",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Matrículas em Pré-escola, por Rede de Atendimento\n2012",
            "legend": { "position": "bottom", "maxLines": len(vars)}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        label = " " .join(var.var.var_nome.decode('iso-8859-1').split()[6:])
        c = [{"v": label}]
        coluna = "d_2012"
        f = getattr(var, coluna)
        v = get_var(f)
        c.append({"v": float(v), "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo0_chart3(localidade):
    # Grafico Matrículas em Pré-escola, por Rede de Atendimento e Demanda Potencial
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=c).one()
        for c in [2064,2061,2068]
    ]

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Matrículas em Pré-escola, por Rede de Atendimento e Demanda Potencial\n2009-2020",
            "isStacked": "true",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {

                "gridlines": {
                    "count": 6
                }
            },

            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 1 }
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        if len(var.var.var_nome.decode('iso-8859-1').split()) == 6 :
            teste = " " .join(var.var.var_nome.decode('iso-8859-1').split()[0:2])
        else:
            teste = " " .join(var.var.var_nome.decode('iso-8859-1').split()[6:])
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": teste,
            "type": "number",
        })

    # dados de 2009-2020
    for ano in (list(range(2009, 2013)) + list(range(2016, 2021))):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo0_chart4(localidade):
    # Grafico Taxa de Atendimento a Pré-escola
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2066).one(),
    ]
    if localidade['loc_pai']:
        pai = db.tb_localidade.filter_by(loc_cod=localidade['loc_pai']).one()
        vars.append(
            db.tb_dados.filter_by(loc_cod=pai.loc_cod, var_cod=2066).one(),
        )
        if pai.loc_pai:
            vars.append(
                db.tb_dados.filter_by(loc_cod=pai.loc_pai, var_cod=2066).one(),
            )

    chart = {
        "type": "LineChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Taxa de Atendimento a Pré-escola\n2009-2012",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Em %",
                "gridlines": {
                    "count": 6
                }
            },

            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 1 }
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        local = db.tb_localidade.filter_by(loc_cod=var.loc_cod).one()
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": local.loc_nome.decode('iso-8859-1'),
            "type": "number",
        })

    # dados de 2009 a 2012
    for ano in range(2009, 2013):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo0_chart5(localidade):
    # Grafico Docentes de Pré-escola com Ensino Superior ou Magistério Completo
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=c).one()
        for c in [2069]
    ]

    chart = {
        "type": "BarChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Docentes de Pré-escola com Ensino Superior ou Magistério Completo\n2009-2012",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Em %",
                "gridlines": {
                    "count": 6
                }
            },

            "formatters": {},
            "displayed": True,
            "legend": { "position": "none" }
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": var.var.var_nome.decode('iso-8859-1'),
            "type": "number",
        })

    # dados de 2009 a 2012
    for ano in range(2009, 2013):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo0_chart6(localidade):
    # Grafico Número Médio de Alunos por Docente
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2070).one(),
    ]
    if localidade['loc_pai']:
        pai = db.tb_localidade.filter_by(loc_cod=localidade['loc_pai']).one()
        vars.append(
            db.tb_dados.filter_by(loc_cod=pai.loc_cod, var_cod=2070).one(),
        )
        if pai.loc_pai:
            vars.append(
                db.tb_dados.filter_by(loc_cod=pai.loc_pai, var_cod=2070).one(),
            )

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Número Médio de Alunos por Docente\n2009-2012",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Em %",
                "gridlines": {
                    "count": 6
                }
            },

            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 1 }
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        local = db.tb_localidade.filter_by(loc_cod=var.loc_cod).one()
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": local.loc_nome.decode('iso-8859-1'),
            "type": "number",
        })

    # dados de 2009 a 2012
    for ano in range(2009, 2013):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart




########### fim eixo 0 ###############


########## EIXO 1 ###############


def eixo1_chart1(localidade):
    # Grafico Matrículas em Creche, por Rede de Atendimento 2009
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=c).one()
        for c in [2045,262,2043,2047]
    ]

    chart = {
        "type": "PieChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "label": "Variavel",
                "type": "string",
              },
              {
                "label": "Valor",
                "type": "number",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Matrículas em Creche, por Rede de Atendimento\n2009",
            "legend": { "position": "bottom", "maxLines": len(vars)}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        label = " " .join(var.var.var_nome.decode('iso-8859-1').split()[6:])
        c = [{"v": label}]
        coluna = "d_2009"
        f = getattr(var, coluna)
        v = get_var(f)
        c.append({"v": float(v), "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo1_chart2(localidade):
    # Grafico Matrículas em Creche, por Rede de Atendimento 2012
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=c).one()
        for c in [2045,262,2043,2047]
    ]

    chart = {
        "type": "PieChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "label": "Variavel",
                "type": "string",
              },
              {
                "label": "Valor",
                "type": "number",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Matrículas em Creche, por Rede de Atendimento\n2012",
            "legend": { "position": "bottom", "maxLines": len(vars)}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        label = " " .join(var.var.var_nome.decode('iso-8859-1').split()[6:])
        c = [{"v": label}]
        coluna = "d_2012"
        f = getattr(var, coluna)
        v = get_var(f)
        c.append({"v": float(v), "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo1_chart3(localidade):
    # Grafico Matrículas em Creche, por Rede de Atendimento e Demanda Potencial
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=c).one()
        for c in [2049,2045,2053]
    ]

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Matrículas em Creche, por Rede de Atendimento e Demanda Potencial\n2009-2020",
            "isStacked": "true",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {

                "gridlines": {
                    "count": 6
                }
            },

            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 1 }
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        if len(var.var.var_nome.decode('iso-8859-1').split()) == 6 :
            teste = " " .join(var.var.var_nome.decode('iso-8859-1').split()[0:2])
        else:
            teste = " " .join(var.var.var_nome.decode('iso-8859-1').split()[6:])
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": teste,
            "type": "number",
        })

    # dados de 2009 a 2012 + 2016 a 2020
    for ano in (list(range(2009, 2013)) + list(range(2016, 2021))):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo1_chart4(localidade):
    # Grafico Taxa de Atendimento à Creche - 2009-2012
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2051).one(),
    ]
    if localidade['loc_pai']:
        pai = db.tb_localidade.filter_by(loc_cod=localidade['loc_pai']).one()
        vars.append(
            db.tb_dados.filter_by(loc_cod=pai.loc_cod, var_cod=2051).one(),
        )
        if pai.loc_pai:
            vars.append(
                db.tb_dados.filter_by(loc_cod=pai.loc_pai, var_cod=2051).one(),
            )

    chart = {
        "type": "LineChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Taxa de Atendimento à Creche\n2009-2012",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Em %",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": ""
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 1 }
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        local = db.tb_localidade.filter_by(loc_cod=var.loc_cod).one()
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": local.loc_nome.decode('iso-8859-1'),
            "type": "number",
        })

    # dados de 2009 a 2012
    for ano in range(2009, 2013):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo1_chart5(localidade):
    # Grafico Docentes de Creche com Ensino Superior ou Magistério e de Auxiliares de Creche com Ensino Médio Completo
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=c).one()
        for c in [2054,2055]
    ]

    chart = {
        "type": "BarChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Docentes de Creche com Ensino Superior ou Magistério e de Auxiliares de Creche com Ensino Médio Completo\n2009-2012",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                   "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": "Em %"
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 1}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": var.var.var_nome.decode('iso-8859-1').split()[0],
            "type": "number",
        })

    # dados de 2009 a 2012
    for ano in range(2009, 2013):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo1_chart6(localidade):
    # Grafico Número Médio de Alunos de Creche por Profissional
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2056).one(),
    ]
    if localidade['loc_pai']:
        pai = db.tb_localidade.filter_by(loc_cod=localidade['loc_pai']).one()
        vars.append(
            db.tb_dados.filter_by(loc_cod=pai.loc_cod, var_cod=2056).one(),
        )
        if pai.loc_pai:
            vars.append(
                db.tb_dados.filter_by(loc_cod=pai.loc_pai, var_cod=2056).one(),
            )

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Número Médio de Alunos de Creche por Profissional\n2009-2012",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {

                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": ""
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 1 }
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        local = db.tb_localidade.filter_by(loc_cod=var.loc_cod).one()
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": u" - ".join([
             local.loc_nome.decode('iso-8859-1'),
            ]),
            "type": "number",
        })

    # dados de 2009 a 2012
    for ano in range(2009, 2013):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


########## EIXO 2 ###############

def eixo2_chart1(localidade):
    # Distribuição das Matrículas nos Anos Iniciais do Ensino Fundamental, por Rede de Atendimento 2012
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=c).one()
        for c in [268,266,267]
    ]

    chart = {
        "type": "PieChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "label": "Variavel",
                "type": "string",
              },
              {
                "label": "Valor",
                "type": "number",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Distribuição das Matrículas nos Anos Iniciais do Ensino Fundamental, por Rede de Atendimento\n2012",
            "legend": { "position": "bottom", "maxLines": len(vars)}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        label = var.var.var_nome.decode('iso-8859-1').split()[-1]
        c = [{"v": label}]
        coluna = "d_2012"
        f = getattr(var, coluna)
        v = get_var(f)
        c.append({"v": float(v), "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo2_chart2(localidade):
    # Gráfico de Distribuição das Matrículas nos Anos Finais do Ensino Fundamental, por Rede de Atendimento 2012
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=c).one()
        for c in [273,271,272]
    ]

    chart = {
        "type": "PieChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "label": "Variavel",
                "type": "string",
              },
              {
                "label": "Valor",
                "type": "number",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Distribuição das Matrículas nos Anos Finais do Ensino Fundamental, por Rede de Atendimento\n2012",
            "legend": { "position": "bottom", "maxLines": len(vars)}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        label = var.var.var_nome.decode('iso-8859-1').split()[-1]
        c = [{"v": label}]
        coluna = "d_2012"
        f = getattr(var, coluna)
        v = get_var(f)
        c.append({"v": float(v), "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart

def eixo2_chart3(localidade):
    # Grafico de Matrículas nos Anos Iniciais do Ensino Fundamental, por Rede de Atendimento 2000-2012
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=268).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=266).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=267).one(),
    ]

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Matrículas nos Anos Iniciais do Ensino Fundamental, por Rede de Atendimento\n2000-2012",
            "isStacked": "true",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {

                "gridlines": {
                    "count": 6
                }
            },

            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 2}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": var.var.var_nome.decode('iso-8859-1').split()[-1],
            "type": "number",
        })

    # Matrículas: dados de 2000-2012
    for ano in range(2000, 2013):
        c = [{"v": str(ano)}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo2_chart4(localidade):
    # Grafico de Matrículas nos Anos Finais do Ensino Fundamental, por Rede de Atendimento 2000-2012


    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=273).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=271).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=272).one(),
    ]

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Matrículas nos Anos Finais do Ensino Fundamental, por Rede de Atendimento\n2000-2012",
            "isStacked": "true",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {

                "gridlines": {
                    "count": 6
                }
            },

            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 2}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": var.var.var_nome.decode('iso-8859-1').split()[-1],
            "type": "number",
        })

    # Matrículas: dados de 2000-2012
    for ano in range(2000, 2013):
        c = [{"v": str(ano)}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo2_chart5(localidade):
    # Grafico de Taxa de Abandono nos Anos Iniciais do Ensino Fundamental, por Rede de Atendimento 2000-2012

    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=241).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=239).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=240).one(),
    ]

    chart = {
        "type": "LineChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Taxa de Abandono nos Anos Iniciais do Ensino Fundamental, por Rede de Atendimento\n2000-2012",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Em %",
                "gridlines": {
                    "count": 6
                }
            },

            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 2}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": var.var.var_nome.decode('iso-8859-1').split()[-1],
            "type": "number",
        })

    # Dados de 2000-2012
    for ano in range(2000, 2013):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart

def eixo2_chart6(localidade):
    # Grafico de Taxa de Abandono nos Anos Finais do Ensino Fundamental, por Rede de Atendimento 2000-2012

    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=256).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=254).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=255).one(),
    ]

    chart = {
        "type": "LineChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Taxa de Abandono nos Anos Finais do Ensino Fundamental, por Rede de Atendimento\n2000-2012",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Em %",
                "gridlines": {
                    "count": 6
                }
            },

            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 2}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": var.var.var_nome.decode('iso-8859-1').split()[-1],
            "type": "number",
        })

    # Dados de 2000-2012
    for ano in range(2000, 2013):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart

def eixo2_chart7(localidade):
    # Grafico Alunos do 5º Ano que Atingiram o Nível Adequado ou Avançado na Prova Brasil, por Rede de Atendimento 2007-2011
    vars = [
		db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2098).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2102).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2100).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2104).one(),
    ]

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
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
            "title": u"Alunos do 5º Ano que Atingiram o Nível Adequado ou Avançado na Prova Brasil, por Rede de Atendimento\n2007-2011",
            "isStacked": False,
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Em %",
                "gridlines": {
                    "count": 6
                }
            },

            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 2}
        },
        "fontes": get_fontes(vars)
    }

    anos = [2007, 2009, 2011]
    for ano in anos:
        chart['data']['cols'].append({
            "id": "p{}".format(ano),
            "label": str(ano),
            "type": "number",
        })

    for var in vars:
        label = var.var.var_nome.decode('iso-8859-1').split()[-1] + " " + var.var.var_nome.decode('iso-8859-1').split()[-6]
        c = [{"v": label}]
        for ano in anos:
            coluna = "d_{}".format(ano)
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart

def eixo2_chart8(localidade):
    # Grafico Alunos do 9º Ano que Atingiram o Nível Adequado ou Avançado na Prova Brasil, por Rede de Atendimento 2007-2011

    vars = [
		db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2099).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2103).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2101).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2105).one(),
    ]

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
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
            "title": u"Alunos do 9º Ano que Atingiram o Nível Adequado ou Avançado na Prova Brasil, por Rede de Atendimento\n2007-2011",
            "isStacked": False,
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Em %",
                "gridlines": {
                    "count": 6
                }
            },

            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 2}
        },
        "fontes": get_fontes(vars)
    }

    anos = [2007, 2009, 2011]
    for ano in anos:
        chart['data']['cols'].append({
            "id": "p{}".format(ano),
            "label": str(ano),
            "type": "number",
        })

    for var in vars:
        label = var.var.var_nome.decode('iso-8859-1').split()[-1] + " " + var.var.var_nome.decode('iso-8859-1').split()[-6]
        c = [{"v": label}]
        for ano in anos:
            coluna = "d_{}".format(ano)
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart





###### fim dos modelos dos gráficos ###########

########## FIM EIXO 0 ###############



##### EIXO 0 - pre-escola #########

def eixo0_chart1(localidade):
    # Grafico Matrículas em Pré-escola por Rede de Atendimento 2009
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=c).one()
        for c in [2061,160,2059,2230]
    ]

    chart = {
        "type": "PieChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "label": "Variavel",
                "type": "string",
              },
              {
                "label": "Valor",
                "type": "number",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Matrículas em Pré-escola por Rede de Atendimento",
            "legend": { "position": "bottom", "maxLines": len(vars)}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        label = var.var.var_nome.decode('iso-8859-1')
        c = [{"v": label}]
        coluna = "d_2009"
        f = getattr(var, coluna)
        v = get_var(f)
        c.append({"v": float(v), "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo0_chart2(localidade):
    # Grafico Matrículas em Pré-escola por Rede de Atendimento 2012
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=c).one()
        for c in [2061,160,2059,2230]
    ]

    chart = {
        "type": "PieChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "label": "Variavel",
                "type": "string",
              },
              {
                "label": "Valor",
                "type": "number",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Matrículas em Pré-escola por Rede de Atendimento 2012",
            "legend": { "position": "bottom", "maxLines": len(vars)}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        label = var.var.var_nome.decode('iso-8859-1')
        c = [{"v": label}]
        coluna = "d_2012"
        f = getattr(var, coluna)
        v = get_var(f)
        c.append({"v": float(v), "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo0_chart3(localidade):
    # Grafico Matriculas e Demanda Potencial
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=c).one()
        for c in [2064,2061,2068]
    ]

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Matriculas em Pré-escola por Rede e Demanda Potencial",
            "isStacked": "true",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Matrículas",
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
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": var.var.var_nome.decode('iso-8859-1'),
            "type": "number",
        })

    # dados de 2000 a 2020
    for ano in (list(range(2009, 2013)) + list(range(2016, 2021))):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo0_chart4(localidade):
    # Grafico Taxa de Atendimento a Pré-escola
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2066).one(),
    ]
    if localidade['loc_pai']:
        pai = db.tb_localidade.filter_by(loc_cod=localidade['loc_pai']).one()
        vars.append(
            db.tb_dados.filter_by(loc_cod=pai.loc_cod, var_cod=2066).one(),
        )
        if pai.loc_pai:
            vars.append(
                db.tb_dados.filter_by(loc_cod=pai.loc_pai, var_cod=2066).one(),
            )

    chart = {
        "type": "LineChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Taxa de Atendimento a Pré-escola",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Taxa de atendimento",
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
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        local = db.tb_localidade.filter_by(loc_cod=var.loc_cod).one()
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": u" - ".join([
                var.var.var_nome.decode('iso-8859-1'),
                local.loc_nome.decode('iso-8859-1'),
            ]),
            "type": "number",
        })

    # dados de 2009 a 2012
    for ano in range(2009, 2013):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo0_chart5(localidade):
    # Grafico % de docentes com ensino superior ou magistério completo
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=c).one()
        for c in [2069]
    ]

    chart = {
        "type": "BarChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"% de docentes com ensino superior ou magistério completo",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"% de docentes",
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
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": var.var.var_nome.decode('iso-8859-1'),
            "type": "number",
        })

    # dados de 2009 a 2012
    for ano in range(2009, 2013):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo0_chart6(localidade):
    # Grafico Número médio de alunos por docente
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2070).one(),
    ]
    if localidade['loc_pai']:
        pai = db.tb_localidade.filter_by(loc_cod=localidade['loc_pai']).one()
        vars.append(
            db.tb_dados.filter_by(loc_cod=pai.loc_cod, var_cod=2070).one(),
        )
        if pai.loc_pai:
            vars.append(
                db.tb_dados.filter_by(loc_cod=pai.loc_pai, var_cod=2070).one(),
            )

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Número médio de alunos por docente",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"alunos/docente",
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
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        local = db.tb_localidade.filter_by(loc_cod=var.loc_cod).one()
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": u" - ".join([
                var.var.var_nome.decode('iso-8859-1'),
                local.loc_nome.decode('iso-8859-1'),
            ]),
            "type": "number",
        })

    # dados de 2009 a 2012
    for ano in range(2009, 2013):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart

############# EIXO 1 - CRECHE #################
def eixo1_chart1(localidade):
    # Grafico Matrículas em Creche, por Rede de Atendimento 2009
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=c).one()
        for c in [2045,262,2043,2047]
    ]

    chart = {
        "type": "PieChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "label": "Variavel",
                "type": "string",
              },
              {
                "label": "Valor",
                "type": "number",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Matrículas em Creche, por Rede de Atendimento\n2009",
            "legend": { "position": "bottom", "maxLines": len(vars)}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        label = var.var.var_nome.decode('iso-8859-1')
        c = [{"v": label}]
        coluna = "d_2009"
        f = getattr(var, coluna)
        v = get_var(f)
        c.append({"v": float(v), "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo1_chart2(localidade):
    # Grafico Matrículas em Creche, por Rede de Atendimento 2012
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=c).one()
        for c in [2045,262,2043,2047]
    ]

    chart = {
        "type": "PieChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "label": "Variavel",
                "type": "string",
              },
              {
                "label": "Valor",
                "type": "number",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Matrículas em Creche, por Rede de Atendimento\n2012",
            "legend": { "position": "bottom", "maxLines": len(vars)}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        label = var.var.var_nome.decode('iso-8859-1').split()[-2]
        c = [{"v": label}]
        coluna = "d_2012"
        f = getattr(var, coluna)
        v = get_var(f)
        c.append({"v": float(v), "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo1_chart3(localidade):
    # Grafico Matrículas em Creche, por Rede de Atendimento e Demanda Potencial
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=c).one()
        for c in [2049,2045,2053]
    ]

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Matrículas em Creche, por Rede de Atendimento e Demanda Potencial\n2009-2020",
            "isStacked": "true",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Matrículas",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": "Ano"
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 1 }
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": var.var.var_nome.decode('iso-8859-1'),
            "type": "number",
        })

    # dados de 2009 a 2012 + 2016 a 2020
    for ano in (list(range(2009, 2013)) + list(range(2016, 2021))):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo1_chart4(localidade):
    # Grafico Taxa de Atendimento à Creche - 2009-2012
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2051).one(),
    ]
    if localidade['loc_pai']:
        pai = db.tb_localidade.filter_by(loc_cod=localidade['loc_pai']).one()
        vars.append(
            db.tb_dados.filter_by(loc_cod=pai.loc_cod, var_cod=2051).one(),
        )
        if pai.loc_pai:
            vars.append(
                db.tb_dados.filter_by(loc_cod=pai.loc_pai, var_cod=2051).one(),
            )

    chart = {
        "type": "LineChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Taxa de Atendimento à Creche\n2009-2012",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Em %",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": ""
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 1 }
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        local = db.tb_localidade.filter_by(loc_cod=var.loc_cod).one()
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": u" - ".join([
                var.var.var_nome.decode('iso-8859-1'),
                local.loc_nome.decode('iso-8859-1'),
            ]),
            "type": "number",
        })

    # dados de 2009 a 2012
    for ano in range(2009, 2013):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo1_chart5(localidade):
    # Grafico Docentes de Creche com Ensino Superior ou Magistério e de Auxiliares de Creche com Ensino Médio Completo
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=c).one()
        for c in [2054,2055]
    ]

    chart = {
        "type": "BarChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Docentes de Creche com Ensino Superior ou Magistério e de Auxiliares de Creche com Ensino Médio Completo\n2009-2012",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Em %",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": ""
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "none"}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": var.var.var_nome.decode('iso-8859-1'),
            "type": "number",
        })

    # dados de 2009 a 2012
    for ano in range(2009, 2013):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo1_chart6(localidade):
    # Grafico Número Médio de Alunos de Creche por Profissional
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2056).one(),
    ]
    if localidade['loc_pai']:
        pai = db.tb_localidade.filter_by(loc_cod=localidade['loc_pai']).one()
        vars.append(
            db.tb_dados.filter_by(loc_cod=pai.loc_cod, var_cod=2056).one(),
        )
        if pai.loc_pai:
            vars.append(
                db.tb_dados.filter_by(loc_cod=pai.loc_pai, var_cod=2056).one(),
            )

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Número Médio de Alunos de Creche por Profissional\n2009-2012",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Em %",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": ""
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 1 }
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        local = db.tb_localidade.filter_by(loc_cod=var.loc_cod).one()
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": u" - ".join([
                var.var.var_nome.decode('iso-8859-1'),
                local.loc_nome.decode('iso-8859-1'),
            ]),
            "type": "number",
        })

    # dados de 2009 a 2012
    for ano in range(2009, 2013):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart

################ FIM EIXO 1 - CHECHE ########



########## EIXO 3 - Ensino Técnico - Marcelo ############

# -*- coding: utf-8 -*-

def eixo3_chart1(localidade):
    # Grafico Matrículas no Ensino Técnico Integrado e Profissionalizante
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2164).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2173).one(),
    ]

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "rede",
                "label": "Rede",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Matrículas no Ensino Médio Integrado e Profissionalizante Técnico\n2009-2012",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": ""
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 2}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": " ".join(var.var.var_nome.decode('iso-8859-1').split()[2:5]),
            "type": "number",
        })

    for ano in range(2009, 2012):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo3_chart2(localidade):
    # Grafico Matrículas no Ensino Médio Integrado e Profissionalizante Técnico
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=c).one()
        for c in [2164, 2182,2191]
    ]

    chart = {
        "type": "PieChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "label": "Variavel",
                "type": "string",
              },
              {
                "label": "Valor",
                "type": "number",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Matrículas no Ensino Médio Integrado e Profissionalizante Técnico\n2012",
            "legend": { "position": "bottom", "maxLines": len(vars)}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        label = " ".join(var.var.var_nome.decode('iso-8859-1').split()[2:5])
        c = [{"v": label}]
        coluna = "d_2009"
        f = getattr(var, coluna)
        v = get_var(f)
        c.append({"v": float(v), "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo3_chart3(localidade):
    # Grafico % de docentes com ensino superior ou magistério completo
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2167).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2165).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2169).one(),
		db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2171).one()
    ]

    chart = {
        "type": "BarChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
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
            "title": u"Matrículas no Ensino Médio Integrado, por Rede de Atendimento\n2012",
            "isStacked": False,
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": ""
            },
            "legend":"none",
            "formatters": {},
            "displayed": True
        },
        "fontes": get_fontes(vars)
    }

    anos = [2012]
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


def eixo3_chart4(localidade):
    # Grafico % de docentes com ensino superior ou magistério completo
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2176).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2174).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2178).one(),
		db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2180).one(),
    ]

    chart = {
        "type": "BarChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
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
            "title": u"Matrículas no Ensino Médio Profissionalizante Técnico, por Rede de Atendimento\n2012",
            "isStacked": False,
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": ""
            },
            "formatters": {},
            "displayed": True,
            "legend":"none"
        },
        "fontes": get_fontes(vars)
    }

    anos = [2012]
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

######## FIM EIXO 3 ENSINO TÉCNICO #############

######## EIXO 4 - ENSINO FUNDAMENTAL - JASMIL #########

def eixo4_chart1(localidade):
    # Grafico Taxa de Escolarização Líquida da População de 15 a 17 Anos
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2149).one(),
    ]
    if localidade['loc_pai']:
        pai = db.tb_localidade.filter_by(loc_cod=localidade['loc_pai']).one()
        vars.append(
            db.tb_dados.filter_by(loc_cod=pai.loc_cod, var_cod=2149).one(),
        )
        if pai.loc_pai:
            vars.append(
                db.tb_dados.filter_by(loc_cod=pai.loc_pai, var_cod=2149).one(),
            )

    chart = {
        "type": "LineChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Taxa de Escolarização Líquida da População entre 15 e 17 Anos\n2009-2012",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Em %",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": ""
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 1 }
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        local = db.tb_localidade.filter_by(loc_cod=var.loc_cod).one()
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": u" - ".join([
                local.loc_nome.decode('iso-8859-1'),
            ]),
            "type": "number",
        })

    # dados de 2009 a 2012
    for ano in range(2009, 2013):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart



def eixo4_chart2(localidade):
    # Grafico Distorção Idade-Série no Ensino Médio, por Rede de Atendimento
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1876).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1874).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1875).one(),
    ]

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Distorção Idade-Série no Ensino Médio, por Rede de Atendimento\n2011-2012",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Em %",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": ""
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 2}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": var.var.var_nome.decode('iso-8859-1').split()[-1],
            "type": "number",
        })

    # Dados de 2011 a 2012
    for ano in range(2011, 2013):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo4_chart3(localidade):
    # Distribuição das Matrículas no Ensino Médio, por Rede de Atendimento 2012

    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=c).one()
        for c in [168,264,265]
    ]

    chart = {
        "type": "PieChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "label": "Variavel",
                "type": "string",
              },
              {
                "label": "Valor",
                "type": "number",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Distribuição das Matrículas no Ensino Médio, por Rede de Atendimento\n2012",
            "legend": { "position": "bottom", "maxLines": len(vars)}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        label = var.var.var_nome.decode('iso-8859-1').split()[-1]
        c = [{"v": label}]
        coluna = "d_2012"
        f = getattr(var, coluna)
        v = get_var(f)
        c.append({"v": float(v), "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo4_chart4(localidade):
    # Grafico de Matrículas no Ensino Médio, por Rede de Atendimento
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=168).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=264).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=265).one(),
    ]

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Matrículas no Ensino Médio, por Rede de Atendimento\n2000-2012",
            "isStacked": "true",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": ""
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 2}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": " ".join(var.var.var_nome.decode('iso-8859-1').split()[-1:]),
            "type": "number",
        })

    # dados: de 2002 a 2012
    for ano in range(2002, 2013):
        c = [{"v": str(ano)}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo4_chart5(localidade):
    # Grafico de Matrículas no Ensino Médio Diurno e Noturno

    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2145).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2147).one(),
    ]

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Matrículas no Ensino Médio Diurno e Noturno\n2009-2012",
            "isStacked": "true",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": ""
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 2}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": " ".join(var.var.var_nome.decode('iso-8859-1').split()[-1:]),
            "type": "number",
        })

    # Populacao: dados de 2009 a 2012
    for ano in range(2009, 2013):
        c = [{"v": str(ano)}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo4_chart6(localidade):
    # Grafico Taxa de Abandono do Ensino Médio, por Rede de Atendimento
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=181).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=180).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=179).one(),
    ]

    chart = {
        "type": "LineChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Taxa de Abandono do Ensino Médio, por Rede de Atendimento\n2000/2002-2005/2008-2012",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Em %",
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
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": var.var.var_nome.decode('iso-8859-1').split()[-1],
            "type": "number",
        })

    # Dados de 2002 a 2012
    periodo = [2000,2002,2003,2004,2005,2007,2008,2009,2010,2011,2012]
    #for ano in range(2000, 2013):
    for ano in periodo:
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart




def eixo4_chart7(localidade):
    # Grafico Porcentagem de Alunos do Ensino Médio Adequados ou Avançados em Língua Portuguesa

    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2152).one(),
    ]

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Alunos que Atingiram o Nível Adequado ou Avançado no Saresp, em Língua Portuguesa\n2007-2012",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Em %",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": ""
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "none" }
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label":"Valor",
            #var.var.var_nome.decode('iso-8859-1'),
            "type": "number",
        })

    # Dados de 2007 a 2012
    for ano in range(2007, 2013):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart




def eixo4_chart8(localidade):
    # Grafico Porcentagem de Alunos do Ensino Médio Adequados ou Avançados em Matemática


    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2153).one(),
    ]

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Alunos que Atingiram o Nível Adequado ou Avançado no Saresp, em Matemática\n2007-2012",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Em %",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": ""
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "none" }
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": "Valor",
            #var.var.var_nome.decode('iso-8859-1'),
            "type": "number",
        })

    # Dados de 2007 a 2012
    for ano in range(2007, 2013):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart



########## FIM EIXO 4 - ENSINO FUNDAMENTAL ############


######## EIXO 5 - ENSINO EJA MARCELO ##########

def eixo5_chart1(localidade):
    # Matrículas na Educação de Jovens e Adultos (EJA) no Ensino Fundamental, por Rede de Atendimento
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2201).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2203).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2205).one(),
    ]

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Matrículas na Educação de Jovens e Adultos (EJA) no Ensino Fundamental, por Rede de Atendimento\n2009-2012",
            "isStacked": "true",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": ""
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 2}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": " ".join(var.var.var_nome.decode('iso-8859-1').split()[-1:]),
            "type": "number",
        })

    # Populacao: dados de 2009 a 2012
    for ano in range(2009, 2013):
        c = [{"v": str(ano)}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart

def eixo5_chart2(localidade):
    # Grafico de populacao em idade escolar
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2208).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2210).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2212).one(),
    ]

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Matrículas no EJA Integradas ao Ensino Profissionalizante\n2009-2012",
            "isStacked": "true",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": ""
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 2}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": " ".join(var.var.var_nome.decode('iso-8859-1').split()[-1:]),
            "type": "number",
        })

    # Populacao: dados de 2009 a 2012
    for ano in range(2009, 2013):
        c = [{"v": str(ano)}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart

def eixo5_chart3(localidade):
    # Matrículas na Educação de Jovens e Adultos (EJA) no Ensino Médio,  por Rede de Atendimento
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2215).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2217).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2219).one(),
    ]

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Matrículas na Educação de Jovens e Adultos (EJA) no Ensino Médio,  por Rede de Atendimento\n2009-2012",
            "isStacked": "true",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": ""
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 2}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": " ".join(var.var.var_nome.decode('iso-8859-1').split()[-1:]),
            "type": "number",
    })

    # Populacao: dados de 2009 a 2012
    for ano in range(2009, 2013):
        c = [{"v": str(ano)}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo5_chart4(localidade):
    # Grafico de populacao em idade escolar
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2222).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2224).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2226).one(),
    ]

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "matriculas",
                "label": "Matriculas",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Matrículas no EJA Integradas ao Ensino Profissionalizante no Ensino Médio por Redes\n2009-2012",
            "isStacked": "true",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": ""
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 2}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": " ".join(var.var.var_nome.decode('iso-8859-1').split()[-1:]),
            "type": "number",
        })

    # Populacao: dados de 2009 a 2012
    for ano in range(2009, 2013):
        c = [{"v": str(ano)}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart

######## FIM EIXO 5 ##############

############ Eixo 6 - condicoes socioeconomicas - Sérgio ##########


def eixo6_chart1(localidade):
    # Grafico de populacao masculina/feminina
    masc = db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=57).one()
    fem = db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=56).one()

    vars = [masc, fem]
    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"População, segundo Sexo\n2000-2013",
            "isStacked": "true",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "gridlines": {
                    "count": 6
                }
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 1 }
        },
        "fontes": get_fontes([masc, fem])
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": var.var.var_nome.decode('iso-8859-1'),
            "type": "number",
        })

    # Populacao: dados de 2000 a 2020
	# Populacao: dados de 2000 a 2013
    for ano in range(2000, 2014):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo6_chart2(localidade):
    # Taxa geometrica de crescimento da populacao
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=157).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=2000).one(),
    ]

    chart = {
        "type": "BarChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Taxa Geométrica de Crescimento Anual da População\n2000/2010 - 2010/2020",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"",
                "gridlines": {
                    "count": 6
                }
            },
			"hAxis": {
                "showTextEvery": 2,
                "title": u"Em % a.a",
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "none" }
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": var.var.var_nome.decode('iso-8859-1'),
            "type": "number",
        })

    # Dados de 2000 a 2012
	# Dados de 2004 a 2011
    periodo = [2010,2020]
    for ano in periodo:
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo6_chart4(localidade):
    # Grafico PIP e PIP per Capta
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1016).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1017).one(),
    ]

    chart = {
        "type": "ComboChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"PIB e PIB per Capita\n2000-2011",
            "vAxes": {
                0: { "logScale": False , "title": "Em milhões de reais correntes"},
                1: { "logScale": False , "title": "Em reais correntes"},
            },
            "hAxis": {
                "showTextEvery": 2,
            },
            "seriesType": "bars",
            "series":{
               0:{"targetAxisIndex":0, "type": "bar"},
               1:{"targetAxisIndex":1, "type": "line"},
            },
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 2}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": var.var.var_nome.decode('iso-8859-1'),
            "type": "number",
        })

    # Populacao: dados de 2000 a 2011
    for ano in range(2000, 2012):
        c = [{"v": str(ano)}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo6_chart3(localidade):
    # Grafico de populacao em idade escolar
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1006).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1009).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1010).one(),
    ]

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"População em Idade Escolar, segundo Faixas Etárias\n2001-2013",
            "isStacked": "true",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "gridlines": {
                    "count": 6
                }
            },
			"hAxis": {
                "showTextEvery": 2,
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 2}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": " ".join(var.var.var_nome.decode('iso-8859-1').split()[-4:]),
            "type": "number",
        })

    # Populacao: dados de 2000 a 2013
	# Populacao: dados de 2001 a 2013
    for ano in range(2001, 2014):
        c = [{"v": str(ano)}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo6_chart5(localidade):
    # Grafico Participação dos Setores no Total do Valor Adicionado
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1495).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1496).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1497).one(),
    ]

    chart = {
        "type": "LineChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Participação dos Setores da Economia no Total do Valor Adicionado\n2000-2011",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Em %",
                "gridlines": {
                    "count": 6
                }
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 2}
        },
        "fontes": get_fontes(vars)
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


def eixo6_chart6(localidade):
    # Grafico Participação dos Setores no Total dos Empregos Formais
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1045).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1046).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1047).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1475).one(),
    ]

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Participação dos Setores da Economia no Total dos Empregos Formais\n2000-2012",
            "isStacked": False,
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Em %",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "showTextEvery": 2,
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 2}
        },
        "fontes": get_fontes(vars)
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


def eixo6_chart7(localidade):
    # Grafico Indice Paulista de Responsabilisade Social, Por Dimensões
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=8).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=9).one(),
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=10).one(),
    ]

    chart = {
        "type": "BarChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
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
            "title": u"Índice Paulista de Responsabilidade Social, por Dimensões\n2008/2010",
            "isStacked": False,
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "gridlines": {
                    "count": 6
                }
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 2}
        },
        "fontes": get_fontes(vars)
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


def eixo6_chart8(localidade):
    # Grafico Índice Paulista de Responsabilidade Social
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=c).one()
        for c in [1468,1469,1470,1471,1472,1473,1474]
    ]

    chart = {
        "type": "PieChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "label": "Variavel",
                "type": "string",
              },
              {
                "label": "Valor",
                "type": "number",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Indice Paulista de Vulnerabilidade Social, segundo Grupos",
            "legend": { "position": "bottom", "maxLines": len(vars)}
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        label = var.var.var_nome.decode('iso-8859-1')
        c = [{"v": label}]
        coluna = "d_2010"
        f = getattr(var, coluna)
        v = get_var(f)
        c.append({"v": float(v), "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart

def eixo6_chart9(localidade):
    # Grafico Mães que tiveram 7 ou mais consultas de pre-natal
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=1028).one(),
    ]

    chart = {
        "type": "ColumnChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Mães que Tiveram Sete ou Mais Consultas de Pré-Natal\n2004-2012",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Em %",
                "gridlines": {
                    "count": 6
                }
            },
			"hAxis": {
                "showTextEvery": 2,
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "none" }
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": var.var.var_nome.decode('iso-8859-1'),
            "type": "number",
        })

    # Dados de 2000 a 2012
	# Dados de 2004 a 2011
    for ano in range(2004, 2012):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart


def eixo6_chart10(localidade):
    # Grafico Taxa de Mortalidade Infantil
    vars = [
        db.tb_dados.filter_by(loc_cod=localidade['loc_cod'], var_cod=63).one(),
    ]
    if localidade['loc_pai']:
        pai = db.tb_localidade.filter_by(loc_cod=localidade['loc_pai']).one()
        vars.append(
            db.tb_dados.filter_by(loc_cod=pai.loc_cod, var_cod=63).one(),
        )
        if pai.loc_pai:
            vars.append(
                db.tb_dados.filter_by(loc_cod=pai.loc_pai, var_cod=63).one(),
            )

    chart = {
        "type": "LineChart",
        "cssStyle": "height:{}px; width:{}px;".format(altura, largura),
        "data": {
            "cols": [
              {
                "id": "ano",
                "label": "Ano",
                "type": "string",
              }
            ],
            "rows": [],
        },
        "options": {
            "title": u"Taxa de Mortalidade Infantil\n2000-2012",
            "fill": 20,
            "displayExactValues": True,
            "vAxis": {
                "title": u"Por mil nascidos vivos",
                "gridlines": {
                    "count": 6
                }
            },
            "hAxis": {
                "title": ""
            },
            "formatters": {},
            "displayed": True,
            "legend": { "position": "bottom", "maxLines": 1 }
        },
        "fontes": get_fontes(vars)
    }

    for var in vars:
        local = db.tb_localidade.filter_by(loc_cod=var.loc_cod).one()
        chart['data']['cols'].append({
            "id": "v{}".format(var.var_cod),
            "label": u" - ".join([
                local.loc_nome.decode('iso-8859-1')
            ]),
            "type": "number",
        })

    # dados de 2009 a 2012
    for ano in range(2000, 2013):
        c = [{"v": ano}]
        coluna = "d_{}".format(ano)
        for var in vars:
            f = getattr(var, coluna)
            v = get_var(f)
            c.append({"v": v, "f": f.decode('iso-8859-1')})
        chart['data']['rows'].append({"c": c})

    return chart

######## fim eixo 6 ##############


###### fim dos modelos dos gráficos ###########

for localidade in localidades:
    local = localidade['loc_nome'].decode('iso-8859-1')
    print u"Processando {l[loc_cod]} {n}...".format(l=localidade, n=local)
    # Eixo 6
    charts = []
    charts.append(eixo6_chart1(localidade))
    charts.append(eixo6_chart2(localidade))
    charts.append(eixo6_chart3(localidade))
    charts.append(eixo6_chart4(localidade))
    charts.append(eixo6_chart5(localidade))
    charts.append(eixo6_chart6(localidade))
    charts.append(eixo6_chart7(localidade))
    charts.append(eixo6_chart8(localidade))
    charts.append(eixo6_chart9(localidade))
    charts.append(eixo6_chart10(localidade))

    with open('../data/charts/6-{}.json'.format(localidade['loc_cod']), 'wb') as o:
        o.write(json.dumps(charts, indent=2))

    # Eixo 0
    charts = []
    charts.append(eixo0_chart1(localidade))
    charts.append(eixo0_chart2(localidade))
    charts.append(eixo0_chart3(localidade))
    charts.append(eixo0_chart4(localidade))
    charts.append(eixo0_chart5(localidade))
    charts.append(eixo0_chart6(localidade))

    with open('../data/charts/0-{}.json'.format(localidade['loc_cod']), 'wb') as o:
        o.write(json.dumps(charts, indent=2))

    # Eixo 1
    charts = []
    charts.append(eixo1_chart1(localidade))
    charts.append(eixo1_chart2(localidade))
    charts.append(eixo1_chart3(localidade))
    charts.append(eixo1_chart4(localidade))
    charts.append(eixo1_chart5(localidade))
    charts.append(eixo1_chart6(localidade))

    with open('../data/charts/1-{}.json'.format(localidade['loc_cod']), 'wb') as o:
        o.write(json.dumps(charts, indent=2))



 # Eixo 2
    charts = []
    charts.append(eixo2_chart1(localidade))
    charts.append(eixo2_chart2(localidade))
    charts.append(eixo2_chart3(localidade))
    charts.append(eixo2_chart4(localidade))
    charts.append(eixo2_chart5(localidade))
    charts.append(eixo2_chart6(localidade))
    charts.append(eixo2_chart7(localidade))
    charts.append(eixo2_chart8(localidade))

    with open('../data/charts/2-{}.json'.format(localidade['loc_cod']), 'wb') as o:
        o.write(json.dumps(charts, indent=2))



 # Eixo 3
    charts = []
    charts.append(eixo3_chart1(localidade))
    charts.append(eixo3_chart2(localidade))
    charts.append(eixo3_chart3(localidade))
    charts.append(eixo3_chart4(localidade))

    with open('../data/charts/3-{}.json'.format(localidade['loc_cod']), 'wb') as o:
        o.write(json.dumps(charts, indent=2))



 # Eixo 4
    charts = []
    charts.append(eixo4_chart1(localidade))
    charts.append(eixo4_chart2(localidade))
    charts.append(eixo4_chart3(localidade))
    charts.append(eixo4_chart4(localidade))
    charts.append(eixo4_chart5(localidade))
    charts.append(eixo4_chart6(localidade))
    charts.append(eixo4_chart7(localidade))
    charts.append(eixo4_chart8(localidade))

    with open('../data/charts/4-{}.json'.format(localidade['loc_cod']), 'wb') as o:
        o.write(json.dumps(charts, indent=2))

 # Eixo 5
    charts = []
    charts.append(eixo5_chart1(localidade))
    # retirado por pedido do Vivaldo - charts.append(eixo5_chart2(localidade))
    charts.append(eixo5_chart3(localidade))
    # retirado por pedido do Vivaldo - charts.append(eixo5_chart4(localidade))

    with open('../data/charts/5-{}.json'.format(localidade['loc_cod']), 'wb') as o:
        o.write(json.dumps(charts, indent=2))
