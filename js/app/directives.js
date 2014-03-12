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
    })
    .directive('vegaMap', function() {
        return {
            restrict: 'E',
            templateUrl: '/graficos/js/app/html/vega-map.html',
            transclude: true,
            scope: {
                url: '@',
                info: '=',
                width: '@',
                height: '@',
                feature: '=',
                features: '=',
                featureLabels: '=',
                geometry: '@',
                parse: '=',
                title: '@',
                scale: '@',
                domain: '=',
                range: '=',
                current: '=',
                alternatives: '=',
                remove: '&onClose'
            },
            link: function(scope, element, attrs) {
                scope.$watch('url', function(curr, prev) {
                    console.log(curr, prev);
                    if(curr) {
                        d3.tsv(curr, function(data) {
                            scope.data = {};
                            $.each(data, function(i, elem) {
                                scope.data[elem.ibge] = elem;
                            });
                            scope.spec.data[0].url = curr;
                            scope.spec.data[1].format.feature = scope.feature;
                            scope.spec.data[1].url = 'data/'+scope.feature+'.topo.json';
                            parse(scope.spec);
                            scope.$apply();
                        });
                    }
                });

                scope.spec = {
                    "width": parseInt(scope.width),
                    "height": parseInt(scope.height),
                    "data": [
                        {
                            "name": "source",
                            "url": scope.url,
                            "format": {"type": "tsv", "parse": scope.parse}
                        },
                        {
                            "name": "topology",
                            "url": scope.geometry,
                            "format": {"type": "topojson", "feature": scope.feature},
                            "transform": [
                                {
                                    "type": "geopath",
                                    "value": "data",
                                    "projection": "mercator",
                                    "center": [-48.0, -22.5459886162543],
                                    "scale": 5000
                                },
                                {
                                    "type": "zip",
                                    "key": "data.properties.CD_GEOCODM",
                                    "with": "source",
                                    "withKey": "data.ibge",
                                    "as": "value",
                                    "default": null
                                },
                                {"type":"filter", "test":"d.path!=null && d.value!=null"}
                            ]
                        }
                    ],
                    "scales": [
                        {
                            "name": "color",
                            "type": scope.scale,
                            "domain": scope.domain,
                            "range": scope.range
                        }
                    ],
                    "marks": [
                        {
                            "type": "path",
                            "from": {"data": "topology"},
                            "properties": {
                                "enter": { "path": {"field": "path"}, "stroke": {"value": "#999999"} },
                                "update": { "fill": {"scale":"color", "field":"value.data.valor"} },
                                "hover": { "fill": {"value": "red"} }
                            }
                        }
                    ]/*,
                    "legends": [
                       {
                         "fill": "color",
                         "properties": {
                           "title": {
                             "fontSize": {"value": 14}
                           },
                           "labels": {
                             "fontSize": {"value": 12}
                           },
                           "symbols": {
                             "stroke": {"value": "transparent"}
                           }
                         }
                       }
                    ]*/
                };

                function parse(spec) {
                    vg.parse.spec(spec, function(chart) {
                        var m = chart({el: scope.vis[0]});
                        m.on("mouseover", function(event, item) {
                            scope.info = scope.data[item.datum.data.properties.CD_GEOCODM];
                            scope.$apply();
                        });
                        m.update();
                    });
                }

                scope.next.bind('click', function(ev) {
                    console.log('next', scope.current);
                    if(scope.current == scope.alternatives.slice(-1)[0]) return;
                    scope.current = scope.alternatives[scope.alternatives.indexOf(scope.current) + 1];
                    scope.info = {};
                    scope.$apply();
                });
                scope.prev.bind('click', function(ev) {
                    console.log('prev', scope.current);
                    if(scope.current == scope.alternatives[0]) return;
                    scope.current = scope.alternatives[scope.alternatives.indexOf(scope.current) - 1];
                    scope.info = {};
                    scope.$apply();
                });
                scope.setLevel = function(f) {
                    scope.feature = f;
                };
            }
        }
    })
;
