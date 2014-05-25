'use strict';

/* Services */

angular.module('patSvc', ['ngResource']).
    factory('photoClient', function($resource){
        return $resource('/api/v1/photos/:photoID/', {photoID:'@id'}, {
            common: {withCredentials: true, crossDomain: true},
            update: {method:'PUT'}
            });
        }).
    factory('galleryClient', function($resource, $routeParams){
        return $resource('/api/v1/galleries/:galleryID/', {galleryID:'@id'},{
            common: {withCredentials: true, crossDomain: true},
            update: {method:'PUT'}
        });
    });