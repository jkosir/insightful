angular.module('analyticsApp.controllers').controller('ContentCtrl',
    ['$scope', '$http', 'constants', function ($scope, $http, constants) {

        var chartConfig = {
            "options": {
                "chart": {
                    type: "column",
                    height: 300
                },
                "plotOptions": {
                    "series": {
                        "stacking": "percent"
                    }
                },
                tooltip: {
                    pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y:.1f}</b> seconds ({point.percentage:.0f}%)<br/>'
                }
            },

            "series": [
            ],
            "title": {
                "text": null
            },
            yAxis: {
                title: null
            },
            xAxis: {
                type: 'datetime'
            }
        };
        $scope.barCharts = [];

        $http.post(constants.urls.content, {action: 'get_data'}).success(function (out_data) {
            $scope.pages = out_data.pages;

            angular.forEach(out_data.interactions, function (value, key) {
                var config = angular.copy(chartConfig);
                config.path = key;

                angular.forEach(value, function (serie_values, serie_name) {
                    config.series.push({
                        name: serie_name,
                        data: serie_values,
                        pointStart: new Date(out_data['start_date']).getTime(),
                        pointInterval: 24 * 3600 * 1000 // one day
                    });
                });

                $scope.barCharts.push(config);
            });
        });

    }]);


