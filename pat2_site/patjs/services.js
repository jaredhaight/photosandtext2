'use strict';

/* Services */

angular.module('patSvc', ['ngResource']).
    factory('photoClient', function($resource){
        return $resource('http://127.0.0.1:port/api/photos/:photoID/', {port:':8001', photoID:'@id'}, {
            common: {withCredentials: true, crossDomain: true},
            update: {method:'PUT'}
            });
        }).
    factory('galleryClient', function($resource, $routeParams){
        return $resource('http://127.0.0.1:port/api/galleries/:galleryID/', {port: ':8001'},{
            common: {withCredentials: true, crossDomain: true}
        });
    });