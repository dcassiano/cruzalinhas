# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Carlos Duarte do Nascimento (Chester)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this 
# software and associated documentation files (the "Software"), to deal in the Software 
# without restriction, including without limitation the rights to use, copy, modify, merge, 
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons 
# to whom the Software is furnished to do so, subject to the following conditions:
#     
# The above copyright notice and this permission notice shall be included in all copies or 
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.
#
"""Carrega um ou mais pontos a partir de um CSV no appengine. "linha" é o nome da linha

Exemplo de chamada na linha de comando (trocar o valor de "cookie" por um pego
após um login, e a URL para a do servidor conforme o caso):

python2.5 /usr/local/bin/bulkload_client.py --filename=pontos.csv 
  --url=http://localhost:8080/load-ponto --kind=Ponto 
  --cookie "dev_appserver_login=\"test@example.com:True:185804764220139124118\""

"""
from google.appengine.ext import bulkload
from google.appengine.api import datastore_types
from google.appengine.ext import search
from models import Ponto, Linha
import geohash

class PontoLoader(bulkload.Loader):
    def __init__(self):
        bulkload.Loader.__init__(self, 'Ponto',
                         [('nome', lambda x: x.decode('utf-8')),
                          ('ordem', int),
                          ('lat', float),
                          ('lng', float)])

    def HandleEntity(self, entity):
        linha = Linha.all().filter("nome =", entity["nome"]).fetch(1)[0]
        ponto = Ponto(ordem=entity["ordem"], linha=linha,
                      lat=entity["lat"], lng=entity["lng"])
        pontosAnt = Ponto.all().filter("linha =", linha).filter(
            "ordem =", ponto.ordem - 1).fetch(1)
        if pontosAnt:
            pontoAnt = pontosAnt[0]
            ponto.setNearhash(pontoAnt)
        ponto.put()
        return None

if __name__ == '__main__':
    bulkload.main(PontoLoader())

