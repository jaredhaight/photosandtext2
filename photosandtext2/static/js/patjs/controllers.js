'use strict';

function photoListCtrl($scope, galleryClient, photoClient, $routeParams, $http, $timeout, $modal, $log, $upload) {
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

    /*
    $scope.options = {
        autoUpload: true,
        url: '/api/v1/galleries/'+$routeParams.galleryID+"/photos"
    };

    $scope.$on('fileuploadadd', function(event, files){
        $.each(files, function (index, file) {
            $scope.gallery.photos.push(file);
        });
    });

    $scope.$on('fileuploaddone', function(event, files){
        console.log(files.result.files);
        $.each(files.result.files, function (index, file) {
            console.log(file);
            var photoObj = photoClient.get({photoID:file.id});
            $scope.gallery.photos.push(photoObj);
        })
    });
    */

    $scope.onFileSelect = function($files) {
    //$files: an array of files selected, each file has name, size, and type.
    for (var i in $files) {
        var file = $files[i];

        $scope.upload = $upload.upload({
            url: '/api/v1/galleries/'+$routeParams.galleryID+'/photos',
            // method: POST or PUT,
            // headers: {'headerKey': 'headerValue'},
            // withCredentials: true,
            // data: {myObj: $scope.myModelObj},
            file: file
            //file: $files //upload multiple files, this feature only works in HTML5 FromData browsers
            /* set file formData name for 'Content-Desposition' header. Default: 'file' */
            //fileFormDataName: myFile, //OR for HTML5 multiple upload only a list: ['name1', 'name2', ...]
            /* customize how data is added to formData. See #40#issuecomment-28612000 for example */
            //formDataAppender: function(formData, key, val){} //#40#issuecomment-28612000
            }).progress(function(evt) {
                console.log('percent: ' + parseInt(100.0 * evt.loaded / evt.total));
            }).success(function(data, status, headers, config) {
                // file is uploaded successfully
                console.log(data);
                var photo = photoClient.get({photoID:data.id});
                $scope.gallery.photos.push(photo);
            });
            //.error(...)
            //.then(success, error, progress);
        }
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

        $scope.ok = function (photo) {
            $scope.photoSave(photo);
            $modalInstance.close($scope.photo);
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    }
}

