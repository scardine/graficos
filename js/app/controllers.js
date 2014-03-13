angular.module('graficos.controllers', [])
    .controller('menuControllerDashboards', [
        '$scope',
        '$http',
        function ($scope, $http) {
            $scope.data = [];
            $scope.lista = [];
            $scope.charts = [];
            $scope.localidade = {
                "loc_cod_ibge": 1000,
                "loc_cod": 1000,
                "nome": "Total do Estado de Sao Paulo",
                "loc_nome": "Total do Estado de São Paulo",
                "loc_pai": 0,
                "loc_ordem": "1000.000.000.000",
                "loc_nivel": 0
            };
            $scope.localidades = [];
            $scope.menu_var = true;
            $scope.filtro = {
                $: '',
                loc_nivel: 70
            };

            $scope.$watch('item.currentNode', function(curr, prev) {
                if(!curr) return;
                console.log(curr);
            });

            $scope.setLocal = function(local) {
                $scope.localidade = local;
            };

            $http({method: 'GET', url: 'data/variaveis.json'})
                .success(function (data, status, headers, config) {
                    $scope.data = data.menu;
                    $scope.lista = [data.menu[0]];
                    $scope.item.currentNode = data.menu[0];
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
                    console.log($scope.localidades);
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
                            ra: "Região Administrativa",
                            rm: "Regiões Metropolitanas"
                        }
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

