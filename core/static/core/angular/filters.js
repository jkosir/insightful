angular.module('analyticsApp.filters', [])
    .filter('secondsdisplay', function () {
        return function (num_seconds) {
            var minutes = Math.floor(num_seconds / 60);
            var seconds = Math.floor(num_seconds % 60);
            if (minutes == 0){
                return seconds + ' seconds';
            }
            else if (minutes == 1){
                return minutes + ' minute ' + seconds + ' seconds';
            }
            else {
                return minutes + ' minutes ' + seconds + ' seconds';
            }

        };
    });