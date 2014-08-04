angular.module('analyticsApp.controllers').controller('OverviewCtrl',
    ['$scope', '$http', 'constants', 'djangoUrl', function ($scope, $http, constants, djangoUrl) {

        $http.post(djangoUrl.reverse('api:overview', [constants.website.id]),
            {action: 'get_data'}).success(function (out_data) {
                $scope.data = out_data;
            });
    }]);
