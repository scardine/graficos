angular.module('graficos.controllers', [])
    .controller('menuController', [
        '$scope',
        '$http',
        function ($scope, $http) {
            $scope.data = [];
            $scope.title = "Índice Paulista de Responsabilidade Social (grupos)";
            $scope.item = {};
            $scope.var = {
                ano: 2010,
                codigo: 7,
                anos: [2008, 2010],
                scale: 'quantize',
                domain: [0, 5]
            };


            $http({method: 'GET', url: 'data/variaveis.json'})
                .success(function (data, status, headers, config) {
                    $scope.data = data.menu;
                    $scope.data[0].collapsed = $scope.data[0].itens[0].collapsed = false;
                    $scope.item.selectNodeLabel($scope.data[0].itens[0].itens[0]);
                })
                .error(function (data, status, headers, config) {
                    $scope.data = {
                        nome: "ERRO",
                        id: "erro",
                        itens: ""
                    };
                });

            $scope.$watch(function() {return $scope.item.currentNode;}, function(curr, prev) {
                if(typeof curr == 'undefined') return;
                if(!curr) return;
                if(isNaN(parseInt(curr.id))) return;
                if(curr.anos) {
                    $scope.var.ano = parseInt(curr.anos.split(',').pop());
                    $scope.var.anos = curr.anos.split(',');
                }
                if(curr.id) $scope.var.codigo = curr.id;
                if(curr.nome) $scope.title = curr.nome;
                if(curr.domain) $scope.var.domain = curr.domain;
                if(curr.scale) $scope.var.scale = curr.scale;
            });
        }
    ]);

