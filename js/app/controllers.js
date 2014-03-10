angular.module('graficos.controllers', [])
    .controller('menuController', [
        '$scope',
        '$http',
        function ($scope, $http) {
            $scope.data = [];
            $scope.title = "Indice Paulista de Responsabilidade Social (grupos)";
            $scope.item = {};
            $scope.ano = 2010;
            $scope.codigo = 7;
            $scope.anos = [2008, 2010];


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
                if(curr && isNaN(parseInt(curr.id))) return;
                if(curr && curr.anos) {
                    $scope.ano = parseInt(curr.anos.split(',').pop());
                    $scope.anos = curr.anos.split(',');
                }
                if(curr && curr.id) $scope.codigo = curr.id;
            });
        }
    ]);

