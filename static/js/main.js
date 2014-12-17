"use strict";

angular.module('pocket', ['ngRoute'])

  .controller('TingxieCtrl', function($scope) {

  })

  .config(function($routeProvider, $locationProvider) {
    $routeProvider
      .when('/', {
        templateUrl: '/static/partials/home.html'
      })
      .when('/tingxie', {
        templateUrl: '/static/partials/tingxie-index.html',
        controller: 'TingxieCtrl'
      })
      .otherwise({ redirectTo: '/'});

      // $locationProvider.html5Mode(true);
  });

// $(document).ready(function() {

//   var audio5js = new Audio5js({
//     ready: function() {
//       this.load('/file?name=22.mp3');
//       this.play();
//     }
//   });

// });

console.log('loaded');