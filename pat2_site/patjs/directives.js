'use strict';

/* Directives */


angular.module('patjs.directives', []).
  directive('appVersion', ['version', function(version) {
    return function(scope, elm, attrs) {
      elm.text(version);
    };
  }]);

angular.module('patjs.directives',[]).
    directive('contenteditable', function() {
        return {
           require: 'ngModel',
                link: function(scope, elm, attrs, ctrl) {
                    // view -> model
                    elm.bind('blur', function() {
                        scope.$apply(function() {
                            ctrl.$setViewValue(elm.html());
                        });
                    });

                    // model -> view
                    ctrl.$render = function() {
                        elm.html(ctrl.$viewValue);
                    };

                    // load init value from DOM
                    //ctrl.$setViewValue(elm.html());
                }
            };
        });
