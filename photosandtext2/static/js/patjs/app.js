'use strict';

// Declare app level module which depends on filters, and services
angular.module('patjs', ['patSvc','ngRoute', 'patjs.directives','mm.foundation']).config(['$routeProvider','$locationProvider', function($routeProvider, $locationProvider) {
    $routeProvider.when('/', {templateUrl: '/static/js/patjs/partials/edit.html',  controller: photoListCtrl});
    $routeProvider.when('/:galleryID', {templateUrl: '/static/js/patjs/partials/edit.html',  controller: photoListCtrl});
    $routeProvider.otherwise({redirectTo: '/'});
  }]).config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});