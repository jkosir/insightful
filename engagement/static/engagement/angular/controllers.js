angular.module('analyticsApp.controllers').controller('EngagementCtrl',
    ['$scope', '$http', 'constants', function ($scope, $http, constants) {
        $scope.pieChartConfigs = [];

        var pieConfig = {
            options: {
                chart: {
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: true,
                    height: 340,
                    type: 'pie'
                },
                tooltip: {
                    pointFormat: '{series.name}: <b>{point.y:.2f} seconds</b><br>Percentage: <b>{point.percentage:.0f}%</b>'
                }
            },
            title: {
                text: ' '
            },

            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.0f} %'
                    }
                }
            },
            series: [
                {
                    type: 'pie',
                    name: 'Average interaction duration',
                    data: []
                }
            ]
        };

        $http.post(constants.urls.engagement, {action: 'get_data'}).success(function (out_data) {
            angular.forEach(out_data.content, function (value, key) {
                var config = angular.copy(pieConfig);
                config.series[0].data = value;
                $scope.pieChartConfigs.push([key, config]);
            });
        });

    }]);


