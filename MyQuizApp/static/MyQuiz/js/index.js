var elem = document.documentElement;
function openFullscreen() {
  if (elem.requestFullscreen) {
    document.getElementById("nav-bar").style.display = "none";
    document.getElementById("footer").style.display = "none";
    document.getElementById("startQuiz").style.display = "none";
    var totalContainer =
      document.getElementsByClassName("quiz-container").length;
    for (var i = 0; i < totalContainer; i++) {
      document.getElementsByClassName("quiz-container")[i].style.display =
        "flex";
    }
    elem.requestFullscreen();
  } else if (elem.webkitRequestFullscreen) {
    /* Safari */
    elem.webkitRequestFullscreen();
  } else if (elem.msRequestFullscreen) {
    /* IE11 */
    elem.msRequestFullscreen();
  }
}

function closeFullscreen() {
  if (document.exitFullscreen) {
    document.getElementById("nav-bar").style.display = "flex";
    document.getElementById("footer").style.display = "flex";
    document.getElementById("startQuiz").style.display = "none";
    var totalContainer =
      document.getElementsByClassName("quiz-container").length;
    for (var i = 0; i < totalContainer; i++) {
      document.getElementsByClassName("quiz-container")[i].style.display =
        "none";
    }
    document.exitFullscreen();
  } else if (document.webkitExitFullscreen) {
    /* Safari */
    document.webkitExitFullscreen();
  } else if (document.msExitFullscreen) {
    /* IE11 */
    document.msExitFullscreen();
  }
}


// Timer 

