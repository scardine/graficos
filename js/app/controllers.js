angular.module('graficos.controllers', [])
    .controller('menuController', [
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
                        range: curr.range
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

