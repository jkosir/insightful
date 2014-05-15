angular.module('analyticsApp').factory('chartService', ['$http', 'constants', '$filter',
    function ($http, constants, $filter) {
        var cache = {};

        return  {
            getData: function (datasets, callback) {
                var notCached = $filter('filter')(datasets, function (item) {
                    return typeof cache[item] === 'undefined'
                });

                notCached = notCached || [];

                if (notCached.length >= 1) {
                    $http.post(constants.urls.monthlychart, {datasets: notCached}).success(
                        function (out_data) {
                            angular.forEach(out_data, function (dataset, name) {
                                cache[name] = dataset;
                            });
                            callback(cache);
                        });

                }
                else {
                    callback(cache);
                }
            }


        }
    }]);