'use strict';

function photoListCtrl($scope, galleryClient, photoClient, $route, $routeParams, $rootScope, $http, $location, $timeout) {
    delete $http.defaults.headers.common['X-Requested-With'];
    $scope.gallery = galleryClient.get({galleryID: $routeParams.galleryID});
    $scope.galleryUpdate = function(gallery) {
        galleryClient.update({galleryID:gallery.id}, gallery, function() {
            $scope.galleryMessage("Saved Gallery!")
        }, function(data){
            console.log("fail?");
        });
    };

    $scope.photoEditInit = function(photo) {
        $scope.photo = photoClient.get({photoID: photo.id});
        $scope.photoEdit = true;
    };

    $scope.galleryMessage = function(message) {
        $scope.galleryMessageStatus = true;
        $scope.galleryMessageContent = message;
        $timeout(function(){
            $scope.galleryMessageStatus = false;
            $scope.galleryMessageContent = null;
        },3000);
    };

    $scope.photoMessage = function(message) {
        $scope.photoMessageStatus = true;
        $scope.photoMessageContent = message;
        $timeout(function(){
            $scope.photoMessageStatus = false;
            $scope.photoMessageContent = null;
        },3000);
    };

    $scope.photoSave = function(photo) {
        photoClient.update({photoID:photo.id}, photo, function(data){
            console.log("success");
            $scope.photoMessage("Saved Photo")
        }, function(data){
            console.log("fail?");
        });
    };

}
