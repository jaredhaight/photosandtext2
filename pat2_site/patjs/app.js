'use strict';

// Declare app level module which depends on filters, and services
angular.module('patjs', ['patjs.filters', 'patjs.directives','patSvc', 'ngCookies', 'blueimp.fileupload', 'ui.bootstrap']).
  config(['$routeProvider','$locationProvider', function($routeProvider, $locationProvider) {
    //$locationProvider.html5Mode(true);
    $routeProvider.when('/', {templateUrl: 'partials/photos.html', controller: photoListCtrl});
    $routeProvider.when('/photo/:photoID', {templateUrl: 'partials/photos.html', controller: photoListCtrl});
    $routeProvider.when('/upload', {templateUrl: 'partials/upload.html', controller: photoUploadCtrl});
    $routeProvider.otherwise({redirectTo: '/'});
  }]);
