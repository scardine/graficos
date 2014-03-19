angular.module('graficos.controllers', [])
    .controller('menuControllerDashboards', [
        '$scope',
        '$http',
        '$timeout',
        function ($scope, $http, $timeout) {
            $scope.data = [];
            $scope.lista = [];
            $scope.charts = [];
            $scope.localidade = {};
            $scope.localidades = [];
            $scope.menu_var = true;
            $scope.filtro = {
                $: '',
                loc_nivel: 99
            };

            $scope.eixo = 0;
            $scope.eixos = [
                "Educação Infantil - Pré-escola",
                "Educação Infantil - Creche",
                "Fundamental",
                "Ensino Técnico",
                "Ensino Médio",
                "Educação de Jovens e Adultos",
                "Condições Socioeconômicas"
            ];

            var updateCharts = function(curr, prev) {
                if(!curr) return;
                var old_eixo, old_local;
                if(typeof curr == 'number') {
                    old_eixo = prev;
                    old_local = $scope.localidade.loc_cod;
                } else {
                    old_eixo = $scope.eixo;
                    old_local = prev;
                }
                var local = $scope.localidade.loc_cod;
                if(!local) {
                    console.log(local);
                    return;
                }
                var old_charts = $scope.charts;

                $http({method: 'GET', url: 'data/charts/'+$scope.eixo+'-'+local+'.json'})
                    .success(function (data, status, headers, config) {
                        $scope.charts = data;
                    })
                    .error(function (data, status, headers, config) {
                        alert("Erro carregando dados.");
                        $scope.charts = [];
                        $scope.eixo = old_eixo;
                    });
            };
            $scope.$watch('eixo', updateCharts);
            $scope.$watch('localidade', updateCharts);

            $scope.setLocal = function(local) {
                $scope.localidade = local;
                if(local.loc_cod == 1000) {
                    $scope.busca = false;
                    $scope.filtro.loc_nivel = 99;
                } else {
                    $scope.busca = true;
                }
            };
            $scope.setNivel = function(nivel) {
                $scope.filtro.loc_nivel = nivel;
                if(nivel != 99) {
                    $scope.busca = true;
                }
            };

            $http({method: 'GET', url: 'data/variaveis.json'})
                .success(function (data, status, headers, config) {
                    $scope.data = data.menu;
                    $scope.lista = [data.menu[0]];
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
                    $scope.localidades.forEach(function(el, i) {
                        if(el.loc_cod == '1000') {
                            $scope.total = $scope.localidade = el;
                            $scope.busca = false;
                        }
                    });
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

            $scope.make_legend = function(mapa) {
                var legend = {};
                var domain, scale, i;
                for(var j=0; j<mapa.features.length; j++) {
                    legend[mapa.features[j]] = {};
                    domain = mapa.domain[mapa.features[j]].sort(function(a,b){return a-b});
                    scale = d3.scale.quantile().domain(domain).range(mapa.range);
                    for(i=0; i<mapa.range.length; i++) {
                        legend[mapa.features[j]][mapa.range[i]] = [];
                    }
                    for(i=0; i<domain.length; i++) {
                        legend[mapa.features[j]][scale(domain[i])].push(domain[i]);
                    }
                }
                return legend;
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
                            ra: "Regiões Administrativas",
                            rm: "Regiões Metropolitanas"
                        },
                        legenda: $scope.make_legend(curr),
                        fontes: "Fonte: " + curr.fonte.join(" , ")
                    })
                }
            });

            $http({method: 'GET', url: 'data/variaveis.json'}).
                success(function (data, status, headers, config) {
                    $scope.data = data.menu;
                    // mapa default
                    $scope.item.currentNode = {"fonte":[""],"range":["#AAAAFF","#8C8CEA","#6F6FD5","#5151BF","#3333AA"],"scale":"quantile","itens":[],"features":["mun","ra","rm"],"domain":{"rm":[71309,105293,120525,949041],"mun":[34,43,43,51,51,51,52,56,56,59,59,59,61,63,64,69,71,72,77,79,79,81,82,82,83,83,83,83,87,87,88,88,88,88,90,92,93,94,97,99,100,101,101,101,101,102,104,104,104,109,111,113,113,113,114,116,118,118,119,119,122,122,123,123,123,124,127,128,129,133,134,134,134,134,134,135,138,138,139,139,139,141,142,142,142,143,144,144,145,145,145,146,147,148,149,149,149,150,152,152,153,153,154,156,156,156,156,156,158,159,160,160,161,162,166,167,171,173,173,175,175,175,176,177,178,179,180,182,182,185,186,186,187,187,187,188,189,190,190,191,195,195,196,198,200,202,203,203,204,205,206,206,207,208,209,209,212,212,213,216,216,218,219,219,221,223,225,225,225,227,228,232,232,234,236,239,239,240,240,241,243,243,244,244,245,246,247,247,247,248,250,250,251,252,253,253,253,254,256,261,262,263,263,264,264,265,268,269,269,270,270,271,271,271,274,276,277,278,281,283,284,286,288,292,293,294,295,295,296,298,298,302,304,305,306,307,308,308,311,315,316,317,317,319,326,328,328,328,330,335,336,336,337,341,341,346,349,352,354,355,356,358,358,361,362,366,366,367,369,374,376,376,376,378,383,384,387,390,390,394,396,396,396,397,401,402,404,406,407,411,412,414,422,428,429,433,435,437,441,441,442,446,449,451,451,454,457,461,462,463,468,471,471,473,474,475,477,477,478,479,493,497,502,507,507,509,514,516,516,519,521,521,524,540,542,543,553,559,566,567,567,568,573,574,578,583,596,598,610,614,615,619,619,621,621,623,625,630,631,639,641,644,649,656,660,663,666,683,687,690,697,702,712,716,721,723,725,734,735,739,739,741,748,755,761,762,763,770,771,778,781,793,796,798,803,806,825,826,826,833,835,837,855,858,875,885,894,899,901,903,909,910,915,916,922,930,943,948,961,965,968,978,990,1002,1006,1023,1039,1043,1045,1059,1063,1063,1076,1078,1088,1091,1105,1115,1125,1125,1128,1131,1137,1155,1192,1194,1201,1218,1222,1229,1231,1236,1260,1264,1284,1293,1301,1302,1311,1318,1326,1328,1331,1339,1347,1361,1361,1367,1412,1415,1450,1453,1454,1460,1481,1487,1489,1514,1526,1531,1533,1537,1569,1583,1589,1597,1599,1600,1610,1612,1614,1672,1700,1735,1747,1748,1802,1829,1840,1865,1888,1903,1912,1942,1945,1947,1958,1996,2032,2054,2057,2071,2100,2128,2131,2169,2173,2186,2203,2213,2278,2288,2316,2323,2376,2381,2393,2419,2484,2486,2487,2489,2541,2574,2722,2781,2804,2814,2832,2876,2910,2998,3004,3007,3133,3276,3304,3321,3340,3365,3393,3396,3477,3549,3590,3591,3610,3610,3666,3732,3757,3821,3846,3939,4021,4053,4068,4202,4333,4422,4467,4507,4516,4532,4781,4786,4812,4915,4926,4960,4993,5091,5115,5338,5362,5367,5396,5414,5452,5875,6231,6263,6395,6418,6650,6737,6950,7213,7289,7396,7491,8289,8411,8821,8837,8974,9192,9410,9430,9791,10047,10239,10239,10897,11078,11279,11306,11543,11639,11982,12229,12385,14577,14784,14927,15667,16168,16260,16264,17118,17578,17640,17691,18935,20014,20107,25843,28442,30752,31739,34415,37267,43707,67506,504615],"ra":[13406,16773,29830,31422,36238,39534,40357,44362,52579,57704,71309,105293,128005,269254]},"nome":"Matrícula Inicial no Ensino Médio","legenda":{"rm":["até 79.465","mais de 79.465 até 106.511","mais de 106.511 até 119.306","mais de 119.306 até 750.197","mais de 750.197"],"mun":["até 183","mais de 183 até 352","mais de 352 até 766","mais de 766 até 2.171","mais de 2.171"],"ra":["até 30.212","mais de 30.212 até 39.599","mais de 39.599 até 51.921","mais de 51.921 até 97.136","mais de 97.136"]},"id":166,"anos":[2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012],"$$hashKey":"00K","selected":"selected"};
                    $scope.mapas.append($scope.item.currentNode);
                    $scope.lista.append($scope.item.currentNode.id);
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

