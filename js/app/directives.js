angular.module('graficos.directives', [])
    .directive('scopeRef', function() {
        return {
            restrict: 'A',
            priority: 1200,
            compile: function(tElement, tAttrs, transclude) {
                return {
                    pre: function(scope, element, attrs) {
                        scope[attrs.scopeRef] = element;
                        element.on('$destroy', function() {
                            scope[attrs.scopeRef] = null;
                        });
                    }
                };
            }
        }
    });
