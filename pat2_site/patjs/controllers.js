'use strict';

function photoListCtrl($scope, photoClient, $route, $routeParams, $rootScope, $http, $cookieStore, $cookies, $location, $modal) {
    delete $http.defaults.headers.common['X-Requested-With'];
    $scope.photos = photoClient.get();

    //This is our photo viewer.
    $scope.open = function (photo) {
        var lastRoute = $route.current;
        $rootScope.hideScrollEnabled = true;
        $scope.$on('$locationChangeSuccess', function(event) {
            $route.current = lastRoute;
        });
        $location.path('photo/'+photo.id);
        var modalInstance = $modal.open({
          templateUrl: '/partials/photo.html',
          controller: photoCtrl,
          resolve: {
              selectedPhoto: function () {
                return photoClient.get({photoID: photo.id});
              }
          }
        });

        modalInstance.result.then(function () {
        var lastRoute = $route.current;
        $scope.$on('$locationChangeSuccess', function(event) {
            $route.current = lastRoute;
        });
        }, function () {
            $rootScope.hideScrollEnabled = false;
            $location.path('/');
        });
    };

    if ($routeParams.photoID) {
        var photo = photoClient.get({photoID: $routeParams.photoID});
        $scope.open(photo);
    }
}

function photoCtrl($scope, $modalInstance, selectedPhoto) {
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
    }
}

function photoUploadCtrl($scope, photoClient, $routeParams, $http, $cookieStore, $cookies) {
    delete $http.defaults.headers.common['X-Requested-With'];
    $scope.options = {
        autoUpload: true,
        url: '/api/photos'
    };

    $scope.photoList =[];
    $scope.uploadList = [];
    $scope.$on('fileuploadadd', function(event, files){
        $.each(files, function (index, file) {
            $scope.uploadList.push(file);
        });
    });
    $scope.$on('fileuploaddone', function(event, files){
        $.each(files.result.results, function (index, file) {
            $scope.photoList.push(file);
        })
    });
}