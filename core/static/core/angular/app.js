var analyticsApp = angular.module('analyticsApp', [
        'analyticsApp.controllers',
        'analyticsApp.filters',
        'ngCookies',
        'ui.router',
        'ui.bootstrap',
        'chieffancypants.loadingBar',
        'highcharts-ng'
    ]).run(function ($http, $cookies) {
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.xsrfCookieName = 'csrftoken';
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    // Add csrf header to post and delete requests
}).config(function ($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    // Adherent to convention ajax request shall have X-Requested-With XMLHttpRequest header
}).config(function (cfpLoadingBarProvider) {
    cfpLoadingBarProvider.includeSpinner = false;
    cfpLoadingBarProvider.startSize = 0.15;
});

analyticsApp.config(['$stateProvider', '$urlRouterProvider', 'constants', '$locationProvider',
    function ($stateProvider, $urlRouterProvider, constants, $locationProvider) {
        $locationProvider.html5Mode(true);
        $urlRouterProvider.otherwise("/overview");

        $stateProvider
            .state('overview', {
                url: '/overview',
                controller: 'OverviewCtrl',
                templateUrl: constants.staticUrl + 'overview/partials/overview.html',
                data: {title: 'Overview'}

            }).
            state('engagement', {
                url: '/engagement',
                controller: 'EngagementCtrl',
                templateUrl: constants.staticUrl + 'engagement/partials/engagement.html',
                data: {title: 'Engagement'}
            }).
            state('visitors', {
                url: '/visitors',
                controller: 'VisitorsCtrl',
                templateUrl: constants.staticUrl + 'visitors/partials/visitors.html',
                data: {title: 'Visitors'}
            }).
            state('content', {
                url: '/content',
                controller: 'ContentCtrl',
                templateUrl: constants.staticUrl + 'content/partials/content.html',
                data: {title: 'Content'}
            });
    }]);

angular.module('analyticsApp.controllers', []);

analyticsApp.run(['$rootScope', '$state', 'constants', function ($rootScope, $state, constants) {
    //Change title to title from routeProvider
    $rootScope.$on('$stateChangeSuccess', function (event, current, previous) {
        if ($state.current.data.title) {
            $rootScope.title = $state.current.data.title;
        }
    });
    //Collapsed by default
    $rootScope.navbarCollapse = true;

    $rootScope.website = constants.website;
}]);
