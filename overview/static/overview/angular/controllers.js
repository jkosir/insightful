angular.module('analyticsApp.controllers').controller('OverviewCtrl',
    ['$scope', '$http', 'constants', function ($scope, $http, constants) {

        $http.post(constants.urls.overview, {action: 'get_data'}).success(function (out_data) {
            $scope.data = out_data;
        });


    }]);


