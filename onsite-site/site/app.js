document.addEventListener('DOMContentLoaded', function(){
  var btn = document.getElementById('mobileToggle');
  var menu = document.getElementById('mobileMenu');
  if(btn && menu){
    btn.addEventListener('click', function(){ menu.classList.toggle('open'); });
  }
});