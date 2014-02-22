'use strict';

function photoListCtrl($scope, galleryClient, photoClient, $routeParams, $http, $timeout, $modal, $log) {
    delete $http.defaults.headers.common['X-Requested-With'];
    $scope.gallery = galleryClient.get({galleryID: $routeParams.galleryID});

    $scope.galleryUpdate = function(gallery) {
        galleryClient.update({galleryID:gallery.id}, gallery, function() {
            $scope.message("Saved Gallery!")
        }, function(data){
            console.log("fail?");
        });
    };

    $scope.message = function(message) {
        $scope.messageStatus = true;
        $scope.messageContent = message;
        $timeout(function(){
            $scope.messageStatus = false;
            $scope.messageContent = null;
        },3000);
    };

    //Open Photo Modal
    $scope.open = function(selectedPhoto) {
        var photoModalInstance = $modal.open({
            templateUrl: '/static/js/patjs/partials/photo_edit.html',
            windowClass: 'photo-modal',
            controller: PhotoModalInstanceCtrl,
            resolve: {
                photo: function() {
                    return selectedPhoto;
                }
            }
        });

        photoModalInstance.result.then(function (photo) {
            $scope.photoSave(photo);
        }, function () {
          $log.info('Modal dismissed at: ' + new Date());
        });
    };

    //Photo Modal Instance
    var PhotoModalInstanceCtrl = function($scope, $modalInstance, photoClient, photo) {
        $scope.photo = photo;

        $scope.message = function(message) {
            $scope.messageStatus = true;
            $scope.messageContent = message;
            $timeout(function(){
                $scope.messageStatus = false;
                $scope.messageContent = null;
            },3000);
        };

        $scope.photoSave = function(photo) {
            photoClient.update({photoID:photo.id}, photo, function(data){
                console.log("success");
                $scope.message("Saved Photo")
            }, function(data){
                console.log("fail?");
            });
        };

        $scope.ok = function () {
            $modalInstance.close($scope.photo);
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    }
}

