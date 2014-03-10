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
                feature: '@',
                geometry: '@',
                parse: '=',
                title: '@',
                current: '=',
                options: '='
            },
            link: function(scope, element, attrs) {
                scope.$watch('url', function(curr, prev) {
                    if(curr) {
                        d3.tsv(curr, function(data) {
                            if(data === null) {
                                alert("Falha ao carregar arquivo " + curr);
                                return;
                            }
                            scope.data = {};
                            $.each(data, function(i, elem) {
                                scope.data[elem.ibge] = elem;
                            });
                            scope.$apply();
                        });
                    }
                });

                var spec = {
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
                            "type": "quantize",
                            "domain": [0, 5],
                            "range": ["#f7fbff", "#deebf7", "#c6dbef", "#9ecae1", "#6baed6"]
                        }
                    ],
                    "marks": [
                        {
                            "type": "path",
                            "from": {"data": "topology"},
                            "properties": {
                                "enter": { "path": {"field": "path"} },
                                "update": { "fill": {"scale":"color", "field":"value.data.valor"} },
                                "hover": { "fill": {"value": "red"} }
                            }
                        }
                    ]
                };

                function parse(spec) {
                    vg.parse.spec(spec, function(chart) {
                        var m = chart({el: scope.vis[0]});
                        m.on("mouseover", function(event, item) {
                            scope.info = scope.data[item.datum.data.properties.CD_GEOCODM];
                            scope.$apply();
                        });
                        /* m.on("mouseout", function(event, item) {
                            scope.info = undefined;
                            scope.$apply();
                        }); */
                        m.update();
                    });
                }
                parse(spec);
            }
        }
    })
;
