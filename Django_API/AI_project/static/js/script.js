// Add shadow on scroll for navbar
(function(){
  const nav = document.getElementById('mainNav');
  function onScroll(){
    if(window.scrollY>10){
      nav.classList.add('scrolled');
    } else {
      nav.classList.remove('scrolled');
    }
  }
  document.addEventListener('scroll', onScroll);
  onScroll();
})();

// Smooth scroll for back to top
document.querySelectorAll('a[href="#top"]').forEach(a=>{
  a.addEventListener('click', e=>{
    e.preventDefault();window.scrollTo({top:0,behavior:'smooth'});
  });
});
