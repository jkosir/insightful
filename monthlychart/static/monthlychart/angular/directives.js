angular.module('analyticsApp').directive('monthlyChart', ['constants', 'chartService',
    function (constants, chartService) {
        return {
            templateUrl: constants.staticUrl + 'monthlychart/partials/monthly-chart.html',
            scope: {},
            controller: ['$scope', '$element', '$attrs', function ($scope, $element, $attrs) {

                var seriesLabels = {};
                angular.forEach(constants.series, function (item) {
                    seriesLabels[item[0]] = item[1];
                });

                $scope.chartConfig = {
                    options: {
                        chart: {
                            type: 'line',
                            height: 200
                        },
                        tooltip: {
                            shared: true
                        }
                    },
                    title: {
                        text: null
                    },
                    series: [],
                    xAxis: {
                        type: 'datetime'
                    },
                    yAxis: {
                        min: 0,
                        title: null
                    }
                };
                Highcharts.setOptions({
                    plotOptions: {
                        line: {
                            animation: false
                        }
                    }
                });
                this.defaultSeries = function () {
                    return $attrs.ngSeries.split(/[, ]+/);
                };
                this.clearChart = function () {
                    $scope.chartConfig.series = [];

                    //Reset colour and symbol counters
                    var chart = Highcharts.charts[$('#monthlychart').data('highchartsChart')];
                    chart.counters.color = 0;
                    chart.counters.symbol = 0;

                };

                this.drawSeries = function (opt) {
                    opt = opt || [];
                    chartService.getData(opt, function (data) {
                        angular.forEach(opt, function (name, idx) {
                            $scope.chartConfig.series.push(
                                {
                                    data: data[name],
                                    name: seriesLabels[name],
                                    id: name,
                                    pointStart: new Date(data['start_date']).getTime(),
                                    pointInterval: 24 * 3600 * 1000 // one day
                                }
                            );
                            // Tooltip for avg time and avg active time
                            if (name.indexOf('avg') != -1) {
                                $scope.chartConfig.series[idx].tooltip = {
                                    valueSuffix: ' seconds',
                                    valueDecimals: 1
                                }
                            }
                        });
                    });

                };
                // Load default series from ng-series attribute
                this.drawSeries(this.defaultSeries());


            }]

        }

    }]);
angular.module('analyticsApp').directive('chartselect', ['constants', function (constants) {
    return {
        restrict: 'AEC',
        require: '^monthlyChart',
        link: function (scope, element, attributes, monthlyChart) {
            // Get jQuery wrapped element
            element = $(element[0]);

            // Render bootstrap multiselect
            element.multiselect({
                buttonText: function () {
                    return 'Select series ' + '<b class="caret"></b>'
                },
                onDropdownHide: function () {
                    scope.$apply(monthlyChart.clearChart());
                    scope.$apply(monthlyChart.drawSeries(element.val()));
                }
            });

            // Set choices
            var choices = [];
            angular.forEach(constants.series, function (option) {
                choices.push({label: option[1], value: option[0]})
            });
            element.multiselect('dataprovider', choices);

            // Select default series
            angular.forEach(monthlyChart.defaultSeries(), function (value) {
                element.multiselect('select', value);
            })

        }
    }
}]);


