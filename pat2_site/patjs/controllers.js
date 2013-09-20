'use strict';

function photoListCtrl($scope, photoClient, $route, $routeParams, $rootScope, $http, $cookieStore, $cookies, $location, $modal) {
    delete $http.defaults.headers.common['X-Requested-With'];

    //This is our photo viewer.
    $scope.open = function (photo) {
        var lastRoute = $route.current;
        console.log('Opened Photo Lightbox');
        console.log('Location path is: '+$location.path());
        $rootScope.hideScrollEnabled = true;
        $scope.$on('$locationChangeSuccess', function(event) {
            $route.current = lastRoute;
        });
        if (($location.path()) != ('photo/'+photo.id)) {
            $location.path('photo/'+photo.id).replace();
        }

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
        console.log('Got routeparams: '+$routeParams.photoID);
        var urlPhoto = photoClient.get({photoID: $routeParams.photoID});
        $scope.open(urlPhoto);
    }
    if (!($scope.photos)){
        console.log('scope.photos not defined');
        $scope.photos = photoClient.get();
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