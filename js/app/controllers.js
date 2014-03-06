angular.module('graficos.controllers', [])
    .controller('menuController', [
        '$scope',
        '$http',
        function ($scope, $http) {
            $scope.data = [];

            $http({method: 'GET', url: 'data/variables.json'}).
                success(function (data, status, headers, config) {
                    $scope.data = data;
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