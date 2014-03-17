#coding:utf-8

import json
import csv
import sqlsoup
import csv
import os
from unidecode import unidecode

db = sqlsoup.SQLSoup('mysql://usu_simedu:usu_simedu@172.16.16.135:3306/simeducacao')
db.tb_variavel.relate(
    'dados',
    db.tb_dados,
    primaryjoin=db.tb_dados.var_cod==db.tb_variavel.var_cod,
    foreign_keys=[db.tb_dados.var_cod]
)
db.tb_dados.relate(
    'localidade',
    db.tb_localidade,
    primaryjoin=db.tb_localidade.loc_cod==db.tb_dados.loc_cod,
    foreign_keys=[db.tb_dados.loc_cod]
)

datum = []
with open("variaveis.csv") as i:
    reader = csv.reader(i)
    head = reader.next()
    for line in reader:
        datum.append(dict(zip(head, line)))

for variavel in datum:
    for k, v in variavel.items():
        if isinstance(v, unicode): continue
        try:
            variavel[k] = v.decode('utf-8')
        except UnicodeError:
            print k, v
    if not variavel["var_cod"]: continue
    print "processando", variavel["var_cod"], variavel["var_nome"]
    var = db.tb_variavel.get(variavel['var_cod'])
    if not var:
        print "Variavel nao encontrada:", unidecode(variavel['var_nome'])
        continue

    anos = [int(ano) for ano in variavel['var_periodo'].split(",")]

    for ano in anos:
        print ano,
        if 'd_{}'.format(ano) not in db.tb_dados.c:
            print "Ano {} nao encontrado pra variavel {}".format(ano, unidecode(variavel['var_nome']))
            continue
        if not var.dados:
            print "Dados nao encontrados..."
        for feature, loc_nivel in (('mun', 70), ('ra', 10), ('rg', 20), ('rm', 30)):
            if not os.path.isdir('../data/{}'.format(feature)):
                os.mkdir('../data/{}'.format(feature))
            if not os.path.isdir('../data/{}/{}'.format(feature, variavel['var_cod'])):
                os.mkdir('../data/{}/{}'.format(feature, variavel['var_cod']))
            with open('../data/{}/{}/{}.tsv'.format(feature, variavel['var_cod'], ano), "wb") as o:
                try:
                    writer = csv.writer(o, delimiter='\t')
                    writer.writerow(["id", "ibge", "localidade", "valor", "label"])
                    for data in var.dados:
                        if not data.localidade:
                            print "localidade {} nao encontrada para variavel {}".format(data.loc_cod, data.var_cod)
                            continue

                        if loc_nivel == 10 and data.localidade.loc_nivel == 30 and data.localidade.loc_cod == 681:
                            pass
                        elif data.localidade.loc_nivel != loc_nivel:
                            continue

                        if not data.localidade:
                            print "Localidade nao encontrada:", data.loc_cod
                            continue
                        label = getattr(data, 'd_{}'.format(ano))
                        label = label.decode('iso-8859-1').encode('utf-8')
                        if label.startswith('Grupo '):
                            valor = int(label[6])
                        else:
                            valor = label.replace('.', '').replace(',', '.')
                            label = variavel["var_nome"].encode('utf-8') + ": " + label
                        writer.writerow([
                            data.localidade.loc_cod,
                            data.localidade.loc_cod_ibge,
                            data.localidade.loc_nome.decode('iso-8859-1').encode('utf-8'),
                            valor,
                            label,
                        ])
                except Exception as e:
                    print e
    print
