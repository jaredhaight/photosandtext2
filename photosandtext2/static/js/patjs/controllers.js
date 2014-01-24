'use strict';

function photoListCtrl($scope, galleryClient, $route, $routeParams, $rootScope, $http, $location) {
    delete $http.defaults.headers.common['X-Requested-With'];
    $scope.gallery = galleryClient.get({galleryID: $routeParams.galleryID});
    $scope.galleryUpdate = function(gallery) {
            galleryClient.update({galleryID:gallery.id}, gallery);
    };

}
