'use strict';

function photoListCtrl($scope, photoClient, galleryClient, $route, $routeParams, $rootScope, $http, $cookieStore, $cookies, $location, $modal) {
    delete $http.defaults.headers.common['X-Requested-With'];

    //This is our photo viewer.
    $scope.open = function (photoId) {
        console.log('Opened Photo Lightbox');

        var modalInstance = $modal.open({
          templateUrl: '/partials/photo.html',
          controller: photoCtrl,
          resolve: {
              selectedPhoto: function () {
                return photoClient.get({photoID: photoId});
              }
          }
        });

        modalInstance.result.then(function () {
        }, function () {
            $rootScope.hideScrollEnabled = false;
        });
    };

    if ($location.search()['photo']) {
        $scope.open($location.search()['photo']);
    }

    if (!($scope.galleries)) {
        $scope.galleries = galleryClient.get();
    }
}

function photoCtrl($scope, $modalInstance, selectedPhoto, $location) {
    $scope.photo = selectedPhoto;
    $scope.message = false;
    $scope.photoSave = function(photo) {
        photo.$save(function() {
            $scope.message = 'Saved!';
            console.log(data);
            }, function(data) {
                console.log(data);
                $scope.message = data.data.message;
                $scope.error = "Error: "+data.data.error;
            }
        );
    };
    $scope.close = function() {
        $modalInstance.dismiss();
    };

    $scope.$on('$routeUpdate',function(e) {
      console.log($location.search().count());
      if($location.search().count() == 0){
          $scope.close()
        };
    });
}

function photoUploadCtrl($scope, photoClient, galleryClient, $routeParams, $http, $cookieStore, $cookies) {
    delete $http.defaults.headers.common['X-Requested-With'];
    $scope.options = {
        autoUpload: true,
        url: '/api/photos'
    };

    $scope.gallery = new galleryClient;

    $scope.photoList =[];
    $scope.uploadList = [];
    $scope.$on('fileuploadadd', function(event, files){
        $.each(files, function (index, file) {
            $scope.uploadList.push(file);
        });
    });
    $scope.$on('fileuploaddone', function(event, files){
        $scope.photoListShow = true;
        $.each(files.result.results, function (index, file) {
            var photoObj = new photoClient(file);
            photoObj.gallery = $scope.gallery;
            $scope.photoList.push(photoObj);
        })
    });

    $scope.savePhotos = function() {
        $scope.gallery.$save(
         function(successResult) {
            $.each($scope.photoList, function(index, photo) {
            console.log(photo.gallery);
            photo.$save(
                function(success) {

                },
                function(error) {
                    photo.error = "Could not upload this file.";
                    console.log(error);
                }

            );
            })
         },
        function(errorResult) {
            $scope.error = "Shit's broken!";
            if(errorResult.status === 404) {

            }
        })
    }
}
