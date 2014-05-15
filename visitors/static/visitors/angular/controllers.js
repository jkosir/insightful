angular.module('analyticsApp.controllers').controller('VisitorsCtrl',
    ['$scope', '$http', 'constants', function ($scope, $http, constants) {
        $http.post(constants.urls.visitors, {action: 'get_data'}).success(function (out_data) {
            angular.forEach(out_data, function(value, key){
                $scope[key] = value;
            });
        });


    }]);


