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
}).directive('contenteditable', function() {
  return {
    require: 'ngModel',
    link: function(scope, elm, attrs, ctrl) {
      // view -> model
      elm.on('blur', function() {
        scope.$apply(function() {
          ctrl.$setViewValue(elm.html());
        });
      });

      // model -> view
      ctrl.$render = function() {
        elm.html(ctrl.$viewValue);
      };

      // load init value from DOM
      ctrl.$setViewValue(elm.html());
    }
  };
});
