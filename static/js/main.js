$(document).ready(function() {

  var audio5js = new Audio5js({
    ready: function() {
      this.load('/file?name=22.mp3');
      this.play();
    }
  });

});