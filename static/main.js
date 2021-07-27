const sr = ScrollReveal({
    distance: '50px',
    duration: 1800,
    reset: true
});

sr.reveal('.text-box',{
    origin: 'top',
});

sr.reveal('.howto_pict',{
    origin: 'left'
});

sr.reveal('.howto_content',{
    origin: 'right'
});

$("nav .nav-link").on("click", function(){
    $("nav").find(".active").removeClass("active");
    $(this).addClass("active");
 });

 const Scrollbar = window.Scrollbar;

 Scrollbar.init(document.querySelector('body'));