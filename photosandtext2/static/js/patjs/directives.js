'use strict';

/* Directives */


angular.module('patjs.directives', []).
    directive('galleryinit', function($timeout) {
    return {
        // Restrict it to be an attribute in this case
        restrict: 'A',
        // Using timeout here lets us save this until after the DOM loads.
        link: $timeout(function(scope, element, attrs) {
            console.log("Recognized directive usage");
            $("#gallery").justifiedGallery({
              rowHeight: 300,
              justifyLastRow: false,
              captions: false
            });
        },200)
    }
});
