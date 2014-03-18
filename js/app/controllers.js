angular.module('graficos.controllers', [])
    .controller('menuControllerDashboards', [
        '$scope',
        '$http',
        '$timeout',
        function ($scope, $http, $timeout) {
            $scope.data = [];
            $scope.lista = [];
            $scope.charts = [];
            $scope.localidade = {};
            $scope.localidades = [];
            $scope.menu_var = true;
            $scope.filtro = {
                $: '',
                loc_nivel: 99
            };

            $scope.eixo = 0;
            $scope.eixos = [
                "Educação Infantil - Pré-escola",
                "Educação Infantil - Creche",
                "Fundamental",
                "Ensino Técnico",
                "Ensino Médio",
                "Educação de Jovens e Adultos",
                "Condições Socioeconômicas"
            ];

            var updateCharts = function(curr, prev) {
                if(!curr) return;
                var old_eixo, old_local;
                if(typeof curr == 'number') {
                    old_eixo = prev;
                    old_local = $scope.localidade.loc_cod;
                } else {
                    old_eixo = $scope.eixo;
                    old_local = prev;
                }
                var local = $scope.localidade.loc_cod;
                if(!local) {
                    console.log(local);
                    return;
                }
                var old_charts = $scope.charts;

                $http({method: 'GET', url: 'data/charts/'+$scope.eixo+'-'+local+'.json'})
                    .success(function (data, status, headers, config) {
                        $scope.charts = data;
                    })
                    .error(function (data, status, headers, config) {
                        alert("Erro carregando dados.");
                        $scope.charts = [];
                        $scope.eixo = old_eixo;
                    });
            };
            $scope.$watch('eixo', updateCharts);
            $scope.$watch('localidade', updateCharts);

            $scope.setLocal = function(local) {
                $scope.localidade = local;
                if(local.loc_cod == 1000) {
                    $scope.busca = false;
                    $scope.filtro.loc_nivel = 99;
                } else {
                    $scope.busca = true;
                }
            };
            $scope.setNivel = function(nivel) {
                $scope.filtro.loc_nivel = nivel;
                if(nivel != 99) {
                    $scope.busca = true;
                }
            };

            $http({method: 'GET', url: 'data/variaveis.json'})
                .success(function (data, status, headers, config) {
                    $scope.data = data.menu;
                    $scope.lista = [data.menu[0]];
                })
                .error(function (data, status, headers, config) {
                    $scope.data = {
                        nome: "ERRO",
                        id: "erro",
                        itens: ""
                    };
                });
            $http({method: 'GET', url: 'data/localidades.json'})
                .success(function (data, status, headers, config) {
                    $scope.localidades = data.lista;
                    $scope.localidades.forEach(function(el, i) {
                        if(el.loc_cod == '1000') {
                            $scope.total = $scope.localidade = el;
                            $scope.busca = false;
                        }
                    });
                })
                .error(function (data, status, headers, config) {
                    alert("Erro carregando dados de localidades.");
                });
        }
    ])
    .controller('menuControllerMapas', [
        '$scope',
        '$http',
        function ($scope, $http) {
            $scope.data = [];

            $scope.lista = [];
            $scope.mapas = [];

            $scope.remove = function(i) {
                $scope.lista.splice(i, 1);
                $scope.mapas.splice(i, 1);
                $scope.item.currentNode = undefined;
            };

            $scope.make_legend = function(mapa) {
                var legend = {};
                var domain, scale, i;
                for(var j=0; j<mapa.features.length; j++) {
                    legend[mapa.features[j]] = {};
                    domain = mapa.domain[mapa.features[j]].sort(function(a,b){return a-b});
                    scale = d3.scale.quantile().domain(domain).range(mapa.range);
                    for(i=0; i<mapa.range.length; i++) {
                        legend[mapa.features[j]][mapa.range[i]] = [];
                    }
                    for(i=0; i<domain.length; i++) {
                        legend[mapa.features[j]][scale(domain[i])].push(domain[i]);
                    }
                }
                return legend;
            };

            $scope.$watch('item.currentNode', function(curr, prev) {
                if(!curr) return;

                if($scope.lista.indexOf(curr.id) == -1) {
                    var ultimo_ano = curr.anos.slice(-1)[0];
                    console.log(curr);
                    $scope.lista.unshift(curr.id);
                    $scope.mapas.unshift({
                        id: curr.id,
                        info: {},
                        feature: curr.features[0],
                        parse: {valor: "number"},
                        title: curr.nome,
                        current: ultimo_ano,
                        alternatives: curr.anos,
                        scale: curr.scale,
                        domain: curr.domain,
                        range: curr.range,
                        features: curr.features,
                        featureLabels: {
                            mun: "Municipios",
                            ra: "Regiões Administrativas",
                            rm: "Regiões Metropolitanas"
                        },
                        legenda: $scope.make_legend(curr),
                        fontes: "Fonte: " + curr.fonte.join(" , ")
                    })
                }
            });

            $http({method: 'GET', url: 'data/variaveis.json'}).
                success(function (data, status, headers, config) {
                    $scope.data = data.menu;
                }).
                error(function (data, status, headers, config) {
                    $scope.data = {
                        nome: "ERRO",
                        id: "erro",
                        itens: ""
                    };
                });
        }
    ]);

