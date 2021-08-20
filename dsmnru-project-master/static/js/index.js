$(window).scroll(function (){
  $('nav').toggleClass('scrolled',$(this).scrollTop() > 100);
});

function preventBack() { 
  window.history.forward(); 
}  

setTimeout("preventBack()", 0);  

window.onunload = function () {
   null 
};  