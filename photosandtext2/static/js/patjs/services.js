'use strict';

/* Services */

angular.module('patSvc', ['ngResource']).
    factory('photoClient', function($resource){
        return $resource('http://127.0.0.1:port/api/v1/photos/:photoID/', {port:':5000', photoID:'@id'}, {
            common: {withCredentials: true, crossDomain: true},
            update: {method:'PUT'}
            });
        }).
    factory('galleryClient', function($resource, $routeParams){
        return $resource('http://127.0.0.1:port/api/v1/galleries/:galleryID/', {port: ':5000', galleryID:'@id'},{
            common: {withCredentials: true, crossDomain: true}
        });
    });