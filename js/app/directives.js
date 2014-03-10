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
                options: '=',
                scale: '=',
                domain: '='
            },
            link: function(scope, element, attrs) {
                scope.data = {};

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
                            "range": ["#f7fbff", "#deebf7", "#c6dbef", "#9ecae1", "#6baed6",
                                        "#4292c6", "#2171b5", "#08519c", "#08306b"]
                        }
                    ],
                    "marks": [
                        {
                            "type": "path",
                            "from": {"data": "topology"},
                            "delay": {"value": 1000},
                            "properties": {
                                "enter": {"path": {"field": "path"}, "stroke": {"value": "#999"}},
                                "update": {"fill": {"scale":"color", "field":"value.data.valor"}},
                                "hover": {"fill": {"value": "red"}}
                            }
                        }
                    ]
                };

                scope.$watch('url', function(curr, prev) {
                    if(curr) {
                        console.log(curr);
                        scope.spec.data[0].url = curr;
                        scope.spec.scales[0].domain = scope.domain;
                        scope.spec.scales[0].type = scope.scale;
                        d3.tsv(curr, function(data) {
                            if(data === null) {
                                alert("Falha ao carregar arquivo " + curr);
                                return;
                            }
                            $.each(data, function(i, elem) {
                                scope.data[elem.ibge] = elem;
                            });
                            scope.$apply();
                        });
                    }
                    parse(scope.spec);
                });

                function parse(spec, options) {
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
                        m.update(options);
                    });
                }

                scope.next.bind('click', function(ev) {
                    if(scope.current == scope.options.slice(-1)[0]) return;
                    var next = scope.options.indexOf("" + scope.current) + 1;
                    if(next >= 0 && next < scope.options.length) scope.current = scope.options[next];
                    scope.info = undefined;
                    scope.$apply();
                });

                scope.prev.bind('click', function(ev) {
                    if(scope.current == scope.options[0]) return;
                    var previous = scope.options.indexOf("" + scope.current) - 1;
                    if(previous >= 0) scope.current = scope.options[previous];
                    scope.info = undefined;
                    scope.$apply();
                });
            }
        }
    })
;
