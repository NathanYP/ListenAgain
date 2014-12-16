"use strict";

var app = angular.module('pocket', ['ngRoute'])

  .controller('TingxieCtrl', function($scope) {

  })

  .config(function($routeProvider, $locationProvider) {
    $routeProvider
      .when('/', {
        templateUrl: '../partials/home.html'
      })
      .when('/tingxie', {
        templateUrl: '../partials/tingxie-index.html',
        controller: 'TingliCtrl'
      })
      .otherwise({ redirectTo: '/'});

      $locationProvider.html5Mode(true);
  });

// $(document).ready(function() {

//   var audio5js = new Audio5js({
//     ready: function() {
//       this.load('/file?name=22.mp3');
//       this.play();
//     }
//   });

// });