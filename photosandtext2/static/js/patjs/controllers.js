'use strict';

function galleryListCtrl($scope, galleryClient, $http, $log) {
    delete $http.defaults.headers.common['X-Requested-With'];
    $scope.galleries = galleryClient.get();

}

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

    $scope.getLocation = function(val) {
    return $http.get('http://maps.googleapis.com/maps/api/geocode/json', {
        params: {
            address: val,
            sensor: false
        }
        }).then(function(res){
            var addresses = [];
            angular.forEach(res.data.results, function(item){
            addresses.push(item.formatted_address);
        });
            return addresses;
        });
    };

    $scope.onFileSelect = function($files) {
    //$files: an array of files selected, each file has name, size, and type.
    $scope.uploadInProgress = true;
    $scope.uploadCountTotal = $files.length;
    $scope.uploadCountProgress = 1;
    console.log("UploadCountTotal: " + $scope.uploadCountTotal.toString());
    console.log("UploadCountProgress: " + $scope.uploadCountProgress.toString());
    $scope.upload = $upload.upload({
        url: '/api/v1/galleries/'+$routeParams.galleryID+'/photos',
        // method: POST or PUT,
        // headers: {'headerKey': 'headerValue'},
        // withCredentials: true,
        // data: {myObj: $scope.myModelObj},
        //file: file
        file: $files, //upload multiple files, this feature only works in HTML5 FromData browsers
        /* set file formData name for 'Content-Desposition' header. Default: 'file' */
        //fileFormDataName: "jahFile", //OR for HTML5 multiple upload only a list: ['name1', 'name2', ...]
        /* customize how data is added to formData. See #40#issuecomment-28612000 for example */
        //formDataAppender: function(formData, key, val){} //#40#issuecomment-28612000
        }).progress(function(evt) {
            console.log(evt);
            $scope.uploadPercent = parseInt(100.0 * evt.loaded / evt.total);
            console.log('percent: ' + parseInt(100.0 * evt.loaded / evt.total));
        }).success(function(data, status, headers, config) {
            // file is uploaded successfully
            console.log(data);
            for (var result in data.objects) {
                var photo = photoClient.get({photoID:data.objects[result].id});
                $scope.gallery.photos.push(photo);
                $scope.uploadPercent = null;
                $scope.uploadCountProgress++;
                if ($scope.uploadCountProgress > $scope.uploadCountTotal) {
                    $scope.uploadInProgress = false;
                }
                console.log("UploadCountProgress: " + $scope.uploadCountProgress.toString());
            }
        });
        //.error(...)
        //.then(success, error, progress);
    };

    //Open Photo Modal
    $scope.open = function(selectedPhoto) {
        if (selectedPhoto.orientation == 'landscape') {
            var windowClass = 'photo-modal-landscape';
        } else {
            var windowClass = 'photo-modal-portrait'
        }
        var photoModalInstance = $modal.open({
            templateUrl: '/static/js/patjs/partials/photo_edit.html',
            windowClass: windowClass,
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

        //Open Photo Delete Modal
        $scope.photoDeleteModal = function(selectedPhoto) {
            var deletePhotoModalInstance = $modal.open({
                templateUrl: '/static/js/patjs/partials/photo_delete.html',
                controller: confirmDeletePhotoModalInstanceCtrl,
                windowClass: "photo-delete-modal-window",
                resolve: {
                    photo: function() {
                        return selectedPhoto;
                    }
                }
            });

            deletePhotoModalInstance.result.then(function (photoDeleted) {
                $log.info('This is the first result after closing the delete photo modal');
                if (photoDeleted == true) {
                    $modalInstance.dismiss('deleted');
                }
            }, function () {
              $log.info('Modal dismissed at: ' + new Date());
              if (photoDeleted == true) {
                  $modalInstance.dismiss('deleted');
              }
            });
        };

       //Delete Photo Modal Instance
        var confirmDeletePhotoModalInstanceCtrl = function($scope, $modalInstance, photoClient, photo) {
            $scope.photo = photo;

            $scope.photoDelete = function(photo) {
                photoClient.delete({photoID: photo.id})
            };

            $scope.photoDeleteConfirm = function (photo) {
                $scope.photoDelete(photo);
                $scope.photoDeleted = true;
                $modalInstance.close($scope.photoDeleted);
            };

            $scope.photoDeleteDismiss = function () {
                $modalInstance.dismiss('cancel');
            };
        };
    };


    //Open Delete Gallery Modal
    $scope.delete = function(selectedGallery) {
        var galleryModalInstance = $modal.open({
            templateUrl: '/static/js/patjs/partials/gallery_delete.html',
            controller: DeleteGalleryModalInstanceCtrl,
            windowClass: "gallery-modal-window",
            resolve: {
                gallery: function() {
                    return selectedGallery;
                }
            }
        });

        galleryModalInstance.result.then(function (gallery) {
            $log.info('This is the first result after closing the delete gallery modal');
        }, function () {
          $log.info('Modal dismissed at: ' + new Date());
        });
    };

   //Delete Gallery Modal Instance
    var DeleteGalleryModalInstanceCtrl = function($scope, $modalInstance, galleryClient, gallery) {
        $scope.gallery = gallery;

        $scope.galleryDelete = function(gallery) {
            galleryClient.delete({galleryID: gallery.id})
        };

        $scope.galleryDeleteConfirm = function (gallery) {
            $scope.galleryDelete(gallery);
            $modalInstance.close($scope.gallery);
        };

        $scope.galleryDeleteDismiss = function () {
            $modalInstance.dismiss('cancel');
        };
    };
}