angular.module('graficos', [
        'ui.router',
        'ngResource',
        //'angular-flash.service',
        //'angular-flash.flash-alert-directive',
        'angularTreeview',
        'graficos.controllers',
        'graficos.directives',
        'googlechart'
    ])
    .run([
        '$rootScope',
        '$state',
        function($rootScope, $state, $stateParams) {
            $rootScope.$state = $state;
            $rootScope.$stateParams = $stateParams;
            $rootScope.user = {};
        }
    ]);
    //.config(function(flashProvider) {
    //    flashProvider.errorClassnames.push('alert-danger');
    //});